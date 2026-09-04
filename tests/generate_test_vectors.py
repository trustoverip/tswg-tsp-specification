"""
TSP Test Vector Generator

Generates deterministic test vectors for the cryptographic primitives used in
the Trust Spanning Protocol (TSP) specification:

  - Ed25519 signing and verification (Section 8.1)
  - HPKE-Auth mode: DHKEM(X25519, HKDF-SHA256) + HKDF-SHA256 + ChaCha20Poly1305 (Section 8.3)
  - HPKE-Base mode: same suite (Section 8.4)

All inputs are fixed (seeded) for reproducibility. Each test vector includes
both inputs and expected outputs so implementations can use them for conformance
checking.

Usage:
    python3 generate_test_vectors.py

Output:
    test_vectors.json  — machine-readable test vectors
    Printed summary    — human-readable overview

Requirements:
    pip install cryptography

Reference: https://github.com/trustoverip/tswg-tsp-specification/issues/14
"""

import hashlib
import hmac
import json
import os
import struct

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.hkdf import HKDF, HKDFExpand
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    PrivateFormat,
    NoEncryption,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def to_hex(b: bytes) -> str:
    return b.hex()


def from_seed(seed_bytes: bytes) -> X25519PrivateKey:
    """Create an X25519 private key from exactly 32 seed bytes."""
    return X25519PrivateKey.from_private_bytes(seed_bytes)


# ---------------------------------------------------------------------------
# DHKEM(X25519, HKDF-SHA256) — RFC 9180 §4.1 and §7.1.2
# ---------------------------------------------------------------------------

SUITE_ID_KEM  = b"KEM\x00\x20"   # DHKEM(X25519, HKDF-SHA256), KEM ID 0x0020
SUITE_ID_HPKE = b"HPKE\x00\x20\x00\x01\x00\x03"  # KEM 0x0020, KDF 0x0001, AEAD 0x0003

Nsecret = 32   # KEM shared-secret length
Nk      = 32   # AEAD key length (ChaCha20Poly1305)
Nn      = 12   # AEAD nonce length
Nh      = 32   # Hash output length (SHA-256)


def _labeled_extract(suite_id: bytes, label: bytes, ikm: bytes, salt: bytes = b"") -> bytes:
    """RFC 9180 §4 LabeledExtract."""
    labeled_ikm = b"HPKE-v1" + suite_id + label + ikm
    h = hmac.new(salt if salt else b"\x00" * Nh, labeled_ikm, hashlib.sha256)
    return h.digest()


def _labeled_expand(suite_id: bytes, prk: bytes, label: bytes, info: bytes, length: int) -> bytes:
    """RFC 9180 §4 LabeledExpand."""
    labeled_info = (
        struct.pack(">H", length)
        + b"HPKE-v1"
        + suite_id
        + label
        + info
    )
    # Single-round HKDF-Expand
    t = b""
    okm = b""
    counter = 1
    while len(okm) < length:
        t = hmac.new(prk, t + labeled_info + bytes([counter]), hashlib.sha256).digest()
        okm += t
        counter += 1
    return okm[:length]


def _extract_and_expand_kem(dh: bytes, kem_context: bytes) -> bytes:
    """RFC 9180 §4.1 ExtractAndExpand for DHKEM(X25519, HKDF-SHA256)."""
    prk = _labeled_extract(SUITE_ID_KEM, b"shared_secret", dh)
    return _labeled_expand(SUITE_ID_KEM, prk, b"shared_secret", kem_context, Nsecret)


def _x25519_public_bytes(private_key: X25519PrivateKey) -> bytes:
    return private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)


def _x25519_dh(private_key: X25519PrivateKey, peer_public_bytes: bytes) -> bytes:
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey
    peer_pub = X25519PublicKey.from_public_bytes(peer_public_bytes)
    return private_key.exchange(peer_pub)


def kem_encap(pk_r_bytes: bytes, sk_e_seed: bytes) -> tuple[bytes, bytes]:
    """
    DHKEM(X25519) Encap.
    Returns (enc, shared_secret) where enc is the ephemeral public key bytes.
    """
    sk_e = from_seed(sk_e_seed)
    pk_e_bytes = _x25519_public_bytes(sk_e)
    dh = _x25519_dh(sk_e, pk_r_bytes)
    kem_context = pk_e_bytes + pk_r_bytes
    shared_secret = _extract_and_expand_kem(dh, kem_context)
    return pk_e_bytes, shared_secret


def kem_decap(enc_bytes: bytes, sk_r: X25519PrivateKey) -> bytes:
    """DHKEM(X25519) Decap. Returns shared_secret."""
    pk_r_bytes = _x25519_public_bytes(sk_r)
    dh = _x25519_dh(sk_r, enc_bytes)
    kem_context = enc_bytes + pk_r_bytes
    return _extract_and_expand_kem(dh, kem_context)


def kem_auth_encap(pk_r_bytes: bytes, sk_s: X25519PrivateKey, sk_e_seed: bytes) -> tuple[bytes, bytes]:
    """DHKEM(X25519) AuthEncap (sender-authenticated). Returns (enc, shared_secret)."""
    sk_e = from_seed(sk_e_seed)
    pk_e_bytes = _x25519_public_bytes(sk_e)
    dh = _x25519_dh(sk_e, pk_r_bytes) + _x25519_dh(sk_s, pk_r_bytes)
    pk_s_bytes = _x25519_public_bytes(sk_s)
    kem_context = pk_e_bytes + pk_r_bytes + pk_s_bytes
    shared_secret = _extract_and_expand_kem(dh, kem_context)
    return pk_e_bytes, shared_secret


def kem_auth_decap(enc_bytes: bytes, sk_r: X25519PrivateKey, pk_s_bytes: bytes) -> bytes:
    """DHKEM(X25519) AuthDecap. Returns shared_secret."""
    pk_r_bytes = _x25519_public_bytes(sk_r)
    dh = _x25519_dh(sk_r, enc_bytes) + _x25519_dh(sk_r, pk_s_bytes)
    kem_context = enc_bytes + pk_r_bytes + pk_s_bytes
    return _extract_and_expand_kem(dh, kem_context)


# ---------------------------------------------------------------------------
# HPKE Key Schedule — RFC 9180 §5.1
# ---------------------------------------------------------------------------

def _key_schedule(mode: int, shared_secret: bytes, info: bytes,
                  psk: bytes = b"", psk_id: bytes = b"") -> tuple[bytes, bytes]:
    """
    RFC 9180 §5.1 KeySchedule.
    Returns (key, base_nonce) for HPKE single-shot usage.
    """
    ks_context = bytes([mode]) + (
        _labeled_extract(SUITE_ID_HPKE, b"psk_id_hash", psk_id)
        + _labeled_extract(SUITE_ID_HPKE, b"info_hash", info)
    )
    secret = _labeled_extract(SUITE_ID_HPKE, b"secret", shared_secret,
                               salt=_labeled_extract(SUITE_ID_HPKE, b"psk", psk))
    key   = _labeled_expand(SUITE_ID_HPKE, secret, b"key",        ks_context, Nk)
    nonce = _labeled_expand(SUITE_ID_HPKE, secret, b"base_nonce", ks_context, Nn)
    return key, nonce


# ---------------------------------------------------------------------------
# HPKE Single-Shot API — RFC 9180 §6
# ---------------------------------------------------------------------------

MODE_BASE = 0
MODE_AUTH = 2


def hpke_seal_base(pk_r_bytes: bytes, info: bytes, aad: bytes, pt: bytes,
                   sk_e_seed: bytes) -> tuple[bytes, bytes]:
    """
    HPKE-Base single-shot seal.
    Returns (enc, ciphertext).
    enc is the ephemeral public key (32 bytes for X25519).
    """
    enc, shared_secret = kem_encap(pk_r_bytes, sk_e_seed)
    key, nonce = _key_schedule(MODE_BASE, shared_secret, info)
    aead = ChaCha20Poly1305(key)
    ct = aead.encrypt(nonce, pt, aad)
    return enc, ct


def hpke_open_base(enc_bytes: bytes, sk_r: X25519PrivateKey,
                   info: bytes, aad: bytes, ct: bytes) -> bytes:
    """HPKE-Base single-shot open. Returns plaintext."""
    shared_secret = kem_decap(enc_bytes, sk_r)
    key, nonce = _key_schedule(MODE_BASE, shared_secret, info)
    aead = ChaCha20Poly1305(key)
    return aead.decrypt(nonce, ct, aad)


def hpke_seal_auth(pk_r_bytes: bytes, sk_s: X25519PrivateKey,
                   info: bytes, aad: bytes, pt: bytes,
                   sk_e_seed: bytes) -> tuple[bytes, bytes]:
    """
    HPKE-Auth single-shot seal.
    Returns (enc, ciphertext).
    """
    enc, shared_secret = kem_auth_encap(pk_r_bytes, sk_s, sk_e_seed)
    key, nonce = _key_schedule(MODE_AUTH, shared_secret, info)
    aead = ChaCha20Poly1305(key)
    ct = aead.encrypt(nonce, pt, aad)
    return enc, ct


def hpke_open_auth(enc_bytes: bytes, sk_r: X25519PrivateKey, pk_s_bytes: bytes,
                   info: bytes, aad: bytes, ct: bytes) -> bytes:
    """HPKE-Auth single-shot open. Returns plaintext."""
    shared_secret = kem_auth_decap(enc_bytes, sk_r, pk_s_bytes)
    key, nonce = _key_schedule(MODE_AUTH, shared_secret, info)
    aead = ChaCha20Poly1305(key)
    return aead.decrypt(nonce, ct, aad)


# ---------------------------------------------------------------------------
# Test Vector Generation
# ---------------------------------------------------------------------------

def gen_ed25519_vectors() -> list[dict]:
    """Generate Ed25519 sign/verify test vectors."""
    vectors = []

    cases = [
        {
            "description": "Ed25519 signing: empty message",
            "seed_hex": "0000000000000000000000000000000000000000000000000000000000000001",
            "message_hex": "",
        },
        {
            "description": "Ed25519 signing: short ASCII message",
            "seed_hex": "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60",
            "message_hex": bytes(b"hello TSP").hex(),
        },
        {
            "description": "Ed25519 signing: TSP envelope bytes (32-byte payload)",
            "seed_hex": "4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb",
            "message_hex": bytes(range(32)).hex(),
        },
    ]

    for c in cases:
        seed = bytes.fromhex(c["seed_hex"])
        msg  = bytes.fromhex(c["message_hex"])
        sk   = Ed25519PrivateKey.from_private_bytes(seed)
        pk   = sk.public_key()
        pk_bytes = pk.public_bytes(Encoding.Raw, PublicFormat.Raw)
        sig  = sk.sign(msg)

        # Verify round-trip
        pk.verify(sig, msg)

        vectors.append({
            "description": c["description"],
            "algorithm": "Ed25519",
            "inputs": {
                "private_key_seed_hex": c["seed_hex"],
                "message_hex": c["message_hex"],
            },
            "outputs": {
                "public_key_hex": to_hex(pk_bytes),
                "signature_hex": to_hex(sig),
            },
            "notes": (
                "Signature covers the message bytes directly. "
                "In TSP, the signed data is {TSP_Envelope || TSP_Payload} "
                "per Section 3.3 of the specification."
            ),
        })

    return vectors


def gen_hpke_base_vectors() -> list[dict]:
    """Generate HPKE-Base test vectors."""
    vectors = []

    cases = [
        {
            "description": "HPKE-Base: empty plaintext, empty AAD",
            "sk_r_seed": "4310ee97d88cc1f088a5576c77ab0cf5c3ac797f3d95139c6c84b5429c59662a",
            "sk_e_seed": "f4ec9b33b792c372c1d2c2063507b684ef925b8c75a42dbcbf57d63ccd381600",
            "info_hex": "",
            "aad_hex": "",
            "plaintext_hex": "",
        },
        {
            "description": "HPKE-Base: short plaintext (TSP payload simulation)",
            "sk_r_seed": "7ef22b03f5a3f6db0f3fca748b37f74f7d24a2a37f4c7b71e3ad756f8a3d1c02",
            "sk_e_seed": "e9b0de1b3a4e5f60718293a4056c7bd8f9e0a1b2c3d4e5f60102030405060708",
            "info_hex": bytes(b"TSP version 0.0.1").hex(),
            "aad_hex": bytes(b"tsp-envelope-aad").hex(),
            "plaintext_hex": bytes(b"Hello, TSP world!").hex(),
        },
        {
            "description": "HPKE-Base: 32-byte plaintext (typical TSP confidential payload)",
            "sk_r_seed": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "sk_e_seed": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            "info_hex": bytes(b"TSP").hex(),
            "aad_hex": bytes(b"envelope").hex(),
            "plaintext_hex": bytes(range(32)).hex(),
        },
    ]

    for c in cases:
        sk_r  = from_seed(bytes.fromhex(c["sk_r_seed"]))
        pk_r  = _x25519_public_bytes(sk_r)
        info  = bytes.fromhex(c["info_hex"])
        aad   = bytes.fromhex(c["aad_hex"])
        pt    = bytes.fromhex(c["plaintext_hex"])

        enc, ct = hpke_seal_base(pk_r, info, aad, pt, bytes.fromhex(c["sk_e_seed"]))

        # Verify round-trip
        recovered = hpke_open_base(enc, sk_r, info, aad, ct)
        assert recovered == pt, "HPKE-Base round-trip failed"

        sk_r_bytes = sk_r.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())

        vectors.append({
            "description": c["description"],
            "algorithm": "HPKE-Base",
            "kem": "DHKEM(X25519, HKDF-SHA256)",
            "kdf": "HKDF-SHA256",
            "aead": "ChaCha20Poly1305",
            "kem_id": "0x0020",
            "kdf_id": "0x0001",
            "aead_id": "0x0003",
            "mode": "base (0x00)",
            "inputs": {
                "recipient_private_key_hex": to_hex(sk_r_bytes),
                "recipient_public_key_hex":  to_hex(pk_r),
                "ephemeral_private_key_seed_hex": c["sk_e_seed"],
                "info_hex": c["info_hex"],
                "aad_hex":  c["aad_hex"],
                "plaintext_hex": c["plaintext_hex"],
            },
            "outputs": {
                "enc_hex":        to_hex(enc),
                "ciphertext_hex": to_hex(ct),
            },
            "notes": (
                "enc is the serialized ephemeral public key (32 bytes for X25519). "
                "ciphertext includes the 16-byte ChaCha20Poly1305 authentication tag. "
                "In TSP, HPKE-Base requires VID_sndr in the confidential payload per §8.4."
            ),
        })

    return vectors


def gen_hpke_auth_vectors() -> list[dict]:
    """Generate HPKE-Auth test vectors."""
    vectors = []

    cases = [
        {
            "description": "HPKE-Auth: sender-authenticated TSP payload",
            "sk_r_seed": "3310ee97d88cc1f088a5576c77ab0cf5c3ac797f3d95139c6c84b5429c59662a",
            "sk_s_seed": "5510ee97d88cc1f088a5576c77ab0cf5c3ac797f3d95139c6c84b5429c59662a",
            "sk_e_seed": "7710ee97d88cc1f088a5576c77ab0cf5c3ac797f3d95139c6c84b5429c59662a",
            "info_hex": bytes(b"TSP version 0.0.1").hex(),
            "aad_hex": bytes(b"tsp-envelope").hex(),
            "plaintext_hex": bytes(b"authenticated TSP message payload").hex(),
        },
        {
            "description": "HPKE-Auth: 32-byte payload (simulates encrypted TSP control fields)",
            "sk_r_seed": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
            "sk_s_seed": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
            "sk_e_seed": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            "info_hex": bytes(b"TSP").hex(),
            "aad_hex": bytes(b"envelope").hex(),
            "plaintext_hex": bytes(range(32)).hex(),
        },
    ]

    for c in cases:
        sk_r  = from_seed(bytes.fromhex(c["sk_r_seed"]))
        sk_s  = from_seed(bytes.fromhex(c["sk_s_seed"]))
        pk_r  = _x25519_public_bytes(sk_r)
        pk_s  = _x25519_public_bytes(sk_s)
        info  = bytes.fromhex(c["info_hex"])
        aad   = bytes.fromhex(c["aad_hex"])
        pt    = bytes.fromhex(c["plaintext_hex"])

        enc, ct = hpke_seal_auth(pk_r, sk_s, info, aad, pt, bytes.fromhex(c["sk_e_seed"]))

        # Verify round-trip
        recovered = hpke_open_auth(enc, sk_r, pk_s, info, aad, ct)
        assert recovered == pt, "HPKE-Auth round-trip failed"

        sk_r_bytes = sk_r.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
        sk_s_bytes = sk_s.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())

        vectors.append({
            "description": c["description"],
            "algorithm": "HPKE-Auth",
            "kem": "DHKEM(X25519, HKDF-SHA256)",
            "kdf": "HKDF-SHA256",
            "aead": "ChaCha20Poly1305",
            "kem_id": "0x0020",
            "kdf_id": "0x0001",
            "aead_id": "0x0003",
            "mode": "auth (0x02)",
            "inputs": {
                "recipient_private_key_hex": to_hex(sk_r_bytes),
                "recipient_public_key_hex":  to_hex(pk_r),
                "sender_private_key_hex":    to_hex(sk_s_bytes),
                "sender_public_key_hex":     to_hex(pk_s),
                "ephemeral_private_key_seed_hex": c["sk_e_seed"],
                "info_hex": c["info_hex"],
                "aad_hex":  c["aad_hex"],
                "plaintext_hex": c["plaintext_hex"],
            },
            "outputs": {
                "enc_hex":        to_hex(enc),
                "ciphertext_hex": to_hex(ct),
            },
            "notes": (
                "enc is the serialized ephemeral public key (32 bytes for X25519). "
                "HPKE-Auth binds the sender's static key into the KEM shared secret, "
                "providing implicit sender authentication at the KEM layer. "
                "In TSP HPKE-Auth mode, VID_sndr in the confidential payload is optional (§8.3)."
            ),
        })

    return vectors


def main():
    print("Generating TSP test vectors...")

    ed25519_vectors   = gen_ed25519_vectors()
    hpke_base_vectors = gen_hpke_base_vectors()
    hpke_auth_vectors = gen_hpke_auth_vectors()

    all_vectors = {
        "version": "TSP vs1.0 Experimental Implementor's Draft Rev 2",
        "description": (
            "Deterministic test vectors for TSP cryptographic primitives. "
            "All inputs are fixed so any conforming implementation must "
            "produce the same outputs."
        ),
        "ed25519_sign_verify": ed25519_vectors,
        "hpke_base": hpke_base_vectors,
        "hpke_auth": hpke_auth_vectors,
    }

    output_path = os.path.join(os.path.dirname(__file__), "test_vectors.json")
    with open(output_path, "w") as f:
        json.dump(all_vectors, f, indent=2)

    print(f"Written: {output_path}")
    print(f"  Ed25519 vectors:   {len(ed25519_vectors)}")
    print(f"  HPKE-Base vectors: {len(hpke_base_vectors)}")
    print(f"  HPKE-Auth vectors: {len(hpke_auth_vectors)}")
    print("\nAll round-trips verified.")


if __name__ == "__main__":
    main()
