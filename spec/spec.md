Trust Spanning Protocol (TSP) Specification
==================

**Specification Status**: Experimental Implementor's Draft Rev 3 (Editor's Draft in progress)

**Latest Draft:**

[https://github.com/trustoverip/tswg-tsp-specification](https://github.com/trustoverip/tswg-tsp-specification)

**Authors:**

- [Wenjing Chu](https://github.com/wenjing), [Futurewei Technologies, Inc.](https://futurewei.com)
- [Samuel Smith](https://github.com/SmithSamuelM), [ProSapien LLC](https://prosapien.com)

**Contributors:**

- The contributor list goes here

**Participate:**

~ [GitHub repo](https://github.com/trustoverip/tswg-tsp-specification)
~ [Commit history](https://github.com/trustoverip/tswg-tsp-specification/commits/main)

------------------------------------

[//]: # (Pandoc Formatting Macros)

[//]: # (\maketitle)

[//]: # (\newpage)

[//]: # (Pandoc Formatting Macros)

[//]: # (::: introtitle)

[//]: # (Introduction)

[//]: # (:::)

## Overview

The Trust Spanning Protocol (TSP) facilitates secure communication between endpoints with potentially different identifier types using message-based exchanges. As long as the endpoints use identifiers based on public key cryptography (PKC) with a verifiable trust root, TSP ensures their messages are authentic and if required, confidential. Moreover, it presents various privacy protection measures against metadata-based correlation exploits. These attributes of TSP allow endpoints to form authentic relationships rooted in their respective verifiable identifiers (VIDs), viewing TSP messages as virtual channels for trustworthy communication.

In recent years, a wide variety of decentralized identifiers have been proposed or are being standardized to meet a diverse set of use cases and requirements. This diversity underscores the critical need for a universal method to connect the systems these identifiers represent, akin to how the Internet Protocol (IP) connected various types of heterogeneous network designs during the initial phases of Internet development. Such a universal interconnection method must preserve the inherent trust embedded in the identifiers and facilitate the meaningful exchange of trust information between endpoints. This is essential for accurately assessing the suitability of the data these identifiers represent for the specific application contexts in which the parties may be engaged.

Note that although this specification primarily addresses decentralized identifier types, existing centralized or federated identifier types such as X.509 certificates can fulfill the VID requirements outlined in this specification. This is achievable within this specification by adopting a compliant format and enhancing the trust foundation of their corresponding support systems and governance processes.

Beyond offering enhanced trust properties when compared to previous solutions and focusing on the interoperability between differing types of VIDs, TSP is conceived as a universal protocol to serve as a foundation for various higher-layer protocols. This design approach draws inspiration from the success of the TCP/IP protocol suite. In the TSP context, directional TSP messages function as a unified primitive to bridge diverse endpoint types, similar to how IP packets enable inter-networking between distinct networks. Task level protocols or applications, intended to operate atop of TSP mirror the roles of TCP or UDP by providing task-specific solutions while harnessing the core properties of the TSP. In order to fulfill such a foundational role, TSP keeps its message primitives simple, efficient, and as much as possible eliminates unnecessary variants.

TSP messages can traverse various transport mechanisms without making prior assumptions about their trustworthiness although users may opt for specific underlying transport protocols for TSP based on various factors such as additional operational or security considerations. TSP messages can be transported directly between endpoints (Direct Mode) or routed via intermediaries (Routed Mode). We first describe the Direct Mode in [Section 3](#messages), followed by the routing mechanism in [Section 5](#routed-messages-through-intermediaries).

TSP stands as the spanning layer protocol within the Trust over IP technology architecture. It occupies a pivotal role, facilitating the twin goals of robust trustworthiness and universal interoperability across the Trust over IP stack. For additional details on the reference architecture, please see [Section 1.2](#reference-architecture).

### Terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [[ref:RFC2119]] [[ref:RFC8174]] when, and only when, they appear in all capitals, as shown here.

[[def: Verifiable Identifier, Verifiable Identifiers, VID, VIDs]]
~ A Verifiable Identifier is a category of digital identifier that meets the requirements set forth in [Section 2](#verifiable-identifiers) of the Trust Spanning Protocol Specification. The requirements include cryptographic verification and assessment of governance as well as the associated [[ref: Support Systems]]. It does not itself define a digital identifier scheme. It is not restricted to a particular type of identifier class such as, centralized, federated, or decentralized identifier trust-based ecosystems.

[[def: TSP Relationship, Relationship, Relationships]]
~ A TSP relationship is a pairing of two [[ref: VIDs]] `<VID_a, VID_b>` where `VID_a` is a VID of the local [[ref: TSP Endpoint]] `A`, `VID_b` is a VID of the remote endpoint `B` where the local endpoint `A` has verified `VID_b` for use in TSP with its `VID_a`. Each [[ref: TSP endpoint]] maintains a [[ref:Relationship Table]] that contains such pairings for all active relationships. This pairing is directional by default, but if the verification has been made mutually in both directions it is referred to as a [[ref: Bi-directional Relationship]].

[[def: Bi-directional Relationship, Bi-directional Relationships]]

~ A [[ref: TSP Relationship]] is directional by default, but if the verification has been made mutually in both directions, it is referred to as a Bi-directional Relationship and is represented as `(VID_a, VID_b)` in the [[ref: Endpoint]] `A`'s [[ref: relationship table]] and `(VID_b, VID_a)` in endpoint `B`'s relationship table. A Bi-directional Relationship means that each endpoint has verified the other's VID indepedently.

[[def: Relationship Table, Relationship Tables]]
~ A table of [[ref: Relationships]] of a [[ref: TSP Endpoint]]. Each entry of the table is a [[ref: Relationship]] where a [[ref: VID]] of the endpoint is one of two VIDs in the pairing. 

[[def: TSP Endpoint, Endpoints, Endpoint]]
~ A TSP Endpoint is a secure computational system that runs the Trust Spanning Protocol. An Endpoint is able to obtain or create certain types of [[ref: Verifiable Identifiers]] possibly through the respective [[ref: Support Systems]], and is able to verify and assess another endpoint's VIDs via their corresponding [[ref: Support Systems]].

[[def: TSP Support System, Support System, Support Systems]]
~ A TSP Support System is a computational system that supports the management of [[ref: VIDs]] and in particular, facilitates assessment and verification of VIDs of an [[ref: Endpoint]]. 

[[def: TSP Intermediary System, Intermediary System, Intermediary, Intermediaries]]
~ A TSP Intermediary System or just "intermediary", is a computational system that assists [[ref: Endpoints]] in forwarding [[ref: TSP Messages]].

[[def: TSP Message, TSP Messages, Messages]]
~ A TSP Message is a single asynchronous message in TSP with assured authenticity and optionally, confidentiality and metadata privacy.

[[def: Nested Message]]
~ Encapsulating specific data — for instance, a sequence of messages or data about the communication — within an additional envelope.  See [Section 4 Nested Messages](#nested-messages)

[[def: Out of Band Introduction, OOBI]]
~ Any method of discovering VIDs and making an initial (insecure) connection to an Endpoint. Referred to as an "OOBI".

### Reference Architecture

![TSP Reference Architecture](images/Reference-Architecture.png)

Figure 1: TSP Reference Architecture

The Trust Spanning Protocol is defined within the Reference Architecture (RA) illustrated in Figure 1. The principal components of this reference architecture are:

- Direct Communication: Endpoints communicate with each other using TSP in direct mode, depicted by an arrowed line labeled number `1`. This communication pattern encompasses two directional relationships, with each endpoint evaluating the other independently.

- Routed Communication: Endpoints communicate using TSP in routed mode through [[ref: Intermediaries]], represented by arrowed lines labeled numbers `2` and `3`. It's important to note that intermediaries are not necessarily trustworthy.

- Identifier Management: Endpoints manage their [[ref: verifiable identifiers]] (VIDs) and associated roots of trust information via an abstract interface with their [[ref: Support Systems]], shown by dotted lines labeled number `4`. Additionally, endpoints verify and assess the counterpart in a [[ref: TSP relationship]] through another abstract interface with their respective [[ref: Support Systems]], denoted by dotted lines labeled number `5`.

### Authenticity, Confidentiality, and Metadata Privacy

In TSP, these properties are defined within the context of a directional [[ref: relationship]] formed by a pair of [[ref: verifiable identifiers]] between a source and a destination [[ref: endpoint]]. In this context, the source is also referred to as the *sender* and the destination as the *receiver* of a message. Authenticity is ascertained by the receiver, providing confidence that the received message remains unaltered and that the message genuinely originates from the sender. Confidentiality ensures that only the sender and receiver have access to the protected confidential payload data content. However, some parts of the message's envelope, not shielded by confidentiality protection, can be observed and used to infringe upon privacy through traffic analysis, correlation or other exploitative means. TSP provides optional mechanisms to safeguard against these vulnerabilities. This specific type of protection is termed *metadata privacy*, differentiating it from the narrower understanding of privacy, which concerns the prevention of content exposure to unauthorized parties, synonymous with confidentiality.

TSP messages always assure authenticity, optionally confidentiality, and if utilized, metadata privacy. The authenticity and confidentiality goals are achieved by a scheme combining public key authenticated encryption (PKAE) and a signature. The metadata privacy protections are achieved by nested TSP messages and routed messages through intermediaries.

The authenticity TSP assures binds both parties: a message attests not only that it was composed by the controller of the sender's VID, but that it was composed for the controller of the receiver's VID. It can therefore neither be attributed to a sender who did not compose it, nor claimed by a receiver to whom it was not addressed, nor disowned by the sender who did.

### Use of Formats

TSP specifies message types that will have varying formats or representations during their lifecycle, both within systems that process or store them and networks that transport them. Additionally, for purposes such as debugging, documentation, or logging, these messages may need to be represented in a text format that is more accessible for human interpretation or better accepted for legal and administrative treatments.

TSP uses [[ref:CESR]] encoding for the envelope, payload structure and signature parts of TSP messages. CESR encoding allows composibility for complex cryptographic objects and easy convertions between text and binary representations while maintaining alignments of data objects. CESR supports definitive conversions between text and binary formats for the same data object. When it is necessary for clarity, we will use `B2T` and `T2B` to denote transformations from binary to text and from text to binary representations, respectively. Within TSP's payload, other types of encoding may also be used in a mixed mode. 

We introduce the notation `“{a, b, c}”` as a concatenation of CESR encoded objects. It is also denoted as `CONCAT` in pseudo code. This does not mean that the data objects have to or are always represented in a concatenated form, but because CESR encoding is self-framed and composible, the actual concatenation can be performed when needed. With that caution, we will follow this method throughout this specification. We use the special value `NULL` to represent an empty string in text or the absence of a data object. Also caution that an empty data field MAY be represented in encodings when it is transmitted. This is because TSP payload encoding use fixed field structure and the absence of a field is represented with a specific code point.

We also utilize text format for clarity and illustrative purposes within this specification. However, it should be understood that such text-based descriptions are solely to illustrate how the messages are structured. Implmentors should be aware of other formats in which cryptographic primitives are operated on or the various ways the message can be encoded for transport. For more details on serialization and encoding, please refer to [Section 9](#serialization-and-encoding).

## Verifiable Identifiers

The Trust Spanning Protocol does not mandate that [[ref: endpoints]] utilize only a single type of identifier and this specification does not define one. However, the efficacy of TSP and the trust assurance in authenticity, confidentiality, and metadata privacy it provides hinge on the methodologies of specific identifiers. Factors such as the construction and resolution coupled with the verification of trust information from their support systems directly influence the degree of trust endpoints can derive from using TSP. In this section, we outline high-level requirements without prescribing how various VID types should fulfill them. All identifiers that meet these standards are termed [[ref: Verifiable Identifiers]] (VIDs). The aim is to enable endpoints, equipped with their chosen VID type or types, to communicate over TSP with the confidence and trust level that those VIDs inherently support.

A foundational prerequisite for TSP is that endpoints operate within a secure computing environment, possibly facilitated by tools such as Trusted Execution Environments (TEEs),  digital wallets, or digital vaults. This list of tools may extend to non-technical ones such as governance conventions or regulations. While TSP aids in transmitting trust signals between endpoints, it cannot instantiate trust where none exists.

In TSP, pairs of TSP endpoints establish directional [[ref: relationships]]. In these relationships, endpoints assess each other's identifiers independently. The verification and appraisal of VIDs remain inherently directional.

### VID Use Scenarios

In the Trust Spanning Protocol, VIDs function as identifiers within protocol envelopes and other control fields (see [Section 3](#messages)). As identifiers in exposed envelopes, VIDs may be visible to third parties with access to the network transport infrastructure, allowing for potential correlation with other identifying transport mechanism information.  Examples of this information may include things such as IP addresses, transport protocol header information, and other metadata like packet size, timing, and approximate location of sender or reciever. To mitigate the risk of metadata exploitation, TSP provides Nested Messages ([Section 4](#nested-messages)) and Routed Messages ([Section 5](#routed-messages-through-intermediaries)) for certain metadata privacy protections. Given the varied roles VIDs play in different scenarios, their management requires careful consideration. To clarify and simplify the discussion, we categorize VID use into three scenarios: public, well-known, and nested.

We refer to scenarios where VIDs are exposed to external entities as their *public* use. The address resolution operations of public VIDs may provide visible information to an adversary.

It's important to note that while additional security measures like TLS or HTTPS can be employed at the transport layer to safeguard VIDs, TSP does not inherently depend on these mechanisms for protection. Consequently, within the context of TSP, even VIDs protected by such transport layer security are treated as if they are '*public*,' assuming they could potentially be accessed or observed by external parties.

Within the category of public VIDs, there is a subclass known as *well-known* VIDs. These are VIDs whose controllers deliberately intend for them to be broadly recognized. The rationale behind making a VID well-known often revolves around streamlining or simplifying the processes of VID discovery, resolution, and verification. However, it's important to recognize that such actions inherently expose additional information to potential adversaries. As a subclass of public VIDs, well-known VIDs must also meet all public VID requirements.

VIDs are considered to be in *nested* use when their usage is protected within another instance of a TSP relationship in a nested mode (See [Section 4](#nested-messages)). Nested VIDs are also called *inner VIDs* which bypass the need for address resolution. Their establishment operations are managed by TSP control messages, and all relevant operations are protected by the outer layer of TSP. For detailed descriptions of the nested mode of TSP, please refer to [Section 4](#nested-messages). The specifics regarding control messages are detailed in [Section 7](#control-messages).

### VID General Requirements
This section specifies general expections TSP requires VIDs to meet. TSP uses VID as an abstract data type that must support a set of abstract operations. This section lists these operations in a format like `VID.OPERATION`.

A VID intended for public use MUST support key rotation, and MUST support verification of the provenance of its key state — that is, an assessing endpoint must be able to establish that the current key state derives from the identifier's inception through a verifiable sequence of changes. Pre-rotation, in which a commitment to the next key is published in advance, is a common mechanism for providing this property, but may not be the only mechanism. The authority to rotate a VID's keys MUST be separate from the VID's signing key, so that an endpoint whose signing key is compromised retains the ability to rotate. VID types provide this separation in different ways — for example, by committing in advance to the next rotation key, or by designating update keys distinct from those published for signing.

A VID intended for private use between endpoints that already have an established TSP relationship need not meet these requirements. Such VIDs are verified within the existing relationship rather than by public resolution, and MAY be simple and static; an endpoint that wishes to change such a VID discards it and establishes a new one.

TSP requires that a VID be verifiable; it does not require that it be implemented in a specific decentralized, centralized or federated ways.

#### Cryptographic Non-Correlation

An endpoint can control multiple VIDs simultaneously and over extended periods. It is imperative that these VIDs are cryptographically non-correlatable in an information-theoretic security context, meaning the knowledge of one VID does not reveal any information about another.

For example, if an adversary observes VIDs `VID_a0` of endpoint `A` and `VID_b0` of endpoint `B` in a relationship `(VID_a0, VID_b0)`, where `VID_a0` is categorized as public and could be linked to a specific endpoint using additional metadata. However, if the same adversary also happens to observe `VID_a1`, it should be impossible by the identifiers alone for the adversary to establish a correlation between `VID_a1` and `VID_a0`, and consequently, to associate `VID_a1` with endpoint `A`.

#### VID Syntax

TSP tries not to impose any additional syntax requirements beyond what any VID type already mandates. But easier interoperability, we require that the VID format be either compliant DID format [[ref:DID]] or compliant URN format [[ref:RFC8141]].

#### Resolution to Transport Address

For every VID to be in public use, the VID MUST support an address resolution operation `VID.RESOLVEADDRESS` for each transport mechanism that the VID supports. 

Implementation of this address resolution operation is VID type specific.

For any VID that is used in nested mode only, an address resolution mechanism is unnecessary.

#### Mapping VID to Keys
VIDs MUST support operations by the controlling endpoint to map a VID of its own to keys required by TSP.
- Mapping to public and private keys used by PKAE: `VID.PK_e` and `VID.SK_e`.
- Mapping to private key or keys used by signature signing: `VID.SK_s` or `VID.SK_s_i`, i = 1..K.

VIDs MUST support operations by an assessing endpoint to map a VID of another endpoint to keys required by TSP.
- Mapping to the public key used by VID verification: `VID.PK_s`.
- Mapping to the public key used by PKAE: `VID.PK_e`.
- Mapping to the public key or keys used by signature verification: `VID.PK_s`, or `VID.PK_s_i`, i = 1..K.

Implementation of these mapping operations is VID type specific. When a VID has multiple signing keys, their order and the number of valid signatures required are determined by the VID type.

These operations return the assessing endpoint's current knowledge of the VID's key state. How current that knowledge is depends on the VID type and its implementation: some maintain key state continuously and reflect a change without being asked, while others are resolved on demand and are only as current as the last resolution.

#### Verification
VIDs MUST support an operation by an assessing endpoint to verify a VID of another endpoint: 
- `VID.VERIFY` for TSP to verify that endpoint `A` has access to the corresponding secret key, `VID.SK_s`, using a PKC algorithm. VID types MAY use additional information in assessing the VID in the same `VID.VERIFY` operation.

Implementation of this mapping and verification operations is VID type specific.

For any VID designated for nested use, while the same verification procedure requirements as outlined above still apply, simpler VID types MAY be employed. This is because the verification process occurs between two endpoints that already possess a verified TSP relationship between them, and the verification is conducted through TSP messages within that established relationship. TSP defines specific message types for such instances of nested VID verification in [Section 7](#control-messages).

#### Handling Changes

A VID's key state may change over time. Most VID types support key rotation, and many support pre-rotation, where a commitment to the next key is published in advance. The mechanism, and the means of verifying a change, are VID type specific — for example a did:webvh verifiable log, or a KERI key event log.

An assessing endpoint therefore treats a resolved VID as valid over a `window` of key state rather than as a fixed value. Rotation advances that window. An endpoint that has cached a resolved VID SHOULD re-resolve it when a signature fails to verify, since the peer may have rotated its keys, and MUST NOT treat a stale cached key state as authoritative.

Because the resolution and verification of key state is VID type specific, TSP does not define a rotation mechanism of its own. TSP requires only that the VID type provides `VID.VERIFY` and the key mappings in [Mapping VID to Keys](#mapping-vid-to-keys) for the current key state.

Note that rotating the keys of a VID is distinct from replacing one VID with another. Key rotation preserves the identifier, and therefore preserves existing relationships. Introducing a new VID is a separate operation, described in [Control Messages](#control-messages).

An endpoint that needs to change a private VID MAY establishe a new one rather than rotating its keys; this is also preferable for unlinkability.

### Examples

The following are examples of identifier types suitable for use as VIDs. They are informative and neither exhaustive nor privileged.

- KERI AID: An Autonomic Identifier (AID) is self-certifying: it is derived from its own inception key state, and its key event log records every subsequent change. Rotation and pre-rotation are native to the log, which provides the verifiable provenance of the current key state from inception. An AID supports multiple signing keys with weighted signing thresholds. An AID is not a DID; it is used directly, and is also the basis of the `did:webs` method below. See [[ref:KERI]].

- `did:webs`: Binds a KERI AID to a web-published DID document. Discovery and transport addresses come from the web location; key state, rotation, and provenance continue to be verified against the AID's key event log. See [[ref:DID-WEBS]].

- `did:webvh`: A web-published DID whose key state is verified against a verifiable history log. The log records rotations together with pre-rotation commitments, allowing a verifier to establish the key state at a point in the identifier's history. When it is used as a VID, the key rotation and pre-rotation features must be supported. See See [[ref:DID-WEBVH]].

- `did:peer`: A pairwise identifier requiring no public infrastructure, generated and exchanged directly between two endpoints. It is intended for private use in nested relationships, and does not meet the requirements for public VIDs. *Numalgo 4* is suitable: its short form is a digest over the DID document, exchanged once in long form and referenced thereafter. See [[ref:DID-PEER]] and [[ref:DID-PEER-4]].

- `urn:said`: A Self-Addressing Identifier is a digest over the document that contains it, expressed as a URN. Verification consists of recomputing the digest over the identified document. A `urn:said` may identify a document held in an authoritative store rather than a decentralized one, which makes it an example of a VID that is verifiable without being decentralized. See [[ref:SAID-URN]].

Several of these are constructed the same way: an AID, a SAID, and the short form of a did:peer:4 are each derived as a digest over the content or key state they identify, and each is - at least in part - verified by recomputing that digest. The identifier syntax differs; the construct does not.

## Messages

TSP operates as a message-based communication protocol. The messages in TSP are asynchronous, can vary in length, and are inherently directional. Each message has a designated sender (alternatively termed "source") and a receiver (or "destination"). Throughout this specification, in particular when we describe the routed mode in [Section 5](#routed-messages-through-intermediaries), the terms "sender" and "receiver" will be used to refer to direct neighbors, while the terms "source" and "destination" will be used for the originating and ending endpoints of the carried message. Within the context of TSP, both the sender and the receiver of a message qualify as "endpoints." Entities such as [[ref: Intermediaries]] or [[ref: Support Systems]] can also function as endpoints when they are participating in TSP communications themselves. For the sake of simplicity, we will uniformly refer to all these entities as "endpoints," unless a distinction is necessary for clarity.

In this section, we specify TSP messages that are used in Direct Mode between neighboring endpoints without any intermediaries in between. By being *direct*, we mean that there is a direct transport layer link between the two endpoints in the TSP layer. In comparision, Routed Mode, specified in [Section 5](#routed-messages-through-intermediaries), involves at least one intermediary or more in the TSP layer.

As outlined in [Section 2](#verifiable-identifiers), VIDs serve as identifiers for any endpoints involved in TSP. Both the sender's VID and the receiver's VID can map to required keys used by TSP in the sender and the receiver, and to a transport address for delivering the TSP message.  The sender and receiver VIDs can be of different VID types.

TSP messages are made of three parts: envelope, payload and signature, as illustrated in the pseudo-formula below.

```text
TSP_Message = {TSP_Envelope, TSP_Payload, TSP_Signature}
```

We now define these parts in the following sections.

### TSP Envelope

The TSP envelope part of a TSP message contains: TSP Version, Sender VID, Receiver VID.

```text
TSP_Envelope = {TSP_Tag, TSP_Version, VID_sndr, VID_rcvr | NULL}
```

- TSP_Tag: A unique code that unambigously flags the start of a TSP envelope.
- TSP_Version: The version of Trust Spanning Protocol. The TSP version should follow semantic versioning practices with three numbers representing MAJOR, MINOR, PATCH. MAJOR version signals backward compatibility MAY not be maintained with previous versions.

The current experimental draft's version is `0.1.0`. When this specification is officially released, the first version is to be `1.0.0`.

VIDs in TSP are encoded with a variable length VID_String that consists of length followed by a bytestring of that length. Two types of identifier syntaxes, DID [[ref:DID]] and URN [[ref:RFC8141]], MUST be supported. Implementations MAY support additional syntaxes beyond these two types.

The DID specification allows various DID Methods. The URN specification allows various URN namespaces. This specification does not mandate any particular DID Methods or URN namespaces but would benefit from such standardizations elsewhere. In all variations, if a TSP implementation does not support any type of VIDs, it SHOULD discard the TSP message.

Please see Section [TSP Envelope Encoding](#tsp-envelope-encoding) for further information about VID encoding. 

`VID_sndr` and `VID_rcvr` (if present) may be different types of VIDs.

### TSP Payload

The TSP payload is either control message payload used by TSP itself or application message payload used by the higher layer. It is structured uniformly with a payload type followed by a series of data fields that is dictated by the type. The payload may be encrypted and encoded as a single ciphertext (entirely confidential), or entirely non-confidential (signed only), but never mixed. The payload field definitions are all described in plaintext in this specification. When it is helpful, we may use affix `_ciphertext` or the adjective confidential to indicate that the data therein is actually encrypted ciphertext of what is being presented.

The TSP payload may be recursively nested where a payload field may itself be a TSP message. See [Nested Messages](#nested-messages). The terms of payload and payload field therefore must only be understood as relative within the current level of payload structure being referenced.

```text
TSP_Payload = {TSP_Payload_Tag, TSP_Payload_Type, TSP_Payload_Field1, ...}
```

The TSP defines payload types that are used for [Nested Messages](#nested-messages), [Routed Messages](#routed-messages-through-intermediaries), and the higher level management of TSP operations [Control Messages](#control-messages).

Higher layer application messages use the general payload type `TSP_GEN`.

#### Payload Fields

Each payload consists of a type and a number of fields determined by the type. They will be defined in the corresponding sections when their functions are defined.

Some payload fields are required by TSP, including the sender VID `VID_sndr` used for ESSR ([[ref:ESSR]]) operations in the *Libsodium Sealed Box* ([[ref:libsodium]]) mode and VID list used in routing mode. When it is necessary to differentiate these fields, we will refer them as Control Fields or Control Payload Fields. These control fields are used for all messages, not just control messages.

#### Ciphertext of the Confidential Payloads

If TSP_Payload is confidential, the corresponding ciphertext is produced as:

```text
TSP_Payload_Ciphertext = TSP_SEAL(TSP_Payload)
```
It is this ciphertext that is encoded and sent on the wire.

The details of the supported PKAE schemes for the `TSP_SEAL` operation are specified in Section [Cryptographic Algorithms](#cryptographic-algorithms).

For the PKAE scheme *Libsodium Sealed Box* ([[ref:libsodium]]), the `VID_sndr` MUST appear as a confidential payload field following the ESSR ([[ref:ESSR]]) method. For the PKAE scheme *HPKE-Base* ([[ref:HPKE]]), the `VID_sndr` field is not mandatory in the confidential payload and MAY be encoded as a NULL VID. See [Section 8](#cryptographic-algorithms) for the details.

On the receiving side, the corresponding TSP primitive is `TSP_OPEN`.

### TSP Signature

The third part of a TSP message is the message signature of the sender.

```text
TSP_Signature = TSP_SIGN({TSP_Envelope, TSP_Payload})
```
On the receiving side, the corresponding primitive is `TSP_SIGN_VERIFY`. The details of the `TSP_SIGN` and `TSP_SIGN_VERIFY` are specified in Section [Cryptographic Algorithms](#cryptographic-algorithms).

### Relationships

A [[ref: TSP relationship]] is a pairing `<VID_a, VID_b>` of two VIDs controlled by the respective endpoints `A` and `B` indicating that endpoint `A` has satisfactorily verified `VID_b` of endpoint `B`.

An endpoint is able to obtain (or create) one or more VIDs possibly through the service of their respective [[ref: Support Systems]]. Let us say `VID_a` is one such VID for endpoint `A`. As a convention, we will use a lower case letter, such as `a`, to indicate that `VID_a` is controlled by the endpoint named with the corresponding upper case letter, say `A`. Details of VID management for any particular VID type is out of scope for this specification but an endpoint will need to implement necessary support for all of the VID types it supports.

Endpoint `A` learns a `VID_b` of endpoint `B` via either [Out of Band Introduction](#out-of-band-introductions) or other TSP [Relationship Forming Protocol](#relationship-forming-protocol). At this point, endpoint `A` chooses `VID_a` and performs necessary verification and appraisal operations on `VID_b` with respect to `VID_a`. If this verification is successful, endpoint `A` may add a relationship `<VID_a, VID_b>` to its relationship table.

Afterwards, endpoint `A` may resolve `VID_b` to obtain a transport layer address for delivery of a TSP message with `VID_a` as the sender `VID_sndr` and `VID_b` as the receiver `VID_rcvr`.

When endpoint `B` receives this TSP message, if this is the first TSP message from `VID_a` to `VID_b` and endpoint `B` has not verified `VID_a` before, endpoint `B` will perform the necessary verification and assessment to evaluate `VID_a` with respect to `VID_b`. If successful, endpoint `B` may also add a relationship `<VID_b, VID_a>` to its relationship table.

In short, one successful TSP message exchange between two endpoints populates one relationship on each endpoint's relationship table. The relationships in their respective tables are the mirror image of each other in the form of `<VID_local, VID_remote>`. We may interpret this relationship as the state that the endpoint has verified `VID_remote` with respect to `VID_local`. We say the pair of VIDs are in a *verified* state. Note that due to the the asynchronous nature of TSP messages such a state is not always synchronized between the two endpoints. Their relationship tables are not guaranteed to be accurate.

Since endpoints may reuse VIDs, an endpoint may have relationships `<VID_a, VID_b>` and `<VID_a, VID_c>` in its relationship table at the same time. Only a pair uniquely identifies a relationship in TSP.

Endpoints may have semantic meaning or application specific meanings associated with their VIDs. For this reason we say an endpoint `A` verifies and assesses a `VID_b` with *respect to* `VID_a`. This evaluation process may have dependency based on the chosen `VID_a`.

After endpoint `B` processes the first TSP message from `VID_a` to `VID_b` and has accepted a new relationship `<VID_b, VID_a>` it may decide to reply with its own TSP message in the opposite direction. It is common, although neither required nor always needed, that the two endpoints want to engage in bi-directional communication. At this point, endpoint `B` can update the corresponding relationship into a [[ref: bi-directional relationship]] `(VID_b, VID_a)`. Upon successfully receiving the return TSP message by endpoint `A`, it can also update its relationship to bi-directional: `(VID_a, VID_b)`.

::: note
The notation `<VID_local, VID_remote>` is used for representing a uni-directional relationship, and `(VID_local, VID_remote)` for a bi-directional relationship.
:::

For details of the relationship forming TSP control messages, please refer to [Section 7](#control-messages). The following Sections [3.6](#sender-procedure) and [3.7](#receiver-procedure) describes in detail the operations required for sending and receiving TSP messages.

### Sender Procedure

We outline the procedures for TSP message senders for the simple Direct Mode case in two parts: the initial message which establishes the relationship and the follow-up messages that occur within that established relationship.

Endpoint `A`, which controls `VID_a` associated with Support System `A*`, acquires `VID_b` of Endpoint `B` through an [out-of-band introduction (OOBI)](#out-of-band-introductions), or a TSP [relationship forming message](#control-messages) of another existing relationship. `VID_b` is tied to Support System `B*`. Note that `A*` could be the same as or different than `B*`. If Endpoint `A` selects to employ `VID_a` to dispatch a TSP message to the Endpoint identified by `VID_b` for the first time, it will be establishing a unidirectional relationship denoted by `<VID_a, VID_b>`.

The following is an example procedure that Endpoint `A` may follow when sending its inaugural message to `VID_b` using its own `VID_a`. This example is only illustrative. Implementors will need to pay consideration to the actual VID types, the chosen transport mechanism's requirements, and the requirements of applications they intend to support.

- Step 1: Resolve `VID_b` to acquire access to the following mandatory information
    - Public keys bound to the VID for TSP: `VID_b.PK_e`, `VID_b.PK_s`
    - All other VID verification information as required by the VID type ([Section 2](#verifiable-identifiers))
    - Transport information if it is not yet known.
- Step 2: Verify `VID_b` with `VID_b.VERIFY`.
- Step 3: Create a TSP message
    - As the first TSP message, it MUST contain the relationship forming payload fields.
    - It MAY optionally also contain other user data. In other words, applications do not have to wait for a round trip delay for relationship establishment.
- Step 4: Use the retrieved transport information in Step 1 to establish a means of transport, if not yet available. Note that this step will be significantly different depending on the details of the transport mechanism of choice. [Section 10](#transports) discusses additional transport considerations.
- Step 5: Send the TSP message.
- Step 5: Update relationship table with `<VID_a, VID_b>`.

For subsequent messages, the procedure is simpler:

- Step 1: Create a TSP message
- Step 2: If the retrieved transport mechanism is ready to use (e.g. if it's cached or kept hot), send the message. If not, refresh operations may be needed first.

Note, in our simplified example above we have not considered any dynamic changes or error conditions that may arise.

### Receiver Procedure

Similar to the previous section, the following example is only illustrative of the reception of a simple Direct Mode TSP message.

If endpoint `B` receives a TSP message of the generic form `{... VID_sndr, VID_rcvr, ... TSP_Payload_Ciphertext, TSP_Signature}`, endpoint `B` may follow these steps to process this incoming message:

- Step 1: Check if the `VID_sndr` and `VID_rcvr` pair matches an existing valid relationship in its relationship table. If yes, jump to Step 5; otherwise this is the first message of this relationship.
- Step 2: Check if `VID_rcvr` is a valid local VID and local rules permit to proceed.
- Step 3: Resolve `VID_sndr` to acquire access to the following mandatory information
    - Public keys bound to the VID for a TSP crypto suite
    - All other VID verification information as required by the VID type ([Section 2](#verifiable-identifiers))
    - Transport information, if it is not yet known.
- Step 4: Verify, and appraise `VID_sndr` using additional information and processes specific to the VID.
- Step 5: Verify the `TSP_Signature`.
- Step 6: Decrypt the `TSP_Payload_Ciphertext`. A decryption failure is also a verification failure.
- Step 7: If the PKAE variant is *Libsodium Sealed Box*, retrieve the sender VID from the decrypted payload plaintext and verify that it matches `VID_sndr`. If the PKAE variant is *HPKE-Base*, then the sender VID field may contain either NULL or a valid VID; if it is a valid VID, also verify that it matches `VID_sndr`, otherwise no checking is necessary for NULL.
- Step 8: Process the rest of the control fields.
- Step 9: Return the payload to the upper layer application.

CESR primitives are canonically encoded: lead bytes and pad bits are zero. A receiver MUST reject a message containing a primitive whose pad bits are non-zero. Because TSP digests and signatures are computed over exact encoded bytes, accepting a non-canonical encoding would admit distinct byte sequences for the same value.

If a message fails any verification or validation step, the receiving endpoint SHOULD silently discard it. Where the message is from a VID with which the endpoint has an established relationship, and the endpoint is responsible for resolving that VID's key state itself (rather than relying on the VID type to do so outside of TSP operations), it SHOULD first re-resolve and retry the verification once, as described in [Key Update](#key-update).

An endpoint SHOULD NOT act on a message when it is unable to confirm the key state of the sending VID, or when the key state it obtains conflicts with the key state it holds rather than extending it. In these cases the endpoint suspends its reliance on that key state: it accepts no message under it, including a message that would otherwise verify, until the key state can be confirmed. An endpoint MAY retain such messages and process them if the key state is subsequently confirmed.

An endpoint MAY direct the transport layer to disconnect, block, or filter further messages from a source whose messages repeatedly fail verification, but SHOULD NOT do so on the basis of a single failure within an established relationship. A receiver SHOULD NOT respond to a failed message, as any response may disclose information to an attacker.

### Out of Band Introductions

Before an endpoint `A` can send the first TSP message to another endpoint `B` it must somehow discover at least one VID that belongs to `B`. If A also wishes to utilize Routed Mode, as specified in [Section 5](#routed-messages-through-intermediaries), then additional VIDs may also be needed before the first TSP routed message can be sent. We call any such method that helps the endpoints discover such prerequisite information an [[ref:Out of Band Introduction]]. There may be many such OOBI methods. Detailed specifications of OOBI methods are out of scope for this specification.

For the purpose of TSP, information obtained from OOBI methods must not be assumed authentic, confidential, or private, although verification and security mechanisms to remedy such vulnerabilities should be adopted whenever possible. TSP implementations must handle all cases where the OOBI information is not what it appears.

Because TSP relationships can be highly authentic, confidential, and potentially provide more privacy with respect to metadata than OOBIs, they can be used for the purpose of passing VID information for forming new relationships. Details of such procedures that can be used for such introductions are specified in Section [Control Messages](#control-messages).

## Nested Messages
When TSP sender `A` dispatches a TSP Message with confidential payload intended for receiver `B`, the observable data structure for any third party not involved in the message exchange between `A` and `B` appears as:

```text
{TSP_Tag, TSP_Version, VID_a, VID_b, TSP_Payload_Ciphertext, TSP_Signature}
```

Over time, with a sustained exchange of such messages, an external observer may accumulate a significant volume of data. This data, once analyzed, could reveal patterns related to time, frequency, and size of the messages. Using `VID_a` and `VID_b` as keys, an observer can index this dataset. It's then possible to correlate this indexed data with other available metadata, potentially revealing more insights into the communication.

To mitigate this threat, TSP offers a technique whereby parties encapsulate a specific conversation — for instance, a sequence of messages — within an additional TSP envelope, as described below.

### Payload Nesting
Suppose endpoints `A` and `B` have established a prior direct relationship `(VID_a0, VID_b0)`.  They can then embed the messages of a new relationship `(VID_a1, VID_b1)`  in the confidential payload of `(VID_a0, VID_b0)` messages. In such a setup, `VID_a1` and `VID_b1` are protected from third party snooping. We may refer `(VID_a0, VID_b0)` the *outer relationship* and the messages of `(VID_a0, VID_b0)` as *outer messages*.  Similarly, `(VID_a1, VID_b1)` the *inner relationship* and the messages of `(VID_a1, VID_b1)` as *inner messages*.

The above description also applies to uni-directional relationships.

This nesting scheme can be illustrated as follows using the confidential data field of its payload.

```text
Outer_Message = {Envelope_0, Payload_0, Signature_0},
Inner_Message = {Envelope_1, Payload_1, Signature_1}, 
Nested_Message = {Envelope_0, Control_Fields_0, TSP_SEAL_0(Inner_Message), Signature0}
```
`TSP_SEAL_0` indicates that the `TSP_SEAL` operation uses the outer message sender's keys. `Control_Fields_0` indicates the control fields of the outer message payload.

In this scheme, the outer message MUST be confidential: the inner message is carried in the outer message's encrypted payload, and it is this outer encryption that conceals the inner message's metadata. We do not otherwise restrict the structures of the inner and outer messages. In particular, the inner message itself MAY be a non-confidential (signed-only) message, since the outer encryption already protects its contents in transit. Applications should note that in that case the confidentiality of the inner payload derives entirely from the outer relationship — it is protected under the outer relationship's keys, not the inner relationship's.

### Nested Relationships

When TSP messages utilize this nesting approach, a new relationship, for example `(VID_a1, VID_b1)`, is created between the same endpoints `A` and `B`. This new type of relationships may be used for providing *context* over the aggregate of all messages between the same pair of endpoints. The privacy protection afforded by this method is designated as one example of *metadata privacy.* Since the nested messages hide the inner VID pair from being collected as a part of potential correlation attacks, we also refer to this style of privacy protection as *correlation privacy.*

The process for establishing such relationships with nested messages is detailed in [Section 7](#control-messages). It's important to note that this nesting can be recursively applied, adding additional layers as required. Inner relationships are situated within an outer relationship that has been verified and deemed suitable for the intended purpose by both participating endpoints. The VIDs engaged in these inner relationships may therefore be considered as *private*, do not require same level of verification as *public* VIDs, and do not require transport layer address resolution of their own.

### A Shorthand Notation
For brevity and ease of presentation, we introduce a shorthand notation for nested messages, and indirectly the relationship in which these messages are communicated, as follows.

``` text
[VID_sndr, VID_rcvr, Payload] = {TSP_Tag, TSP_Version, VID_sndr, VID_rcvr, TSP_Payload, TSP_Signature}
```
This is only a simplication in notation. All message fields remain the same as defined in the previous sections, including the control fields and the generation of ciphertext and signature fields.

``` text
[VID_sndr_out, VID_rcvr_out, [VID_sndr_in, VID_rcvr_in, Payload_in]] = {
    Envelope_out, TSP_SEAL_out(Inner_Message), Signature_out }

where,
Inner_Message = [VID_sndr_in, VID_rcvr_in, Payload_in, Signature_in]
```

Such a notation does not imply any extra requirements or restrictions for the messages. 

For example, we may use the following shorter notation to represent the example nested message shown above:

`[VID_a0, VID_b0, [VID_a1, VID_b1, Payload]]`

In this notation, the term `Payload` should be interpreted as the rest of the payload that we are not paying attention at the moment since we often are focused on the control fields to describe TSP's operations without burdening ourselves with other parts of the payload. When in doubt, please refer to the corresponding message definition sections and the encoding sections for clarity.

## Routed Messages Through Intermediaries

Intermediaries are systems utilized by endpoints to enhance various aspects of TSP communication, such as asynchronous delivery, reliability, performance, among others. In this specification, our primary focus is on their role in ensuring metadata privacy protection for communications between endpoints.

### Metadata Privacy in Routed Mode

Metadata privacy is one of the primary goals of deploying TSP in the routed mode. The TSP endpoints, the sender and receiver, aim to route their messages through chosen intermediaries, maintain the same authenticity and confidentiality properties of TSP, and enhance the protection of metadata privacy related to the following exposures:

- The exposed direct neighbor relationship VIDs and related network transport information used to carry TSP messages are publicly knowable by all third parties. The TSP routed mode shields exposure of VIDs in endpoint-to-endpoint relationships through nested envelopes as defined in [Section 4](#nested-messages).
- VIDs used in routing and part of route information are knowable by the intermediaries along the routing path by necessity. The intermediaries are given only limited trust related to carrying out routing functions. Another layer of nesting allows endpoints to shield their inner contextual relationship VIDs from the intermediaries in the routing path.

In the high level, an overall endpoint-to-endpoint TSP routed mode involves three types of relationships.

- Direct neighbor relationships
    - Sender and its intermediary relationship
    - Intermediary to intermediary relationship
    - Receiver and its intermediary relationship
- Endpoint-to-endpoint relationship
- Nested private endpoint-to-endpoint relationship

TSP routing is accomplished by combining a list of designating intermediaries in the routing path with those intermediaries unwrapping nested messages and routing via direct neighbor relationships. The neighbors may create a specific routing context relationship for the purpose of routing messages en route.  A typical three hop pattern of TSP routed messages will traverse from source endpoint `A` to its intermediary `P`, then from `P` to another intermediary `Q`, and then from `Q` to the destination `B`. Naturally, the number of intermediaries in the route path may not be limited to 2. We generalize such a route path as `VID_hop1, VID_hop2, ..., VID_hopk, VID_exit`, where:
- `VID_hop1` is the VID of the first intermediary that is in direct relationship with the source.
- `VID_hop2, ..., VID_hopk`: are VIDs of the intermediaries in the chosen route path. `VID_hopk` must be the last intermediary that is in direct relationship with the destination endpoint.
- `VID_exit`: This is the VID by which the destination is known to the `hopk` intermediary in their direct relationship. It is chosen by the destination, and is the VID the destination shares with the source in order to be reached over that route.

The final entry in the hop list is the destination's own VID with its intermediary, rather than the intermediary's VID in that relationship. Either would allow the intermediary to identify the relationship, but carrying the destination's VID means the identifier exposed to the source, and to intermediaries along the route, is one the destination chose rather than one its intermediary chose. It also leaves the intermediary free to change the VIDs it uses without invalidating the routing information its clients have already shared, so that an intermediary cannot oblige its clients to re-establish their routing information with every correspondent with a change of its own VID in their relationship.

The exact nature of how the intermediaries exchange necessary information in order to perform the routing of TSP messages needs not be fixed or follows a pre-determined way. We describe some ways in which this may be accomplished but implementors are free to use other ways to achieve the same goal.

### Routed Messages

For routed messages, we need to distinguish the terms “sender”, “source”, “receiver”, and “destination". We reserve the terms “sender” and “receiver” for direct neighbor relationships between whom the message is being transported from one party to another (i.e. being routed). We reserve the terms “source” and “destination” for endpoint-to-endpoint relationships between whom the carried inner message is being communicated.

As we will see below, the source endpoint MAY choose the first hop of the route, then must acquire the remaining route path information `[VID_hop2, ..., VID_hopk, VID_exit]` before it can attempt to route a TSP message through a series of intermediary hops. This route path information MAY be acquired in part from an [Out-Of-Band Introduction](#out-of-band-introductions), TSP control message ([Section 7](#control-messages)), or may be communicated by other means outside the scope of this specification.

For the common case of `k = 1 or k = 2`, the route hop list MAY be acquired via a simple arrangement:
- The source endpoint `A` chooses an intermediary `P` and establishes a relationship with `P`, `(VID_a1, VID_p1)`, then `VID_hop1` is `VID_p1`. This VID is used as the `VID_rcvr` in the envelope.
- The destination endpoint `B` chooses an intermediary `Q` and establishes a relationship with `Q`, `(VID_b1, VID_q1)`, then `VID_exit` is `VID_b1`. The intermediary `Q`, as a common service provider, may have published a well-known public `VID_q0`, then `VID_hop2` could be `VID_q0`.
- The destination endpoint `B` MAY share the routing information `(VID_q0, VID_b1)` in the Out-Of-Band Introduction mechanism or via a control payload TSP message in another TSP relationship, together with its chosen `VID_destination`.
- The source endpoint `A` combines the routes together to form the whole message: `[VID_a1, VID_p1, VID_q0, VID_b1, Payload]`.
- If the intermediary chosen by `B` is also acceptable to `A`, and the parties accept a single intermediary (with the potential loss of some metadata protection), then the resulting route may simply be `[VID_sndr, VID_intermediary_rcvr, VID_exit, Payload]`.

TSP routed messages have the same TSP Envelope as TSP messages sent in direct mode but extend the control field of the payload with the following structure:

``` text
Control_Payload_Fields = {VID_sndr, VID_hop2, ..., VID_hopk, VID_exit}
```
The first field `VID_sndr` is the sender VID required by ESSR ([[ref:ESSR]]) PKAE schemes. This field is always present in every TSP payload; its value MAY be the NULL VID `4BAA` where the PKAE variant permits, as specified in [Ciphertext of the Confidential Payloads](#ciphertext-of-the-confidential-payloads) and [Receiver Procedure](#receiver-procedure).

The VIDs following the first `VID_sndr` is an ordered list of next hop VIDs of intermediary systems and the last VID represents the destination endpoint. The list can vary in length from 1, 2, to k > 2, and should be interpreted as an ordered routing path with the `VID_hop2` coming first, followed by `VID_hop3`, `VID_hop4` etc... Note that the first hop is already identified as the `VID_rcvr`.

In our shorthand notation, we also include the destination’s intermediary VIDs.

``` text
[VID_sndr, VID_rcvr, VID_hop2, ..., VID_hopk, VID_exit, Payload]
```

The VID hop list MUST be in the control payload fields.

Each intermediary processes the received TSP message `{VID_sndr, VID_rcvr, Payload}` normally and after `TSP_OPEN` it MUST process the control payload information to see if routing hops are present. If they are, the intermediary MAY consult other administrative or operational conditions then decide to forward the message payload to the next hop identified by the first VID in the list. The forwarded message will use that VID as `VID_rcvr` and remove it from the list before forwarding.

If the confidential payload fields are chosen for the routing fields, then for any third party, this message appears as a normal TSP message in the form of `{VID_sndr, VID_rcvr, Ciphertext, Signature}`.

### Direct Neighbor Relationship and Routing

Endpoint `A` chooses an intermediary, denoted as `P`, and forms a bidirectional neighbor relationship. In Figure 2, the neighbor relationship between `A` and `P` is illustrated as: `(VID_a1, VID_p1)`, which is assumed to be established before message routing takes place. This assumption also applies to neighbor relationships between intermediaries `P` and `Q`, and between endpoint `B` and its intermediary `Q`, as shown in Figure 2. Message routing between endpoint `A` and endpoint `B` takes place within this established network of relationships.

![Direct Neighbor Relationships](images/Direct-Neighbor-Relationships.png)

Figure 2: Direct neighbor relationships

These direct neighbor relationships allow for direct TSP messages as listed below:

- `[VID_a1, VID_p1, Payload]`
- `[VID_p0, VID_q0, Payload]`
- `[VID_q1, VID_b1, Payload]`

We will detail each party’s operations in the following sections.

#### The Source Endpoint
The source endpoint `A` sends the following routed message to intermediary `P`:

``` text
[VID_a1, VID_p1, VID_q0, VID_b1, Payload]
```

Again, the VIDs (`VID_q0` and `VID_b1`) may become known to endpoint `A` prior to this step via an OOBI, a TSP control payload, or another discovery protocol out of scope of this specification. Note that in this outer layer, all VIDs are public while `p0` and `q0`, as public VIDs of intermediaries may also be well-known.

#### The Source Endpoint's Intermediary

The source’s intermediary `P` MUST support routed messages. As previously specified, the intermediary MUST decrypt the payload, if the payload is confidential then process its control fields to retrieve the route VID(s). The next VID in the list, `VID_q0` in this case, is the next hop’s VID. `P` MUST attempt to route the carried message to the next hop if not barred by administrative or operational conditions from doing so.

If the `(VID_p0, VID_q0)` relationship is pre-existing, `P` will already know how to forward the message. If it is not pre-existing but `VID_q0` is public, `P` can resolve it and establish a new `<VID_p0, VID_q0>` or `(VID_p0, VID_q0)` relationship using normal procedures specified in [Section 3](#messages). `P` then routes the message to `Q` using the following message:

``` text
[VID_p0, VID_q0, VID_b1, Payload]
```

Note that the new `VID_sndr` and `VID_rcvr`, and the shortened VID route list (`VID_b1` only).

#### The Destination Endpoint's Intermediary

The destination’s intermediary, `Q`, also decrypts, if it's confidential, the control payload fields to retrieve the remaining route VID list. The next VID in the list, `VID_b1`, is the next hop’s VID. `Q` must attempt to route the carried message to the next hop.

If `VID_b1` is given to endpoint `A` by `B` itself in either an Out-Of-Band Introduction or a TSP control payload message, the `<VID_q1, VID_b1>` or `(VID_q1, VID_b1)` relationship should be pre-existing, and `Q` will know how to forward the message. If that relationship is not found in its local relationship table (ie the relationship hasn't been established), the intermediary `Q` should consider this an error. Otherwise, `Q` forwards this message to endpoint `B` using the following direct message:

``` text
[VID_q1, VID_b1, Payload]
```

Note that this is a normal direct message as the route VID field is now empty.

#### The Destination Endpoint

When the destination receives the message it is now a normal direct mode message: `[VID_q1, VID_b1, Payload]`. Note that endpoints are not required to handle routed messages that contain additional next hop VID or VIDs.
Unlike direct mode messages, this message’s sender `VID_q1` is of the intermediary `Q`, but the source is `A`; and its receiver `VID_b1` is associated with the relationship with `Q`, not `A`. This means that the destination endpoint `B` can not be assured of the message’s authenticity, confidentiality, or metadata privacy. To solve these problems, endpoints MUST use additional procedures specified in the following sections.

### Endpoint-to-Endpoint Messages


In [Section 5.3](#direct-neighbor-relationship-and-routing), we defined a routed operation method that enables a source endpoint to send a TSP message to a destination endpoint via a series of intermediaries, using a hop-by-hop approach. However, while this approach provides a way of message delivery from the source to the destination, it doesn't uphold the core trust properties TSP aims to provide — specifically, authenticity, confidentiality, and metadata privacy — with respect to third parties or intermediaries. In this section, we define endpoint-to-endpoint messages carried within the payload of routed messages and the corresponding endpoint-to-endpoint relationship which does ensure authenticity, confidentiality, and a degree of metadata privacy. This operation is illustrated in Figure 3 below.

![Endpoint-to-Endpoint Relationship Through a Routed Path](images/Endpoint-to-Endpoint-Relationship-Through-A-Routed-Path.png)

Figure 3: Endpoint-to-Endpoint relationship between endpoints A and B through a routed path

#### The Source Endpoint

The source endpoint `A` will create an endpoint-to-endpoint relationship with endpoint `B` using the same procedure specified in [Section 3](#messages). Instead of direct messages as in Section 3, the endpoint `A` will use routed messages defined in [Section 5.3](#direct-neighbor-relationship-and-routing). Recall in Section [5.3.1](#the-source-endpoint), endpoint `A` sends the following message to intermediary `P` en route to eventual destination `B`:
``` text
[VID_a1, VID_p1, VID_q0, VID_b1, Payload]
```
To create an endpoint-to-endpoint relationship between `A` and `B`, Endpoint `A` will encapsulate its [relationship forming message](#control-messages) with endpoint `B` as follows:

``` text
[VID_a1, VID_p1, VID_q0, VID_b1, [VID_a2, VID_b2, Payload_e2e]]
```

Because this is the first layer at which endpoint-to-endpoint communication takes place, a source that requires confidentiality with respect to the intermediaries MUST encrypt at this layer, and MUST NOT rely on the protection provided by the direct neighbor relationships as permitted in [Section 4](#nested-messages). Where the source does not require confidentiality — for example where the payload is intended to be public — it MAY send the endpoint-to-endpoint message as a non-confidential (signed-only) message, and the intermediaries will be able to read it. Signing at this layer is required in either case, as it is for all TSP messages.

#### The Destination Endpoint

As described in [Section 5.3](#direct-neighbor-relationship-and-routing), this message will be delivered to the destination `B` in the form of,
``` text
[VID_q1, VID_b1, Payload]
```
This message is routed transparently by the intermediaries (or a single intermediary). The destination endpoint `B` decrypts its confidential payload to retrieve the inner message with `Payload_e2e`:
``` text 
[VID_a2, VID_b2, Payload_e2e]
```

Note that the intermediaries (or intermediary) have visibility to `VID_a2` and `VID_b2` but not to `Payload_e2e` if it is embedded in the confidential payload fields.

Now the destination `B` has a Direct Mode message from the source with `VID_a2` and addressed to its own `VID_b2` and can perform the same procedure as specified in [Section 3](#messages) to ensure authenticity and confidentiality, and establish the corresponding relationship `<VID_a2, VID_b2>`. In terms of metadata privacy, `VID_a2` and `VID_b2` are not visible to third parties but are visible to intermediaries. 

To minimize potential risks of exposure, the intermediaries SHOULD not process the endpoint-to-endpoint VIDs `VID_a2` and `VID_b2` and MUST NOT store `VID_a2` and `VID_b2` in any persistent storage.

As described in [Section 4](#nested-messages), endpoints may use nested messages to further strengthen metadata privacy. This is also true for routed messages. In the next section, we specify such a nested method such that contextual VIDs between endpoints `A` and `B` can be hidden from the intermediaries as well.

### Nested and Private Endpoint-to-Endpoint Messages

In this section, we specify an operation using nested messages over the endpoint-to-endpoint messages described in the previous section. The purpose of this nested mode is to hide the private contextual VIDs from being visible to the intermediaries. Use of this method is optional.

The nested private endpoint-to-endpoint pattern is illustrated in Figure 4.

![Nested Endpoint-to-Endpoint Relationship Through a Routed Path](images/Nested-Endpoint-to-Endpoint-Relationship-Through-A-Routed-Path.png)

Figure 4: Nested endpoint-toendpoint relationship between endpoints A and B through a routed path

#### The Source Endpoint
Using procedures defined in Sections [4](#nested-messages) and [5](#routed-messages-through-intermediaries), endpoints `A` and `B` choose `VID_a3` and `VID_b3` respectively for the private contextual relationship. The source `A` then sends its message to `B` using a message described in the previous section as follows:

``` text
[VID_a1, VID_p1, VID_q0, VID_b1, [VID_a2, VID_b2, Payload_e2e]]
```

The nested inner message is then embedded into the `Payload_e2e`:
``` text
[VID_a3, VID_b3, Payload_inner]
```

Since `Payload_e2e` is inside of the endpoint-to-endpoint confidential payload, `VID_a3` and `VID_b3` are not visible to intermediaries.

#### The Destination Endpoint
As described in [Section 5.4](#endpoint-to-endpoint-messages), the destination `B` receives:
``` text
[VID_q1, VID_b1, [VID_a2, VID_b2, Payload_e2e]]
where,
Payload_e2e = [VID_a3, VID_b3, Payload_inner]
```

`B` then decrypts `Payload_e2e` as needed, and then verifies and forms another relationship `<VID_a3, VID_b3>` and receives the payload `Payload_inner`.

### Routing with a Single Intermediary

The endpoints `A` and `B` may use the same intermediary, i.e, `P` = `Q`. Since `A` and `B` usually choose their intermediaries independently this scenario may happen by coincidence. Regardless of how it occurs, the operation specified in this section continues to ensure the same trust properties as with differing intermediaries except for the fact that a compromise of a single intermediary may expose the whole routing path.

### Routing with More Than Two Intermediaries

When the intermediary hop count `k > 2`, the routed message format remains the same. The routing hops between intermediaries, e.g. between `P` and `Q`, will be repeated multiple times.

The source endpoint MAY learn and compose the route path by a combination of the source's choices, and/or the destination's choices (that have been shared with the source via the Out-Of-Band Introduction mechanism, separate TSP message with control payload fields, or other means that are out of scope for this spec).

## Multi-Recipient Communications

This section is informative.

TSP messages are between two endpoints identified by `VID_sndr` and `VID_rcvr`. This is a typical point-to-point messaging pattern. Upper layer applications that use TSP, however, may implement some methods of sending messages to multiple recipients using the TSP messages defined in this specification. This section describes two simple methods. 

Native TSP multicast messages are out of scope for this specification.

### Multi-Recipient List

In this scheme, an endpoint maintains a list of relationships `(VID_0, VID_remote_i)` where `VID_0` is a local VID, and `i = 1..K-1`. For each message payload, one copy of a TSP message is sent over each relationship: `[VID_0, VID_remote_i, Payload], i = 1..K-1`.

For a group of `K` member endpoints, there will be `K-1` bi-directional relationships at each endpoint. The total mesh group consists of `K(K-1)` relationships. If these are all simple Direct Mode relationships, each endpoint will use one VID for the group.

Endpoints in such a group MAY also use Nested Mode and Routed Mode as they wish for each or all of these relationships.

Each TSP message is duplicated and individually encrypted (if confidential) over each relationship.

The group membership management mechanism MAY be implemented using TSP relationships themselves as an introduction mechanism. For example, if `endpoint_0` has an existing relationship with each other member `endpoint_i, i = 1..K-1`, it may use those relationships to introduce the members to each other, so that they can establish relationships `(endpoint_i, endpoint_j), i, j in range of 1..K-1, i != j`.

See [Section 3.7](#out-of-band-introductions).

### Anycast Intermediary

A common use case of sending TSP messages to multiple recipents is to anycast authenticated but not encrypted messages to anyone who is interested in receiving them, e.g. by subscribing to a messaging service or by social media recommendation algorithms.

Since these messages are not confidential, the distribution of these messages can be performed by an intermediary.

Although these messages are authenticated to a sender's VID, the messages between the sender and its intermediary can still be confidential. In fact, they can be communicated from the source to its intermediary over a Nested Mode relationship specific to the anycast group (or similar notions supported by the intermediary). The details of such mechanisms are out of scope for this specification.

## Control Messages

This section specifies control payload fields that are required for the proper functioning of TSP. TSP Messages that carry such *control fields* can be informally referred to as *Control Messages*. This naming convention is not exactly precise however as what we typically consider fields, such as VID_sndr and VIDs of intermediary hops, are also payload fields used for TSP control functions. To contrast with the payload fields used for control functions, we refer other fields in the payload *data fields*.

TSP defines a set of payload types. TSP payload type codes are allocated only by this specification, in coordination with [[ref:CESR]]. Higher layers define their own content within the XSCS (data) and XCTL (control) payloads, which TSP carries opaquely. This structure ensures a standardized approach for the essential components of the message while allowing adaptability for specific use cases or additional requirements at the higher layer. 

### Relationship Forming Protocol
#### TSP Digest

TSP uses a *self referencing* or *self addressing* digest in its relationship forming protocol messages defined below. It is calculated according to the *SAID* (Self Addressing Identifier) convention as described in the [[ref:CESR]] specification. The supported hash or digest functions are listed in section [Secure Hash and Digest Functions](#secure-hash-and-digest-functions). 

TSP Digest is calculated and contained in the message that it is based on. In a bi-directional relationship formation exchange, the request message contains its own TSP Digest field which identifies the request message, and the reply message contains both the Digest it received from the requester and its Reply_Digest. Conceptually, this exchange creates two uni-directional relationships, one (from the requester) can be identified by the Digest, and the other (From the replier) can be identified by the Reply_Digest. The two digests are bound together as the Reply_Digest's calculation includes the Digest of the incoming request, as described in the sections that follow.

For the message that contains it, its TSP_Digest is computed over the binary serialization of that message's own TSP_Version, VID_sndr, VID_rcvr, and Payload fields (the plaintext payload, before encryption), with these rules:

 - The `-E##` (or `--E#####`) and `-Z##` (or `--Z#####`) framing tags and the Padding_Field are excluded from the computation; the payload type code is included. `Signature_new` is excluded because it is produced after the digest and signs it.
 - During derivation, the digest field's own slot is filled with the dummy byte 0x23 over its full length (e.g. 33 bytes for a 256-bit digest), then the digest is computed and its CESR-encoded value replaces the dummy.
 - The hash function is identified by the digest's own CESR derivation code (e.g. I = SHA2-256, F = Blake2b-256), from [Secure Hash and Digest Functions](#secure-hash-and-digest-functions).
 - In a nested message, "the message" means the innermost message that carries the digest, not any outer routing envelope. A digest that is echoed from a prior message (e.g. the Digest copied into a TSP_RFA) is copied verbatim, not recomputed. Verification reverses the derivation.

Note that the SAID calculation for TSP messages is in binary domain, so is its result used.

In describing this digest field, we will use TSP_DIGEST in the context of the message that it is identifying and it should be interpreted as the result of the above self referential calculation.

The sender and receiver of these TSP digests SHOULD save them as part of the relationship state if they wish to use them as a thread identifier or to validate the relationship formation process in the future.

#### Direct Relationship Forming
When an endpoint `A` learns  the VID for another endpoint `B`, say `VID_b`, through an Out-Of-Band Introduction method, the endpoint `A` MUST use the following message type to form a direct relationship with `B`. Suppose the source VID that endpoint `A` uses is `VID_a`, then the relationship A and B establishes is `(VID_a, VID_b)`.
``` text
Out-Of-Band Introduction to A: VID_b
The relationship forming message from A to B: [VID_a, VID_b, Payload]
Payload fields:
    - Type = TSP_RFI (Relationship Forming Invite)
    - Digest = TSP_DIGEST
    - Nonce_Field = Nonce
```
This `TSP_RFI` is required for forming a relationship between two *direct* endpoints. It is not permissible that one endpoint which has learned a VID of the other simply starts with an application level message without first having an exchange of TSP control messages. If an endpoint receives an application message destined to one its legitimate VIDs, but it has not established a relationship from the source VID in the message to its own VID (i.e. the destination VID in the message), it SHOULD drop the message.

Endpoint `B` retrieves and verifies `VID_a`, and if agrees, replies with the following:
``` text
Message: [VID_b, VID_a, Payload]
Payload fields:
    - Type = TSP_RFA (Relationship Forming Accept)
    - Digest = Digest of the corresponding `TSP_RFI`
    - Reply_Digest = TSP_DIGEST
```
The result is a bi-directional relationship `(VID_a, VID_b)` in endpoint `A` and `(VID_b, VID_a)` in endpoint `B`. The Digest is recorded by both endpoints and can be used in future messages in `<VID_a, VID_b>`, and similarly Reply_Digest for `<VID_b, VID_a>`.

If endpoint `B` fails to verify `VID_a`, it SHOULD silently drop the message and MAY direct the transport layer to disconnect or otherwise block or filter out further incoming messages from `VID_a` for a period of time.

If endpoint `B`, for any other reason, does not want to or can not engage with endpoint `A`, it MAY simply remain silent (if `B` does not want to give `A` any private information), or it MAY reply with a `TSP_RFD` message as specified in Section [7.4](#relationship-events) with proper event code (if `B` is willing to risk additional information disclosure by providing `A` some useful information). 

If endpoint `B` is OK with receiving the incoming messages from endpoint `A`, but declines to reply to endpoint `A` to establish the opposite direction relationship, it MAY simply remain silent. 

Other actions that endpoint B may take MAY be application specific and are left unspecified.

In all of the above cases, the responding party (endpoint `B`) should be careful about privacy leaks if it chooses to respond to an incoming message. The most private option is to remain silent.

#### Race Condition of TSP_RFI

It is possible that two endpoints `A` and `B` may initiate a TSP_RFI message to each other at roughly same time with the same pair of `VID_a` and `VID_b`. Under such a race condition, endpoint `A` may have sent an TSP_RFI for <VID_a, VID_b>, and while it is waiting for a TSP_RFA, receives a TSP_RFI for <VID_b, VID_a>. The endpoints MUST break this race condition based on the Digest field in the TSP_RFI. The rule is that both endpoints keep the TSP_RFI whose Digest is lower by lexicographical comparison, and discard the other.

#### Relationship over a Routed Path
Suppose endpoint `A` learns from another endpoint `B` through an Out-Of-Band Introduction method the VID for `B`, say `VID_b`, together with a routing path, `{ …, VID_hopk, VID_exit}`. Endpoint `A` MUST use the following control message to form a relationship with `B`. Suppose the source VID that endpoint `A` uses is `VID_a`, and optionally endpoint `A` specifies a reply path `{ …,  VID_rhopk, VID_rexit}`, then the relationship `A` and `B` establishes is `(VID_a, VID_b)`.

``` text
Out-Of-Band Introduction: VID_b, VID_hop2, …, VID_hopk, VID_exit
The relationship forming message = [VID_a, VID_b, …, VID_hopk, VID_exit, Payload]

Payload fields:
    - Type = TSP_RFI
    - Digest = TSP_DIGEST
    - Nonce_Field = Nonce
    - Reply_Path = ..., VID_rhopk, VID_rexit
```

Endpoint `B` retrieves and verifies `VID_a`, and if agrees, replies with the following:

``` text
Return message: [VID_b, VID_a, …, VID_rhopk, VID_rexit, Payload]
Payload fields:
    - Type = TSP_RFA
    - Digest = Digest of the corresponding `TSP_RFI`
    - Reply_Digest = TSP_DIGEST
```
In the above illustration, endpoint `A` has chosen at least its direct intermediary {`VID_rhopk`, `VID_rexit`}. If endpoint `B` sends the reply message to its direct intermediary and that intermediary knows how to route to `A`'s intermediary `VID_rhopk`, then all is good. Optionally, endpoint `B` may also add additional hops, illustrated above as `...` hop list. The minimal required condition is that the last intermediary in `B`'s hop list knows how to reach the first hop in `A`'s list. 

In common cases, intermediaries MAY use well-known public VIDs and know how to reach each other.

Note, either `A` or `B` may choose to specify a routed path for the relationship forming messages. If one party specifies a routed path while the other party does not (but they both agree to such an arrangement), then the result can be a relationship over a routed path in one direction but via a direct path in the other direction.

The result of the above message exchange is a bi-directional relationship `(VID_a, VID_b)` in endpoint `A` over a routed path to `B` and vice versa. 

#### Parallel Relationship Forming

If endpoints `A` and `B` have a relationship `(VID_a0, VID_b0)` in `A` and `(VID_b0, VID_a0)` in `B`, they can establish a new parallel relationship using the current relationship as a means of referral.

Endpoint `A` sends to `B` this relationship forming message:

``` text
Message: [VID_a0, VID_b0, …, Payload], 
we omitted the optional route path VID list so this can either a Direct or Routed message.

Payload fields:
    - Type = TSP_RFI
    - VID_new = VID_a1
    - Reply_Path = VID_list | NULL
    - Digest = TSP_DIGEST
    - Nonce_Field = Nonce
    - Signature_new = TSP_SIGN(the preceding payload) by VID_new
```

In this procedure, `VID_a1` is the new VID for endpoint `A`. If endpoint `B` picks `VID_b1` and replies with `TSP_RFA`, then the new relationship `(VID_a1, VID_b1)` is parallel to `(VID_a0, VID_b0)` in endpoint `A`, and similarly in `B`.

If the `Reply_Path` is present, then `B` MUST use the routed path specified by `Reply_Path` to send the `TSP_RFA` message to endpoint `A` as defined in the previous section [Relationship over a Routed Path](#relationship-over-a-routed-path).

``` text
Return message: [VID_b1, VID_a1, …, Payload]
Payload fields:
    - Type = TSP_RFA
    - Digest = Digest of the corresponding `TSP_RFI`
    - Reply_Digest = TSP_DIGEST
```

#### Nested Relationship Forming

If endpoints `A` and `B` have a relationship `(VID_a0, VID_b0)` in `A` and `(VID_b0, VID_a0)` in `B`, they can also establish a new nested relationship using the current relationship as a referral. The new relationship is *private* as discussed in Section [2.1](#vid-use-scenarios).

Endpoint `A` sends to `B` the following relationship forming message: 

``` text
Message: [VID_a0, VID_b0, …, [VID_a1, NULL, Payload]]
where the optional VID list is omitted so `(VID_a0, VID_b0)` can be either Direct or Routed Mode.

Payload fields:
    - Type = TSP_RFI
    - Digest = TSP_DIGEST
    - Nonce_Field = Nonce
```

The VID `VID_a1` used in the nested relationship MAY be a *private* VID, for example `did:peer`. With the use of such private VID, the receiver can verify it using its self-contained information without accessing an external [[ref: Support System]]. 

::: note
Verification information for a private VID is often carried in the TSP_RFI itself. For example, the long form of `did:peer:4` embeds the DID document in the identifier, and `VID_new` is accompanied by its own signature.
:::

Endpoint `B` replies to `A` the following message if it chooses: 

``` text
Return Message: [VID_b0, VID_a0, …, [VID_b1, VID_a1, Payload]]
where the optional VID list is omitted so the outer relationship can be either Direct or Routed Mode.

Payload fields:
    - Type = TSP_RFA
    - Digest =  Digest of the corresponding `TSP_RFI`
    - Reply_Digest = TSP_DIGEST
```
The new relationship formed by the above control message exchange is: `(VID_a1, VID_b1)` in `A` and `(VID_b1, VID_a1)` in `B`. This relationship is private. The verification can be done through the above two messages privately if the endpoints use private VIDs with self-contained verification information. No address resolution procedure is required because it relies on the outer relationship.

The outer relationship can be either direct or over routed mode, the same procedure applies. Similarly, the outer relationship itself can be a nested relationship, the same procedure applies. The resulting new relationship can only be used for nested messages with the coupled outer relationship.

A same procedure can also be used for creating new parallel relationships with the following messages below. Here the outer relationship is `(VID_a0, VID_b0)`; the existing nested relationship is `(VID_a1, VID_b1)`; the new relationship being created is `(VID_a2, VID_b2)` that is nested inside the same outer relationship.

``` text
Message: [VID_a0, VID_b0, …, [VID_a1, VID_b1, Payload]], 
we omitted the optional route path VID list so this can either a Direct or Routed message.

Payload fields:
    - Type = TSP_RFI
    - VID_new = VID_a2
    - Reply_Path = VID_list | NULL
    - Digest = TSP_DIGEST
    - Nonce_Field = Nonce
    - Signature_new = TSP_SIGN(the preceding payload) by VID_new
```
And endpoint `B` replies with:

``` text
Return message: [VID_b0, VID_a0, ..., [VID_b2, VID_a2, Payload]]
Payload fields:
    - Type = TSP_RFA
    - Digest = Digest of the corresponding `TSP_RFI`
    - Reply_Digest = TSP_DIGEST
```

#### Relationship Forming Decline or Cancel
Bidirectional relationships in TSP are essentially a combination of two unidirectional relationships that involve the same pair of VIDs. Due to the asymmetric nature of TSP messages, it's possible for a relationship to exist unidirectionally for a time — where messages flow in one direction but not yet in the reverse. This scenario can occur both when a relationship is being established and when it's being terminated. It is also permissible that endpoints simply want to keep a unidirectional relationship if they choose to.

While sending explicit messages to cancel a relationship is not strictly necessary in TSP, such messages MAY be beneficial for upper-layer protocols that require a clear and definite termination of relationships. For this purpose, endpoints utilize `TSP_RFD` (Relationship Forming Decline) control messages.

During a relationship forming process, the receiver of a `TSP_RFI` request MAY choose to respond to the sender to *decline* the request. While such a decline message may expose certain vulnerabilities, some application scenarios may warrant such an action to give certainty to the upper layer applications. In such cases, the same `TSP_RFD` message is used for declining a `TSP_RFI` request.

The process for canceling an existing relationship or declining a requested new relationship is uniform, regardless of whether the relationship uses a direct or a routed path, or if it is nested.

For a relationship denoted as `(VID_a, VID_b)` in endpoint `A`, `A` can initiate the cancellation by sending a `TSP_RFD` message. The same could happen from `B` to cancel in the opposite direction. This process is asynchronous, meaning it's possible for cancellation messages from both `A` and `B` to cross paths.

When `A` initiates the cancellation, `A` sends a control message with the following structure:

``` text
Message: [VID_a, VID_b, Payload]
Control payload fields:
    - Type = TSP_RFD
    - Digest = the previously received Digest or Reply_Digest
```

When `B` Receives a cancellation:

If the relationship is `(VID_b, VID_a)` in `B`: `B` should reply with `TSP_RFD` and then remove the relationship from its local relationship table.

If the relationship is `<VID_a, VID_b>` in `B`: `B` should remove the relationship but does not need to send a reply.

If the relationship does not exist or is not recognized: `B` should ignore the cancellation request.

When `B` is declining a `TSP_RFI` from `A`, and chooses to send an explicit message, then `B`'s `TSP_RFD` is as follows:

``` text
Message: [VID_b, VID_a, Payload]
Payload fields:
    - Type = TSP_RFD
    - Digest = Digest from the corresponding `TSP_RFI`
```
### Relationship Events

#### Padding Message

A padding message is a TSP message with a payload containing only a padding field besides required control fields. Such padding messages MAY be used as a mechanism to defend against traffic analysis based threats. The payload type is `TSP_PAD`.

If endpoint `A` chooses to send a padding message to `B`, the message will be as follows:

``` text
Message: [VID_a, VID_b, Payload]
Payload fields:
    - Type = TSP_PAD
    - Nonce_Field = Nonce
    - Padding_Field = Padding
```

The receiver SHOULD silently discard padding messages.

Note that an upper layer protocol may send their own similar messages without no real content. In that case, however, the payload type would be `TSP_GEN`.

#### Key Update

Key rotation for a VID is performed out of band, by the mechanisms of the VID type, as described in [Handling Changes](#handling-changes). TSP defines no control message for key rotation: any such message would have to be authenticated by the very key state whose change it announces, and the receiving endpoint would still have to confirm the change against the VID's provenance chain.

A relationship in TSP is a pair of VIDs, not a pair of keys. Rotating the keys of a VID therefore does not directly affect any relationship in which it participates: the relationship, its thread identifier, and any nested relationships within it are unchanged. An endpoint does not need to notify its peers of a rotation within TSP, and does not need to re-establish relationships after one. A private VID used in a nested relationship need not be rotated; an endpoint that wishes to change such a VID may simply establish a new one, which is also preferable for unlinkability.

An endpoint learns of a peer's rotation in one of two ways, depending on how the VID type is implemented and deployed. The distinction is not a property of the VID type alone: the same type may be deployed either way.

##### Key state maintained by the VID implementation
Some VID implementations maintain the key state of a peer continuously, observing the peer's published key history and reflecting a change without being asked. Key event logs with watchers, and verifiable histories with witnesses, are examples.

An endpoint in such a deployment takes no action of its own. The operations in [Mapping VID to Keys](#mapping-vid-to-keys) return current key state, and messages that failed to verify during the interval before the change was observed simply resume verifying. The timeliness of recovery is a property of that implementation.

##### Key state resolved by the endpoint
Other implementations publish key state but do not deliver changes to those relying on them, and an endpoint must resolve the peer's VID for itself. It then holds that state as a cached value, and the authoritative source remains the VID's provenance chain. Such an endpoint SHOULD re-resolve the peer's VID and retry the verification once before discarding a message that fails to verify, as the failure may be the result of a rotation the endpoint has not yet observed. And it SHOULD re-resolve before acting on a message that arrives after a silence longer than its re-verification threshold. This threshold is a local policy choice; endpoints need not agree on it and it is not communicated.

A peer that has been silent may have rotated its keys during that silence without the endpoint having had any occasion to observe it, and the threshold bounds how long such a change may remain unobserved before the endpoint acts on a message. This second case is the one that matters under compromise: stale key state is internally consistent, so a message signed with a compromised key verifies and gives no warning — but an attacker must send a message in order to exploit it, and that message is itself the trigger for the re-resolution that will update the key state.

Because re-resolution may be provoked by messages an endpoint has not authenticated, an endpoint SHOULD bound the rate at which it resolves any one peer's VID. Rotations are relatively infrequent, so a limit that permits one resolution within an interval does not materially delay recovery.

##### Recovery
An endpoint that rotates its keys because they may have been compromised should be aware that peers holding a stale key state may continue to accept messages signed with the old key until they obtain the new one. The timeliness of that is a property of the VID type and of the peer's own policy. A TSP endpoint can always re-establish a suspect relationship using another relationship that is not suspect.

## Cryptographic Algorithms

TSP utilizes VIDs that are strongly bound to public-key pairs. The authenticity and confidentiality properties of TSP rely on public-key signature and encryption schemes based on public-key cryptography. In this section, we specify the supported cryptographic schemes and how they combine together as a TSP crypto suite. The choices we make here reflect our priorities to:
- achieve the strongest notions of security with respect to modern and efficient algorithms,
- have clear specifications in standards for interoperability,
- prefer schemes that have high quality open source implementations. 

The overall design and use of self-framed encoding allows TSP easy adaptability to future requirements, including new cryptographic schemes and the implementation of post-quantum cryptography.

TSP combines public-key authenticated encryption (PKAE) with public-key signatures. This combination is necessary for several reasons:
- In TSP, authenticity (both the identity of the sender and integrity of the message) is required for all messages while confidentiality is optional.
- PKAE schemes have weaknesses, such as Post Compromise Impersonation (PCI) attacks, which TSP aims to guard against in order to support its wider use cases.

No naive composition of public-key encryption and signature achieves authenticated encryption in the public-key setting. [[ref:ESSR]] separates unforgeability against a third party from unforgeability against the receiver, the latter being the stronger requirement since a receiver can decrypt and so has capabilities a third party does not, and shows that Encrypt-and-Sign, Sign-then-Encrypt, and Encrypt-then-Sign each fail at least one of these notions. Two attacks illustrate why. An adversary that strips a signature from a ciphertext and applies its own can claim authorship of a message whose content it never learned. And a receiver able to construct a second message and key pair yielding the same ciphertext can assert that the sender addressed that message to it.

TSP therefore follows the construction ESSR proposes — Encrypt Sender-key then Sign Receiver-key — carrying the sender's identity within the confidential payload and covering the receiver's identity by the signature for the *Libsodium Sealed Box* mode. In the HPKE-Base mode, the binding of the sender identity is achieved through AAD in the HPKE construction, and implementors MAY optionally still carry the sender VID in the confidential payload or the default NULL value. Either way, the first binding defeats substitution of the signature, since the sender identity found within the ciphertext contradicts it, or it will fail to decrypt in HPKE; the second prevents a receiver from altering, after the fact, what the signature was taken over. TSP binds VIDs where ESSR binds public keys. A VID is bound to its keys by the requirements of [VID General Requirements](#vid-general-requirements), and the substitution is preferable here: a binding to a VID survives rotation of the keys behind it, where a binding to a public key would not.

Together these give the authenticity TSP requires of every message. A message cannot be attributed to a sender that did not compose it, cannot be claimed by a receiver to which it was not addressed, and cannot be disowned by the sender that did compose it — the last being the sense in which TSP's authenticity is closely related to non-repudiation. It also follows that a party holding a receiver's key cannot produce a message that appears to come from a legitimate sender, since that would require the sender's signing key; Post Compromise Impersonation by an adversary that has obtained a receiver's key is precluded for this reason. (Note that compromise of a sender's own signing key is a different matter, discussed in [Key Compromise and Recovery](#key-compromise-and-recovery).)

### Public-Key Signatures
`Ed25519` is an EdDSA signature algorithm using `Curve-25519` and `SHA2-512` as defined in IETF [[ref:RFC8032]]. 

Ed25519 supports a stronger sense of unforgeability, namely SUF-CMA (Strong UnForgeability under Chosen Message Attack).

TSP implementations MUST support Ed25519.

#### Post-Quantum Signatures

TSP supports post-quantum digital signatures using ML-DSA-65 (Module-Lattice-Based Digital Signature Algorithm, security category 3), as defined in [[FIPS204]] (also known as CRYSTALS-Dilithium). An endpoint uses ML-DSA-65 or Ed25519 according to the signature key type of its VID. The signature encoding is specified in [ML-DSA-65 Signature](#ml-dsa-65-signature).

### Public-Key Authenticated Encryption

TSP uses strong public key encryption schemes that supports IND-CCA2 (Indistinguishability under Adaptive Chosen Ciphertext Attack). These schemes are also called Integrated Encryption Schemes (IES), ECIES if using Elliptic Curves, or Hybrid Public Key Encryption (HPKE) since they combine public key cryptography with the efficiency of symmetric key encryption/decryption operations. These schemes follow similar designs that incorporate a key exchange mechanism (KEM), a key derivation function (KDF), and a symmetric encryption scheme using the ephemeral derived key, or formalized as an Authenticated Encryption with Associated Data (AEAD) function. The use of AEAD also leads to the acrynym PKAE (public-key authenticated encryption). We use the term PKAE as a general term for this class of algorithms.  

#### TSP Encryption and Decryption Primitives

TSP defines a standard way to encrypt a single TSP message to a receiver's public key. The operations use the following `seal` and `open` primitives.

``` text
Ciphertext = TSP_SEAL(VID_sndr, VID_rcvr, Plaintext)
Plaintext = TSP_OPEN(VID_sndr, VID_rcvr, Ciphertext)
```

This section specifies all PKAE schemes that TSP implementations MUST or optionally SHOULD support.

#### Hybrid Public Key Encryption (HPKE) 

HPKE is a draft standard defined in IETF [[ref:HPKE]] which formalizes and generalizes similar schemes and implementations that support encryption of messages for a receiver with a public-private key pair. [[ref:HPKE]] defines a framework from which we specify a subset of concrete configuration to best meet TSP requirements. HPKE uses modern cryptographic algorithms and has been studied with proofs of IND-CCA2 security. The HPKE-Base mode does not use sender authentication in the HPKE itself. The algorithms in a HPKE suite are KEM (Key Exchange Mechanism), KDF (Key Derivation Function), and AEAD (Authenticated Encryption with Associated Data function). Schemes that follow [[ref:HPKE]] have seen adoption in Messaging Layer Security [[ref:RFC9420]] and TLS Encrypted ClientHello [[ref:RFC9849]].

TSP implementations MUST support HPKE-Base mode as defined in this document.

##### HPKE Cryptographic Algorithm Suite

HPKE configuration(s) supported by TSP:

Primitive | Code | Description
----:|----:|--------:
KEM | 0x0020 | DHKEM(X25519, HKDF-SHA256)
KEM | 0x647a | X25519MLKEM768 (PQ/T hybrid)
KDF | 0x0001 | HKDF-SHA256
AEAD | 0x0003 | ChaCha20Poly1305

A VID's encryption key type selects the KEM; the KDF and AEAD are the same in both cases.

##### HPKE-Base Mode

The HPKE-Base mode does not authenticate the sender at the HPKE layer; that is, it does not allow the receiver to verify that the sender possessed a given KEM private key. This omission is intentional. In TSP, sender authentication is provided by the TSP_Signature over the envelope and payload, and the binding of the ciphertext to the sender identity required by the ESSR construction is provided by the associated data `aad`, which includes `VID_sndr` from the envelope. A ciphertext that does not open under the receiver-computed `aad` MUST be rejected. The sender VID MAY additionally be included as the first confidential payload field; when present it MUST match `VID_sndr` in the envelope.

In the HPKE-Base mode, for a TSP message that uses a confidential payload, the ciphertext MUST be generated by the HPKE-Base single-shot API defined in [[ref:HPKE]] as follows:

``` text
def TSP_SEAL(VID_sndr, VID_rcvr, Confidential_Fields_Plaintext):
    pkR = VID_rcvr.PK_e
    aad = CONCAT(TSP_Version, VID_sndr, VID_rcvr)
    info = the TSP CESR code `YTSP-`
    pt = Confidential_Fields_Plaintext
    enc, ct = SealBase(pkR, info, aad, pt)
    return CONCAT(enc, ct)

Ciphertext = TSP_SEAL(VID_sndr, VID_rcvr, 
                Confidential_Fields_Plaintext)

```
The receiver MUST use the corresponding single-shot API to decrypt:

``` text
def TSP_OPEN(VID_sndr, VID_rcvr, Confidential_Fields_Ciphertext):
    skR = VID_rcvr.SK_e
    aad = CONCAT(TSP_Version, VID_sndr, VID_rcvr)
    info = the TSP CESR code `YTSP-`
    enc, ct = SPLIT(Confidential_Fields_Ciphertext)
    return OpenBase(enc, skR, info, aad, ct)

Plaintext = TSP_OPEN(VID_sndr, VID_rcvr,  
                Confidential_Fields_Ciphertext)
```

In HPKE-Base mode the VID_sndr confidential field is NULL VID by default. It MAY carry the sender VID; when it does, it MUST equal VID_sndr in the envelope.

Note that the 'aad' input is the CESR serialized octet sequence of the cleartext message fields preceding the ciphertext — the version, both VIDs. The sender computes `aad` from the values it places in the envelope. On the receiver side, the `VID_rcvr` MUST be taken from the receiver's local value or checked for equality with the value in the received message, while the other fields are taken from the received message as encoded on the wire. The `VID_sndr` in `aad` MUST also match the VID used in the signature verification. `TSP_Tag` is not included in `aad`.


##### HPKE PQ and PQ/T Algorithms

Post-quantum support in TSP is not a separate mode — it is HPKE-Base with the post-quantum/traditional hybrid KEM X25519MLKEM768 (0x647a), as defined in [[ref:HPKE-PQ]]. The KEM is selected by the recipient VID's encryption key type; all other HPKE-Base processing, framing, and AAD are unchanged. Note that [[ref:HPKE-PQ]] is an active Internet-Draft; this reference is to be updated to the RFC on publication.

#### Libsodium Sealed Box

Libsodium is a popular open source software library that is a fork of [[ref:NaCl]]. Among many modern and easy-to-use cryptographic tools, it provides an implementation of a crypto\_box primitive that is essentially a non-standardized PKAE scheme. We specify a way for TSP to use the Libsodium Sealed Box API as a PKAE choice here because of its popularity. However, since the sealed box API is not standard alongside the fact that the Libsodium community is also implementing HPKE options in parallel, implementors SHOULD consider migrating to the HPKE option specified in this document. We MAY remove this option in the future.

##### Sealed Box

Per [[ref:libsodium]] documentation, the combined mode API defined in `C` is as follows.

``` c
int crypto_box_seal(unsigned char *c, const unsigned char *m,
                    unsigned long long mlen, const unsigned char *pk);
```
`crypto_box_seal()` encrypts plaintext `m` of length `mlen` using the receiver's public key `pk`, and outputs to buffer `c` the ciphertext. 

``` c
int crypto_box_seal_open(unsigned char *m, const unsigned char *c,
                         unsigned long long clen,
                         const unsigned char *pk, const unsigned char *sk);
```
`crypto_box_seal_open()` decrypts the ciphertext `c` of length `clen` using the receiver's public key `pk` and the receiver's secret key `sk`, and outputs the plaintext to `m`.

##### TSP Use of Sealed Box for PKAE

To use sealed box as the PKAE in TSP, for TSP message that uses confidential payload, the ciphertext MUST generated by `crypto_box_seal()` API as follows (in pseudocode) or an equivalent procedure:

``` text
def TSP_SEAL(VID_sndr, VID_rcvr, Confidential_Fields_Plaintext):
    pkR = VID_rcvr.PK_e
    pt = Confidential_Fields_Plaintext
    mlen = Length(pt)
    ciphertext = crypto_box_seal(pt, mlen, pkR)
    return ciphertext

Ciphertext = TSP_SEAL(VID_sndr, VID_rcvr,
                Confidential_Fields_Plaintext)
```

The receiver MUST use the corresponding `crypto_box_seal_open()` API procedure or an equivalent to decrypt:

``` text
def TSP_OPEN(VID_sndr, VID_rcvr, Confidential_Fields_Ciphertext):
    pkR = VID_rcvr.PK_e
    skR = VID_rcvr.SK_e
    ct = Confidential_Fields_Ciphertext
    clen = Length(ct)
    output = crypto_box_seal_open(ct, clen, pkR, skR)
    return output

Plaintext = TSP_OPEN(VID_sndr, VID_rcvr,  
                Confidential_Fields_Ciphertext)
```

For *Libsodium Sealed Box*, the `VID_sndr` field MUST be present in the Confidential Control Fields (as required by [[ref:ESSR]]).

##### Sealed Box Cryptographic Algorithms

Per [[ref:libsodium]] documentation, the sealed box API leverages the `crypto_box` construction which in turn uses `X25519` and `XSalsa20-Poly1305`, and uses `blake2b` for nonce. As a non-standard implementation, such information is not precisely known and is implementation specific depending on the open source development of libsodium.

### Secure Hash and Digest Functions

All TSP implementations MUST support the following secure hash and digest functions. They can be used for nonce and digest constructions as the operator TSP_DIGEST.

- SHA2-256 [[def-FIPS180-4]]

- Blake2b [[ref:RFC7693]]

## Serialization and Encoding

TSP uses CESR [[ref:CESR]] (master code table for `-_AAACAA`) for message serialization and encoding. The TSP payload however may have data encoded in other formats including CBOR, JSON, and MsgPak that are compatible formats to interleave within CESR streams.

This version of TSP uses the CESR code table at genus AAA, Version 2.00, identified by the genus/version code `-_AAACAA`. As the specifications of TSP, CESR, and the CESR code table may evolve without being fully synchronized, we will increment the TSP version (the MINOR version number, for instance) to reflect code table changes and keep track of the mapping.

In this section, we describe the relevant CESR codes used in TSP.

### TSP Envelope Encoding
The TSP Envelope consists of four objects: TSP_Tag, TSP_Version, VID_sndr, VID_rcvr. Each VID is a VID_String. The CESR encoding of these are as follows.

Object | Description | Code | Note
----:|----:|--------:|--------:
TSP_Tag | Indicating the start of a TSP envelope | `-E##` or `--E#####`| Use `-E##` for signable data up to 4095 quadlets/triplets, `--E#####` for signable data up to 1,073,741,823 quadlets/triplets. The length does not include signature part.
TSP_Version | TSP protocol version | `YTSP-###` | The current version is `YTSP-ABA`. The three `###` characters should represent MAJOR, MINOR, PATCH version as in semver 2.0.0 scheme.
VID_String | short VID with lead pad size 0 | `4B##` | The VID string is in a variable length of either 2 Base64 size characters limited to 4095 quadlets/triplets (short VID) or 4 Base64 characters limited to 16,777,215 quadlets/triplets (long VID). In each case, there are 3 variations depending on the lead pad size of 0, 1, or 2.
 ^ | short VID with lead pad size 1 | `5B##` | ^ 
 ^ | short VID with lead pad size 2 | `6B##` | ^ 
 ^ | long VID with lead pad size 0 | `7AAB####` | ^ 
 ^ | long VID with lead pad size 1 | `8AAB####` | ^ 
 ^ | long VID with lead pad size 2 | `9AAB####` | ^ 

The TSP protocol code is `YTSP-` which is unique in the CESR code and is used in HPKE-Base mode `info` input parameter.

The NULL VID is encoded as `4BAA`.

::: note
CESR uses a unit of 4 Base64 letters (Quadlet) to represent an equivalent unit of 3 bytes in binary (Triplet). Therefore, a two letter count code `0E##` in text domain provides a value in range of 0 to 4095 (`64 x 64 - 1`) where each unit is a quadlet/triplet. The corresponding value in actual bytes in binary is 12,285 (`4095 x 3`). Similarly, `--E#####` provides 0 to 1,073,741,823 (`64^5 - 1`) quadlets/triplets which corresponds to 3,221,225,469 bytes in binary.
:::

### TSP Payload Encoding
TSP payload consists of a `TSP_Payload_Tag`, a payload field type, and payload fields required for the type, as specified in [TSP Payload](#tsp-payload). For a confidential payload, the cleartext structure is encoded first; the ciphertext is then produced over that encoding in its entirety, including the tag, and carried as the ciphertext field. We first describe the encoding of this simple structure then the encodings of [Nested Messages](#nested-messages) and [Routed Messages](#routed-messages).

The payload fields include *control fields* that are required for the correct operations of TSP. Encodings of all required control fields are defined below. Higher layer application *data fields* may use broader CESR encoding mechanisms including interleaving JSON, CBOR or MsgPak encodings.

#### TSP Payload Tag
Object | Description | Code | Note
----:|----:|--------:|--------:
TSP Payload | short or long TSP payload | `-Z##` or `--Z#####` | Use `-Z##` for payloads up to 4095 quadlets/triplets, `--Z#####` for up to 1,073,741,823 quadlets/triplets

#### Payload Field Types
Following the Payload Tag is a number of payload fields. Each field is encoded with a payload type and additional data depending on the type. The top level TSP payload field types consist of the following CESR codes using the three character code table starting with `X` as defined in CESR [[ref:CESR]] version 2.0 (master code table for `-_AAACAA`).

Object | Description | Code | Note
----:|----:|--------:|--------:
CTL | generic control payload field | `XCTL` | The CESR code for 3-character quadlets/triplets is `X`. The `CTL` type allows control messages in unrestricted generic format.
SCS | upper layer payload | `XSCS` | The acrynym "SCS" stands for `sniffable CESR stream`, which is treated as a single object that the upper layer decides how to process. Upper layer payload should be encoded as an SCS type.
HOP | a nested messge that includes a list of VID hops | `XHOP` | This type is used for nested and routed messages
PAD | variable length padding | `XPAD` | This type is used to generate messages that carry no meaningful information other than its metadata.
RFI | relationship forming invite | `XRFI` | Invitation to form a new TSP relationship
RFA | relationship forming accept | `XRFA` | Accepting a new TSP relationship in response to a RFI, thereby forming a bi-directional relationship
RFD | relationship forming decline | `XRFD` | Declining a new TSP relationship in response to a RFI, or as an cancellation of an existing relationship

#### Higher Layer Payload

Higher layer application payload (Type = `TSP_GEN`) MUST use type encoding `XSCS` followed by a generic CESR stream including supported interleaving of JSON, CBOR, and MsgPak encoded data. 

The generic CESR stream MUST use the CESR count code `-A##` (for shorter length) or `--A#####` (for longer length).

The overall higher layer payload is as follows:

``` text
-Z## | --Z#####, XSCS, VID_sndr | `4BAA`, Padding_Field, -A## | --A#####, higher-layer-payload-stream
```
where, ## or #### stands for a 2 or 4, respectively, character code of the length of the payload. All counts start immediately after the count code, not including the count code itself. The encoding of `VID_sndr` is specified in [TSP Envelope Encoding](#tsp-envelope-encoding). The encoding of the padding field is specified in [Padding Field](#padding-field).

#### Padding Field

Padding field is encoded as a variable length field as follows. The content of the pad is undefined and should not contain useful information. The receiver endpoint processes the pad by discarding it.

Object | Description | Code | Note
----:|----:|--------:|--------:
Padding field | short Padding field with lead pad size 0 (i.e. its length is a multiple of 3) | `4B##` | The padding string is in a variable length of either 2 Base64 size characters limited to 4095 quadlets/triplets (short) or 4 Base64 characters limited to 16,777,215 quadlets/triplets (long). In each case, there are 3 variations depending on the lead pad size of 0, 1, or 2.
^ | short padding with lead pad size 1 | `5B##` | ^
^ | short padding with lead pad size 2 | `6B##` | ^
^ | long padding with lead pad size 0 | `7AAB####` | ^
^ | long padding with lead pad size 1 | `8AAB####` | ^
^ | long padding with lead pad size 2 | `9AAB####` | ^

If no padding is desired, then the padding field MUST be encoded as 0 length, i.e. `4BAA`.

::: note
To avoid confusion, the term padding or padding field means the payload field itself while the shorter pad is the number of 0, 1 or 2 bytes of zero's added in front of the chosen padding field for encoding alignment.
:::

#### VID Hop List Field

The VID hop list field can appear in various messages. It is encoded as follows:

``` text
-J## | --J#####, VID_0, VID_1, ... 
```
Here both ## and #### still represent counts of length of the string that follows which is the concatenation of VIDs, not the number of VIDs. The encoding of each VID is specified in [TSP Envelope Encoding](#tsp-envelope-encoding).

#### Reply_Path Field

`Reply_Path` carries the route over which the replying endpoint is to send its `TSP_RFA`, as described in [Relationship over a Routed Path](#relationship-over-a-routed-path). It is a VID hop list, encoded as specified in [VID Hop List Field](#vid-hop-list-field), and is `-JAA` when the reply is to be sent directly.

#### Referral Field

`Referral_Field` carries a new VID introduced over an existing relationship, together with that VID's own signature. It is a generic list, `-J## | --J#####`, containing `VID_new` followed by `Signature_new`, and is `-JAA` when the message is not a referral. `Signature_new` is encoded as specified in [TSP Signature Encoding](#tsp-signature-encoding).

#### Nonce

Nonce is encoded with a two character code `0A` followed by 24 characters which represents the 128 bit nonce value.

#### Digest

- For SHA2-256, it is encoded with a one character code `I` followed by 44 characters which presents the 256 bit digest.
- For Blake2b-256, it is encoded with a one character code `F` followed by 44 characters which presents the 256 bit digest.

#### Confidential Payload Ciphertext

The confidential payload is encoded as a single ciphertext field. Its corresponding plaintext has the same format as any of the payload fields defined in this specification.

For each supported cipher scheme, CESR defines a short and a long length count code. And each then has variations of pad length 0, 1, and 2 for alignment. This results in a total of 6 variations for each scheme. All encoding codes are as follows:

Encryption Scheme | Description | Code | Note
----:|----:|--------:|--------:
Sealed Box X25519 Cipher |short length ciphertext | '4C##' | lead pad size 0
Sealed Box X25519 Cipher |short length ciphertext | '5C##' | lead pad size 1
Sealed Box X25519 Cipher |short length ciphertext | '6C##' | lead pad size 2
Sealed Box X25519 Cipher |long length ciphertext | '7AAC####' | lead pad size 0
Sealed Box X25519 Cipher |long length ciphertext | '8AAC####' | lead pad size 1
Sealed Box X25519 Cipher |long length ciphertext | '9AAC####' | lead pad size 2
HPKE-Base Cipher |short length ciphertext | '4F##' | lead pad size 0
HPKE-Base Cipher |short length ciphertext | '5F##' | lead pad size 1
HPKE-Base Cipher |short length ciphertext | '6F##' | lead pad size 2
HPKE-Base Cipher |long length ciphertext | '7AAF####' | lead pad size 0
HPKE-Base Cipher |long length ciphertext | '8AAF####' | lead pad size 1
HPKE-Base Cipher |long length ciphertext | '9AAF####' | lead pad size 2

The short length `##` counts for ciphertext up to 4095 quadlets/triplets and `#####` for up to 1,073,741,823 quadlets/triplets.

##### HPKE-Base Mode Ciphertext
The HPKE ciphertext consists of the concatenation of the Encapsulated Key structure `enc` and the encrypted payload `ct`.

``` text
HPKE-Base:
...
enc, ct = SealBase(pkR, info, aad, pt)
return CONCAT(enc, ct)
```

The `enc` is defined by HPKE [[ref:HPKE]] which contains identifiers for KEM, KDF and AEAD functions and a bytestring for the encapsulated key.

Name | Data Type | Value Registry | Description
----:|----:|--------:|--------:
kem\_id | uint | HPKE KEM IDs Registry | Identifier for the KEM
kdf\_id | uint | HPKE KDF IDs Registry | Identifier for the KDF ID
aead\_id | uint | HPKE AEAD IDs Registry | Identifier for the AEAD ID
enc | bstr | NA | Encapsulated key defined by HPKE

The ID values that MUST be supported by TSP:
Primitive | Code | Description
----:|----:|--------:
KEM | 0x0020 | DHKEM(X25519, HKDF-SHA256)
KEM | 0x647a | X25519MLKEM768 (PQ/T hybrid)
KDF | 0x0001 | HKDF-SHA256
AEAD | 0x0003 | ChaCha20Poly1305

::: note
`SHA256` should be read as `SHA2-256`. The HPKE [[ref:HPKE]] and many other specifications still use `SHA256` to mean `SHA2-256`.
:::

##### HPKE PQ and PQ/T Encoding

The post-quantum ciphertext uses the same encoding as HPKE-Base — the `4F/5F/6F/7AAF/8AAF/9AAF` codes. There is no separate post-quantum ciphertext code. The KEM (and hence the size of the encapsulated key `enc`) is determined by the recipient VID's key type, so the receiver knows how to split `CONCAT(enc, ct)`.

##### Libsodium Sealed Box Encoding
See [[ref:CESR]] on X25519 Sealed Box cipher bytes encoding.

#### Interleaved JSON, CBOR or MsgPak Payload

An application payload (type XSCS) or control payload (type XCTL) is a generic CESR stream for the upper layer. It may contain native CESR and/or non-native serializations — JSON, CBOR, or MsgPak. TSP carries this payload opaquely; the upper layer parses its content. TSP itself does not interpret it.

Because the payload sits inside TSP messages, a non-native serialization cannot be free-interleaved. Per [[ref:CESR]], it MUST be encoded as a CESR primitive and enclosed in the non-native message group -H## (or --H#####). TSP uses the Bytes primitive (4B/5B/6B, chosen by length for lead-byte alignment) in the binary domain to carry the serialization bytes.

A payload may contain one or more such -H## (or --H#####) groups in sequence, alongside native CESR — for example a JSON object followed by a CBOR map. This sequencing is the interleaving.

```text
-A## | --A#####, ( -H## | --H##### (4B|5B|6B)## <serialization bytes> ) + [and/or native CESR]
```

#### Nested Payload
In TSP Nested Mode, the inner TSP message is carried inside a payload field of the outer TSP message. When the outer message is being parsed, the message may carry a simple application payload or a nested TSP message which will require additional processing.

The outer message MUST be encoded with payload type `XHOP`. If this is a direct relationship nested message, the overall message payload is as follows:

``` text
-Z## | --Z#####, XHOP, VID_sndr | `4BAA`, -JAA, Padding_Field, Encoded_TSP_Message
```
Because this is a message between direct neighbors, the VID hop list field is empty which is encoded as `-JAA`. The inner message can be any correctly encoded TSP message including its envelope, payload and signature. The starting payload length must count the nested message. 

#### Routed Payload
Routed payload is encoded as a nested payload with a non-empty routing hop list.

``` text
-Z## | --Z#####, XHOP, VID_sndr | `4BAA`, -J## | --J#####, VID_1, ..., Padding_Field, Encoded_TSP_Message
```
The hop list field encoding is specified in [VID Hop List Field](#vid-hop-list-field). The rest is identical to nested payload.

#### Control Message Encoding
Control messages are composition of payload fields that are used for TSP's own control mechanisms. The following sections define these payload fields in its plaintext text mode. The actual final encoding will be in ciphertext format as described in [Confidential Payload Ciphertext](#confidential-payload-ciphertext).

In every payload layout below, `VID_sndr` is the ESSR sender field. It is always present and MAY be the NULL VID `4BAA` under HPKE-Base; under Libsodium Sealed Box it MUST carry the sender's VID. See [Receiver Procedure](#receiver-procedure).

##### TSP_RFI

The TSP_RFI payload is specified in [Direct Relationship Forming](#direct-relationship-forming).

```text
-Z## | --Z#####, XRFI, VID_sndr | `4BAA`, Digest, Nonce, Reply_Path, Referral_Field, Padding_Field
```

A direct invite has `Reply_Path` = `-JAA` and `Referral_Field` = `-JAA`. An invite that asks for a routed reply carries a non-empty `Reply_Path`. An invite that introduces a new VID over an existing relationship, as in [Parallel Relationship Forming](#parallel-relationship-forming), carries a populated `Referral_Field` and MAY carry either form of `Reply_Path`.

`Signature_new` within the `Referral_Field` is made by `VID_new`'s key over {`XRFI`, `VID_sndr | 4BAA`, `Digest`, `Nonce`, `Reply_Path`, `VID_new`}. The referral field's own code and count are not covered; the message signature covers them.

##### TSP_RFA

The TSP_RFA payload is specified in [Direct Relationship Forming](#direct-relationship-forming).

```text
-Z## | --Z#####, XRFA, VID_sndr | `4BAA`, Digest, Reply_Digest, Padding_Field
```

An accept has one form. Where it accepts a referral, the accepting endpoint's new VID is the sender of the message rather than a payload field, so its control of that VID is proven by the message signature; see [Parallel Relationship Forming](#parallel-relationship-forming).


##### TSP_RFI Nested

A `TSP_RFI` is nested by composing it inside a nested outer message:

```text
-Z## | --Z#####, XHOP, VID_sndr | `4BAA`, -J## | --J#####, VID_HOP_1, ..., Padding_Field, Encoded_TSP_Message
```

The `Encoded_TSP_Message` is an ordinary TSP message — envelope, payload and signature — whose payload is a `TSP_RFI` exactly as specified above. Its envelope sender is the new VID, so the message's own signature is made by that VID, and it is that signature which authenticates the new VID; the payload's `Referral_Field` is `-JAA` unless the nested exchange is itself a referral, as in [Nested Relationship Forming](#nested-relationship-forming). The hop list is `-JAA` when the outer relationship is direct.

##### TSP_RFA Nested

A `TSP_RFA` is nested by composing it inside a nested outer message:

```text
-Z## | --Z#####, XHOP, VID_sndr | `4BAA`, -J## | --J#####, VID_HOP_1, ..., Padding_Field, Encoded_TSP_Message
```

The `Encoded_TSP_Message` is an ordinary TSP message — envelope, payload and signature — whose payload is a `TSP_RFA` exactly as specified above. Its envelope sender is the accepting endpoint's new VID and its receiver is the inviting endpoint's new VID, so the message's own signature is made by the accepting endpoint's new VID, and it is that signature which authenticates it. The hop list is `-JAA` when the outer relationship is direct.

##### TSP_RFD

The `TSP_RFD` message can be constructed as follows in a direct relationship,

```text
-Z## | --Z#####, XRFD, VID_sndr | `4BAA`, Digest, Padding_Field
```
For nested or routed relationships, the same message is encoded as an inner message in the nested or routed outer message. The `Digest` field MUST reference the corresponding relationship formation `XRFI` or `XRFA` message's digest, respectively.

##### Generic Control Message

A TSP generic control message uses the `XCTL` code in the CESR code table and its payload can be any conformant stream, including interleaving JSON, CBOR, or MsgPak encodings.

```text
-Z## | --Z#####, XCTL, VID_sndr | `4BAA`, Padding_Field, -A## | --A#####, higher-layer-payload-stream
```
##### Padding Message

A TSP padding message uses the `XPAD` code in the CESR code table. 

```text
-Z## | --Z#####, XPAD, VID_sndr | `4BAA`, Nonce, Padding_Field
```

### TSP Signature Encoding
The TSP Signature is encoded as an attachment group in CESR. TSP allows multiple signatures. The general structure is the attachment group code, followed by the indexed signature group code, then 1 or more signatures of supported types.

- Attachment group: `-C##` or `--C#####` (Attachment length up to 4,095 quadlets/triplets for `-C##` or up to 1,073,741,823 quadlets/triplets for `--C#####`)

- Indexed signature group: `-K##` or `--K#####` (Indexed signature group up to 4,095 quadlets/tripletsfor `-K##` or up to 1,073,741,823 quadlets/triplets for `--K#####`)

#### Ed25519 Signature

An Ed25519 (EdDSA) signature is always 64 bytes. Within the indexed signature group it is encoded with the code `B#` — the character B identifying an Ed25519 indexed signature, followed by one Base64 character giving the index of the signing key in the VID's key list — then 2 lead bytes and the 64-byte signature in binary. The full primitive is 88 characters in the text domain (66 bytes in binary), i.e. 22 triplets.

#### ML-DSA-65 Signature

An ML-DSA-65 signature is always 3309 bytes. It is identified by the CESR code `1AAQ`, followed by the 3309-byte signature in binary. As 3309 is a multiple of 3, no lead-pad bytes are required. The equivalent text format is 1103 triplets. The full primitive is 4416 characters in the text domain.

::: note
The code point 1AAQ is provisional. It is the next available code in the CESR master code table for genus -_AAACAA and does not conflict with any currently assigned code, but it has not yet been formally registered. See CESR issue #14.
:::

## Transports
The TSP messages are mostly agnostic to transport mechanisms which deliver them from a sender to a receiver endpoint. The authenticity, confidentiality, and privacy properties of the TSP messages are designed to be independent of the choice of transport layer. This is one of the main goals of TSP. That being said, it does not mean that the choice and implementation of transport mechanisms are not important to the proper functioning of TSP. In this section, we describe a generic service interface between TSP and the transport layer, and provide guidance on some aspects of how various transport mechanisms can be used to carry TSP messages.

This section is informative.

### Transport Service Interface

In this section, we define a generic transport service interface that the TSP layer relies on. Each actual transport mechanism then instantiates a particular mechanism. Interoperability of TSP requires the interoperability of transport mechanisms. We discuss a few examples of these mechanisms in the next section [Transport Mechanism Examples](#transport-mechanism-examples).

- `TSP_TRANSPORT_SETUP`: called by the TSP layer to perform necessary preparation before sending or receiving TSP messages.

Some transport mechanisms MAY require a preparation step (e.g. connection setup or login) before any message can be sent. This step is optional or can be a NOP.

The input to this operation is the transport address of a VID (either local or remote): TSP\_TRANSPORT\_PREPARE(`VID.RESOLVEADDRESS`). The return value of such a step can be a handle of the access point or a failure code. For bi-directional relationships, this operation is called twice, one for sending (with the remote VID) and another for receiving (with the local VID).

If this call is for the sender and the corresponding `TSP_TRANSPORT_SEND` can do send operation without prior preparation, or if this call is for the receiver and the corresponding `TSP_TRANSPORT_RECEIVE` can do receive operation without prior preparation, then this step can be skipped. If a caching mechanism is in use and the necessary access point is being cached, this step can be a NOP.

- `TSP_TRANSPORT_SEND`: called by the TSP layer to send one TSP message

This operation may return success or a failure code. The input to this operation is the handle of the transport and a TSP message.

- `TSP_TRANSPORT_RECEIVE`: called by the transport layer to trigger the TSP layer to process a received message.

The input to this operation is the TSP relationship and a TSP message. 

- `TSP_TRANSPORT_TEARDOWN`: called by the TSP layer to remove what was set up in the `TSP_TRANSPORT_SETUP` step. This is optional and can be a NOP.

- `TSP_TRANSPORT_EVENT`: called by the transport layer to report events to the TSP layer, e.g. errors. The input to this operation is the relationship and respective event information data structure.

For each transport mechanism supported, TSP implementations instantiate these operations in a way that facilitates interoperability.

### Transport Mechanism Examples

These examples are for illustration only. Detailed bindings for specific transports are to be specified in companion documents for implementation guidelines elsewhere.

- HTTPS

A TSP message can be carried as an HTTP request body to the endpoint resolved from the receiver's VID. Responses, or a long-lived stream such as Server-Sent Events or a WebSocket, carry messages in the return direction. This is the common choice where endpoints are reachable as web services.

- QUIC

A TSP message can be sent as a stream or datagram payload. QUIC provides its own framing, so message boundaries are preserved. Its connection setup maps to TSP_TRANSPORT_SETUP, and its built-in encryption is independent of TSP's own.

- Matrix

A TSP message can be carried as the content of a Matrix event in a room shared by the endpoints. Matrix's own federation and store-and-forward handle delivery.

- Message Queues

A TSP message can be a queue message; the receiver's VID resolves to a queue or topic. Suited to asynchronous and intermittently connected endpoints.

- Email

A TSP message can be carried as a message body or attachment, in text form where a binary attachment is inconvenient. Delivery is store-and-forward with no timeliness guarantee, which suits applications tolerant of long delays.

- Paper Messages

A TSP message can be printed, for example as a QR code, and transferred physically. This illustrates that the properties of the TSP message are carried by the message itself.


## Security and Privacy Considerations

TSP assures the authenticity of every message and, at the sender's choice, its confidentiality. Both are properties of the message itself, established by the sender's keys and verified against the receiver's, and they hold whatever transport carried the message and whatever systems relayed it. The construction that provides them is described in [Cryptographic Algorithms](#cryptographic-algorithms).

Where endpoints use nested or routed messages, TSP additionally limits what third parties and intermediaries can observe. What it limits, and what it does not, is described below.

Properties beyond these belong to the layers above and below TSP. An application requiring ordering, delivery, or freshness of its own obtains them from the layer that understands what its messages mean; a deployment requiring properties of the path obtains them from the transport it selects.

### Binding of identifiers
The construction in [Cryptographic Algorithms](#cryptographic-algorithms) binds the verifiable identifiers (VIDs) of both parties into each message. The VIDs in turn bind with their public keys and key states.

For the sender's identity, bound to the ciphertext through the associated data in *HPKE-Base* and carried within the confidential payload in *Sealed Box*, this indirection is an overall improvement: the binding is to an identifier whose key material may change, so it continues to hold across a rotation.

For the receiver's identity, covered by the signature, the basis differs. ESSR, which binds public keys directly, relies on the receiver's public key being fixed at the moment of signing, so that a receiver cannot afterwards assert that a message was addressed under some other key. A VID is fixed in the same way, but what it resolves to is not, and TSP provides no means to establish which key state was current when a signature was made.

The property — receiver unforgeability, in the terms of [[ref:ESSR]] — is retained because the two bindings compose. To assert that a different message was received, a receiver would have to produce a plaintext and a key pair reproducing the ciphertext the sender signed. In HPKE-Base that ciphertext verifies only under associated data naming the sender's and receiver's VIDs as they appear in the envelope, so any such plaintext would be bound to the same two parties. In Sealed Box the plaintext would itself have to be a well-formed payload naming the sender's VID, since a verifier checks that field against the envelope and the signature. No scheme specified here admits a collision meeting these constraints. Where the sender's VID is also carried in the confidential payload under HPKE-Base, the two bindings are independent, and an implementation that does not wish to rely on the associated-data handling of a newer HPKE implementation obtains the same property from the payload check alone.

### Key Compromise and Recovery
A VID has keys with distinct roles: a signing key, a decryption key, and the authority to change them. What can be recovered depends on which is compromised, and claims about recovery should be considered in that context. TSP requires that rotation authority be separate from the signing key ([VID General Requirements](#vid-general-requirements)).

Given that separation, an endpoint whose signing or decryption key is compromised can restore the security of its future communication by rotating the compromised key. This property is known as post-compromise security. Recovery is not global: it takes effect with respect to each peer independently, when that peer obtains the new key state. Until then the peer holds key state that is stale but internally consistent, and a message signed with the compromised key verifies without any indication of error.

Whether that key state is obtained by the TSP implementation or by the VID implementation beneath it is a matter of deployment: in some arrangements the change is observed and applied without TSP being involved at all, and the endpoint's key mappings simply begin returning the new state. What follows describes what an endpoint should consider where the responsibility falls to it.

#### Obtaining Current Key State
Some VID implementations maintain and distribute current key state independently — e.g. by observing a peer's published key history, comparing what independent observers report, and treating a conflicting history as evidence rather than as an error to be resolved by choosing one. An endpoint in such a deployment need do nothing: its key mappings reflect the change, and messages that failed during the interval simply resume verifying.

An endpoint that instead resolves key state on demand — returning to the VID's provenance chain for itself —  must determine for itself when to do so, and its exposure is bounded by how promptly it does. It has three occasions: when a message fails to verify, when a message arrives after a long silence, and on its own schedule. The first two are the common cases and cost nothing when nothing is happening. The third matters against an adversary that sends messages which verify under the superseded key, since such messages produce neither a failure nor a silence, and only an occasion that is independent of received traffic will fire.

An endpoint reduces its exposure further by resolving over a path independent of the one carrying TSP messages, and by consulting more than one source and comparing what they return. An adversary must then control several channels at once rather than one. Where the paths are not in fact independent — as they may not be if both traverse the same network — the benefit is correspondingly smaller.

An endpoint that resolves key state for itself sets a re-verification threshold, described in [Key Update](#key-update), and that threshold determines how long a peer's compromised key remains usable against it. The cost of a short threshold is low: the check is made when a message arrives after a silence, so it falls once when a dormant relationship resumes rather than periodically or on every message. An endpoint should therefore choose it against the consequence of acting on a message rather than against the cost of resolving, and should consider resolving before acting on a message whose effects are difficult to reverse, whatever threshold it has set.

#### Denial of Service
An endpoint that resolves in response to a message it has not authenticated can be made to resolve by anyone able to send it such a message, and the sender and receiver VIDs are visible in the envelope of any observed message. Resolution is more expensive than the message that provokes it, and an adversary can direct many endpoints to resolve the same VID at once, so the cost may fall on the peer's infrastructure rather than on the endpoints themselves. This is inherent in treating a verification failure as a signal, and is bounded by limiting the rate at which any one peer's VID is resolved: legitimate rotations are infrequent, so a limit that permits one resolution in an interval constrains an adversary without materially delaying recovery.

An adversary may also consume that allowance so that a genuine rotation is not resolved promptly. The delay is bounded by the interval and requires the adversary to sustain the effort.

Refusing to act on unconfirmed key state has an availability cost of its own, and an endpoint should distinguish being unable to reach a resolver, which is common and usually transient, from obtaining a key history that conflicts with the one it holds, which is evidence of compromise. Retaining a message until its sender's key state can be confirmed is preferable to discarding it and to acting on it.

#### Rotating Keys
An endpoint rotating keys as a matter of hygiene should publish the new key state and allow it to propagate before signing with the new keys, so that peers do not encounter failures at all. An endpoint rotating because keys may have been compromised should do the opposite: invalidate the old key state immediately and accept that peers will fail, since every moment the superseded key remains valid is exposure. In that case the endpoint may also send a padding message to the peers with which it has relationships. A peer holding stale key state will fail to verify it and will therefore obtain the new key state, whereas a peer that receives nothing has no occasion to. Because such a message is signed with the new keys, an adversary holding the compromised keys cannot produce one.

#### Limits
Where the rotation authority itself is compromised, rotation is not a remedy: the adversary can produce a key state that verifies. Whether any recovery is available is a property of the VID type — a commitment made in advance to the next rotation keys prevents an adversary holding the current keys from rotating at all; delegation allows a delegating identifier to supersede a compromised delegate; and recording the first version of a key history that is observed, and treating a later conflicting version as evidence, makes such an attack apparent rather than silent. Where a VID type provides none of these, compromise of rotation authority is unrecoverable, and this should weigh in the choice of VID type.

An adversary that can prevent an endpoint from obtaining a peer's key state can prevent it from learning of a rotation for as long as it holds that position. No arrangement described here defeats such an adversary; the arrangements above oblige it to maintain that control continuously, and across more than one channel, rather than to act once.

Recovery applies only to future communication. TSP does not provide forward secrecy: an adversary that has recorded earlier messages and later obtains the decryption key can read them. An endpoint for which this matters should limit what it retains, and may rotate decryption keys on a schedule rather than only in response to compromise.

### Metadata Exposure and Intermediaries
The authenticity and confidentiality of a TSP message do not depend on the transport that carries it or on the intermediaries that relay it. Its metadata does. This section describes what remains observable when the mechanisms in [Nested Messages](#nested-messages) and [Metadata Privacy in Routed Mode](#metadata-privacy-in-routed-mode) are used, and what an endpoint entrusts to an intermediary when it uses one.

What follows describes what a TSP message exposes at the TSP layer, independently of the transport carrying it. Deployments commonly use an encrypted transport, and where they do, a party observing the network sees neither the envelope nor its VIDs. This does not alter what an intermediary learns, since an intermediary terminates the transport and processes the message in any case, and it does not conceal the timing and size of what is carried or the transport addresses between which it passes. TSP does not require an encrypted transport, and the properties it provides do not depend on one.

TSP exposes VIDs, not identities. What learning a VID discloses is determined by how its controller chose and uses it, not by the protocol: a VID may be a long-lived public identifier or a random string used once. The exposure a party accumulates is therefore correlation — a record of which identifiers were seen together, and when — and an endpoint limits it by how it allocates and changes the VIDs it uses, as described in [Cryptographic Non-Correlation](#cryptographic-non-correlation).

#### What Remains Observable
Every TSP message exposes the pair of VIDs of the relationship that carries it, together with whatever addressing the transport requires to deliver it. Nesting conceals the VIDs of an inner relationship, and routing conceals the source and destination from third parties; neither conceals the outer pair, which is what an observer of that hop sees.

Timing, size, and frequency survive encryption, nesting, and routing alike. An observer of a hop learns that a relationship exists between the VIDs it can see, and can accumulate the times, sizes, and frequency of what passes. An observer able to see more than one hop may be able to relate a message across them by its timing and size. TSP itself does not batch, reorder, or delay messages to frustrate this; whether anything does is a property of the arrangement between intermediaries rather than of TSP, and an endpoint that requires resistance to such an observer needs to know what its intermediaries actually do.

#### What An Intermediary Learns
An intermediary that relays a routed message sees the VIDs of its direct relationships with its neighbors, the timing and size of what passes through it, and the remaining entries of the hop list, of which it consumes the entry addressed to it before forwarding.

It also sees the endpoint-to-endpoint envelope, which names the VIDs the source and destination use with each other. [Section 5](#routed-messages-through-intermediaries) requires that an intermediary neither process nor store these, but they are not concealed from it. These VIDs need reveal nothing about the endpoints beyond themselves, so what an intermediary accumulates is a correlation record rather than knowledge of who the parties are. Endpoints that wish to limit even this carry their relationship in a further nested relationship inside the endpoint-to-endpoint one, whose VIDs no intermediary sees; the endpoint-to-endpoint VIDs may then be changed freely, so that what the intermediaries observe does not link across time.

The exposure is not equal. The source's intermediary holds its client's VID, the hop list it was given, and the endpoint-to-endpoint pair, and can relate all of them. The destination's intermediary sees only its own client, the party that forwarded to it, and the endpoint-to-endpoint pair; where further relays lie between the two, it does not learn of the source's intermediary at all.

It is also directional. A source's routing VID is replaced at its first intermediary and travels no further, whereas whatever the destination advertises as its entry point must be known to the source and to every party that handles the message from there on. What that entry point actually reaches is out of scope: TSP does not specify a routing protocol, the arrangement in [Section 5](#routed-messages-through-intermediaries) is an example, and a destination or its intermediary may place any degree of indirection behind the VID that is advertised.

The hop list is likewise not a complete path. It names the intermediaries the endpoints themselves selected, and TSP does not specify how a message travels between them; intermediaries arrange that among themselves by whatever means they have agreed, which need not be TSP and need not be direct. Further parties may therefore handle a message without appearing in the hop list and without the endpoints having chosen them or knowing of them. What a message exposes at a given hop is determined by TSP; what the path as a whole reveals is also affected by arrangements among intermediaries.

The VID a destination advertises in order to be reached is in effect a routing capability: any party holding it can cause messages to be delivered over that route. Delivery is not acceptance — a message from a VID with which the destination has no relationship is discarded — but an endpoint that wishes to control who can route to it advertises a different VID to each correspondent.

The message the exit intermediary delivers to the destination is an ordinary direct message with an empty route list, and is indistinguishable on the wire from another.

#### End-to-end Protection in Routed Mode
In routed mode the source and destination communicate through an endpoint-to-endpoint relationship carried within the messages exchanged between direct neighbors. The source encrypts and signs at that layer with its own keys, and the destination therefore authenticates the source itself rather than the intermediary that delivered the message.

This depends on the requirement in [Section 5](#routed-messages-through-intermediaries) that the source sign at that layer, which it does for every TSP message. Confidentiality at that layer is separate and optional: an endpoint that requires it encrypts there rather than relying on the protection of the routed path, since that protection is provided by intermediaries rather than by the other endpoint. An endpoint that does not encrypt at that layer — for a payload intended to be public, for instance — leaves the content readable by the intermediaries that relay it, without affecting the destination's ability to authenticate the source.

#### What An Intermediary Is Trusted For
An intermediary cannot read an endpoint-to-endpoint payload if encrypted, cannot alter a message without invalidating a signature, and cannot originate one that the destination will accept as coming from the source. Three things are left to it.

It observes. It knows which of its neighbors are communicating, when, and how much, and an intermediary serving many endpoints accumulates a correspondingly larger view. Intermediaries in a path can combine what each has seen to reconstruct more than any one holds alone.

It retains, or does not. The requirement that an intermediary not store the endpoint-to-endpoint VIDs it handles is not enforced by any mechanism in TSP; it is a commitment by the operator.

It delivers, or does not. TSP provides no delivery guarantee, and an intermediary that declines to relay a message cannot be distinguished by the sender from one that has not yet delivered it.

The properties that require no judgement about an operator are authenticity and confidentiality, which are cryptographic. Metadata privacy and availability in routed mode are not among them.

#### Measures Available to An Endpoint
An endpoint that does not wish to rely on such trust has measures of its own. Carrying a relationship in a nested relationship inside the endpoint-to-endpoint one removes its VIDs from what any intermediary sees, leaving them identifiers that can be changed freely. The padding field and padding messages obscure the size and timing that would otherwise be observable. Using several intermediaries, rather than routing all traffic through one, prevents any single one from accumulating a complete record; using different intermediaries with different correspondents fragments it further, so that reconstructing the whole requires those operators to combine what they hold. None of these requires an intermediary to behave in any particular way — they reduce what any one of them is in a position to observe.

### Introductions
An endpoint learns a VID before it can communicate with its controller, and [Out of Band Introductions](#out-of-band-introductions) states that information so obtained must not be assumed authentic. The consequence is easily overlooked: an introduction conveys a VID and nothing more. Trust in that VID begins when the endpoint verifies it.

What verification establishes is that the party communicating controls the keys bound to that VID, and therefore that messages within the relationship come from the same party throughout. It does not establish who that party is. A verified VID is an identifier that can be relied upon consistently, not an identity.

Associating a VID with an identity — a person, an organization, a role, an entitlement — is done by other means, and after the relationship exists rather than before it. Verifiable credentials and similar attestations serve this purpose, and the relationship itself provides an authentic and confidential channel over which they can be exchanged and corroborated. What such an association is worth depends on the issuer of the attestation and on the endpoint's reasons for trusting it, neither of which is within the scope of this specification. Such attestation protocols are considered as examples of Trust Tasks on top of the TSP layer.

Where an introduction arrives over a channel with no authenticity of its own, a party able to interfere with that channel could substitute a VID of its own, and the resulting relationship would be entirely valid with the wrong counterparty. This is why a TSP relationship is a better channel for an introduction than one without authenticity, and why an endpoint that has established one has gained a place to begin rather than a conclusion.

### Implementation
Several requirements elsewhere in this specification exist for reasons that are not evident from the requirement alone.

TSP digests and signatures are computed over encoded bytes rather than over the values those bytes represent. An implementation that accepts a primitive whose padding is not canonical therefore admits two distinct byte sequences for the same value, with different digests and different signature inputs. This is why a receiver rejects them rather than normalizing them.

A receiver that fails to verify or validate a message discards it silently and does not respond. Any response — an error, a different timing, a change in subsequent behavior — is information available to a party that has not authenticated itself.

TSP sets no maximum message size, and the sizes an encoding permits are large. An implementation that allocates according to a declared length before it has verified anything can be made to exhaust its memory by a sender that declares one. Bounding what it will accept, and validating as it reads, are matters for the implementation rather than the protocol.

## References

### Normative References

**[[def:DID]]**. Decentralized Identifiers (DIDs) v1.0, https://www.w3.org/TR/did-1.0/

**[[def:CESR]]**. *Composable Event Streaming Representation (CESR)*, v1.1, Samuel Smith, Philip Feairheller,
, https://trustoverip.github.io/kswg-cesr-specification/.

**[[def:libsodium]]** The Sodium cryptographic library, https://doc.libsodium.org/. Authors: https://raw.githubusercontent.com/jedisct1/libsodium/master/AUTHORS. 

**[[def:HPKE]]**: Hybrid Public Key Encryption, 6 July 2026, https://www.ietf.org/archive/id/draft-ietf-hpke-hpke-04.txt

**[[def:HPKE-PQ]]**: Post-Quantum and Post-Quantum/Traditional Hybrid Algorithms for HPKE, 6 July 2026, https://www.ietf.org/archive/id/draft-ietf-hpke-pq-05.txt

**[[def:FIPS180-4]]**. Secure Hash Standard (SHS), National Institute of Standards and Technology (U.S.), August 2015, https://doi.org/10.6028/NIST.FIPS.180-4.

**[[def:FIPS203]]**. Module-Lattice-Based Key-Encapsulation Mechanism Standard, National Institute of Standards and Technology (U.S.), August 2024, https://doi.org/10.6028/nist.fips.203.

**[[def:FIPS204]]**. Module-Lattice-Based Digital Signature Standard, National Institute of Standards and Technology (U.S.), August 2024, https://doi.org/10.6028/NIST.FIPS.204.

**[[def:RFC2119]]**. Key words for use in RFCs to Indicate Requirement Levels, *S. Bradner*, March 1997, https://datatracker.ietf.org/doc/html/rfc2119.

**[[def:RFC7693]]**. The BLAKE2 Cryptographic Hash and Message Authentication Code (MAC), *M-J. Saarinen, Ed., J-P. Aumasson*, November 2015, https://datatracker.ietf.org/doc/html/rfc7693.html.

**[[def:RFC8032]]**. Edwards-Curve Digital Signature Algorithm (EdDSA), *S. Josefsson, I. Liusvaara*, January 2017, https://datatracker.ietf.org/doc/html/rfc8032.

**[[def:RFC8141]]**. Uniform Resource Names (URNs), *P. Saint-Andre, J. Klensin*, April 2017, https://datatracker.ietf.org/doc/html/rfc8141.

**[[def:RFC8174]]**. Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words, *B. Leiba*, May 2017, https://datatracker.ietf.org/doc/html/rfc8174.




### Informational References

**[[def:KERI]]**. Key Event Receipt Infrastructure (KERI), Trust over IP Foundation. https://trustoverip.github.io/kswg-keri-specification/.

**[[def:SAID-URN]]**. Namespace Registration for Self-Addressing Identifiers (SAID), IANA, urn:said, 2026. https://www.iana.org/assignments/urn-formal/said.

**[[def:DID-WEBS]]**. did:webs Method Specification, Trust over IP Foundation. https://trustoverip.github.io/kswg-did-method-webs-specification/.

**[[def:DID-WEBVH]]**. did:webvh Method Specification v1.0, Decentralized Identity Foundation. https://identity.foundation/didwebvh/v1.0/.

**[[def:DID-PEER]]**. Peer DID Method Specification, Decentralized Identity Foundation. https://identity.foundation/peer-did-method-spec/.

**[[def:DID-PEER-4]]**. DID Peer Numalgo 4, Decentralized Identity Foundation. https://github.com/decentralized-identity/did-peer-4.

**[[def:ESSR]]**. Authenticated Encryption in the Public-Key Setting: Security Notations and Analyses, *Jee Hea An*, Cryptology ePrint Archive, Paper 2001/079. https://eprint.iacr.org/2001/079.

**[[def:NaCl]]**. The security impact of a new cryptographic library, *D. J. Bernstein, Tanja Lange, Peter Schwabe*, LATINCRYPT 2012. https://nacl.cr.yp.to/.

**[[def:JWE-HPKE]]**. Use of Hybrid Public Key Encryption (HPKE) with JSON Web Encryption (JWE), *T. Reddy, H. Tschofenig, A. Banerjee, O. Steele, M. Jones*, draft-ietf-jose-hpke-encrypt-22, 6 July 2026, https://www.ietf.org/archive/id/draft-ietf-jose-hpke-encrypt-22.txt.
                    
**[[def:COSE-HPKE]]**. Use of Hybrid Public-Key Encryption (HPKE) with CBOR Object Signing and Encryption (COSE), *H. Tschofenig, B. Moran*, draft-ietf-cose-hpke-26, 4 July, 2026. https://www.ietf.org/archive/id/draft-ietf-cose-hpke-26.txt. 

**[[def:RFC9420]]**. The Messaging Layer Security (MLS) Protocol, *R. Barnes, B. Beurdouche, R. Robert, J. Millican, E. Omara, K. Cohn-Gordon*, July 2023, https://www.rfc-editor.org/rfc/rfc9420.txt.

**[[def:RFC9849]]**. TLS Encrypted Client Hello, *E. Rescorla, 奥 一穂 (K. Oku), N. Sullivan, C. A. Wood*, March 2026, https://www.rfc-editor.org/rfc/rfc9849.txt.

## Appendix A: Test Vectors

These vectors are generated by the reference implementation and verified by it. Every value a message depends on is given, so that a vector may be regenerated byte for byte rather than only decrypted: the identifiers with their private keys, the ephemeral key material each message used, and the nonce where one applies.

The key material is given as a key rather than as a generator seed, so that any implementation can use it: for the Libsodium Sealed Box, the ephemeral X25519 secret; for HPKE-Base over X25519, the `ikmE` from which the encapsulation key pair is derived, as [[ref:HPKE]] gives for its own vectors. The public half of each is the first 32 bytes of the ciphertext and may be checked against the message. The one vector using post-quantum key types is the exception, for the reason given where it appears; it is verified by decrypting it.

All identifiers are `did:peer`, whose long form embeds its own document, so a verifier requires no resolver and no network. Each carries the transport `tsp://`, a stub present only so that these vectors are self-contained; no message here is delivered, so the value is inert.

The private keys below are published. These identifiers must never be used for any purpose but checking these vectors.

The field sequence of each payload is specified in [Section 9](#tsp-encoding); it is not repeated here.


### Identifiers

`alice`

``` text
id         did:peer:4zQmUL61Nc1F7ioiKxHNqwnJXX4srhFsKKPo6TrCmhM3dfpq
longForm
  did:peer:4zQmUL61Nc1F7ioiKxHNqwnJXX4srhFsKKPo6TrCmhM3dfpq:z25NRJMKpQ
  KwnUm6k9FbTSp1eqANorDtFimHW9nGdLSgAbN1UhsQANFAnhij8VXrrwnDDG5Rb7HGrY
  pBGZRy3EbgmxirqJi3WuNfiajavps6kAfnvk9ykxGqcxH4u7P2TJohfbvigGMTMGxAhq
  kU4JDkWYi1sBp266n8tzTzD3DfRUAMspuGDnE6KM7r55U1tmXkDtRRWy97BFdh9HKfA3
  CPhA3gFdwRRV45CP1kGiaYU2rfwYAncrd1vfsAsZS8CoqbDWBgm7wGQNBXkjE8SuhKA8
  zv64cwpvbjJZioW7tx6Jo986sMDshig678dSR8whhc1zq4ZeaeDzGB6SbUZrpXXpd4aH
  y5AQQF7fwmStceXXEsNa4zL8xAhTszp2yFhLF399Q83hTdka8gUWyyQ26LUFDXCUivSf
  PxFRyUZZEQEK54sZZFP44MQoC4dDRrDqd2tyKMjTkdxVTg1Tvk1k9CNRUoHzdrboeESK
  mmdN39Ms3xRCVTN7cU6qGFW7Uz9xqhCinaKpzgRLp6ZSvmX4NcCTbruQeb3vMvHvJLCk
  MghQp
sigKeyType Ed25519
pkS        b5DCBaChqWVVGJOsGWcKuKti0SKfm53pTfOwuj-hm9g
skS        MqiUK5zsViOi9QxQlyMXvPdraQghVOASyFiAvlFXp4U
encKeyType X25519
pkE        4ZKJH0k2hjrBnFa83B8ZWx2dQYjQmbnc2nJW6urQSWg
skE        0G2OObWQl0Nz9fR8LyBvzVGVLezU3wu5Y7payTJY2BE
```

`bob`

``` text
id         did:peer:4zQmZmCAsG7j1ewTjXjtddwujik33CE2cMbYSPagpMiYnt1A
longForm
  did:peer:4zQmZmCAsG7j1ewTjXjtddwujik33CE2cMbYSPagpMiYnt1A:z25NRJMKpQ
  KwnUm6k9FbTSp1eqANorDtFimHW9nGdLSgAbN1UhsQANFAnhij8VXrrwnDDG5Rb7HGrY
  pBGZRy3EbgmxirqJi3WuNfiajavps6kAfnvk9ykxGqcxH4u7P2TJohfbvigGMTMGxAhq
  kU4JDkWYi1sBp266n8tzTzD3DfRUDuzmWt547vK52UYFjqvYuqeZke48ht1Tn7veKyU9
  an3DBDEK5iNnMZuTwssYn9WboW5tdbdA3dyKiqwbBwrTUQsaAbpAaMzKCsFouHetYm3r
  6ft4Ewh5F6sQeWtVzScGmrWr2M9rcyLyRC4nC711Sfh3q6tNeb393SqeLs1uMVD3AJ7m
  LMWGmaYSuMBewWRcaJZdEiDe4NjZa12WSuZ9hZ9UYigEMByhwiT8WVsgiNEjFwcQLdof
  owERUKhYYNv1sgDfZ4K7MGRtdkJw3eZRbP1T9NPwyDsiBycnKipqn4MfcnDMWVMSsiQC
  g1xprkVvtgtgjhYkG1A7w9UGk5497ytKuFMpzwJbu8cAxLqTFZ1phe8cft61Euqj1eoC
  Q1X5E
sigKeyType Ed25519
pkS        -ezxE2yQV7bti34Ofz1Cgy_Ykf3_t6ob2zc4evBKZS4
skS        8sDXUkHnFe7exy1sGdCZl9kQQb-Xz-wuMBcGKXkVetw
encKeyType X25519
pkE        c2fBIIJWZgJFNKZ0SS7k63Q_73kW1nnwaAf2vIb-mGA
skE        j952DlpES4WEaSrY72PZwOi1j035m9iFxsZh_OKfcOE
```

`nested_alice`

``` text
id         did:peer:4zQmehsjMuPkPjzg7WF2tH5X1SGuFMxacJB9RETLFwjgMDqX
longForm
  did:peer:4zQmehsjMuPkPjzg7WF2tH5X1SGuFMxacJB9RETLFwjgMDqX:z25NRJMKpQ
  KwnUm6k9FbTSp1eqANorDtFimHW9nGdLSgAbN1UhsQANFAnhij8VXrrwnDDG5Rb7HGrY
  pBGZRy3EbgmxirqJi3WuNfiajavps6kAfnvk9ykxGqcxH4u7P2TJohfbvigGMTMGxAhq
  kU4JDkWYi1sBp266n8tzTzD3DfRUDxc1EGZZ8oysc2HpdT4rEuGHZoobGpKmo4XJSoDP
  KF6CfUWCr2UyzMv8dbCQWeugCqsUqQuASukLHjNPpzRx8cuSRSA7kDNG9civ4UoFrWhg
  vdSrPgBjeQYQFREA9ctDXCG7QkoYfNrpLhHXZ3LK3C1Jm7hQtmX926LQ75V82SSRPmwX
  BYXGx153XZuCm98znoU8cWADwCtJ6GhVrUSZPkkaPgrZqE1pFukaCvZf4gstRoZEwGrt
  DhyDdk5L6SpoLxEYCYfgFGmYpo7a1PojKqFFqp1NLzgfimW8XEuq9sL3BXraAz6kxRXC
  nbeEmSNHxzgJxe9S17WFsTn2jtFHLQFHgRxzpjhdXeysKxYJSDng8Cjjk8WdZeN5YkmK
  sve5z
sigKeyType Ed25519
pkS        _-E1m_BLThHwhUuYhV0YovargFtQUkox6LnwhHx6Nnc
skS        gOpqJhU4I8_MNADm8rODdfaMP4dv61uP8VwY8e0mjNw
encKeyType X25519
pkE        NJwm8WK_zTmq60S-bjrbr1OjURO0FBfEjaTlZhmDm0Y
skE        e2EIWSYsqFudoECVTglwKwX_i_t36CGjjDCCRF7uQ7A
```

`nested_bob`

``` text
id         did:peer:4zQmSMw413keKhgpTpYm1q8jzmpqNYwddVGPubkHNgp3qQei
longForm
  did:peer:4zQmSMw413keKhgpTpYm1q8jzmpqNYwddVGPubkHNgp3qQei:z25NRJMKpQ
  KwnUm6k9FbTSp1eqANorDtFimHW9nGdLSgAbN1UhsQANFAnhij8VXrrwnDDG5Rb7HGrY
  pBGZRy3EbgmxirqJi3WuNfiajavps6kAfnvk9ykxGqcxH4u7P2TJohfbvigGMTMGxAhq
  kU4JDkWYi1sBp266n8tzTzD3DfRUAgR84nfSphZZkXtF4LsDaKz5V52HNNgWgz1k8aFk
  jSCzTgyVcS7f2RwomT1HfyLVrW3UqCszF7iJ9vpfMviins6mHyfBkcA3bJbpeKoVTqem
  LZ9XgkhhGxnszeDAr8HAGrwTysiGmZeJUoweCk2RyP5f1QyWBqcNcRyDRjkShHQgpcVP
  y2iKceZYQbZsMRVTJveWDuzbAMzAeX2XsXDGE8y6r2dEKLikSRqFFYwGTrNEBjmkfQ9D
  nkRbQAK3ZoKKT94khAhbw8tZkDK3w48Vjb6XZkEcpWbpwsrAM4RDPcS7UJq3fH3WCoeS
  DQWoXyxncPoYmNaBK6PtwQe3PhaMoUBwUUFtEsDCuVCrAz6vpvMyZaeMv4EbmBGYwtMu
  nWhxG
sigKeyType Ed25519
pkS        eGi5FU5ZXN-kavLZRr_ozjAXFzUPsv14y8CyPCOuR84
skS        6X6bCFv20GqJXHcnIBba3cILwFv9eawgwOL2HgOp6ig
encKeyType X25519
pkE        5tBNodlJELEWNo9d-rgDxcYf1ldc9fruci9PtWqUgAo
skE        0xi9nim9P3GuGznEHJJFL2JGpuCPqtCYFJ0EvBGj9Qo
```

`p`

``` text
id         did:peer:4zQmXuYx5quNpAYvu1syaoHpJWxHceBM8PnAS1J84mjEo118
longForm
  did:peer:4zQmXuYx5quNpAYvu1syaoHpJWxHceBM8PnAS1J84mjEo118:z25NRJMKpQ
  KwnUm6k9FbTSp1eqANorDtFimHW9nGdLSgAbN1UhsQANFAnhij8VXrrwnDDG5Rb7HGrY
  pBGZRy3EbgmxirqJi3WuNfiajavps6kAfnvk9ykxGqcxH4u7P2TJohfbvigGMTMGxAhq
  kU4JDkWYi1sBp266n8tzTzD3DfRUDEQsmpmjBHzq8cijG6sryWW5nVPht6pYsbuY4ccU
  dfcph7owJRDqYg99MemT1i7k3HvTxvnop9E89WNwWZiDLmJk5tssb7rQSatDkq2kvRhg
  W8eVyFnsoTdg2h87tsGpE8p6tQNyZpzAnTNVUe886osyyavxqQccEcm8idNnFEXEqtLL
  1oENMQvaWr8CsYUPy1rUpmv9xFPBay42n54ssn99hEMCahvW1sLFjHwcxGGco6PSMZT5
  DCw9yhUVSAeYpJ6eC4a2tjXB3tjcFeWifhxkp1u2yLJ1bcdxmJDvbKPghPVeCYYEm7g7
  RjrdFKKX1534YVEvwgeTi6H6ujmSvvs6xLwDjkmRwYpgPAucS9TMgVGJgDpEXD1brQZU
  P3PBJ
sigKeyType Ed25519
pkS        4aeb8EZ5rJciXQvEjl1LDcZaST67KdYnqvZ2BYWU5Y8
skS        WW-aIOkC8AcowW-6H-MmjFoUA92mzz1XYmp5DsLpxE0
encKeyType X25519
pkE        ajg137oz_TtbqqxihWdMYGblF9NLtFpDg8mv06leNVQ
skE        ivpbTN8fMgb3oj1S3tQ5SC5UAjDQ5oLuOlmrkbJKy38
```

`q`

``` text
id         did:peer:4zQmTKaSRexnzX2ecu1eYRusFNeWbrT5jbjr3YjtfgciZc1Q
longForm
  did:peer:4zQmTKaSRexnzX2ecu1eYRusFNeWbrT5jbjr3YjtfgciZc1Q:z25NRJMKpQ
  KwnUm6k9FbTSp1eqANorDtFimHW9nGdLSgAbN1UhsQANFAnhij8VXrrwnDDG5Rb7HGrY
  pBGZRy3EbgmxirqJi3WuNfiajavps6kAfnvk9ykxGqcxH4u7P2TJohfbvigGMTMGxAhq
  kU4JDkWYi1sBp266n8tzTzD3DfRUBoRT26HWqurFNeBrp2Z5RXkhxkhyxAnpoB6ZS1Ct
  hQZKhEgZz8ubr2Q29a9C2ZYyuCNNuWCCUhfm8AASng7btZiV16P3qyFpbMk1dpwabugu
  NC2hBAycwQ1pniBp3yDGdTrSDg7Mvd62zkzDJfCXhxTQJQ5SQvAu1bb5ZGonmjMfu3fU
  877FfvbYL1gqYDKcH7hZ7NnifTQP345XsY2tTav6vR2vUAzDiWwvpVJ9gApPWJExs3A8
  EBw3wke2m2C9uQpdu4XRaxVzWgtGd1NL3LFwcf34gEksj2VsURD4VNhdjQ4MkKSFy7ux
  gDSyqTXUdr1GEGeQGAtcFTq5anuPnN9kDHm48WihypUQ48jo3zM5JXE1fhL1Xypi5rWn
  3tkip
sigKeyType Ed25519
pkS        qUfbbaVzKhhddujMaJNSl9C8eGWCOBjA3WT4UGzXNOU
skS        GolUele6xQTKisWaDZT9Q6dUNGg93_y__h-J3X_m5aU
encKeyType X25519
pkE        M5Qk6RSrDUckHiQlmduCMbu9HW6AZbJCfkQEQqWShSI
skE        GHZ-LhpY_K1f_PvDW6loXWLvFIcc6majVAR8_jWgL4c
```

### Test Vectors for Direct Mode TSP Message

#### direct-sealed-box

A confidential application message under the libsodium anonymous sealed box. The sender's static keys play no part in the encryption, so sender authenticity rests on the ESSR sender VID inside the payload, which this suite requires, together with the outer signature. See [Section 9](#tsp-encoding) §8.3, 9.1, 9.2.8, 9.5.

``` text
sender     alice
receiver   bob
skEm       EgVuWV1WsPbu8JDwzSWiCUkkjCeQUl0PkwIY_wtN3RA
pkEm       wfprioKR4GMkMcd24cr7B7sM1_iy88nTHbvkED2YVys

message
  -EBYYTSP-ABA4BATZGlkOnBlZXI6NHpRbVVMNjFOYzFGN2lvaUt4SE5xd25KWFg0c3Jo
  RnNLS1BvNlRyQ21oTTNkZnBx4BATZGlkOnBlZXI6NHpRbVptQ0FzRzdqMWV3VGpYanRk
  ZHd1amlrMzNDRTJjTWJZU1BhZ3BNaVludDFB4CAtwfprioKR4GMkMcd24cr7B7sM1_iy
  88nTHbvkED2YVysWC_6GFqzGqxjBQhW05P2nlttvJtG8bu8WM2kZJiLlOeT7b2Wg0URD
  RYhOFeb4EtB8XpEUW6KqjqW_zwj79vMTAdrf8vq4u27MbDCQpI8qzeiGLN8B-tak3SI1
  vKAADx68VHVg5TQM-CAX-KAWBAAEBcQdynkYZuKDtCFr96nFQYAYqzFkccyYPS0gtlTp
  ebinrsiEvafy7BI8mzfW-GrzH3zWIVclfElXBm8aB1oP

payload
  -ZAcXSCS4BATZGlkOnBlZXI6NHpRbVVMNjFOYzFGN2lvaUt4SE5xd25KWFg0c3JoRnNL
  S1BvNlRyQ21oTTNkZnBx4BAA-AAF5BAEAGhlbGxvIHdvcmxk
```

#### direct-hpke-base

The same message under HPKE-Base. The aad is CONCAT(TSP_Version, VID_sndr, VID_rcvr), which is exactly the envelope preceding the ciphertext; info is the five bytes YTSP-. The ciphertext field is enc followed by ct, with the AEAD tag inside ct. See [Section 9](#tsp-encoding) §8.2, 9.1, 9.2.8.

``` text
sender     alice
receiver   bob
ikmE       zmfPZS31ZecVid-0CvG0x7YPwxkwy_8TLqggDcwUDJg
pkEm       1T4oA1pSbehBiIwnoXFGA24kgHowT34VdE95wF9qjSs

message
  -EBFYTSP-ABA4BATZGlkOnBlZXI6NHpRbVVMNjFOYzFGN2lvaUt4SE5xd25KWFg0c3Jo
  RnNLS1BvNlRyQ21oTTNkZnBx4BATZGlkOnBlZXI6NHpRbVptQ0FzRzdqMWV3VGpYanRk
  ZHd1amlrMzNDRTJjTWJZU1BhZ3BNaVludDFB4FAa1T4oA1pSbehBiIwnoXFGA24kgHow
  T34VdE95wF9qjStBsok4fIkbu8IKODF2nsZMUAmS5BqxDbbYrvl_TNGpz2omwJgYX4bS
  YoTeKse4-CAX-KAWBADHuTmj_7jyUCkkalySPOFiy5pTbNtjEODiwwJZlI5DqMk5Wutx
  4LIOWkAAa3uee2b_0Kh5SXaFq65MedyO5VYJ

payload
  -ZAJXSCS4BAA4BAA-AAF5BAEAGhlbGxvIHdvcmxk
```

#### direct-signed-only

A non-confidential message. The payload sits in the payload position in the clear, under the same -Z## framing a confidential payload uses once decrypted; there is no separate non-confidential field. See [Section 9](#tsp-encoding) §3.5, 9.1.

``` text
sender     alice
receiver   bob

message
  -EA3YTSP-ABA4BATZGlkOnBlZXI6NHpRbVVMNjFOYzFGN2lvaUt4SE5xd25KWFg0c3Jo
  RnNLS1BvNlRyQ21oTTNkZnBx4BATZGlkOnBlZXI6NHpRbVptQ0FzRzdqMWV3VGpYanRk
  ZHd1amlrMzNDRTJjTWJZU1BhZ3BNaVludDFB-ZAMXSCS4BAA4BAA-AAI5BAHAHB1Ymxp
  YyBhbm5vdW5jZW1lbnQh-CAX-KAWBAD-jhE5h1oMTf-JsSEMVdJ2ntTahc3PFi25mQ6k
  PvbnPqfuhIQzTKxuTvfYauG95msg_yb2eryo3wvg1YoX7xAP

payload
  -ZAMXSCS4BAA4BAA-AAI5BAHAHB1YmxpYyBhbm5vdW5jZW1lbnQh
```

### Test Vectors for Relationship Control Messages

#### control-rfi-direct

A TSP_RFI. Its Digest is the message's own self-addressing identifier: computed over the version, both envelope VIDs and the payload fields, with the digest's own slot filled with the 0x23 dummy and the padding field excluded. A direct invite has an empty Reply_Path and an empty Referral_Field, both -JAA. See [Section 9](#tsp-encoding) §7.2.1, 7.2.2, 9.4.1.

``` text
sender     alice
receiver   bob
ikmE       ew2j30RF7AyIl6ompEoE-0acQb8yg_Iyk303CTx8HJ8
pkEm       U9I24IIKCz-mPGP1IZcfMZohp_eBlv-BBlfLm7vbUWk

message
  -EBSYTSP-ABA4BATZGlkOnBlZXI6NHpRbVVMNjFOYzFGN2lvaUt4SE5xd25KWFg0c3Jo
  RnNLS1BvNlRyQ21oTTNkZnBx4BATZGlkOnBlZXI6NHpRbVptQ0FzRzdqMWV3VGpYanRk
  ZHd1amlrMzNDRTJjTWJZU1BhZ3BNaVludDFB4FAnU9I24IIKCz-mPGP1IZcfMZohp_eB
  lv-BBlfLm7vbUWlcL29m6RzNgGaA3yIiD3pFzZJXgoeCU1eij4KirnEhlzPGETY8c46g
  rFfA0oxKauyhQSKfn8OxuivWKEaP0_r0j9JfxngveOHpa0A7mCV8dm3taohU-CAX-KAW
  BAA_tgpqb5e4Vfz2bXZ9ZMrk0K_pw4tSD7xd9PfHv6uPYLhaVLNap-E4pVf2GGLw0qKe
  adFPDV2WT4gGX2Nww_AF

payload
  -ZAWXRFI4BAAIFv8e5p6Z1i2FPunuNF26mSr2AHU5zPJGb7nBuVIPr6e0AARERERERER
  ERERERERERER-JAA-JAA4BAA
```

#### control-rfa-direct

A TSP_RFA. The Digest is copied verbatim from the invite it answers; the Reply_Digest is this message's own SAID, derived the same way. The two digests are what identify the two directions of the relationship thereafter. See [Section 9](#tsp-encoding) §7.2.2, 9.4.2.

``` text
sender     bob
receiver   alice
ikmE       vU7UpVjzd8nDZDHJ1NKaDdwEzUDHI7PRmK1Udx160J4
pkEm       qVZSTmoBq-jrBX8d1pa40Yk5J28FT14vIHOh8-GN6VU

message
  -EBVYTSP-ABA4BATZGlkOnBlZXI6NHpRbVptQ0FzRzdqMWV3VGpYanRkZHd1amlrMzND
  RTJjTWJZU1BhZ3BNaVludDFB4BATZGlkOnBlZXI6NHpRbVVMNjFOYzFGN2lvaUt4SE5x
  d25KWFg0c3JoRnNLS1BvNlRyQ21oTTNkZnBx4FAqqVZSTmoBq-jrBX8d1pa40Yk5J28F
  T14vIHOh8-GN6VXzL1VMQNnLb62gQT0KXkUQj74Jikwx7vUJlxbrJdtnskeHwsE-0heO
  yQ9hbgVIPjbvbro4DiNE-jSYkdv-xhIF8v7UTyc7OLTwd9ay2_hd6kaXfsa8Ecxv3_3d
  eNYe-CAX-KAWBAB_2tB6-CHdYpaTYbgbvYgRNzQGL_LUn-sy_sga4tWPdHcnH2cUeqvF
  6r4k9EivaZLLem7S2YfZI2kAsWWTVXYJ

payload
  -ZAZXRFA4BAAIFv8e5p6Z1i2FPunuNF26mSr2AHU5zPJGb7nBuVIPr6eIB3iJQFdVqm5
  fH9RoScnqBs5fIofg9UUDPj8Cm_LkGYS4BAA
```

#### control-rfd

A TSP_RFD. It carries one digest, naming the relationship being cancelled, and no nonce: the nonce this message once had was removed, since a cancellation needs no freshness of its own. See [Section 9](#tsp-encoding) §7.3, 9.4.5.

``` text
sender     alice
receiver   bob
ikmE       16WX82PmX4bBjabLDE16md_SNXRJfNa0xPn5_fp6GVE
pkEm       OLoHxJkegv3Q68EgUa1HPL_ELnoSkq5XE30aiOOC604

message
  -EBKYTSP-ABA4BATZGlkOnBlZXI6NHpRbVVMNjFOYzFGN2lvaUt4SE5xd25KWFg0c3Jo
  RnNLS1BvNlRyQ21oTTNkZnBx4BATZGlkOnBlZXI6NHpRbVptQ0FzRzdqMWV3VGpYanRk
  ZHd1amlrMzNDRTJjTWJZU1BhZ3BNaVludDFB4FAfOLoHxJkegv3Q68EgUa1HPL_ELnoS
  kq5XE30aiOOC606B3B1YEcvuD4SDsz6TJiaJavy3u83tzf2rlJFV1NsV3QJqO3GwG2gH
  xOBeTblt_9yZcAaBs9-hgEO9nm-5-CAX-KAWBACH2iTSkMLf5JsDKTu9JUmptveFad52
  vuynvG5FUwMqSSvDUpAG9QphNBY2CmwZNVQStTjwNWG-NzaiQt_hJw0F

payload
  -ZAOXRFD4BAAIFv8e5p6Z1i2FPunuNF26mSr2AHU5zPJGb7nBuVIPr6e4BAA
```

#### control-rfi-sealed-box

A TSP_RFI under the libsodium sealed box, the suite the specification keeps only for existing implementations. Two payload rules differ from HPKE-Base: the Digest is Blake2b-256, whose CESR code is F rather than I, and VID_sndr MUST carry the sender because the sealed box is anonymous, where HPKE-Base defaults it to the NULL VID. See [Section 9](#tsp-encoding) §7.2.1, 8, 9.4.1.

``` text
sender     alice
receiver   bob
skEm       Z4ALsIFbWmoNYPFkP6mR5CYbOlwk3Oa07reQ9j9BbYo
pkEm       DvRIPYQKw_paPzePKdSbkGiRcRNmjYHhx0gYr0S543I

message
  -EBlYTSP-ABA4BATZGlkOnBlZXI6NHpRbVVMNjFOYzFGN2lvaUt4SE5xd25KWFg0c3Jo
  RnNLS1BvNlRyQ21oTTNkZnBx4BATZGlkOnBlZXI6NHpRbVptQ0FzRzdqMWV3VGpYanRk
  ZHd1amlrMzNDRTJjTWJZU1BhZ3BNaVludDFB4CA6DvRIPYQKw_paPzePKdSbkGiRcRNm
  jYHhx0gYr0S543IUTpqE3k4s9HkuJRqrD8LXaYNucbfQLrI9Q_TfieiYffgOvSAPhO5c
  Aisip55K2b2AbuPDV4Zk5EnAMy7-470OWR2mI3ouzQl4meT26JPSyg_rg7X_evwr8ZJy
  5MbImIzNsXyhokDa-xx64NI2P9EtoAp7jAt2L_c9YW-tI0x9gtg3b53hlA0RJj1GWRop
  -CAX-KAWBADpDxx2j-GxAdAbAMV57_2ieRHgJniYg9zwHZXVAVS3JLfRDe2y4iEN2rQk
  FUe2i_iam6ucCwHRUELVXLEOddYG

payload
  -ZApXRFI4BATZGlkOnBlZXI6NHpRbVVMNjFOYzFGN2lvaUt4SE5xd25KWFg0c3JoRnNL
  S1BvNlRyQ21oTTNkZnBxFAQ__3XiGDTJoRE3D0dX6vL9mIKCqGteryySXu5yNgvW0AAR
  ERERERERERERERERERER-JAA-JAA4BAA
```

### Test Vectors for Direct Mode Nested TSP Message

#### nested-direct

A nested message. The outer payload is XHOP: sender VID, an empty hop list -JAA because the outer relationship is direct, a padding field, then a complete inner TSP message with its own envelope, payload and signature. The inner VIDs are did:peer short forms, 57 characters each, which is what the two endpoints use once they have exchanged the long form that carries the document. See [Section 9](#tsp-encoding) §4, 9.4.15.

``` text
sender     alice
receiver   bob
ikmE       wTSnRd6U5rWz-3yO0ngUXXg_6V5WgUjGbGLk0LrLj0g
pkEm       2lwtszl6nTuyUHQPcfgHqTOLcllbgMpL5_tD3myO5ko

message
  -ECeYTSP-ABA4BATZGlkOnBlZXI6NHpRbVVMNjFOYzFGN2lvaUt4SE5xd25KWFg0c3Jo
  RnNLS1BvNlRyQ21oTTNkZnBx4BATZGlkOnBlZXI6NHpRbVptQ0FzRzdqMWV3VGpYanRk
  ZHd1amlrMzNDRTJjTWJZU1BhZ3BNaVludDFB4FBz2lwtszl6nTuyUHQPcfgHqTOLcllb
  gMpL5_tD3myO5kqpyGOhlgwX9CKraR5Zqsd5gQo7pmzcqtklHmtpSe0VUGRKNk7lkfZ2
  0A6iBtCP1VqpCenjGyAJ53mdytJaBU4yQlfk6_h_qkKkr8jSQoN13rtqJFnFKtSekDzd
  d8MtUk82fdLHrNnmk8228jNhzbL2mewQhT_V3x1-FikjdZELf5LksMYsRVdiTbIqnVk0
  Co_EAAO_fNEtKS-g8X2RFjJ4RHAqC-HmTC9rQg-YRasfnB2d9HuK9nLecMZspuUHPEV7
  Tw6UDpjSHAqwyxLkQ7Lxxgmjc4_5WRW40q8smgcd2coX_MBnjRKhY-7T4Gbo4wQ1g-6K
  dFgfRPbxU8mK9tN2Ch3HAEgajunFklLWpwyRRJjTYTteYXy4Z8_fYvksFnulwaI14fXV
  SZw-H5wT4Tiua76wgDGaWUrR-CAX-KAWBAAkhxeb5pP-zAgzjEdQkHMcjb3_U6C5KH-N
  an-SU1Mhrog7UzKu1EWq8wqEU_JByX0RbDz_wXMke_SbjOG9JcsC

payload
  -ZBiXHOP4BAA-JAA4BAA-EBFYTSP-ABA4BATZGlkOnBlZXI6NHpRbWVoc2pNdVBrUGp6
  ZzdXRjJ0SDVYMVNHdUZNeGFjSkI5UkVUTEZ3amdNRHFY4BATZGlkOnBlZXI6NHpRbVNN
  dzQxM2tlS2hncFRwWW0xcThqem1wcU5Zd2RkVkdQdWJrSE5ncDNxUWVp4FAa18xMvIf8
  fW5FF3cOHHKPlmJY7CNOU4gMdUw06e03UW_1PVt1O92_IkwQWqsgqb--yVFkjJd6aYMU
  klWFZRedb-1Dges-0k1J6Ci_CRjw-CAX-KAWBADMVJ3ENHk7SRgzuBbzonXVQ2vu4uVt
  LAu4Icbg1s69jW9RYPw4TaZKFvVR27mf32fuxj1YhrGBaf9hyEfFAJoJ

innerPayload
  -ZAJXSCS4BAA4BAA-AAF5BAEAGhlbGxvIHdvcmxk
```

### Test Vectors for Routed Mode Message

#### routed

A routed message. The outer message goes to the first intermediary, and its XHOP payload carries the rest of the path as a hop list followed by the complete endpoint-to-endpoint message. The last entry of the hop list is the destination's own VID at its intermediary, not the intermediary's VID; the list shrinks by one at each hop. The hop list count is the byte length of the concatenated VIDs, not the number of them. See [Section 9](#tsp-encoding) §5.2, 5.3.3, 9.4.16.

``` text
sender     alice
receiver   p
ikmE       H_LnY626_NNxiT6uU0Cd6029AGyYDUMOKrr3BlRyk4g
pkEm       u3jQxhX4ryavA7_XLCdatfNVJssymR8KjHMqFhCjl1c

message
  -EDGYTSP-ABA4BATZGlkOnBlZXI6NHpRbVVMNjFOYzFGN2lvaUt4SE5xd25KWFg0c3Jo
  RnNLS1BvNlRyQ21oTTNkZnBx4BATZGlkOnBlZXI6NHpRbVh1WXg1cXVOcEFZdnUxc3lh
  b0hwSld4SGNlQk04UG5BUzFKODRtakVvMTE44FCbu3jQxhX4ryavA7_XLCdatfNVJssy
  mR8KjHMqFhCjl1fHhCX_UWAqrxNVo7bN-T0MGRTxtZbXHohFBpJBtj56fuw7UmON9OGL
  5WewM8NS0pCOIVlwvkg3zFasindp0QF9RtKf60Y5ZewPVLKJE6zrYGM2B6fCupmO_qBm
  BJjXuHWh01-rGzvpFO_-Lldld7PmcFCcTrJDwLb39GhO_MQ8anZkjGz3AOAArmiwDhfV
  o5PNWj-7OnZ5fsKE5hBbf_2ZGN059sGqofoBGzM3KV9eCcZccBL0gmUCp5pqy_VTzsB1
  9HhzED39WmMiFK67ZwFMmME9yBfMk9hRjyiq7UTulmS6E4X-TJSOhoMq7a3jrDKLzLeF
  yh6v_Jbu5_aYnz_dohJstsSkhwqCSuQxudCHC9pumoAaO4rE9pg8N1_yMg3bHL7i_SwH
  ELoRSb9zMJy_BDGNeNPqYE7UdwnDanzHVqJ3UHzfkt9mwK4TSkS5YVmYsO2yhFRbK7_P
  R_J5qlizbUX8oJpm8B7JOrnBT9cUZTCVG2ykcJHrsqNrAlJCHtCl8g9LGpQXjo2PuVqp
  qF08fFYat_qR3HlZbOPOF13DE9-IoatO88XmFIPoLXd07MA9-CAX-KAWBACFpYywiBN-
  4IGmaNbJjoMGzmmLRFPtFdZ9Lo6Zhy-skvljp5e3qLMi-5rGYJO0D93U0A_V1O5gTC9L
  DSUlvjAG

payload
  -ZCKXHOP4BAA-JAo4BATZGlkOnBlZXI6NHpRbVRLYVNSZXhuelgyZWN1MWVZUnVzRk5l
  V2JyVDVqYmpyM1lqdGZnY2laYzFR4BATZGlkOnBlZXI6NHpRbVNNdzQxM2tlS2hncFRw
  WW0xcThqem1wcU5Zd2RkVkdQdWJrSE5ncDNxUWVp4BAA-EBFYTSP-ABA4BATZGlkOnBl
  ZXI6NHpRbWVoc2pNdVBrUGp6ZzdXRjJ0SDVYMVNHdUZNeGFjSkI5UkVUTEZ3amdNRHFY
  4BATZGlkOnBlZXI6NHpRbVNNdzQxM2tlS2hncFRwWW0xcThqem1wcU5Zd2RkVkdQdWJr
  SE5ncDNxUWVp4FAa_Gblg2mbPRmyh5lhWb0A-hzL-Neyd0LKd1gGhh-ILyOsKH7KHRVU
  qhRWKUcoR8U9j2EogB7xFwucVDU959TAd9Q2QqSjB-jE9i6eegLP-CAX-KAWBADtlMyQ
  Tv0kh9azrwhi4zZBRWSjYytoDK1DSDI3ipa5yqU7_YYADFl32dyFqvSZdh_YxLD5EcpC
  K0Me6sA8aA4J

innerPayload
  -ZAJXSCS4BAA4BAA-AAF5BAEAGhlbGxvIHdvcmxk
```

### Test Vectors for Post-Quantum Key Types

#### Identifiers

`pq_alice`

``` text
id         did:peer:4zQmbLqu3weZtsnNesBzecCZm5FA6uaGkgCWYR5Wndr6Gzzd
longForm
  did:peer:4zQmbLqu3weZtsnNesBzecCZm5FA6uaGkgCWYR5Wndr6Gzzd:zbR16eTfJ9
  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
  fjZR4sbgvdo9p8F8QJPN
sigKeyType MlDsa65
pkS
  -XNPEJoCD0SXNM9Z1Ek_Ah3JXU94GgMiqsGZ9VlhtD-ibb_VSt7Kft0622kvaA7nYI8A
  1STW6uYfs4EQwElWrjLKUAxyIRGj490atsxFZdlpBJhDzY5GugJfhnT_MTHlM2R1OJHR
  NVpL7rqAQCFhFMv_s3n_nu6ERT07HE0v4-IV7BzADacxQvizGxUiBMD5_xIBOGFJRsHX
  yWnxFZkZUlYlMiiA7Czj_ja6qPeNhFQtQJgkCp1hrIteqAXGyBK9ngctYOHypXkwMAG8
  rO74UW53CHyrCU7FuL13nDmiXxOaEDzZ4e1fbLm_wcmgl7KTCWFsoFyRyZiEHY1IPYXl
  TlCZjP5s2FzCpoTXO_XvQK-iOcTMesC1-_xkXYJPjjhhyq4aR6Y_gQUBTHG0EROH7NzK
  RAOCJ0905kxpP5zKv0EYWkMSJcigfgXhREC7Iq6JDyRw0VLpu3czeF4xG0VdojBUJKQC
  hDzkDWC9PzgZKLvktmN9W7-yFw573qgeWY4oWnl4ZPrKoqgcGGcAMMRGG12iEdjvy0kq
  xg7SUUIho2dUl_lN9FivvNOBGrVfDoL2HBCuEawJA9cVhgNtMxD1OV1QRRrm0MuKzSVO
  d7M8DH-cRLBb4n_5wSApn53h_5OM6T_uCdrfRjl9FWgiazeXwGb9ivlJR0OjRKQS9aKi
  U4oP4QK4tzm9IVf7fbmOH66sUh4Cgy2JCjt8Sqhvhp4sySpA_WIUzvhdm52hKFoRx-_F
  Jc35nGMia7tvsgPpc-GlHCdMQXB873Lfrn2yZgIXz1Ji1UIAlqtKFRqVBCRiBlwhAXT9
  xjrPmpD7PcLXUWe_8pTNI-1t8QqcOl_S9GbQTAnyhkoSaApimo3EzxRyjxoksn0DnX9F
  KEeguxGEZ0dhXuUT9Et-9FylvkKgd0ZTU_RzMWgdWfS0JEhqUE2uMgJrKYaCzZO5C84o
  2gSbIyXcyvKukoQ2YVA3qF6qBoj5fiL5atJ2VDxqgg2D2Q2RWL2QUeAbpw50odvjKLQU
  bW2YLAHuPMnxZCn9MyeXwVjoasyELSemUurKHsxWwnonMAmQ46kxjgv4s5asGxMLrP_-
  fKtwMEt1epJ3Anicdt4FpD0Rf2EbyCW5KH7jPPz8mq3Tr7Dx5er8jqfT46Zi3Wlx0fIw
  ryB5ON8yQrMTtBRvSMSQndty2JHKoKhylYc4KoVszqx8d8Ia4IkjwNNrvQAQomPUM2s8
  Wf9HuQwHwwGjhuGQefHiUBnOqbn057HXKuWrFYY-enzKBLaSnwVD0zatyIrkPfocI0Px
  oCSQIlUrriyAUbOs53drxBdF7bh7urVZjPL2KrPyaC-evLUrFpTl8F1BCUlREpmDSx55
  LjbcbHQyf9WZY2835gMT096InMv3JrLbuwHyz8hd6oy_FqdJpjrYQK9REajLxmZNVCTP
  hqxdoUn0cJvnq8uOgn8qVa9AFkxUWT3eLe-IwTo3EnuLxoyvl657a0JsBofp1roFkt0D
  PlAiNK12ffdclWql6c6S1-W__6um0L_ZcnIMznII7demQ0RQVKBd1ycs9wlJ66GLgxgS
  40OIZL8OuKp1Ht9vkl5DScgkPt_zKSEdbnEnfXlo70eKAb4fkJaJyTYT4r-wPskiBqUZ
  W8NmJrh8ioK7FyImJYxHXOBgkOD7bReyZJr5kkWD2WWrB-jPr70W_Glk7b7PdwS9Hf3l
  eB8MfZCfOUFbRksbPaz89qOsHcBOM3_F5UthxqUboxREizv41xkN88IHQhmpAyvS3ZXq
  Apr3x2mjkzp7kCUdJFVY2Gk4BX3h7o732Um6UW_TXE1HPvUnqQo2OxfLzw-9xcM0AQbJ
  SrTeC-hD3ZHpJyEHue-4srYvloWjoZqbwcXJUcMiPdNFDfSDiysqwAuN9VUFSCMAzGly
  L-sytuTrr1rYEY3KshQ3vjFLxiiiCa6ZBn5Je-s6IHBP-OFTAIylZVLtgq4WDKo9Q1zo
  ulzk6SGHZJ1QF0Q-AxGpiA9We2kq2B040q1jLewPkFLq2dVH45UAzTlvUiUXWg1_sKPh
  HQHy5gf8S-z6jg5DnDhCik9W2lDMicBYJe1b4_ykBDbPD9Nzabt6L5JcDH-Y9NaYEzHf
  cx6DqkHy1XDQ6mgxaBLDueY1hAY4YPOuNDoyxhkliEpyc7_Jlogu4RXYWoDft822kyto
  0vlnyPgEE12Cc2jrpZiixy6_hb8euWXtpznMmHHN44qBCTIpcbmq1_uPbC_oxOSp_Tel
  90TQev9fyMqFVCBYMgb4Ar9YWKnz2FT1hV7RrGoqFGH6lL62wUelyIa6kQFdBUw31gEX
  fs3TLyQKL_ZTSh7bXNZS79sfdrh5FekYQS9UpXpnMRq4Gfe_GMdk6Qn7aVRddFrVJviH
  nTE0cSyEZb8aU3MfTPVVmj5aIDN7TuNG8lI7OzAbZXU-rJpHygn7_6upjNkWJzO88Y2e
  NuidcrrwtnLL7aGOQsSHIcjIGF3JgB2XJciVmSfxnTSvTtV-ZZRoXwp3mYZsqY3JrfUn
  -URIo7QTrLO1vlIBCMgxoJeIeDGG4_0wq-YG4202WKVB45US_fgGGhLDcfpsdHm5eZU_
  pNKYl-uCN89pb1vDrEA
skS
  -XNPEJoCD0SXNM9Z1Ek_Ah3JXU94GgMiqsGZ9VlhtD_kAdF67qjgAqtaOSUMDFnsYqIr
  fi6KACV4hnd82xS-9eniQETgp6ws5_-nsj1FHN8IWQMhm1VBcY1xBkejH4s02jxt8376
  jgka4Uqf0q_QlX_Skzpg9TfQT_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__f5jXsq1b
  W7PIMuvslJmvvQtJLgB434F_Gmdx7z3zee30OzRQWa257gETLsDtgFwux8KNV43FcDVu
  dsf7jh9C9102AlmOCRmbqE3NR92yGY-PkpHb1zpsK_CKpThiStJtpqGHfrxuF9WWrL_H
  O7QQhOHIawt-u8_KFDX-x1uTR8PH75PARzDAfvGp8UZOw8pdocNXXYdPrVan4AzRfdKT
  UMW-XjkKd-TrEhkq1QGkIBosojve_BhJDdHymDtoT7HQPRdzd-pKPNSl6lP4TwQYqdOq
  vmcoELhKVtAjxAAQIhuhL4AzU8fEarsOvkQq1oC4ewNI81NbSSZ0A5Z7iJGo-pPn0LsS
  _clkxjAQBD5ht3_XRc3yMT7I1h-AEGYxa_UfzYnlqDaWh-GQMd0hSRTkVf2SGSIsSp4U
  SPHPZR2SURtpBHp659F6Zm5L5j-ROemWvk0PkhArmY71acQFpFAYK6ddoyxZhIWEJm9L
  Dj68cuStJV2p2RTS7MDrLXN6iVSFmV4cyqoOZXLxGeNfrZ5QGRgTJqpRbaxhBC9LrVCL
  jT-0aodjRoqONUCfj4ADgz8qjrQo9Nkx_UjX7HWU_fDfh0eS2UjUqnGJHY0ATaeQ-7IE
  _WtU5ayqdK0_wlh6ZABAkFR-ShaY76KKNmTcdrq2cjp9A45cfUhv0fOkJqOBQBD8jDxS
  -cD_L6SGGt11zcELxObDADc89r_4Deeq9HsLbT36vHvZrZ5wMeZUPsJUVjkGvVbmUTi5
  544X6WZu2lX1JVuIdfrunzlYc1hWh7M8MNwSSlbqt38ImXtel1c0X993uMnLcHTISrM6
  FBsEcfFZ3P7t_GT-iImrLKTNBwahPJMFw0XXyz8CUuJjuVIdl1UBNBqs4NO0gp-qxU0A
  _anAk-ia6jlk440a2EsnB9T99pYFu1yu5ucYtb_171nK1NErw_KKRQqRl9RLbJN32GTR
  81lSWAyVmhVwP0_3-fhT9HfSALGvYbBu2ZMX7-PmM9_LossI8c-mfH7OngGhO5M55FfM
  AYnceKZeDUZxgWbijMmH3O-Bw7VUraYPniJQvBpjaqg2TOD1tph41P1SiHsvJ2q-OY_-
  r8kf8c8wRCWsgUemf2rbLwuWnrKWufcrgQm_AnQG2peAbyCHXXLi4X6hZRy_DogdTcXI
  divgvE_0WwDcdVYEy5S9q2WvsY2uKTHvqiabK-h8B_f_v21HszG5TZDFt38zT0GhBt9e
  eoywR1TOViKxgh_M7cLg6P0UUUehw4jyt8TqC2u6Q-0l4IA8wO4l8Fe3LqKZBAwvkEY1
  q01ZCOf9cqLLf0Z3KyuudyFs4zco2AFQw9EnWgI5l17V2kcm5ji3AWpieqiXZj5f9YjR
  5XDX1NbOYcBJ9Zl7XpvS-Ktb4rlgppHy3kCfX3GkvfxYeatevZNvDtvnsPW9Up3zwVcf
  8N7KzcrAcUNmePUnP2jlaWBXTx2KytqOeqTb5gE6KTi9hXI2YM2JTT7I3oO1hL5QMDda
  ALseviir5-Vv0UHmWagUmAQZ6azbvDMhXzmRb4AqIX2Si6dZCrHbwZB0qYVIcQ9piXIn
  OamryzIkOnx7A4w2YKD2cCpmdJuL0p-VrbuaMIOg1HFfD6fYugFV2X4l7-vdcC2JDCp6
  UWWMdbSJdgQW6IcmETG1lYjB8rbvh_5W45lqHwTxbftQNadIU4ep-uyMgu98-ZSsvI2n
  36yqrObPHTTw2_micQqATm5ejI_W3dOeTt6xbFgAAn-9i3yTeEFGU1N3BDbo7ndnf5Kc
  xeiZGep6vkX2WSKmaITO0TkQmvMXx3FN7u6ATxOO6go-B79O5p9UMI9cG2Tw21A4sp2H
  Q8ejUyIm6xp1oMQncOv74VlTwmvgmgQHOqC6EUvnZ5E4VKva8ewNDoSVvcSoCiOD6FF5
  xd7CKKukkgFkPO53y9l_aXvbtgQ4EL76V5FPziJiAVclvDdc0Xh_pmg8JkssVR2IS-fQ
  qhAtG688UwTOWXqeZjS85uGAabOQsvjzy1_Wx4dC7bV6NWHko8VN8-CeTlpdc0iLyHwQ
  _V2lgTlysCtenAvDQGGAZ2kZ2LWeWVJfg1zFCkKnZ0El5ismIzlloVoPXs_u0q5krVw1
  tmr3TUdu9kVj69wwvggHe28m9ceQMfoZW42ltQYRDf7Io7pHufW27mCpJdGHmpFUmj3O
  Fm6eJVt2ybHxNWBIybAEQsoDCT853y-Jd-Z2qq-uA1iJ95jtweT38FeUbRq2kLFXN1iK
  wLoPqSuuUKfudWhzs-2Spb1gYJHlxQ_HqkNfM8I0qtRj3gJY5lOKLZB3pFFgDDWgHH0A
  LPxgiEI6FbcIMvPcaEJzMBJww1eZ5tssn130LcN0ImDOpG9SHY9WFXocuLYhcCwdpSE9
  1uibnwoVEbJ4oyZNRhn7E5yAPZ3UyA-aSqj4ZhN2MdDdDPFMTIwBxzn6-8FJNYZPo-zD
  0hL0dcFEBaOTVQpKi_Bm2VQpaNoLva5BVL1g40M5Xkj_R6PL1JMAAjIn5y6gdXu104uW
  riMmv0x9EUHOb_LlOrXXHe-MPyjoe3jOIZSBKQD7zAtF_qBQFSdpmz63BiIBuG2PK1kj
  Z117tRSPzIZrgxiY4l-1fqtY1jzBIZzG_kykNC0eLPMB-NuMdQSaUPLvMA0k4PpYWMAz
  qCVU2JwPha7TTVHGbn77qZSfx4KnOdVQFdj9rQ9U2idFmZY7jMAQnVYHefGJTDghCyTJ
  BRrXyOQS-IVkDbr8af1ZtHKGf2gWYQ3lZS-IBLc3YSb6qlTc-nYOjB6j1k7xj_1BMgv8
  _P1ZXQKkQg4GyEi-FTG_DfTlo0V0kASIcztDp84tG_iswh9ov_OmJ9MWGq7JH2NPiLZM
  HPWlKNRuoXcwZJq-ftydxxOZTWO4R41YMlI5n__osufkfEgqwJwZkCGuiTti0qRhPw-e
  Q_WkOwEVZ5FaK1w1vWmwGnuHw79JA7aCUIY-e4WUsp3oEjvl5jIgmsGfE_TzeawF_OeG
  Zw4P5Ek0NXfVBYDQHKMPoYH58SZ3Jyj0UXNP1ApMPUZFgbxENfpneAwzqnlWXUFYu4df
  Fs4FLX9zyBDRsdS73qAZZpIe8_vtMdnHyRf0NhFxHXZrWInReuoDbp490SeAPI2lwD19
  AZSNLEHGfkQ90IJBtHMQYaTw3XBaZjfGvNH8nB8BOGWqnNgeIkjj84oiQGZmfXYOLx8V
  tNz3-_XrOWwHz47IP67FRHwCPKgPcnty9UL2B6eLpnV_9Dn487pwESVXJW1pUZSOk0C4
  7xuc
encKeyType X25519MlKem768
pkE
  LDlJhENyVToDWclSyYcaamqm-AMGyZfM04FVB7Gk4UISujKxtGTNJ9IL0EiEy7iGMjai
  _hFlTfZR-WkJZ5Fyc3SSlndE-MJK5CIpM9sT8aeKetJ60nKzpoMI_xIYSQC_eWlwCgW9
  qzs019oOUebC6KOJMNhitrRY8QFFOds_TlouG2NxKgLPK1Y5XnaIrZGC9SWEVJW-7WMj
  -0iWrSEGibxn0RYRR_o8crt0mDMZvZAgGgGaQuRfUueUDtB4HNfBkMgoN3tPhvxwytRX
  qIQlB-opY5dgk9lgVLpEGXdN5UGkZZJHN-nOU2eD1nMqFHIW5hd6gEUyUwTDRdiX9ppP
  uwFdCBFbVJE6Gip7qWpK2MZVVJIXt0iRyfB00apPFsQ3ffdE74FQnCIDILhR-OI0zmbA
  2fNOEviXugeJZdTEyRViJqh8CtsFnjEwASxLxTQQ2kROE0AHwMAbK3Rq-aGciRmjkmFj
  cIFInAyAPSJxs4B924qV3QEjAeCvPdg7XiWcelC4MymZTsDPoJYMSAFS9vMdL6ksIeGa
  NUM_07rDh1Bu7FRiCYCO6ncP1Rc1jsYdTftq55uor0OFdoXH0DIuwOdVg5BnixWU4ctS
  bgM7hORDH5M2AERFFPe4exgcwgKi3BFUicySVrsRrjrAL-JP5GY-n-Km9tByCQRH0xCD
  DLIVa0pjzYGCi9cdnLkwjJIdy_RhUieIDraW78nAC1kcliWqEPJxVfx3LhyX8ILDocXC
  TKERjCUAtZFa0sclFvwB__p0Sdu9qZNWyCUj_9g5efxRG4aHO-EVHap608m6J4SZuQLP
  bBmzDhx_ixdvrIZjXSWNjDVqpPl_J6EdxCKZUWcBfAxOPNqvSHAnsxa5fuFbMLgbcIKX
  gmPNDRgb5yJJNpBC9ElxPANAQzgSxFJ7mFO6X3cYqPqaAqMDWWgrx9FBdxZjzhKkHKVI
  RthZM7mUprZsLLCrXeim0Uh-MMwhc9QafKg5I_m7YWYiEZrBFSxyErFg43NpKvQE0CQz
  BpG3ATYD-eAXfKKmj2wG_9SU3GQrXMTISNRRXDSHFUmOivV-A8QbYFkLZlGZe3EX2EOU
  4xl_u3WrB2PIn8gIlcCkhSJ7t_d0YUFJQRxw8vWDsLqD39usXJdhLCoI-CYi1Ay3HaKw
  FahJRuoybPa6tnKx_spngaHGIwOayalmyalRIssG3ll3k3m5NZhQ6nwsSKKj-EnCEAkl
  UnltTPBqSZlmZYU93XKClQdlWxOxFPUetpdgxftsGxxv2QnA3YhkyseyBOBaY3rJagFL
  ooA2a4i4-hNt5KRZveDG4jGqiSQxvjNDDIHBHWMftDonTnFTgbQDIzHMYfVvTWnDDna7
  pOEJWzK8FJSgBaW88tU8X5sGlYNOxPSD9ZeGZGJzxRAlwjfCjVQ64-aCPjUJWnhFtOKx
  mscQKqISe1ui_CpTnlauL0Gvh0pHlNzFPxPF6jHLVZE3DPU78FNnRXwVi_COqVM9_rue
  mamWHZshksI7owuMVYolTmud7uaHENqLAbodwGAvSuQdbRAN18ZMSFKCAwtBcV6TArgC
  jxMta2YeSPbOuy7Q8p1TRYfghQ3pfur2LLUQb8yYRQDSIsP_hb-ON7AMWQ
skE        U18eGAUfzboX6GC7iBsTD4kOqA9pmCX0DH36kQBZYAA
```

`pq_bob`

``` text
id         did:peer:4zQmZsKmffnwYVbGLb6ZmZ8gkgyTs8D76YQRBt5YnFNK4Sno
longForm
  did:peer:4zQmZsKmffnwYVbGLb6ZmZ8gkgyTs8D76YQRBt5YnFNK4Sno:zbR16eTfJ9
  9Xoc7v6yvCwgqpXiUWJ5RMTAWexrX6YFkXodM2wkuiQyG7iqsx7tm7faaHiJL7W46nNv
  6V4cBFjHEX93hCNheVmzujcjFJCo1JAbzfmXvrobaNqAaRgddhcijygjPg6GGgRVcu1j
  vwSaLnNFH56AsqM9cLAvGcwikP16rgqTujduji1CD9ufyqBqFt5wk2k2LrZD8XBZSs6D
  S5i1bhYLKP24dj8EGsF4UHGRyGBoBqy7tDWKSt9c7NXjDmrzfcUdGXEVaSrnGsz5wAr5
  WwrxsqLRicmR7H4n8Us9ZUHsQ3aVRwZqnBHVp8MtYMR6fESwFDfXxgvVfBkgxScA8HrQ
  B4fEXW9MKHjrybocV5QRXgLLZDPwzzCsnZ1yPu1S5SNYGvwfwVMwM7CTELKfGUtD9bhu
  cX2EGJte68Veqj6hegxmJ8k97Cp8Gp3YVMRtwe1pXeqqC74noaMpAxS8oPvULqfWnsNw
  ywmgXB2oS8Frh2ey8xoYNqA3ReSnc5HJy6JVbRxyCB6Qap684hcmo2BBRVwXnNrQdbeE
  NpiJBkuyDD4QGg77etieFLXTR11mNZxnymrSfX5WR1M9rr9eZD7zQir5tF9nfCbYxTJB
  cKV4Qhu7gnHQk6h1oT8kxgHoiRCLrsABmnFGC6wB8KJuM4KxvPqX1cPkYi1R2hAQpfM4
  Fk8bMUJn6GGCdeB7EuHq7J9YtBmHtfq3Vyoao37nNQhqfoiAD8JaFsmbyitAXzKQpman
  zxH14Z1eXKsHHMTb4rMqbdLNY6WHpwkMu4K9oVdU1HprvF2v2vJgimbKu9tU9D7Zr5A8
  dYzQqJ3qQE7eW8byPj7rFGKT9EFvggmhehRxDZumBS1QX1m1TEztm4QHiNRKrftqASEH
  nkz2ibtm2EpwejRMAeMt6yyMGeqAaMXZ7g5j9SniK1cYZvsZ2rbUr6kFTugJgcfzqE6v
  oGHbhxyfXMRvgvCunc57MBGNZCSBPGuhxKCwWquMbDQ3CjLGhkoNudXsLrZ4nCz86tjQ
  ZDpiPupRVpXBiLKmVbKVtncftaCmeCgB91QYg7Fr2wRJhGKcE2JrLfBS4woeS4dnUV9x
  UijmHUNh5Mnu7M32YvW5BNr8BJUP12uSkQQEBeuAibqwirQSpruYk5Q7vxbSuGM8r1FU
  u4CWEserDV8LPCDAz8QxfsG2mZm2APEUuwNhgSRdSu9ZzLhSaCFdio9EHSS4sou9BX4L
  ajCkV3CDiFR75pEjKibaktg4Rh3QiXbFo6sgNUF9PQmrL2Wb3NeA4pTfL16rjxovczdB
  236XKNfNgMBe388de5thMSu2PQVAzN7YzqxxXurXX3jKvXPd5pSyvhqFQxwb5fUoMju9
  9UKjmKksP9NCeobiYnAxYCXnPc714iAzDxD9o1u2PVSgkYn2t4SacfYQ4Cpwr42psvre
  3EzQrgHSyAnG92nYhgWhnrUV4c9WE2gxS7sNC5v3s4ZyDjaR4WvYZdvcbg5sd5pCn2ya
  7KwPvzQrPacgjGxekcBW84JrjCnYic5xZVTKVRdTjmAAbgTDfUZfSbSkbzZ14vjsheNn
  9vCnaNkZGeqf5kYGX1EVPv3Q39A5YzNrEnCMuEimqB29gJzxqm5cZY1kyjnEA1wvmWQ1
  fWbtPFYSakNoNyvwX6viZdiPJ5LMh7gKeeUwkQz5UhddcF3dXkEDQZcfLofK74W4szty
  ttH8NMKwyy8e7KTtxBFqtZW6VnTQY17571V7rdGHbdzQk5d4UENq2rkixsTYxuf8DiRJ
  aVJudbHPjAiwKEwk3r7zfpfr8ErtvmGa9GhCSmkpZfRhHqBDCde3LSZmdHqEbeNLukXz
  C8yc4BsU9GJg4rGSCqRuL29ZqwvdPNc1nYQ6m7nPKXVJsGAav2WYuGiBemMjvs6rMMtr
  pR8Q7GPzJAm6j9SCwQ8V6c84V9YkyJka3GFt1AyqyrN9h1R6rQo1rgXu4Sm7VArd7JPt
  n7354nAmBaRGvo7uwJkNYWFLHpxFVFTVzyWkCcs6GsuUEmQh2gdquHdQpeGpbaDWYXfc
  zqTf9DhrGrb5fByAHcuAsGu3okYghuk6Gveg3148P1uEFEtn9am8Q6m9bq8bAwJisMZv
  x4ESFQtPfZj5k5sqzx3rtcGQQVaoiefcKLDV5VnNwH3wui7bSuoo6PjXG7jhNdWXdiLy
  2RykzE5kURcjFswy6zkHshaFxRqzfYoof93cgrr7vnuKSxtWkbp1H8FKvVNFrqQ9omRB
  x31U2vvYoThvGgyAE2QEbPMoeVVBas5YJygCMdSQfvsuviWc3dX6qjP7yLj8xVrSxUb4
  DWL9wLAL1fjWjAt87cHtze8KJPEjzDGea5WNPYBMdnUjyovm7UnVvqkp8JhrJQeFCyyM
  rCjJTCRV8o33LQQy6Qb8iav7Eo8jNAiHoFKK63na39cZgJteMLrVDNxezcBN1JWvp4GQ
  DaUUjNCC3y37B55ac11Tx2UZ1YV3mosfnFZDsQuPdPWTNL4EwWcHsTx39QfRgKdY5JWF
  2DSWhbtPyBkXks1agxHrRoFbRK6ceNSkro1WFFFQ8aqg7D5J3D8FkUwBVMWGaayaGdZR
  wSK58xgdV44HuvbXtyY87invGMQ7ppEhV13xJb1HfvxPyVr7JCMAxivHUTJnGyababUP
  2LtpzURf4pUFf2tR3VExman17P2LXg1VEVQ4W51i6Kv3ia6rEJG1k51BGuXtZfaY3MaW
  vbVJWh3QV2zKvffqVzokLv5K47ShSebPK5h5ZHdssQ12ZYzCypJYEaEMaaQ1iLBhL9CF
  epvpcFeH8qSDvMtoZu42iHxf1tsMwFcWj826Yd5vg4mhkReZDCgieGfEnBGFQRcDzCsk
  8MQhDKsN8XavgWzqp7xCo1LYsVwo5KrgXf1R9vew4t5msP85pUvcpr5G55rNwvafXB4R
  6Xr7YvweBRSe8D4QvqV1yvEDdG3B6V7MuWgKgiytneNsMDejtwMMqkxgitocWt1EomQn
  Gvmq1kJmBvxYoCBj7Moyu49Amfic6WZhrvUyV4fDYBsCcjUMjDRvEdn4wmptPnjumvrb
  Mx1RT5UYCsEEvRrbe7mxL6y3ohy1iMiEeLszSsGyKPcSCerMaTMZEcyqyo4UVqFCdRSS
  w9R1SNE2aV5WVpmoyCETkkY6nVew6n5bdazECiCFEnEXyZpUc5N9LFuKwmRDFSCjj4PR
  5Ddb1LZAhrA3FQ8JEqCpfeBbvSvENAQf1Rrb2BuRJjyFipyekQdTU38fMznAtkKLGDcG
  HMdDuHetTvYwjzBm7AnVfZQpurJqrYEhhwfQyyh1bjbbDEGyK2s4StmKD4aBKmxzomTd
  Uy99MQcMP6FLyxwHc1wXHcHENYMA3Pdc6KNQaEQvuTquM3HArbti9eRN1nVFQZ5Fbt5V
  38hYyZoH1hz1bMBH7MpfqrctxJpT2X7wYMq3ZUxVT8gY2gJ4ZFwbCgt1H1v22hyt5jPA
  XSHKE76zBvJ3gUmHEsktWssTf6isA9DnAF2ujdaiTs6ZzQ4tKvuF56CAEyWgiEMTiEV6
  oBrBvn5hc52iicPEBgUymzJdnmNQy381rNExzEP7CVnBLuuiRCoVKrhrW8MwrupS4Xy3
  JJQtAouC9RJCYyjUHTSUU3oXj993Pd9bQBUWhXmLUmhDqYuC9DWmuiuRMX9YTTmjdEDj
  RT4ovNx7zUgKcSaGxkRgHfS9EikjKk9cCx2u6vaMkQMU439f9vgXVTxCxHFsm6K4JnBp
  78sLE9tyFFqJWxYakT7s1o6nYGRkPWFYiqzQgmW3pDnenVRdiCvyUjhvXARm2PMjpuDw
  M9NFCNbJGPmL7ZSuFmUhFHds6pS4EeJKDzTWnYhRUJmvFEZYFJ6gj8YJoZuCbhDAg68N
  gfM9nMv8nDpuqf3W1UH8Lojb6fvrXzT8adabKDwSDnx1VYCa3MRoG1SY3MRituEtq8wD
  ViF95NzAjZT7kGQ4qFLyTKVZhKcVFNJewJGCtMXXPSWz7ZMozzes814La2vrjFNKj6vM
  V5php93k7PUMArpC3BRygvNZqf8v7xLFrZ4gjJ9BhEGsrrxHVTu3rTwMbczJhiuD28Jt
  ehCpoqv7mhuN2aexiHpSjtmSsrKHi8MsqfQ8vEnc1sEYxoajhj8WYghsV4n5Bf84cg5T
  XcyuBSy64Y6g83en7q57EKzpczeAmcR5Viief2QLt2NMyGkLGT3QENQdYkCSx1WuU9v1
  3i7mLoZzeJWz4YQ9fy3249BqGvEP8jCppHkzXXa574R32EKfcZqgLDy3MM7GCxqQ51JG
  CPZhX9qBYEkm21JbHG2gUmxc5ysqsAarUzXoezwzBLcwK9m9VLbgS2ddVLmxM18fVofH
  WnBZBcdqANAvzQgNezfonhvW5acbC5i3rxFufoJWQE9Lz8ZVqDk4KkTMFHdxfmC5XZj1
  17kSbmxytFmeXoEd7eoxixZctUgkUQWo3YVEzQ8vvTGSsy3of36TiTEbwFEjGddTLSHy
  3RNXnDt7siPHYBxUKPyVnBT8USrrwK5zwDu3iAV8F9goWsH4SHSxGCLNPkqDroUhMSHB
  nDrFtg643nPBGWXvLmuLghZdCBG5mb7YZpAU4Hz43AY1sd5W99LnBx4ZHYhAWfW66Qe5
  cvda4amCqKFeZx9kN3Wbk1V49CArQbg8VevBaUnEUfAgiJagKGXc1TS1sxqiJe5YxDHS
  dFKiAdmuaTcHu2gfo6AauQX5EiQmhCRX7Ff5mcPXQCasf4FXAofVeCZycwqB5SCqoDjf
  CYAoJnpDejKDsWHwEA68DgNE93s7gs6rNymfWmD6iFn3Q96sEKBaSbqZJcM4zXhuUooE
  FndykRZNhnqB1hVhj2AJAt1Ap6TEQfBvgrn9LjrXapveAA3ueb1Mu5eCCEuMZFnxTZQZ
  t6fiaQf9PrKTqLrXxN6NpyrXqDiepNJyYgJiXXZX3Dm8M1o5bbHhTXJAsaFgm9KoAkvz
  FQBP9bRTVGds5vDDPiEYEhqqCagLma2u2QQAYWE1oLhGFMSXEq3aqfeCXtfqcuEardLy
  jVCevuqRWjwc2gGBVd79Pc9j58rkKzA7Zqhe7H9hzyduhNkvszthinP2eptxepxuWmSb
  zWudcWDfE7nUkZwqb7WXEKKTKoopMcKuGStsHhr4bCvKx7YT924m91EWvwfFvvQyKvsy
  MXFrpp7h9YiW2X8N6sjegEYDMkoc9asgnzYwJSXDYBP8QPsE1yFjoSza3PPecuTZPxfH
  c9JvVxrXLTJzecJHFmyoaLsKquK5kT4yQYM8L9U7nnzUrD6Rkm4qu1WnJfQE6Pbwphzm
  MxSQ7NTqj2dfdrjiCFxoHUEBacPXEiNywLJL9wE9KXYfMd6Tq1uqzmCycjFdD3GLTyB6
  C4JZ3idhwEhqkyuDTM8zEPgACfkd91WBYEpd2B7CbiHKPqQdFKk2eThNDFT6Sfuix8NT
  i7HRfFfy3J7JAamtUfQp6P5zbgQvZKMbZ9i9e4KggPPAh6WMuQywNnxcVFhrUPGf1HAT
  jFPqyK64udgWqxPKMmBqkJANFhN6DUfyqfbGUp3BccZSggTZeY3EMkSp5Zxxfnvk2cqv
  Tkxj4PzTGhcyJDDg2mLWhV9DeFHwbLYtaxhm4uowMtHoTtuZzyQQgAz3hy3as7BB9x6Y
  nEhxCB9pFnedQo3fU5bJunTb3b2iSPSWbyanMPhgcCSWw6WxAH3xbTzGGH2mnSyde848
  skCH2Y2aQJ6Eni8zLUH5AoKJZVb9LdMKkQijNYsu1CzRb7auWfLqXguxCRJQNhjqqsN3
  MHmvsXDWZoskPxwp9WJmfeWTgQYjweZKRXEwhm2K67SM1cakQcYVcyxdYai2KjYiYQ68
  S1qrHJzvrNYvH51BBWRyuAwx7tEGDGTrzot4XkpNtM2amtjBkAXPuqcRA8a4GPRjCcXM
  EWLQDYBFnghwfr2nbiwMtRbVej5CrfWjpequskuJ963HRw7SoWTZMSRZSeDNRe8kPMMp
  erphRzp62LvED1iunyURaU7MedX2AkGh3b8h9y6qkjQivgKrfvMp72V7WcwhFuWhXX8J
  q5NA83c6eGmPGyswFTWjvqVpW2KtRmQWsjvtpNHMVxU94ogePP96ox6P5sVuNvsoLx4G
  qicdLK8dk7anCqwLPzFgWg1GmFvZU7oxpuruTtvZaehZFbKkP2Bq2T5WgAQPTs2fkrz6
  i5mrCG8CDbMPrhxVsijC9pJuEwZbibEGRBN3waVN9uCui8waPDv8ST3TsRSYsAZAxQN9
  cD77ax2QSiTAjLSNUJEsJKpc2WUzNpXyWbr6aVxavQsT6zUVTVBKEgrWV1nB6xa7YQCj
  sB9SrHLDHua7ASpbHama
sigKeyType MlDsa65
pkS
  E3fHwPPFvz4VSA_VgU5wZEsUlBUk8TgMt8NVYFf0MyDTsbWUhMbwZgals8GrGYdy-WRR
  Rc3IUudHYAiZonL7XjueeMzM-WV52zZOLVsCEk-G2ZsPGXSfNBGa1B6tVKV-J_ZvgMq2
  H7_gBcDSeWEKHNbi8B0Pqwq6eVI_plXTkkb2lnyhzhzt839E5_dUBNvCXlvQvqjgdRla
  RV8ttcy8n9XrAWiTk87-79lahLCSP7rrTGulnMbv2V2jffRbwyDbAJb5lb1fnh7J9FFK
  L-LvbmMUN3TTsQvdcSj5UZsnqb7O5FCCKZDvOpBdG6yk9DVgc0Br3E43PNAIkNHafecp
  vG3jTphxAO2Vwe0W13Vwq-VcAxdY1Gs1aJJSCROY6j8LeJs26t_gBcgYndNQ7-2ExZlK
  2nUdUAtHex-73NOvWOf9CS5diU9Zp6xDSN4idQyle5LxgPPp0zzFvckKI1pE5r54S4oU
  f41sxzzayKkUebhLs4gQuCKDnwI3hg9EFaM4z1t3hXg57lbrk9ZlDeYCEEH-597a-Bsn
  OfxzMpiNuj10FMD0u1XLHA7vHm2n1R8QpLfEc4Vsl0gWTUg4zg747Yk3oyO86-sjh6s4
  lwJWj-OXIxk9kF7Es_k4Sz9Az8BiPPP7MYo4XKaSchqEDhMUxf3TsuCzLHPLJ1Lmk3Aj
  PphJRVa19T6n8BLLbzimeqTD2Q_1Df0j8LUrL364if98TJuXed7Oxr1ZBFayHJ5P9ci0
  CXe_tcgDag8ZTVmBhldxMIsY92OGvANEyxqad89tco5-11O69TRIJn1I1jSA1TWfCBYP
  kQh_uBQWe6llkSDIg1wI_2vd1COJCHkYSO7TdgmASEai_ATmp4ZJ0bG9QafDzphcyjRD
  uTNA1EOFGQVzN0_ffLaRlZRXmvPoDTvuLzpK2hxqkikzg9r8-GunMiXIlB9RIfuABJu-
  7iEu2LqXjyDOMXz53ghysFjo4ntpZNlliphGA6Z0-RZBW115ZDUMqJ7n328PWm_hjCmi
  ImHYBc3nOR0MrnVHGTKig1d1DonX5-Qkd81aRpN7_mvvJGs7EWijpsXPjrrpPbarOCJx
  LbVB7idTUFZ8YeJI-p4uZRGQhnOb18XRcs2i6nzHGAkGlt1w0rbf6wLDXlHUiscE1PVX
  pzeaG95oTX_fEqTB6SASxd3LFmXhAjio1TS82IJmZtiu9XGGaNpxf6EptCY1H0PCriZ0
  jXMMXcw7c1dytTmzZzmBzdfse8kqZLOEcOjWn8LYYMCqD_S8u9eLlPOIBEjEkm5KCgat
  x8l03o-qCiAe18YwlW1HUwaVQHlbDOffLjuuOmfwNEEVZT498PejsmiJ-I3WolWYmELm
  j1gIOBe1dsFYbTnF5WsB8G6Yeu9ICagcBbRbJNPEmSweL6LIEq-W-dazqGrSF_P8YYdC
  IM1iB3k7VC_oP70_Zet_tdMeOKzNb-C4fcly3WUMVd_DqiyzzANd4JqO_378znOYZF1X
  WBdh2-VIA1_NTa_I9CBFgJDZepHJnlOPbskq8qc61ZG_WXz7MmdJe1QK8jBFjarJp7q2
  8h4937gjoppnWSbvQNSwnNK3U3QnyT_HGCCepTfLgHU9mNEQ-Y0lBwtLprrOR7x98Lfx
  QrtAQ8XhsKqrHk-k4o5T6QcmAtWcSmGXwRDIGDKT9hjAWI1JtDer_HDw3_GJDpbxUZuh
  bVniBaDOjSBH6jHUUUJlEnbujSzOdS__CLwehEkbJ8o8CAUcfE1b2D9netchY7w77Pfd
  g_DcuI22gWWqqcSVshGhG9aJ_RWG87RaxX0OCkKek1JxSbSH38KdrbxqotlLoxJbRgDx
  AxViEZYUBesBJgomnFgYTpdroOU_lwWv97s9FDoVa-dU1oTDjfrEDdkeZNvZm5ZRF-5g
  xx4zBytSdh6favFK8xJPCGGrlQcB9HGMDyl5uIgo8BesLnyj-ITsK39RAbDPUP5GGGCx
  cKNSalO4kwXDtjvPVegOuOdbu8BIyVi43ye-YcOm6b3fuXD3AQ6w-GuVwlJifBtAInau
  wP6MKXg3jV_Lr8QCb6oIKNpVCL93dJhE_ldoJoVC06NL4MLNYkkQpmLN-Zxc6DBn0z3x
  0rdJVrIEUQGXurHMW66c7v-uiIGLexvCd4O9lKm_8ZApB6hYet7MPkAXYBOX6SEnpDuQ
  RghZeKuHOlpoi_RBBGlHcy6qN-w4fu_-P5RZk6A9M7XwE4qu4W1gtMdmZOpZgX9T7KY_
  L39g9VoRpQv1SqfOAn5uX2ZRM5zatWbtbcgr4ZwHQ97BPwIi2KF_w4JhWB4FfzQufjLk
  xp-WPecCWr9an98mDhwdPJr1-_QSQPjM-ZOl971L1kVT9WJPQc3ErIHQHZwXPvD7wjLt
  3cmHVRdaspKt9qqxAWBmyZs4zqahyEgS0Z3Ds8DZXwDT_xKQFvSwR3FVfcMtWLs_xCCm
  IHKkxp8myRpXS9WOBwWD7am6-isL3EVJXlmyS7IKxQlpWWttniwnMpIw80ujyAb9EZpC
  UkCFu2DpWzEd44B5RMfFrDNO4uZaiyFxsZJyieKv-zTtQs8BI3WR4qdtV2gTQpM7xn53
  bzpSbBD63emxl6Nb9mQ
skS
  E3fHwPPFvz4VSA_VgU5wZEsUlBUk8TgMt8NVYFf0MyCcFajzHL3w3t4tiA8DnPHO_Lie
  tFcKL1Rn8dSJriXTTOsJwQ2uNPpvZbnxfxBVfk0x7FhsZIsUCMc-M86km5LsYgBxOAkk
  R-QtJ7K2LOoiCSPFYTgZzwQD45C7gUlwg7NIhlBiJDFhAVOCVzIXMjZyQnhSYAUBZ3iF
  OBNSUAMRImYxcHY0RSiERAdCEHgCEBUHg4SEUiAXRmGCSHcDUjYTdWMDcRNDiEVgMohy
  A3B1hmMgIhV1dgA2YiN0JlRkRWNRBEE1SHMkVBBWQlcRdSRVERdVQRV0SBN1eAJkQYck
  UYRDEFFYNIdlgBEzFQNlMVGAVgYSOGgmNTIIiCZ3MDVEhncVQjQ2ODVIdoaBF1VoVxID
  JCR2EhETBkKHQzZmR4MSFhIhYBIyQVeHNzhWdoIzNkdUModxKFiCMGBUFSZCEhIjMyVl
  MjMGWIUBQQd1FCiFhFAEdYdHI0gSJBJ1Zoh2ByRBczJFZkg3hDgXMFSAJICHMEgCOFd1
  V4JEWHdhgBQ3MlJmQkdwRAUkADiCIRImRGV0FUGFcheIIFVTgnFQZmc1NAI0aHU4gDch
  c3MXeFEUNniGB4FBgzUAZ2EThjNSIRRERSFHcoVHJiBIASiDd0hmgndnWGV1EYdBcAgE
  M2F4MBgYZCFoUYQVZgBlc2dnVkFRARYDdRFVABUnYSMTRzFRh0MDA3USUIYCNQhwRWVx
  UkVXF3UUYjAgZzU0dmAQEIOHR4hhOEgxBgMWBDcXUkd1CHMUAHFAVXSFFYF1VmA4hDF3
  V1B3cgR1FYSAdyhFgWRXSEECETdyNFJFc1WDSEJREBUgMEdEQAGGJDEQVQiBVCJoUAZk
  MEIXcogVeFEQN4NHNjIneCYEASI3GFIyBXYSBVRVIUZUeIczESVFAiEgUihoUhE0FGBY
  RVAzhjFngmMDcTM1QlBDZjFkQoKGcIhIR3IQRIMDeFSAGBGIdRJxJXB1UYc4c4ISVFJl
  BXYQZQOBR1AhEkCAeFJScCQzEmIyNTJHMDAxOGRoI3QkcWYYExNBASGCAEA2VFAxGHJg
  KDN3gVdiQgJzKBRneEgTFIFXI4VUVjNQJjCHcIdkKHQFdXQBKAYlc2eANGUlBHVoB0QS
  cRJ0YAc3VTBxZ1EEEiWFGAQwNmNUFSUQdiYTJXeGJSQBQWZCCFeFYSgBVGZQUhEXNAN1
  ExYkdHRjAHUYF2IiMGViBjQTRDF3NQdGU3BDWBd3RSRyYFSDE3F2c4Y0YDgEYXMDJjeH
  YCURYmgmIQNnSDQwFyZFdgA0AhRhQnIkIUIRSAAQVwUwZ1iCiBJECGRnY0IQQQIGEWAA
  UCcDaDEWIjZ1hkIHAUiDiDIxYHQHhgZkMyU1iDcBQoCBBVBXB2BGQTYIVmeIaCSINTNT
  cQFANFETMgKBhShYAoZBZ4WEUxMFJTYRAkYiECIQOCGFYwh4gwiHEjA3EBNGEmVRFTdl
  WIQIZWYUJARjdxIhM1AzIFQWQWNxaHQWeGFxIWaIYHglElQzNQVIAFIyQyiGaBN0goFD
  BGcAQIATNjB0V1E4NlQQVxBoZYBAgYgCIDQCNSNyIlYBUCADCHYFFwYzYQIwOHIzNmhV
  RWA4YDdihDFhZlVVZQgFJGdoiIhVMQQ4ZDNTAggkJAEEKBVwEXSAMWYlRSI1ZTZ2QDVF
  FkVUcyWDFRUScocxVWBhgIiHhYVwSBMhhwiHhwiIdRIFcVU3h0VRQwKFhGJ4NlGHhDJ1
  JQIgEiY1GFhxN2AIAEOIcDAFSIJwcmgIYIgXdyNDVXgWBwFhZhF1M2ZFcngAM0aBgReB
  VkEHh1AjcAiBcBMyeBJCU2JRhWd0UndmiFFwQgRXEIFoJWQXBUZEeAFiQjAjAiJhZGAT
  IyFIJAcYAyIoIYKEQII2MQFkMDQXI0ZSRhhjAUIRRCeGgFOGBGECAmAGJngmQXYTJSN2
  Y4BhRYdhcjgXKAdWhCIDg4M3CGJRQIRXdBgVEQURFFVmNycCVzJmYhgWE0VSJAVoNnZy
  hxNWEUcGPwOZJ5PpSe0dmUdmL-i4fNu8uQiOIiTy5QagcmszKyUsQ0wlvrq8XugBfeEB
  AcTq8C4JxlYHw2gJfKe7xEvIDwN_-0RT9BEZ9ie-Hn4LPnNBD2xPzwGYmflfc4-q2Y1g
  VPQ6nW16Hyy26dY91s5Pf5v3XWVDlpSKn8pAf7iKKle5o-Vasmtsi_ySIETw6N4Iw-Os
  Wb48vwQdQcQEL09vUUxkGoodnfoA751RtQ7aSkyZix3IOlac08Iw3uMvIyK9oKp1xpL3
  Z8wN0GJCAKiV-te8p1_B3HgQgMXdm452_wcGehu2ZdYkyWEkgZzql8NALm8qDsn8XElF
  KhdtMiCTpRLkgk_pq_oQFElY-FolMaLbQq-tEjF9vN0EbqFzg0G30-WbFrEj75kUZoHv
  slCyn2QVDgCT66AlIEIc8TWIm6L0V3p2pEnSGeR6k27sUT7IDkRl-EmlcHh0KQsnWpZX
  8cYw--ZOX5iM3RpqMvlyAONuE3A4cmBZBovL2Dh6urXfrf48Er0TTv6k80L52M4tX-s3
  1aq88ExWDSs0BO6ZW-MwI21LcHvE4dlwiKFcWCJrjNl5M8nSe2D57xrCSYWXd-QJ6AER
  0kacN225v5mbZ2aodUFQnn93yB6kd-nPkceEKjMtpEzz_fz7TliJjDbfD34K9p0Qixsb
  udU5BaKy7NKETjTIp68wdygASUJpNZHhak9immFn6mIp_d9jHZKtkKQ2CuXlDgDnG_Cw
  ejxC3iZlg_-Ba0hLFDiKi2vPoO0CueToCnCsdRi3MNpF_FKITvH_mxzZHZJ6kFJ9kzbS
  11R6ZrAEFkZ18OM5z98X1U5xqmkEVKT5_iJx8Pu8fgn-8o8WkbBl96goiY3RKidnEwKR
  h8ENFfTocH0qbJHDZGfyUVioZxUpaQ8GVNfsUEUmcr8eqW6MNrDu606y54c5Rw4DHywM
  EvklG6nLd1G3u30QMmmmQ0u1wJG9TY4iFRUK6NavaudfMRaYXw7zHMj_SKzNBNgV5A4w
  iOvAsdlQoRo5_AKsDkdTH6uKdaKg8EYbjVIzEmghoO9p3sdW6s9UgnePioFPQE_HeI1w
  E5XB6xYERaLrMHN41qQvLeqjbis6cIojg1gm_PEdM_W5G815b2Xg8R2psr1bAQlRyz5X
  Jq2QkhxPlyS5WkvkGAcU5DqtUOSt_NTbgdqV1eZ79Tvp9_ZbBzSPDq24a7StrHf7FNfo
  oY8J6_egZvP2TYGtwV4rz_QNxI1Dzrh2ltIlZjjLWyPGCulNsf9_YGacEomwK3wERDYM
  IvOMWyCb9K8cdi8t9KqpySnzfl2ZdMSFGZ_YW6boipY3LvIjCNUtqEdcMAo76aD-UdG-
  dRN4kaPpIdbtBTKp4HS9qHNyk3Wznpco2zj5gte9J7RrvOlR9OuVwDOm_cfNSuY6URpn
  kdYbSy3fKyMUQ1tQWujbSd5_fpyDXbsGmdY-zB_zWEhOXScL2lK7KHgJZxJj_G9jjk8R
  o2FmAicUK5Vd2MeVMBlke5bIgYjtUgMX4UkobSSyGMAbid6e-ErTAahWeGxoGdC2Lqcg
  JxKGAhEZqvMM0DeUMS4gZmdEA8TXqAGhodTI9xNFecDZoN82pC-QfNHnb7GZJulCgHXL
  BC-AE2zqx7PY5y0Zcfl6sPrFYBVTnixewwAXes4K0ORO3SO2UFEi0WSTVkMjj4bzZTwl
  hQ3VV2c1FjznmOCbNJIJ8TWaivkUmYrLCpTWf5muFQ5nMMj32AZ4WP7vmG4kJSiEShPX
  9QbeFX8_lc6m8XXpd1-9YTGYSRPukYoXUJg9twdx99d84oH7Sth5jSIfSYs2SDNfYQfu
  0OzaEkRBhn7pZSPtTR0KaGeRQy7zdXXAVp1dA4aMuk4a3OnjvzDcBaE0h9uYOA8YN0rg
  HzPzMe07f6zUttgxYyW4Yg5dgCknKlt0ocImI-us22r0guisgLuk7efZnPrQl-Jj0pVV
  ituB4g869_9l7_bD4SVynhJoJynGmtBF3yITp_k5LRbvRysW9pRlYFVchWO-PX17ErA7
  gChnEiTw1IFPMHZiGv5z1_WLq1nk0I1O9hqCmH59t8yOMMbpDMA8eCvDMY-mdg2f_rk5
  RRhrUCWSps0L4S2OCLS3Cy5ZS4732itmBmvnRWCIOk9rYQKGjN67xLBqAfl7Q1y0jx_7
  c_kHMV5xbLE6TEXux6--LyZHWKEF3OCH81cthgcyt0yG1UaTp3NEI_v5aWuwUH4l4UsX
  CcJAwiL9Ed577GNI1YbC6pwPOPcn_8hPO-BdwMW7sAdPTgeB7lKUTT4unvJT_Ie76Cmq
  hathL67pDD-rFQBUMYjcGISyorczAdb2dKN7-MyvGuDpb9ZfMM283gRNpcPEgYGzTtar
  IEEVyv9diHaIFKjd5nD4ixAqJKBYv8CUOUpB2tCpXyM_kss_HdO8ovToK3QPuGilavKS
  OgZH1gT4IQAgECb7dMDJ0AwtHVlmme9Orvs4Ksf8tgmT3R9mKWaGFRqglAuTSyOVELXa
  PVCpGPBn3mmpjSbZLMWFwS8Q5K3imihRMwgUtoqvurrUy6FwnbKOwaPszKo6hmH_9OhY
  7HXD57Iefzlpd9nlc8seIcrPBY9mBlFOmqIYZj31hJU3Essq6RtzU4qaTREaZVHMTP53
  ZJzG-bVpPMjpv4XrBPgxfaWyX7mmhJXZlLTseZAm5bXyJ_SntA4sLzxXWIzExaaef8lN
  0aqsoLd-lA4mw9W4g911Qin1oWmuXIjr34HoOvGUek53jf6unxmkwc7epNWdxxBhjWmK
  ZzHDglaJjB960hECqDXlKUHGXnhcAdV8d7AF-hg6afLXc_hfi1n5ZLDArmTK29Q6VEz3
  Jtsq6U6GdGDlPVvG_aZqCUVbFuP9Tj-dROMEXe54Iz3oF5OfYQYoicWTynEPXHvmv48E
  Jq-vtY3tMFutsKNKKSGkv8POR63-zFUlmbNueDjRxhRuZ5VYpK5QCRKWi27D3J0iPP5h
  D1KznMs5UAm7OzqssAB_x_VDzhaWpDhsVL4xVuNi4Sr0am_deFivikUpoKUZMoKtVH9Q
  uzZ88a4BGneW2Xe3HonCIo-Gjdebo6W6vbKafRVAO9OGKziRhDki4XZhEpcYksCOQQgl
  7K6dHus-_tsfPVqn0asVptnnE-Jz0_WC23H5rpMfJHFuLbbNEn9-bcWdR3nhgRlIF4Rr
  wLVaf4qzR37Z0GFPX0AJrkr4LPS_B8G9u0Ci1A97y6OfTH8BDknSom7dapD3px8_dzvS
  -vvJRt0fTMfZ9TauM_DtaDbJ9uO8ahZPIKoFsRte2NtzEVaF0jCPq252OcFRv-fi8Hal
  jZkc
encKeyType X25519MlKem768
pkE
  CjuwTpSwD7NFkpXPXZdGLPQB4zwvnVYVKXGYnGljHQk0ojR4nLMQFtuS0ncgAiyXUoaH
  gGAVFIdCnBeLVIuVdlEf0Jy7xXzORRU6cVmq9rF49OtY4YFb1dor56oe5NJhmvWMbGIM
  K_cZPGGbYAZYe7A_JjKMUjB8eHkDcMql4bal8ialj8EZRNsdlkI7wPlGw1ocvDNgC9sd
  gaVU3_HLbqRy3cGAjtLGU5keIBFZBRZ3h3WJDiqFtIgyNMHCRFBwV9ULsNey5XiJKItj
  JFilF8JUCUapMfJwKZg41utgl2pemzBiHUnHcQNyR2A9ljpGc6SAjJpNVmp4LrQXAaEh
  oeMb1VqK6XMt4cRVlmCiMfWNsyyY5WZDArYMs_aSN5TPDQJWuxUTSHQG-wxD7asfzXSP
  ZTXPdsR7BRIlahKfazuSZGbObICOcsu02mldPsGts5VmDTsNfvFQycjGjMGTfhcdg6Oz
  fFNO0iaFgNxM-xkEdUaYKZOf6TVWxurKOUWExDqDkZavQigMr-imb2dWltsr-nicngYS
  Qkt-ZGx6Z4kbuIVx4nuH9ValTBM03bvIaMEjc1U0aUODWFzGtmVN0gdqxUYwyPS6-xip
  zGt3LYY4FoCix8IWCTthIxNCK0ys1MtCFSF_BiPLwvbL7koFzQcbpuq79uOgm8eOJzGT
  iQEmIDS-CPC3izKlvepQbLLPelYoDyUPyKilHzq8NsiunORnD-N0Vpdq70kT4_OysbyK
  JrxE95i4valbYxoHmLmovtgdudfIebGVjyJbuYRuZWQwFpq6oHNJrOgugwl9IeKwM8U_
  8FrP8xeLz1dx_8FwSXhcy4VF4agzpeFLlBSCqMwr6Zmg9DIIpZoFfrPEMBkeZ0An0wKG
  fsWkOlK3BzCgDiBdCwKA7aJgMTpEp7k-apPNYZEnBmiTjnmkPHQuLJPBJHN17qUH15qj
  WTG7LWGeTKazMHkeh1JkKEC_hlqWDOVht_Bff-Wmw2IWaIBGR0wOkKoepFBJSgdtEVSo
  2ClCgoaAZayZneGQXDOUpCAz1fKhx6DAMgUs9zyLOfEHD4xh78WDjlGnrDE_swtkYxQQ
  B4NNV-OW97JicwleFvPK40p3ajNKdCJdUExDRXIdjhmDgLML9KS0JOkDBWdacnFqT1db
  ZaO3r6eYi3UJ32IxukJSCjVnNMhn-5LAyLwjbwwdDoitSRlF9aUE8VcVE9CmGSpP8nrN
  7ykLpEeSEsE0b2IURvaVvgg_WTQoJ0pamDrAWcidG5ZpMTNOIidpqxawNjiJm9dJ1pF0
  Xqc7SdSR9RqPhewCB_yK9consyRuznlH_VAQqSEovJSZQxOHtEq4mGhhHdcOk8GZJgOw
  tuhMm3CPBoOfaUxTeFV3OQwPeAq3GrwSJ2AYd9gLz5IGrGY0hIp2FEg1jOYYuJmxg5A6
  xCuZG6VhWUKnWbya47kO7seKGdmN8UAZ3bOjw4qQyQMJE8JsgyM5nfwVqLrBF1aGZJJ_
  5XYok0w2ErgTNLohapmmDGha7EpRBsBiaOLMgnqwXM_m7jARCM0X6ccg8WDwuDxZndFw
  XZzkIc5zs0HY4usCp2THOwDodeS0VXLTpwYfo7zyF68l8XetCT-GxlxSEw
skE        CDZNS-gKPeJMsblGZC33c-6rrv-JsuuVfitTnkg6wnw
```

#### direct-hpke-base-pq

The same message as direct-hpke-base, to endpoints whose VIDs declare post-quantum key types. Post-quantum support is not a separate mode: this is HPKE-Base with the X25519MLKEM768 hybrid KEM, selected by the recipient VID's encryption key type, and the ciphertext code is the same 4F as any other HPKE-Base message. What changes is size — the encapsulation is 1120 bytes rather than 32 — and the signature, which is ML-DSA-65 under the code 1AAQ rather than an indexed Ed25519 signature. There is no sealed-box counterpart to this vector; that suite has no post-quantum option. This is the one vector with no published ephemeral value: the hybrid KEM derives no ephemeral keypair, drawing encapsulation randomness instead, so there is nothing of that shape to publish and check. Its bytes reproduce from the recorded seed. See [Section 9](#tsp-encoding) §8.2, 8.3, 9.2.8.

``` text
sender     pq_alice
receiver   pq_bob

message
  -EGwYTSP-ABA4BATZGlkOnBlZXI6NHpRbWJMcXUzd2VadHNuTmVzQnplY0NabTVGQTZ1
  YUdrZ0NXWVI1V25kcjZHenpk4BATZGlkOnBlZXI6NHpRbVpzS21mZm53WVZiR0xiNlpt
  Wjhna2d5VHM4RDc2WVFSQnQ1WW5GTks0U25v5FGFAG_gn35RNoXWKshZoo7uJpjoK4rc
  Kk2jfCWOYB5delcb_W29HoRlEL0dSVeU4hgMITPH3cryDD1lyXErM9gmApU_t3X2VMWT
  bHMN8i8YqhdzaUnPWWDqRNtFjChapB_euEuUWFXJYvlz7tyudeTDJxbbXFn5s_fzwvfK
  wPMsvzF0asVGhxKC77xe3cMht126-gHc0xx908WrHrMVUtfLXWQiQmIsnXcbHqPwbHnx
  DWamgaWPkbwjebDDnJGHwkAg1jBz9_Wo6RYymhGpBGqc2L9IsGfYSzy9PaSb22sg5BtT
  LO1vf3o_d3KoAks7uHG7RYDQgarMl4pWZUaICod3MK7yZlTR9LOsnXqkn2UXMyNg5Tr0
  bX6iEIw4bM77HXu2Ic84eF-2DfgXbK2I6DdH-KcH2b2EMmv95kC4WED-jPGoQA2Wd7kB
  NYlbYouQU4nDmmdVjOVvo2AeD0_aDu3cN2nQyINx34ryTcGjG6sfg6H6FYWT6yET7vpf
  PpZlx_cs_qq9QC9d5yjZOSzyEmgQE4a0QVGtxdk8a_Bd2O8gGutWbM5fFNLoPEwreECP
  HIuhuMBXMmIqRS1igha8yN_dvapSle1WrHVy9EADQww4KzR8DHvPVuqbCEKtm5_zA0jY
  iLtiiCGkfUJnBI5k07acUjSSmWz3idGItf-SmY4latHXAeWF6i18cJZkJjV2MA3s1ufE
  0xB2QgRMs_zwpDAB94ICwBUcMBuce40rVhamBx4_RPvr-FsX_IUMBOCRf-p_Av3RKqE2
  KQa83IgWUbgUnvXHsmNOtArVpTD5wtIDB-Pcwq_jvOgyKYupgddkTwo9jY50q4R3u2Nv
  m47NjurQKJ1jvmVsv-ouSfIYGeUrqWOkbwjfkgenLJHv7ZnXE2bPI-KkkM4n5f2OjCfH
  uirtQnstKEd4gCbhUSx5BSpjoNLT77emBWb_NjiKdCZ8dugvuu48R9uaAc3PtBQyf1xk
  yHpUoge7FLHRDC_Kc4mITunie4eC4SjaBpyVwL2PwW-pPr8J1RHOX0KNqxFq_7ZocLPd
  zAtgaYkLO7kaIBRKH4gGPRsoO4eyk0DrUzIaZBqp4VJRE7EcE48FjtneHHvjPc0eA4v3
  5CWpdPtvEHgeAwsXgfF64Bn_PIMgyMt29Ja-s7Ob4j4TGOBXxxdMUhf67z9nnUARnLej
  12ARzaz9Wa00fQjfvJQVaxbjeZ9kFDM69vjW997615Oxute1YenKcZqACx9EoghOqj_x
  wJphXfBIQcy27pYcOPDm5Q1vjLryDv5kyyp0bIni5sIqUQnrJ9InUy2VBtSB0wE_drno
  iwQu2_rMb_M0jgnuNZ-N3Y9haW4AMX7a-5uttqK-eyQO0OogmCBr8pLN0ZC7aQz2KbPl
  _TDxQQgrCn2ra_1VsYn8hl0x_D1FQUeB4y6bA3LnfUuVkYYYoUFQQGy5oCdT-AjqCSqf
  OoGRjRRBfsOpm67DykdVa1BXIEgfXNPCzfHzPHvAkYdH1aar1fOZINtK9jKJZjz-5Rti
  E2yvMWqj628njag-IiDxyVRM1-5WD2VR-CRR-KRQ1AAQ7lG6KIMGuSHrKLzGbLDrkCKa
  1exarWA7Go0792shiM2psZaZuqyfY7fO0V0vY4B4uCOlCWiRxbAR3JzslRQnRzE34f7C
  seSlcO_Xv-yR1USl0Ad3i9dkdjsqrp8boBA4unSl8IEi5b6syuIORGnQCQZvO1xbHTra
  _xwdNe9H-yvnaeZe-e9JrvI6wTEXKpwfzj6JhUliPiQiZffpC9aFiaMz4b8s6i37tWRy
  gHFrlCS97tV2fCL9XkGms5vjLzNVBmhBw-NvcgLSrtfXLpvBOmNIphE3kzFAi0vZUa2p
  hQKuFmlviyFrPHPlVAN9Q5WGbst425cS2bIE9meRNnD2i7Y5F74aSPwbow5KDpQQc3Rc
  h3OWWDRjspuxx9zYTkMRIatosRJtXc2dNnGrRoUHKF2-5DKrJ5Gx9J9sFm4f1OQ4Iokx
  mGj-YkjRPiPukYFvUFrobfRx3kyhHzxoHpMgmkN98dh24tlVbVpcsWXwhXkfoGy2fvTM
  QE3EE7ItA3deCXumiFwHeCFpNOjyEaLj_s9zBI6NF3lvtR0Ex17w-YehP7_zyufpwguC
  nyxxbHFAbZDOXGc5jMntG2QvosPYirxVoEQUaQg4nZFCikoWbh7KgjXtzLnctKBIRn6D
  SeNYNdIweq2M3YUJOkk-Au9tTFSO8UvmPiww5oDBT927QrpeyOLVBuHYBC8HFFe7_Xbm
  BC2T-_qCs68f4OqhLbMdK2SM3O36hIXK81QbWR-2_3Zy7qgLRVRiHNIsycmWibYsD_Mm
  SzM7s__J-jzDTISOuj-ZtoKtAcmYndpLZLzkpWoKfxHSfX_PUH1T0My5nhGypx5zSQ2N
  xOur_PoYERR0bijcAAmzqRm2xtBaGqI6YbPm_88y3hlzU4N1wcFlyoc8R68rHZk25UR5
  oVi4veVi4_s1itJ1tNVUojKvbYpLOUnVa_A3-G4B6uYBrIW7svDbBzV8cp-ptNGkBrIy
  h3xNSftImjH641Y49wSfds2RS7K4_QJyJpeRyhLTD3xabL1QkKO2hqNFD0aEtLtCPdpa
  UvFxrCgL7vXdR86-KnJOP5bedbWNiYGRbUU7JdOQt2pFOqMlW0TWfl7-313tavijKuy4
  DoSCA_cjlWsc7XWT8zPk0gTSFrN8QH5EF2rAZNt1F7HjZibEDlzC5fb559Y9TB3Kud_L
  GKfOjqcFQDrRKGpaJTFnBbgBZdk2Mt96QVMUUYJTvHjeUlbFi7MtNrSuGjTItrf2SZWq
  _c0MJN1T6KX6ZPEVvqTZ31shLhwXW1MysbGdavuF_-Z9ZXwUYeWdmi9mWAfio10dfEKh
  pjnnxHVaPk7mpKH2883L3GnkzV1GQSJbeykEv-bEgmSEmVNo1QwFcAEBTfndi_vUmSxT
  tNWUct7Nv7nfvUTmyy6FECGTYaLoT8VfZRPn0hwi5axZM--6lC9qLEWk8PGWQk6FEFoj
  6jcJS0s69IzasBXE-JyZaKKOORagAjOxYoAv3K0h8N7wSxupoukUwRrYn-4WxAddpfFL
  TuFGwoqfp4Va0VZXsMZtuXXUkqlPSCfBrvs7m56GDRVCmLGJlI7QlMMjNgde2dxgKo8s
  qL8mYjZDHAJG732BaGAmGNI31KFy2lCe0ot7JOF5vy8UMBAfHGEprgQpCvRAfzHeJSSR
  g8ZqfQTCOjKIuGQeKRxYhEXv74-ZaCVNF2qE02ldQ3ugkt642VQXvo-rGSmH17L7P6T3
  JkU7zUvnO3HMrgI0xSzY1RHRgICCeFi35s7cqliW0jHbuHhQ3VkzY8ZXO8LBLM2nwbor
  6BetQYmgrhWefqg_QOXyKnnuuwT8sZneNDKpfxPLD_3CKSib56PoRdmZIjM8f1xKcje4
  ceJktg32XunXWUlDM1ptOLPb7vzniVZycycC_0tqsNk0V_NSbR_wnVsE80t7d0y8uKV7
  i2-nISibVd6MuQoIVq3dNJ8ebJZkvTNIApOPlPe3KpyZn73C-oROuGINs7I7QDfkrHzs
  Vm-2V7pRYfpdtGNJnXacAdT29Jz20PQBQh11laHcRh-o3JSmzQHRbsHVYi6oBUIi_NUn
  yLe5lfWXB3BPafxPCVbTBw_WtwEYUBEzpbvNIx_9kaGP068S4Co-qwCRFIS6dsR6d7O_
  TGsPfddpgESp0XmeWqtsu4x3nTipUVwlDlf9yL4iaOknwejxzdG-CvTlPUCTjXfuE1mv
  35tptCWjP-64IHPANUHQVfok9otzwWS5Y-y4Ih3yEX9Sriq7WOWp0SVgZNZ7J1r4f3gh
  Hl2zo6W_ec8M5mOLAFJjZQNQzSInA2ZrmtuJ8lXhYht0ydTblDhi1Woprz-hBsmoSVxe
  2pvjlJSmHgEQUsH__NR-83AP2atgi1MdUqOQWQDCpW6DjYgbOhP4xZiu6jdFqp6AAyUp
  b6w7NrTqsObzZrwFD72ibmGA3baV1v-z8XSFhYi6FKBf-QLRO_AFzyc0w_vRquM6E_h2
  X271_SkYSp5A1YtdepapEU6O_e2ivK2lP6ctlv_F2QVFfF-8Lsw-aS9iIJsvrRBXqFct
  6KkF9XSW7nBcVmKXL-RMZNf2XTtBMta2O2vohS6R1M04g5Ls1w-4dk1jG1XVABNF9o_E
  Cf2ARKMKICbJsQppnJd00Gb5yKpbOwt0D51YOOKF5aPmCl0kX0eB70EHBYa0MIcZuRs5
  SZooDOVe1sLLrTphX1uHY0TapWKX0_42-434qVgMiSCc7KxJEVDSHHoEof_DVVX9zKdX
  CbfK5Nykyj8qfDOX21vZP_yNB171nFSpu7kxqrN7q3mC4YMxzPZzFzfgPmWqSDTXBYFx
  zFmt_wSJSVCjJATRlw8mg1Ay-8xQHWT5K5zikRuNoIgS_cy7kUC8t1EvGN99SHCAvDqN
  6GMemIv8Av_rCRhlnpVR1XbhutWjrPqoVh4XV7iCBfewlJYIOtocv20tLlbplxC_3WA7
  goKoKLn1QDrlRuk0lslueye6vIOMNBZv_brPkAilqAkbUVYtiMmnGXOvB3U-rzJ54D9k
  QkI_zJarhT-wSaMCnoBd2KHyR4rfGnBXCs6xGwvWycET9E8q5ApDjYVAZoOBOl6KwKzC
  tPz8H2cKmeezVkL3IvTVZsWZEr55WWwioQhPnXpCAgZI0HqEwCfITKh_d_0-Nt3PJdXQ
  ygL9Z6EKKxe6fGfs1rx33U86fOiWVftpRWY9WnpreUZQSov3OgtFSeFQbgK2C3WZOgOl
  6rfzKu9pQjXWHmk-xxWMCIKKSTBmfv2eHzzp8UnBoKSUALNNSMXxA5vUwGDh6iGziC8O
  0QGex5prNNspjLd99B0TO-NqJVeNd0fwQ5iHWiswfr1Ak3jzYqAyq6mRlUG5mIHNAiDL
  Qb_EizjMQapBSM_QvvZabVHf8EiBNJwvTp0N4ag_XNlf3eOnplLWWRQShRE2nwpZverw
  Ng4AWe7KpvgaHjMNJaj3RzJ5jvYjGdWxd0EreuUE0L_RBDrkXEJVtXo47sys0ykg0i9b
  J2GkPyx_TNi8TcrPsKPl4YDbpFG6GZbX0rEJhPwe-MeLAqOriUAPQGblT5RFFTf3Yt5s
  ovMPGkeFy9yybB430UuNm_DcbbrP5_HZqnQ7gp7E5Fws1uBz03IXEUkGlTonBGuRV8s3
  _FsRpTr3fM7UFr3eK1OYuMNkCbja5tTVXLLTFmGx2F-5EbapDDSFNrVgfr5QQ29qxFc6
  h9KqN5cKReBQBMMA_LdL74iR2RLMLBltlI8e4PVztX-tXmsvMe6LMFHVAeCcGIHugx48
  Aaiun-XrAPLG80iRaMBeXNYTYXsnTM7nPk7APJ8FKrbpxKTVKM7fMtddVoYghVpGIPIB
  o1eGaPRpf1HK1O2XIzR61PoRBGJjRTQlMd4iGlQ6vKA9ss9-3DioRtSrnqws5eoTxN3k
  eYBn-d_jZJws9r4YE3hYyfx-an9jafBQIIwYJ9c1Xi4wd_6KonPhIQig0NLpn4Y_phs4
  s0Oy8QLGPkTTKHUc3jClCKjoesBbp4WVqb3ffLiZ2rgyYaSKWK2e6Dt57ajcOZuUuGQh
  To_CbYTiycGWXNfc_aa7hmA0zM3Aiy1QYN0R4vk0BRGmwJsRuU0uVMRdKD7TbjCNxeKW
  Vnp87Xs4YUyrcCWaj9eW6Vr_e22tPdS32o1sE53D6np0TjdBJHujiUqkaxZQmYRzie92
  eLlHFqNkuIX5PNGGQUYit0pDJCwx7HQHcVYxcmzhe4CuoEYDGAqt7w7TjI1l8buOk81Z
  NVHq_IlYf_Q1z8vj9R8qjynQY_CY_ldgMhgq64-F7KvMPrGMWUQJTifjgHEDYeZ97ktz
  3oIeOUEAxQTfS6ciJmwhyIQ9hJvj9RAWJV1lc57F-i9SWYq5N-R4ecsaQVl8mMoAAAAA
  AAAAAAAAAAAAAAAAAAAAAAAAAAAABQ4TFRge

payload
  -ZAJXSCS4BAA4BAA-AAF5BAEAGhlbGxvIHdvcmxk
```
