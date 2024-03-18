Trust Spanning Protocol (TSP) Specification
==================

**Specification Status**: vs1.0 Experimental Implementor's Draft

**Latest Draft:**

[https://github.com/trustoverip/tswg-tsp-specification](https://github.com/trustoverip/tswg-tsp-specification)

**Authors:**

- [Wenjing Chu](https://github.com/wenjingchu), [Futurewei Technologies, Inc.](https://futurewei.com)
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

The Trust Spanning Protocol (TSP) facilitates secure communication between endpoints with potentially different identifier types, using message-based exchanges. As long as these endpoints use identifiers based on public key cryptography (PKC) with a verifiable trust root, TSP ensures their messages are authentic and, if optionally chosen, confidential. Moreover, it presents various privacy protection measures against metadata-based correlation exploitations. These attributes of TSP together allow endpoints to form authentic relationships rooted in their respective verifiable identifiers (VIDs), viewing TSP messages as virtual channels for trustworthy communication.

In recent years, a wide variety of decentralized identifiers have been proposed or are being standardized to meet a diverse set of use cases and requirements. This diversity underscores the critical need for a universal method to interconnect these differing identifiers, akin to how the Internet Protocol (IP) interconnected various physical network designs during the initial phases of internet development. Such a universal interconnection method must preserve the inherent trust embedded in the identifiers and facilitate the exchange of trust information between endpoints. This is essential for accurately assessing the suitability of these identifiers for the specific applications in which the parties are engaged.

Note that although this specification primarily addresses decentralized identifier types, existing centralized or federated identifier types, such as X.509 certificates, can fulfill the VID requirements outlined in this specification. This is achievable by adopting a compliant format and enhancing the trust foundation of their corresponding support systems and governance processes.

Beyond offering enhanced trust properties compared to previous solutions and interoperability between VIDs, TSP is conceived as a universal protocol, serving as a foundation for various higher-layer protocols. This design approach draws inspiration from the success of the TCP/IP protocol suite. In the TSP context, directional TSP messages function as a unified primitive to bridge diverse endpoint types, similar to how IP packets enable inter-networking between distinct networks. Task level protocols or applications, intended to operate atop of TSP, mirror the roles of TCP or UDP, providing task-specific solutions while harnessing the core properties of the TSP. In order to fulfill such a foundational role, TSP keeps its message primitives simple, efficient, and as much as possible, eliminates unnecessary variants.

TSP messages can traverse various transport mechanisms without making prior assumptions about their trustworthiness, although users may opt for specific underlying transport protocols for TSP based on various factors, including additional security considerations. TSP messages can be transported directly between endpoints (Direct Mode) or routed via intermediaries (Routed Mode). We first describe the direct mode, followed by the routing mechanism in [Section 6](#routed-messages-through-intermediaries).

TSP stands as the spanning layer protocol within the Trust over IP technology architecture [1]. It occupies a pivotal role, facilitating the twin goals of robust trustworthiness and universal interoperability across the Trust over IP stack. For additional details on the architecture, please see Section 1.2 below and the informative reference [1].

### Terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [[ref:RFC2119]] [[ref:RFC8174]] when, and only when, they appear in all capitals, as shown here.

[[def: Verifiable Identifier, Verifiable Identifiers, VID, VIDs]]
~ A Veifiable Identifier is a category of digital identifiers that meet requirements set in [Section 2](#verifiable-identifiers) of the Trust Spanning Protocol Specification. The requirements include, among others, cryptographic verification and assessment of governance and associated [[ref: Support Systems]]. It does not itself a defined digital identifier scheme. It is not restricted to a particular type of identifiers, for example, centralized, federated, or decentralized.

[[def: TSP Relationship, Relationship, Relationships]]
~ A TSP relationship is a pairing of two VIDs `<VID_a, VID_b>` where `VID_a` is an [[ref: VID]] of the local endpoint `A`, `VID_b` is a VID of the remote endpoint `B`, and the local endpoint `A` has verified `VID_b` for use in TSP with its `VID_a`. Each [[ref: TSP endpoint]] maintains a [[ref:Relationship Table]] that contains such pairings for all active relationships. This pairing is directional by default, but if the verification has been made mutually in both directions, it is referred to as a [[ref: Bi-directional Relationship]].

[[def: Bi-directional Relationship, Bi-directional Relationships]]
~ [[ref A TSP Relationship]]] is directional by default, but if the verification has been made mutually in both directions, it is referred to as a [[ref: Bi-directional Relationship]]. [[ref: Bi-directional Relationship]] is represented as `(VID_a, VID_b)` in the endpoint `A`'s relationship table and `(VID_b, VID_a)` in endpoint `B`'s relationship table. A Bi-directional Relationship means that each endpoint has verified the other's VID indepedently.

[[def: Relationship Table, Relationship Tables]]
~ A table of [[ref: Relationships]] of a [[ref: TSP Endpoint]]. Each entry of the table is a [[ref: Relationship]] where a VID of the endpoint is one of two VIDs in the pairing. 

[[def: TSP Endpoint, Endpoints]]
~ A TSP Endpoint is a computational system that runs the Trust Spanning Protocol. An Endpoint is able to obtain or create certain types of [[ref: Verifiable Identifiers]] possibly through the respective [[ref: Support Systems]], and is able to verify and assess another endpoint's VIDs via their corresponding [[ref: Support Systems]].

[[def: TSP Support System, Support System, Support Systems]]
~ A TSP Support System is a computational system that supports the management of VIDs and in particular facilitates assessment and verification of VIDs of an [[ref: Endpoint]]. 

[[def: TSP Intermediary System, Intermediary System, Intermediary, Intermediaries]]
~ A TSP Intermediary System, or just an intermediary, is a computational system that assist endpoints in forwarding [[ref: TSP Messages]].

[[def: TSP Message, TSP Messages, Messages]]
~ A TSP Message is a single unit of asynchronous message in TSP with assured authenticity, confidential (if chosen), and optionally metadata privacy.

### Reference Architecture

<img src="reference-architecture.png" alt="TSP Reference Architecture" style="width:800px;"/>

The Trust Spanning Protocol is defined within the Reference Architecture (RA) illustrated in Figure 1. The principal components of this reference architecture are:

- Direct Communication: Endpoints communicate with each other using TSP in direct mode, depicted by an arrowed line labeled number 1. This communication pattern encompasses two directional relationships, with each endpoint evaluating the other independently.

- Routed Communication: Endpoints communicate using TSP in routed mode through [[ref: intermediaries]], represented by arrowed lines labeled numbers 2 and 3. It's important to note that intermediaries are not necessarily trustworthy.

- Identifier Management: Endpoints manage their verifiable identifiers (VIDs) and associated roots of trust information via an abstract interface with their [[ref: Support Systems]], shown by dotted lines labeled number 4. Additionally, endpoints verify and assess the counterpart in a TSP relationship through another abstract interface with their respective support systems, denoted by dotted lines labeled number 5.

### Authenticity, Confidentiality, and Metadata Privacy

In TSP, these properties are defined within the context of a directional relationship formed by a pair of verifiable identifiers between a source and a destination endpoint. In this context, the source is also referred to as the sender and the destination as the receiver of a message. Authenticity is ascertained by the receiver, providing confidence that the received message remains unaltered and that the message genuinely originates from the sender. Confidentiality ensures that only the sender and receiver have access to the protected confidential payload data content. However, some parts of the message's envelope, not shielded by confidentiality protection, can be observed and used to infringe upon privacy through traffic analysis, correlation or other exploitative means. TSP provides optional mechanisms to safeguard against these vulnerabilities. This specific type of protection is termed "metadata privacy," differentiating it from the narrower understanding of privacy, which concerns the prevention of content exposure to unauthorized parties, synonymous with confidentiality.

TSP messages always assure authenticity, optionally confidentiality, and if utilized, metadata privacy. The authenticity and confidentiality goals are achieved by a scheme combining a public key authenticated encryption (PKAE) and a public key signature. The metadata privacy protections are achieved by nested TSP messages and routed messages through intermediaries.

### Use of Formats

TSP specifies message types that will have varying formats or representations during their lifecycle, both within systems that process or store them and networks that transport them. Additionally, for purposes such as debugging, documentation, or logging, these messages may need to be represented in a text format that is more accessible for human interpretation or better accepted for legal and administrative treatments.

TSP uses CESR encoding for the envelope, payload structure and signature parts of TSP messages. CESR encoding allows composibility for complex cryptographic objects and easy convertions between text and binary representations while maintaining alignments of data objects. Within TSP's payload, other types of encoding may also be used in a mixed mode. 

We introduce the notation `“{a, b, c}”` is a concatenation of CESR encoded objects. This does not mean that the data objects have to or always are in a concatenated form, but because CESR encoding is self-framed and composible, the actual concatenation can be performed whenever is needed. With at caution, we will follow this simple method throughout this specification and postpone the encoding details to [Section 9](#serialization-and-encoding).

In this specification, we utilize text formats for clarity and illustrative purposes. However, it should be understood that such text-based descriptions are solely to illustrate how the messages are structured. Implmentors should be aware of other formats in which cryptographic primitives are operated on or the message is encoded for transport. For more details on serialization and encoding, please refer to Section 7.

## Verifiable Identifiers

The Trust Spanning Protocol does not mandate that endpoints utilize only a single type of identifiers and this specification does not define one. However, the efficacy of TSP and the trust assurances in authenticity, confidentiality, and metadata privacy it provides hinge on the methodologies of VIDs. Factors such as the construction and resolution of these identifiers, coupled with the verification of trust information from their support systems, directly influence the degree of trust endpoints can derive from using TSP. In this section, we outline high-level requirements without prescribing how various VID types should fulfill them. All identifiers that meet these standards are termed [[ref: Verifiable Identifiers]] (VID). The aim is to enable endpoints, equipped with their chosen VID type or types, to communicate over TSP with the respective confidence and trust level that those VIDs inherently support.

A foundational prerequisite for TSP is that endpoints operate within a secure computing environment, possibly facilitated by tools such as Trusted Execution Environments (TEEs),  digital wallets, or digital vaults. This list of tools may extend to non-technical ones such as governance conventions or regulations. While TSP aids in transmitting trust signals between endpoints, it cannot instantiate trust where none exists.

In TSP, pairs of TSP endpoints establish directional [[ref: relationships]]. In these relationships, endpoints assess each other's identifiers independently. The verification and appraisal of VIDs remain inherently directional.

### VID Use Scenarios

In the Trust Spanning Protocol, VIDs function as identifiers  within protocol envelopes and other control fields (see Section 3). As identifiers in exposed envelopes, VIDs may be visible to third parties with access to the network transports, allowing for potential correlation with other identifying transport mechanism information, such as IP addresses, transport protocol header information, and other metadata like packet size, timing, and approximate location. To mitigate the risk of metadata exploitation, TSP provides Nested Messages (Section 4) and Routed Messages (Section 5) for certain metadata privacy protections. Given the varied roles VIDs play in different scenarios, their management requires distinct considerations. To clarify and simplify the discussion of these scenarios, we categorize VID uses into three scenarios: public, well-known, and private.

We refer to the scenarios where VIDs are exposed to external entities as their 'public use'. The address resolution operations of public use VIDs may provide visible information to an adversary.

Figure 2: An example of public use VIDs where a0 and b0 are used in the first layer above a public transport mechanism. Additionally, a0 and b0 may also be made ‘Well-Known’, labeled as awkn and bwkn.

It's important to note that while additional security measures like TLS or HTTPS can be employed at the transport layer to safeguard VIDs, TSP does not inherently depend on these mechanisms for protection. Consequently, within the context of TSP, even VIDs protected by such transport layer security are treated as if they are 'public,' assuming they could potentially be accessed or observed by external parties.

Within the category of public use VIDs, there is a subclass known as 'Well-Known VIDs'. These are VIDs whose controllers deliberately intend for them to be broadly recognized. The rationale behind making a VID well known often revolves around streamlining or simplifying the processes of VID discovery, resolution, and verification. However, it's important to recognize that such actions inherently expose additional information to potential adversaries. Figure 2 above also shows  an example of Well-Known VIDs. As a subclass of public VIDs, well-known VIDs must also meet all public VID requirements.

Figure 3: VIDs a0 and b0 are in public use; VIDs a1 and b1 are in private use.

VIDs are considered to be in 'private use' when their usage is safeguarded within another instance of TSP relationship through a nested approach (See Section 4). This private utilization is facilitated by nesting, where the inner VIDs bypass the need for address resolution. Their establishment operations are managed by TSP control messages, and all relevant operations are secured by the encryption provided by the outer layer of TSP. For an in-depth explanation of these nested modes of TSP, please refer to Section 4. The specifics regarding control messages are detailed in Section 7.

### VID General Requirements
This section specifies general expections TSP asks VIDs to meet. TSP uses VID as an abstract data type that must support a set of abstract operations. This section also lists these operations in a format like `VID.OPERATION`.

#### Cryptographic Non-Correlation

An endpoint can control multiple VIDs simultaneously and over extended periods. It is imperative that these VIDs are cryptographically non-correlatable in an information-theoretic security context, meaning the knowledge of one VID does not reveal any information about another.

For example, in Figure 3, an adversary might observe VIDs a0 and b0, which are categorized as public and could be linked to a specific endpoint using additional metadata. However, if the same adversary also happens to observe VID a1, it should be impossible, based on the design of the VIDs, for the adversary to establish a correlation between a1 and a0, and consequently, to associate a1 with endpoint A.

::: issue
Use an alternative expression to tie to 128-bits of strength
:::

#### VID Type

Each VID type MUST have a unique type code allocated for its exclusive use. The type code is out of an integer number space of 1..262144.

::: issue
Need to add how the code space is administered.
:::

#### VID Syntax

TSP tries not to impose any additional syntax requirements beyond any VID type already mandates. But since TSP uses CESR for VID encoding, any VID's syntax MUST specify at least one compliant CESR encoding. 

#### Resolution to Transport Address

For every VID to be in public use, the VID MUST support an address resolution operation `VID.RESOLVEADDRESS` for each transport mechanism that the VID supports. 

Implementation of this address resolution operation is VID type specific.

For any VID that is used in private only, an address resolution mechanism is unnecessary.

#### Mapping VID to Keys
VIDs MUST support operations by the controlling endpoint to map a VID of its own to keys required by TSP.
- Mapping to public and private keys used by PKAE: `VID.PK_e` and `VID.SK_e`.
- Mapping to private key or keys used by signature signing: `VID.SK_s` or `VID.SK_s[i]`.

VIDs MUST support operations by an assessing endpoint to map a VID of another endpoint to keys required by TSP.
- Mapping to the public key used by VID verification: `VID.PK_s`. (*Is it always the same as the signing key?*)
- Mapping to the public key used by PKAE: `VID.PK_e`.
- Mapping to the public key used by signature verification: `VID.PK_s`.

Implementation of these mapping operations is VID type specific.

#### Verification
VIDs MUST support an operation by an assessing endpoint to verify a VID of another endpoint: 
- `VID.VERIFY` for TSP to verify that endpoint `A` has access to the corresponding secret key, `VID.SK_s`, using a PKC algorithm. VID types MAY use additional information in assessing the VID in the same `VID.VERIFY` operation.

Implementation of this mapping and verification operations is VID type specific.

For any VID designated for private use, while the same verification procedure requirements as outlined above still apply, simpler VID types MAY be employed. This is because the verification process occurs between two endpoints that already possess a verified TSP relationship between them, and the verification is conducted through TSP messages within that established relationship. TSP defines specific message types for such instances of private VID verification in Section [Control Payloads](#control-payloads).

#### Handling Changes

::: issue
TODO
:::

### Examples

::: issue
This section should include a list of example [[ref: Verifiable Identifiers]]. The list may include: KERI AID, `did:webs`, `did:x509`, `did:peer` for private use, and one or two examples based on a public blockchain. For each example, information discussions can provide recommendations on how the required primitives may be implemented.

TODO
:::

## Messages

TSP operates as a message-based communication protocol. The messages in TSP are asynchronous, can vary in length, and are inherently directional. Each message has a designated sender (alternatively termed "source") and a receiver (or "destination"). Throughout this specification, in particular when we describe the routed mode in Section 6, the terms "sender" and "receiver" will be used to refer to direct neighbors, while the terms "source" and "destination" will be used for the originating and ending endpoints of the carried message. Within the context of TSP, both the sender and the receiver of a message qualify as "endpoints." Entities such as Intermediaries or Support Systems can also function as endpoints when they are participating in TSP communications themselves. For the sake of simplicity, we will uniformly refer to all these entities as "endpoints," unless a distinction is necessary for clarity.

In this section, we specify TSP messages that are used in Direct Mode between neighboring endpoints without any intermediaries in between. By being *direct*, we mean that there is a direct transport layler link between the two endpoints in the TSP layer. In comparision, Routed Mode, specified in [Section 5](#routed-messages-through-intermediaries), involves at least one intermediary or more in the TSP layer.

As outlined in Section 2, VIDs serve as identifiers for any endpoints involved in TSP. Both the sender's VID and the receiver's VID can map to required keys used by TSP in the sender and the receiver, and to a transport address for delivering the TSP message.  The sender and receiver VIDs can be of different VID types.

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

Some other text

::: issue
The code table is still to be finalized
:::

TSP_Tag is encoded in CESR as: `-E##`, where `-E` indicates a TSP message, and ## is a two Base64 character string representing a number space of 4095 unique values. The TSP_Tag MUST be set to `-EAA`. All other values are reserved.

TSP_Version is encoded as `X###`, where `###` is a three Base64 character string representing a number space of 262144.

VIDs in TSP are encoded with a VID_Type and a VID_String. If the VID type has variable length, then the VID string consists of length followed by a string of that length.

VID_Type is encoded as another tag `X###`. Please see Section [VID Type](#vid-type) for further information about VID types.

VID_String's format is determined by each VID type. 

`VID_sndr` and `VID_rcvr` (if present) may have different VID types.

### TSP Payload

The TSP payload is where application's data goes. It is divided into two parts: Non-Confidential Fields and Confidential Fields. The confidential fields are encrypted and appear in the payload as ciphertext. It is up to the upper layer to choose where their data will go. 

```text
TSP_Payload = {Non_Confidential_Fields, Confidential_Fields_Ciphertext}
```

#### Non-Confidential Fields

The non-confidential fields are optional, and if present, not encrypted. They may contain header and data fields.

The non-confidential header fields may contain data Type and Subtype codes, and other fields for control use. The non-confidential data fields can be any data fields encoded in CESR, including mixed JSON, CBOR and MsgPack encoded data as supported by CESR.

::: issue
Type and subtype code to be finalized
:::

#### Confidential Fields

The confidential fields of the payload are encrypted through PKAE. What is encoded in the message is the ciphertext of the corresponding plaintext which may contain both header and data fields in the same way as the non-confidential fields.

And the ciphertext is produced as:

```text
Confidential_Fields_Ciphertext = TSP_SEAL({Confidential_Fields_Plaintext})
```

The details of the supported PKAE schemes for the `TSP_SEAL` operation are specified in Section [Cryptographic Algorithms](#cryptographic-algorithms).

The confidential header fields may contain an optional list of VIDs, the payload data Type and Subtype codes, and other control fields. We will define these fields when we define individual payload fields for specific messages.

For PKAE schemes *HPKE-Base* [ref:RFC9180] and *Libsodium sealed box* [ref:TOADD], the `VID_sndr` MUST appear in the confidential heade fields following the ESSR scheme from [2]. See [Section 8](#cryptographic-algorithms) for the details.

The header fields also contain a list of intermediary hop VIDs for Routed Mode messages. See [Section 5](#routed-messages-through-intermediaries) for the detailed description.

The confidential payload data field can be any data encoded in CESR, including mixed JSON, CBOR and MsgPack encoded data as supported by CESR. Since TSP message itself is encoded in CESR, it can be embedded in the data field, resulting a [[ref:Nested Message]].

On the receiving side, the corresponding TSP primitive is `TSP_OPEN`.

#### Header Fields

As described above, healder fields may appear in non-confidential or confidential fields. They have the same format and meaning regardless of whether they are encrypted. However, certain header fields are required to be in confidential fields if confidentiality is desired by the application.

- *Type* and *Subtype*

The `Type` is an allocated code indicating quickly what the payload is intended for. For example, an upper layer application may use type code similar to TCP or UDP port numbers.

The type code `TSP_CTL` is reserved and special. It indicates that the payload data fields that followed are for the control operations of TSP and should be passed on to the TSP rather than an application. When control data is present, a TSP message MAY optionally contain normal application data as well. The control data SHOULD come before the user data when both are in the same payload.

The type code `TSP_GEN` is reserved. It is used by applications where this code is not needed or doesn't care.

For each `Type`, a space of `Subtype` is available for use by the application designated by the `Type`. The use of subtype is optional.

For `TSP_CTL`, we will introduce `Subtype` codes in Section [Control Payloads](#control-payloads).

- *Thread-ID*

::: issue
To do
:::

- *Nonce* and/or *Timestamp*

::: issue
To do
:::

### TSP Signature

The third part of a TSP message is the signature signed by the sender.

```text
TSP_Signature = TSP_SIGN({TSP_Envelope, TSP_Payload})
```

On the receiving side, the corresponding primitive is `TSP_SIG_VERIFY`. The details of the `TSP_SIGN` and `TSP_SIG_VERIFY` are specified in Section [Cryptographic Algorithms](#cryptographic-algorithms).

### TSP Message Examples

Applications can use TSP messages, as defined above, in any way they want. In this section, we discuss two common scenarios that may be particularly useful. In the first case, all user data is in the confidential data fields and TSP assures both authenticity and condientiality. In the second case, all user data is in the non-confidential data fields.

#### Authentic and Confidential (AAC) Messages

```text
Authentic_Confidential_Message  = {TSP_Envelope, Confidential_Payload_Ciphertext, TSP_Signature}
                                = {TSP_Tag, TSP_Version, VID_sndr, VID_rcvr, 
                                    Confidential_Payload_Ciphertext, TSP_Signature},
where,

Confidential_Payload_Ciphertext = TSP_SEAL ({Confidential_Payload_Header, 
                                                Confidential_Payload_Data}),

and

TSP_Signature = TSP_SIGN({TSP_Envelope, Confidential_Payload_Ciphertext}).
```

These messages use the `VID_sndr` and `VID_rcvr` pair and has no non-confidential fields, i.e. all payload is encrypted.

#### Authentic Non-Confidential (ANC) Messages

```text
Authentic_Non_Confidential_Message  = {TSP_Envelope, Non_Confidential_Payload, TSP_Signature}
                                    = {TSP_Tag, TSP_Version, VID_sndr, 
                                        Non_Confidential_Payload, TSP_Signature},
where,

TSP_Signature = TSP_SIGN ({TSP_Envelope, Non_Confidential_Payload}).
```

These messages do not have `VID_rcvr` and the payload is entirely non-confidential. 

### Relationships

A [[ref: TSP relationship]] is a pairing `<VID_a, VID_b>` of two VIDs controlled by the respective endpoints `A` and `B` indicating that endpoint `A` has satisfactorily verified `VID_b` of endpoint `B`.

An endpoint is able to obtain (or create) one or more VIDs possibly through the service of their respective [[ref: Support Systems]]. Let us say `VID_a` is one of such VIDs for endpoint `A`. As a convention, we will use lower case letter, such as `a`, to indicate that `VID_a` is controlled by the endpoint named with the corresponding upper case letter, say `A`. Details of VID management for any VID type is out of scope for this specification but an endpoint will need to implement necessary supports for all of its supported VID types.

By [Out of Band Introduction](#out-of-band-introductions) or other TSP relationship formation messages(#control-payloads), endpoint `A` learns a `VID_b` of endpoint `B`. At least point, endpoint `A` chooses `VID_a` and performs necessary verification and appraisal operation on `VID_b` with respect to `VID_a`. If the verification is successful, endpoint `A` may add a relationship `<VID_a, VID_b>` to its relationship table.

At this point, endpoint `A` may resolve `VID_a` to obtain transport layer address for delivery of a TSP message with `VID_a` as the sender VID and `VID_b` as the receiver VID.

When endpoint `B` receives this TSP message, if this is the first TSP message from `VID_a` to `VID_b`, endpoint `B` will perform necessary verification and assessment to evaluate `VID_a` with respective to `VID_b`. If successful, endpoint `B` may also add relationship `<VID_b, VID_a>` to its relationship table.

In short, one successful TSP message between two endpoints populates one relationship on each endpoint's relationship table. The relationships in their respective tables are the mirror image of each other in the form of `<VID_local, VID_remote>`. We may interprete this relationship as the state that the endpoint has verified `VID_remote` with respect to `VID_local`, or the pair of the VIDs are in a *verified* state. Note that because of the asynchronous nature of TSP messages, such state is also not always synchronized between the two endpoints. Their relationship table is not guaranteed to be always accurate.

Since endpoints may reuse VIDs, an endpoint may have relationships `<VID_a, VID_b>` and `<VID_a, VID_c>` in its relationship table at the same time. Only a pair together uniquely identifies a relationship.

Endpoints may have semantic meaning or application specific allocations associated with VIDs. For this reason, we say an endpoint `A` verifies and assesses a `VID_b` with *respect to* a local `VID_a`. The evaluation process may have dependecy on the chosen `VID_a`.

After endpoint `B` processed the first TSP message from `VID_a` to `VID_b` and accepted a new relationship `<VID_b, VID_a>`, it may decide to reply with its own TSP message in the opposite direction. It is common, although neither required nor always needed, that the two endpoints want to engage in bidirectional communications. At this point, endpoint `B` can update the corresponding relationship into a [[ref: bidirectional relationship]] `(VID_b, VID_a)`. Upon successfully receive the return TSP message by endpoint `A`, it can also update its relationship to bidirectional: `(VID_a, VID_b)`.

::: note
The notation `<VID_local, VID_remote>` is used for representing a unidirectional relationship, and `(VID_local, VID_remote)` for a bidirectional relationship.
:::

For details of relation forming TSP message, please refer to [Section 7](#control-payloads). The following Sections [Sender Procedures](#sender-procedures) and [Receiver Procedures](#receiver-procedures) describes in more detail the operations required for sending and receiving TSP messages.

### Sender Procedure Example

We outline the procedures for TSP message senders for the simple Direct Mode case in two parts: the initial message which establishes the relationship, and the follow-up messages that occur within that established relationship.

Endpoint `A`, which controls `VID_a` associated with Support System `A*`, acquires `VID_b` of Endpoint `B` through an [out-of-band introduction (OOBI)](#out-of-band-introductions) method, or a TSP [relationship forming message](#control-payloads) of another existing relationship. `VID_b` is tied to Support System `B*`. Note that `A*` could be the same as or different from `B*`. If Endpoint `A` selects to employ `VID_a` to dispatch a TSP message to the Endpoint identified by `VID_b` for the first time, it will be establishing a unidirectional relationship denoted by `<VID_a, VID_b>`.

The following is an example procedure that Endpoint `A` may follow when sending its inaugural message to `VID_b` using its own `VID_a`. This example is only illustrative. Implementors will need to pay considerations to the actual VID type's and the chosen transport mechanism's requirements, and the requirements of applications they intend to support.

- Step 1: Resolve `VID_b` to acquire access to the following mandatory information
    - Public keys bound to the VID for TSP: `VID_b.PK_e`, `VID_b.PK_s`
    - All other VID verification information as required by the VID type (Section 2 [Verifiable Identifiers](#verifiable-identifiers))
    - Transport information, if it is not yet known.
- Step 2: Verify `VID_b` with `VID_b.VERIFY`.
- Step 3: Create a TSP message
    - As the first TSP message, it MUST contain the relationship forming payload fields.
    - It may optionally also contain other user data. In other words, applications do not have to wait for a round trip delay for relationship establishment.
- Step 4: Use the retrieved transport information in Step 1 to establish a means of transport, if not yet available. Note that this step will be significantly different depending on the details of the transport of choice. Section 10 [Transports](#transports) discusses additional transport considerations.
- Step 5: Send the TSP message.
- Step 5: Update relationship table with `<VID_a, VID_b>`.

For subsequent messages, the procedure is simpler:

- Step 1: Create a TSP message
- Step 2: If the retrieved transport mechanism is ready to use (e.g. if it's cached or kept hot), send the message. If not, refresh operations will be needed first.

In the above much simplified example, we have not considered any dynamic changes or error conditions.

### Receiver Procedure Example

Similar to the previous section, the following example is only illustraitve for the receiver of a simple Direct Mode TSP message.

If endpoint `B` receives a TSP message of the generic form `{... VID_sndr, VID_rcvr, ... Confidential_Payload_Ciphertext, TSP_Signature}`, endpoint `B` may follow these steps to process this incoming message:

- Step 1: Check if the `VID_sndr` and `VID_rcvr` pair matches an existing valid relationship in its relationship table. If yes, jump to Step 5; otherwise this is the first message of this relationship.
- Step 2: Check if `VID_rcvr` is a valid local VID and local rules permit to proceed.
- Step 3: Resolve `VID_sndr` to acquire access to the following mandatory information
    - Public keys bound to the VID for a TSP crypto suite
    - All other VID verification information as required by the VID type (Section 2 [Verifiable Identifiers](#verifiable-identifiers))
    - Transport information, if it is not yet known.
- Step 4: Verify, and appraise `VID_sndr` using additional information and processes specific to the VID.
- Step 5: Verify the `TSP_Signature`.
- Step 6: Decrypt the `Confidential_Payload_Ciphertext`. 
- Step 7: If the PKAE variant requires, retrieve the sender VID from the decrypted payload plaintext and verify that it matches `VID_sndr`.
- Step 8: Process the rest of control fields.
- Step 9: Return the payload to the upper layer application.

### Out of Band Introductions

Before an endpoint `A` can send the first TSP message to another endpoint `B`, it must somehow discover at least one VID that belongs to `B`. If they also wish to utilize the [Routed Mode](#routed-messages-through-intermediaries), as specified in [Section 5](#routed-messages-through-intermediaries), then additional VIDs may also be needed before the first TSP routed message can be sent. We call any such method that could help the endpoints discover such prerequisite information an Out of Band Introduction (OOBI). There may be many such OOBI methods. Detailed specifications of OOBI methods are out of scope.

For the purpose of TSP, information obtained from OOBI methods must not be assumed authentic, confidential or private, although mechanisms to remedy such vulnerabilities should be adopted whenever possible. TSP implementations must handle all cases where the OOBI information is not what it appears.

Because TSP relationships can be highly authentic, confidential and potentially more private with respect to metadata, they can be used for the purpose of passing VID information for forming new relationships. Details of such procedures are specified in Section [Control Payloads](#control-payloads).

## Nested Messages
When TSP sender `A` dispatches a TSP Message with confidential payload intended for receiver `B`, the observable data structure for any third party not involved in the message exchange between `A` and `B` appears as:

```text
{TSP_Tag, TSP_Version, VID_a, VID_b, TSP_Payload_Ciphertext, TSP_Signature}
```

Over time, with a sustained exchange of such messages, an external observer may accumulate a significant volume of data. This data, once analyzed, could reveal patterns related to time, frequency, and size of the messages. Using `VID_a` and `VID_b` as keys, an observer can index this dataset. It's then possible to correlate this indexed data with other available metadata, potentially revealing more insights into the communication.

To mitigate this threat, TSP offers a technique whereby parties encapsulate a specific conversation — for instance, a sequence of messages — within an additional TSP envelope, as described below.

### Payload Nesting
Suppose endpoints `A` and `B` have established a prior direct relationship `(VID_a0, VID_b0>), they can then embed the messages of a new relationship `(VID_a1, VID_b1)`  in the confidential payload of `(VID_a0, VID_b0)` messages. In such a setup, `VID_a1` and `VID_b1` are protected from third party snooping. We may refer `(VID_a0, VID_b0)` the *outer relatioship and the messages of `(VID_a0, VID_b0)` as *outer messages*, and `(VID_a1, VID_b1)` the *inner relationship` and the messages of `(VID_a1, VID_b1)` as *inner messages*.

The above description also applies to unidirectional relationships.

This nesting scheme can be illustrated as follows using the confidential data field of its payload.

```text
Outer_Message = {Envelope_0, Payload_0, Signature_0},
Inner_Message = {Envelope_1, Payload_1, Signature_1}, 
Nested_Message = {Envelope_0, {Non_Confidential_Fields_0,
                                TSP_SEAL_0({Header_Fields_0, Inner_Message})}, Signature0}
```

In this scheme, the inner message MUST use the confidential data field of the outer message in order to achieve the protection of the inner message metadata. Other than that, we do not restrict the structures of inner and outer messages. For example, if the endpoints do not find the need for additional encryption of the inner message, they MAY choose to use the non-confidential payload fields for the inner message payload data. Applicatios should be aware that the confidentiality assurances would only be extended to the outer relationship if the inner message is embedded in the non-confidential field of the outer message.

### Nested Relationships

When TSP messages utilize this nesting approach, a new relationship, for example `(VID_a1, VID_b1)`, is created between the same endpoints `A` and `B`. This new type of relationships may be used for providing *context* over the aggregate of all messages between the same pair of endpoints. The privacy protection afforded by this method is designated as one example of *metadata privacy.* Since the nested messages hide the inner VID pair from being collected as a part of potential correlation attacks, we also refer to this style of privacy protection as *correlation privacy.*

The process for establishing such relationships with nested messages is detailed in Section 5.2. It's important to note that this nesting can be recursively applied, adding additional layers as required. Inner relationships are situated within an outer relationship that has been verified and deemed suitable for the intended purpose by both participating endpoints. The VIDs engaged in these inner relationships are therefore *private*, do not require same level of verification as *public* VIDs, and do not require transport layer address resolution of their own.

### A Shorthand Notation
For brevity and ease of presentation, we introduct a shorthand notation for nested messages, and indirectly the relationship in which these messages are communicated, as follows.

``` text
[VID_sndr, VID_rcvr, Payload] = {TSP_Tag, TSP_Version, VID_sndr, VID_rcvr, Payload, Signature}
```
This is only a simplication in notation. All message fields remain the same as defined in the previous sections, including the generation of ciphertext and signature fields.

``` text
[VID_sndr_out, VID_rcvr_out, [VID_sndr_in, VID_rcvr_in, Payload_in]] = {
    Envelope_out, {Non_Confidential_Fields_out, TSP_SEAL_out(Header_Fields_out, Inner_Message)},
    Signature_out }

where,
Inner_Message = [VID_sndr_in, VID_rcvr_in, Payload_in, Signature_in]
```

Such a notation does not imply any extra requirements or restrictions for the messages. 

For example, we may use the following shorter notation to represent the example nested message shown above:

`[VID_a0, VID_b0, [VID_a1, VID_b1, Payload]]`

## Routed Messages Through Intermediaries

## Multi-Recipient Communications

## Control Payloads

## Cryptographic Algorithms

## Serialization and Encoding

## Transports

## Security and Privacy Considerations

## References

### Normative References


### Informational References
[//]: # (\newpage)

[//]: # (\makebibliography)

[[spec]]

[1]. ToIP Technology Architecture Specification (DRAFT)
[1]: https://github.com/trustoverip/TechArch/blob/main/spec.md

## Appendix A: Test Vectors

### Test Vectors for Direct Mode TSP Message

### Test Vectors for Direct Mode Nested TSP Message

### Test Vectors for Routed Mode Message

