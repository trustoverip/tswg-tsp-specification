Trust Spanning Protocol (TSP) Specification
==================

**Specification Status**: vs1.0 Experimental Implementor's Draft Rev 2

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

The Trust Spanning Protocol (TSP) facilitates secure communication between endpoints with potentially different identifier types using message-based exchanges. As long as the endpoints use identifiers based on public key cryptography (PKC) with a verifiable trust root, TSP ensures their messages are authentic and if required, confidential. Moreover, it presents various privacy protection measures against metadata-based correlation exploits. These attributes of TSP allow endpoints to form authentic relationships rooted in their respective verifiable identifiers (VIDs), viewing TSP messages as virtual channels for trustworthy communication.

In recent years, a wide variety of decentralized identifiers have been proposed or are being standardized to meet a diverse set of use cases and requirements. This diversity underscores the critical need for a universal method to connect the systems these identifiers represent, akin to how the Internet Protocol (IP) connected various types of heterogeneous network designs during the initial phases of Internet development. Such a universal interconnection method must preserve the inherent trust embedded in the identifiers and facilitate the meaningful exchange of trust information between endpoints. This is essential for accurately assessing the suitability of the data these identifiers represent for the specific application contexts in which the parties may be engaged.

Note that although this specification primarily addresses decentralized identifier types, existing centralized or federated identifier types such as X.509 certificates can fulfill the VID requirements outlined in this specification. This is achievable within this specification by adopting a compliant format and enhancing the trust foundation of their corresponding support systems and governance processes.

Beyond offering enhanced trust properties when compared to previous solutions and focusing on the interoperability between differing types of VIDs, TSP is conceived as a universal protocol to serve as a foundation for various higher-layer protocols. This design approach draws inspiration from the success of the TCP/IP protocol suite. In the TSP context, directional TSP messages function as a unified primitive to bridge diverse endpoint types, similar to how IP packets enable inter-networking between distinct networks. Task level protocols or applications, intended to operate atop of TSP mirror the roles of TCP or UDP by providing task-specific solutions while harnessing the core properties of the TSP. In order to fulfill such a foundational role, TSP keeps its message primitives simple, efficient, and as much as possible eliminates unnecessary variants.

TSP messages can traverse various transport mechanisms without making prior assumptions about their trustworthiness although users may opt for specific underlying transport protocols for TSP based on various factors such as additional operational or security considerations. TSP messages can be transported directly between endpoints (Direct Mode) or routed via intermediaries (Routed Mode). We first describe the Direct Mode in [Section 3](#messages), followed by the routing mechanism in [Section 5](#routed-messages-through-intermediaries).

TSP stands as the spanning layer protocol within the Trust over IP technology architecture [spec-in[form:TOIP-TAS]]. It occupies a pivotal role, facilitating the twin goals of robust trustworthiness and universal interoperability across the Trust over IP stack. For additional details on the reference architecture, please see [Section 1.2](#reference-architecture).

### Terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [[spec-norm:RFC2119]] [[spec-norm:RFC8174]] when, and only when, they appear in all capitals, as shown here.

[[def: Verifiable Identifier, Verifiable Identifiers, VID, VIDs]]
~ A Veifiable Identifier is a category of digital identifier that meets the requirements set forth in [Section 2](#verifiable-identifiers) of the Trust Spanning Protocol Specification. The requirements include cryptographic verification and assessment of governance as well as the associated [[ref: Support Systems]]. It does not itself define a digital identifier scheme. It is not restricted to a particular type of identifier class such as, centralized, federated, or decentralized identifier trust-based ecosystems.

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

#### Cryptographic Non-Correlation

An endpoint can control multiple VIDs simultaneously and over extended periods. It is imperative that these VIDs are cryptographically non-correlatable in an information-theoretic security context, meaning the knowledge of one VID does not reveal any information about another.

For example, if an adversary observes VIDs `VID_a0` of endpoint `A` and `VID_b0` of endpoint `B` in a relationship `(VID_a0, VID_b0)`, where `VID_a0` is categorized as public and could be linked to a specific endpoint using additional metadata. However, if the same adversary also happens to observe `VID_a1`, it should be impossible by the identifiers alone for the adversary to establish a correlation between `VID_a1` and `VID_a0`, and consequently, to associate `VID_a1` with endpoint `A`.

#### VID Syntax

TSP tries not to impose any additional syntax requirements beyond what any VID type already mandates. But easier interoperability, we require that the VID format be either compliant DID format [[ref:DID]] or compliant URN format [[spec-norm:RFC8141]].

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
- Mapping to the public key used by signature verification: `VID.PK_s`.

Implementation of these mapping operations is VID type specific.

#### Verification
VIDs MUST support an operation by an assessing endpoint to verify a VID of another endpoint: 
- `VID.VERIFY` for TSP to verify that endpoint `A` has access to the corresponding secret key, `VID.SK_s`, using a PKC algorithm. VID types MAY use additional information in assessing the VID in the same `VID.VERIFY` operation.

Implementation of this mapping and verification operations is VID type specific.

For any VID designated for nested use, while the same verification procedure requirements as outlined above still apply, simpler VID types MAY be employed. This is because the verification process occurs between two endpoints that already possess a verified TSP relationship between them, and the verification is conducted through TSP messages within that established relationship. TSP defines specific message types for such instances of nested VID verification in [Section 7](#control-messages).

#### Handling Changes

::: issue #4
TODO
https://github.com/trustoverip/tswg-tsp-specification/issues/4
:::

### Examples

::: issue #5
This section should include a list of example [[ref: Verifiable Identifiers]]. The list may include: KERI AID, `did:webs`, `did:x509`, `did:peer` for private use, and one or two examples based on a public blockchain. For each example, information discussions can provide recommendations on how the required primitives may be implemented.
https://github.com/trustoverip/tswg-tsp-specification/issues/5
:::

- KERI AID


- `did:webs`


- `did:x509`


- `did:peer` for private use


## Messages

TSP operates as a message-based communication protocol. The messages in TSP are asynchronous, can vary in length, and are inherently directional. Each message has a designated sender (alternatively termed "source") and a receiver (or "destination"). Throughout this specification, in particular when we describe the routed mode in [Section 5](#routed-messages-through-intermediaries), the terms "sender" and "receiver" will be used to refer to direct neighbors, while the terms "source" and "destination" will be used for the originating and ending endpoints of the carried message. Within the context of TSP, both the sender and the receiver of a message qualify as "endpoints." Entities such as [[ref: Intermediaries]] or [[ref: Support Systems]] can also function as endpoints when they are participating in TSP communications themselves. For the sake of simplicity, we will uniformly refer to all these entities as "endpoints," unless a distinction is necessary for clarity.

In this section, we specify TSP messages that are used in Direct Mode between neighboring endpoints without any intermediaries in between. By being *direct*, we mean that there is a direct transport layler link between the two endpoints in the TSP layer. In comparision, Routed Mode, specified in [Section 5](#routed-messages-through-intermediaries), involves at least one intermediary or more in the TSP layer.

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
- TSP_Version: The version of Trust Spanning Protocol. The TSP version should follow semantic versioning practices with three numbers representing MAJOR, MINOR, PATH. MAJOR version signals backward compatibility MAY not be maintained with previous versions.

The current experimental draft's version is `0.0.1`. When this specification is officially released, the first version is to be `1.0.0`.

VIDs in TSP are encoded with a variable length VID_String that consists of length followed by a bytestring of that length. Two types of identifier syntaxes, DID [[ref:DID]] and URN [[spec-norm:RFC8141]], MUST be supported. Implementations MAY support additional syntaxes beyond these two types.

The DID specification allows various DID Methods. The URN specification allows various URN namespaces. This specification does not mandate any particular DID Methods or URN namespaces but would benefit from such standardizations elsewhere. In all variations, if a TSP implementation does not support any type of VIDs, it SHOULD discard the TSP message.

Please see Section [TSP Envelope Encoding](#tsp-envelope-encoding) for further information about VID encoding. 

`VID_sndr` and `VID_rcvr` (if present) may be different types of VIDs.

### TSP Payload

The TSP payload is where application data goes. It is either control message payload used by TSP itself or application message payload used by the higher layer. It is structured uniformly with a payload type followed by a series of data fields that is dictated by the type. The payload may be encrypted and encoded as a single ciphertext. The payload field definitions are all described in plaintext in this specification. When it is helpful, we may use affix `_ciphertext` or the adjetive confidential to indicate that the data therein is actually encrypted ciphertext of what is being presented.

The TSP payload may be recursively nested where a payload field may itself be a TSP message. See [Nested Messages](#nested-messages). The terms of payload and payload field therefore must only be understood as relative within the current level of payload structure being referenced.

```text
TSP_Payload = {TSP_Payload_Tag, TSP_Payload_Type, TSP_Payload_Field1, ...}
```

The TSP defines payload types that are used for [Nested Messages](#nested-messages), [Routed Messages](#routed-messages-through-intermediaries), and the higher level management of TSP operations [Control Messages](#control-messages).

Higher layer application messages use the general payload type `TSP_GEN`.

#### Payload Fields

Each payload consists of a type and a number of fields determined by the type. They will be defined in the corresponding sections when their functions are defined.

Some payload fields are required by TSP, including the sender VID `VID_sndr` used for ESSR operations and VID list used in routing mode. When it is necessary to differentiate these fields, we will refer them as Control Fields or Control Payload Fields. These control fields are used for all messages, not just control messages.

#### Ciphertext of the Confidential Payloads

If TSP_Payload is confidential, the corresponding ciphertext is produced as:

```text
TSP_Payload_Ciphertext = TSP_SEAL(TSP_Payload)
```

The details of the supported PKAE schemes for the `TSP_SEAL` operation are specified in Section [Cryptographic Algorithms](#cryptographic-algorithms).

For PKAE schemes *HPKE-Base* ([[spec-norm:RFC9180]]) and *Libsodium Sealed Box* ([[ref:Sealed Boxes]]), the `VID_sndr` MUST appear as a confidential payload field following the ESSR scheme. See [Section 8](#cryptographic-algorithms) for the details.

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

Endpoint `A` learns a `VID_b` of endpoint `B` via either [Out of Band Introduction](#out-of-band-introductions) or other TSP [relationship formation messages](#control-payloads). At this point, endpoint `A` chooses `VID_a` and performs necessary verification and appraisal operations on `VID_b` with respect to `VID_a`. If this verification is successful, endpoint `A` may add a relationship `<VID_a, VID_b>` to its relationship table.

Afterwards, endpoint `A` may resolve `VID_b` to obtain a transport layer address for delivery of a TSP message with `VID_a` as the sender `VID_sndr` and `VID_b` as the receiver `VID_rcvr`.

When endpoint `B` receives this TSP message, if this is the first TSP message from `VID_a` to `VID_b` and endpoint `B` has not verified `VID_a` before, endpoint `B` will perform the necessary verification and assessment to evaluate `VID_a` with respect to `VID_b`. If successful, endpoint `B` may also add a relationship `<VID_b, VID_a>` to its relationship table.

In short, one successful TSP message exchange between two endpoints populates one relationship on each endpoint's relationship table. The relationships in their respective tables are the mirror image of each other in the form of `<VID_local, VID_remote>`. We may interprete this relationship as the state that the endpoint has verified `VID_remote` with respect to `VID_local`. We say the pair of VIDs are in a *verified* state. Note that due to the the asynchronous nature of TSP messages such a state is not always synchronized between the two endpoints. Their relationship tables are not guaranteed to be accurate.

Since endpoints may reuse VIDs, an endpoint may have relationships `<VID_a, VID_b>` and `<VID_a, VID_c>` in its relationship table at the same time. Only a pair uniquely identifies a relationship in TSP.

Endpoints may have semantic meaning or application specific meanings ssociated with their VIDs. For this reason we say an endpoint `A` verifies and assesses a `VID_b` with *respect to* `VID_a`. This evaluation process may have dependecy based on the chosen `VID_a`.

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
- Step 6: Decrypt the `TSP_Payload_Ciphertext`. 
- Step 7: If the PKAE variant requires, retrieve the sender VID from the decrypted payload plaintext and verify that it matches `VID_sndr`.
- Step 8: Process the rest of the control fields.
- Step 9: Return the payload to the upper layer application.

### Out of Band Introductions

Before an endpoint `A` can send the first TSP message to another endpoint `B` it must somehow discover at least one VID that belongs to `B`. If A also wishes to utilize Routed Mode, as specified in [Section 5](#routed-messages-through-intermediaries), then additional VIDs may also be needed before the first TSP routed message can be sent. We call any such method that helps the endpoints discover such prerequisite information an [[ref:Out of Band Introduction]]. There may be many such OOBI methods. Detailed specifications of OOBI methods are out of scope for this specification.

For the purpose of TSP, information obtained from OOBI methods must not be assumed authentic, confidential, or private, although vierification and security mechanisms to remedy such vulnerabilities should be adopted whenever possible. TSP implementations must handle all cases where the OOBI information is not what it appears.

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

In this scheme, the inner message MUST use the confidential payload of the outer message in order to achieve the protection of the inner message metadata. Other than that, we do not restrict the structures of inner and outer messages. For example, if the endpoints do not find the need for additional encryption of the inner message, they MAY choose to use the non-confidential payload for the inner message payload data. Applications should be aware that the confidentiality assurances would only be extended to the outer relationship if the inner message is embedded in the non-confidential field of the outer message.

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
- `VID_exit`: This is the VID used by `hopk` intermediary for its direct relationship with the destination.

The exact nature of how the intermediaries exchange necessary information in order to perform the routing of TSP messages needs not be fixed or follows a pre-determined way. We describe some ways in which this may be accompalished but implementors are free to use other ways to achieve the same goal.

### Routed Messages

For routed messages, we need to distinguish the terms “sender”, “source”, “receiver”, and “destination". We reserve the terms “sender” and “receiver” for direct neighbor relationships between whom the message is being transported from one party to another (i.e. being routed). We reserve the terms “source” and “destination” for endpoint-to-endpoint relationships between whom the carried inner message is being communicated.

As we will see below, the source endpoint MAY choose the first hop of the route, then must acquire the remaining route path information `[VID_hop2, ..., VID_hopk, VID_exit]` before it can attempt to route a TSP message through a series of intermediary hops. This route path information MAY be acquired in part from an [Out-Of-Band Introduction](#out-of-band-introductions), TSP control message ([Section 7](#control-messages)), or may be communicated by other means outside the scope of this specification.

For the common case of `k = 1 or k = 2`, the route hop list MAY be acquired via a simple arrangement:
- The source endpoint `A` chooses an intermediary `P` and establishes a relationship with `P`, `(VID_a1, VID_p1)`, then `VID_hop1` is `VID_p1`. This VID is used as the `VID_rcvr` in the envelope.
- The destination endpoint `B` chooses an intermediary `Q` and establishes a relationship with `Q`, `(VID_b1, VID_q1)`, then `VID_exit` is `VID_q1`. The intermediary `Q`, as a common service provider, may have published a well-known public `VID_q0`, then `VID_hop2` could be `VID_q0`.
- The destination endpoint `B` MAY share the routing information `(VID_q0, VID_b1)` in the Out-Of-Band Introduction mechanism or via a control payload TSP message in another TSP relationship, together with its chosen `VID_destination`.
- The source endpoint `A` combines the routes together to form the whole message: `[VID_a1, VID_p1, VID_q0, VID_b1, Payload]`.
- If the intermediary chosen by `B` is also acceptable to `A`, and the parties accept a single intermediary (with the potential loss of some metadata protection), then the resulting route may simply be `[VID_sndr, VID_intermediary_rcvr, VID_exit, Payload]`.

TSP routed messages have the same TSP Envelope as TSP messages sent in direct mode but extend the control field of the payload with the following structure:

``` text
Control_Payload_Fields = {VID_sndr|NULL, VID_hop2, ..., VID_hopk, VID_exit}
```
The first VID in the control fields `VID_sndr` is the VID required by ESSR PKAE schemes. If a PKAE scheme does not require this field, for example `HPKE_Auth`, then this MAY be NULL.

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
[VID_a1, VID_p1, VID_q0, VID_q1, Payload]
```

Again, the VIDs (`VID_q0` and `VID_q1`) may become known to endpoint `A` prior to this step via an OOBI, a TSP control payload, or another discovery protocol out of scope of this specification. Note that in this outer layer, all VIDs are public while `p0` and `q0`, as public VIDs of intermediaries may also be well-known.

#### The Source Endpoint's Intermediary

The source’s intermediary `P` MUST support routed messages. As previously specified, the intermediary MUST decrypt the payload, if the payload is confidential then process its control fields to retrieve the route VID(s). The next VID in the list, `VID_q0` in this case, is the next hop’s VID. `P` MUST attempt to route the carried message to the next hop if not barred by administrative or operational conditions from doing so.

If the `(VID_p0, VID_q0)` relationship is pre-existing, `P` will already know how to forward the message. If it is not pre-existing but `VID_q0` is public, `P` can resolve it and establish a new `<VID_p0, VID_q0>` or `(VID_p0, VID_q0)` relationship using normal procedures specified in [Section 3](#messages). `P` then routes the message to `Q` using the following message:

``` text
[VID_p0, VID_q0, VID_q1, Payload]
```

Note that the new `VID_sndr` and `VID_rcvr`, and the shortened VID route list (`VID_q1` only).

#### The Destination Endpoint's Intermediary

The destination’s intermediary, `Q`, also decrypts, if it's confidential, the control payload fields to retrieve the remaining route VID list. The next VID in the list, `VID_q1`, is the next hop’s VID. `Q` must attempt to route the carried message to the next hop.

If `VID_q1` is given to endpoint `A` by `B` itself in either an Out-Of-Band Introduction or a TSP control payload message, the `<VID_q1, VID_b1>` or `(VID_q1, VID_b1)` relationship should be pre-existing, and `Q` will know how to forward the message. If that relationship is not found in its local relationship table (ie the relationship hasn't been established), the intermediary `Q` should consider this an error. Otherwise, `Q` forwards this message to endpoint `B` using the following direct message:

``` text
[VID_q1, VID_b1, Payload]
```

Note that this is a normal direct message as the route VID field is now empty.

#### The Destination Endpoint

When the destination receives the message it is now a normal direct mode message: `[VID_q1, VID_b1, Payload]`. Note that endpoints are not required to handle routed messages that contain additional next hop VID or VIDs.
Unlike direct mode messages, this message’s sender `VID_q1` is of the intermediary `Q`, but the source `A`; and its receiver `VID_b1` is associated with the relationship with `Q`, not `A`. This means that the destination endpoint `B` can not be assured of the message’s authenticity, confidentiality, or metadata privacy. To solve these problems, endpoints MUST use additional procedures specified in the following sections.

### Endpoint-to-Endpoint Messages


In [Section 5.3](#direct-neighbor-relationship-and-routing), we defined a routed operation method that enables a source endpoint to send a TSP message to a destination endpoint via a series of intermediaries, using a hop-by-hop approach. However, while this approach provides a way of message delivery from the source to the destination, it doesn't uphold the core trust properties TSP aims to provide — specifically, authenticity, confidentiality, and metadata privacy — with respect to third parties or intermediaries. In this section, we define endpoint-to-endpoint messages carried within the payload of routed messages and the corresponding endpoint-to-endpoint relationship which does ensure authenticity, confidentiality, and a degree of metadata privacy. This operation is illustrated in Figure 3 below.

![Endpoint-to-Endpoint Relationship Through a Routed Path](images/Endpoint-to-Endpoint-Relationship-Through-A-Routed-Path.png)

Figure 3: Endpoint-to-Endpoint relationship between endpoints A and B through a routed path

#### The Source Endpoint

The source endpoint `A` will create an endpoint-to-endpoint relationship with endpoint `B` using the same procedure specified in [Section 3](#messages). Instead of direct messages as in Section 3, the endpoint `A` will use routed messages defined in [Section 5.3](#direct-neighbor-relationship-and-routing). Recall in Section [5.3.1](#the-source-endpoint), endpoint `A` sends the following message to intermediary `P` en route to eventual destination `B`:
``` text
[VID_a1, VID_p1, VID_q0, VID_q1, Payload]
```
To create an endpoint-to-endpoint relationship between `A` and `B`, Endpoint `A` will encapsulate its [relationship forming message](#control-messages) with endpoint `B` as follows:

``` text
[VID_a1, VID_p1, VID_q0, VID_q1, [VID_a2, VID_b2, Payload_e2e]]
```

Because this is the first layer where endpoint-to-endpoint communication takes place, the source MUST use its own encryption and signing and not opt out as described in [Section 4](#nested-messages).

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
[VID_a1, VID_p1, VID_q0, VID_q1, [VID_a2, VID_b2, Payload_e2e]]
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

### Multi-Recipent List

In this scheme, an endpoint maintains a list of relationships `(VID_0, VID_remote_i)` where `VID_0` is a local VID, and `i = 1..K-1`. For each message payload, one copy of a TSP message is sent over each relationship: `[VID_0, VID_remote_i, Payload], i = 1..K-1`.

For a group of `K` member endpoints, there will be `K-1` bi-directional relationships at each endpoint. The total mesh group consists of `K(K-1)` relationships. If these are all simple Direct Mode relationships, each endpoint will use one VID for the group.

Endpoints in such a group MAY also use Nested Mode and Routed Mode as they wish for each or all of these relationships.

Each TSP message is duplicated and individually encrypted (if confidential) over each relationship.

The group membership management mechanism MAY be implemented using third party relationship referral. For example, if `endpoint_0` has one existing individual relationship with each other member `endpoint_i, i = 1..K-1`, then `endpoint_0` may use those relationships to help establish relationships `(endpoint_i, endpoint_j), i, j in range of 1..K-1, i != j`.

Please refer to [Section 7](#control-messages) for details of relationship referral control messages.

### Anycast Intermediary

A common use case of sending TSP messages to multiple recipents is to anycast authenticated but not encrypted messages to anyone who is interested in receiving them, e.g. by subscribing to a messaging service or by social media recommendation algorithms.

Since these messages are not confidential, the distribution of these messages can be performed by an intermediary. For details of such TSP messages, see Section [3.5.2](#authentic-non-confidential-anc-messages).

Although these messages are authenticated to a sender's VID, the messages between the sender and its intermediary can still be confidential. In fact, they can be communicated from the source to its intermediary over a Nested Mode relationship specific to the anycast group (or similar notions supported by the intermediary). The details of such mechanisms are out of scope for this specification.

## Control Messages

This section specifies control payload fields that are required for the proper functioning of TSP. TSP Messages that carry such *control fields* can be informally referred to as *Control Messages*. This naming convention is not exactly precise however as what we typically consider fields, such as VID_sndr and VIDs of intermediary hops, are also payload fields used for TSP control functions. To contrast with the payload fileds used for control functions, we refer other fields in the payload *data fields*.

For either Direct Mode or Routed Mode endpoint-to-endpoint relationships, Authentic and Confidential (AAC) messages defined in [Section 3.5.1](#authentic-and-confidential-aac-messages) SHOULD be used with control data being carried in the confidential payload fields.

Both the control and data sections of the payload are extendable. While we define the necessary TSP control fields here, higher layers have the flexibility to expand upon them. This structure ensures a standardized approach for the essential components of the message while allowing adaptability for specific use cases or additional requirements at the higher layer. 

### Relationship Forming Protocol
#### TSP Digest

TSP uses a *self referencing* or *self addressing* digest in its relationship forming protocol messages defined below. It is calculated according to the *SAID* (Self Addressing Identifier) convention as described in the [[ref:CESR]] specification. The supported hash or digest functions are listed in section [Secure Hash and Digest Functions](#secure-hash-and-digest-functions). 

TSP Digest is calculated and contained in the message that it is based on. In a bi-directional relationship formation exchange, the request message contains its own TSP Digest field which identifies the request message, and the reply message contains both the Digest it received from the requester and its Reply_Digest. Conceptually, this exchange creates two uni-directional relationships, one (from the requester) can be identified by the Digest, and the other (From the replier) can be identified by the Reply_Digest.

In describing this digest field, we will use TSP_DIGEST in the content of the payload which should be interpreted as the result of the above self referential calculations over the payload (excluding any padding that may be introduced).

The sender and receiver of these TSP digests SHOULD save them as part of the relationship state if they wish to use them as a thread identifier or to validate the relationship formation process in the future.

#### Direct Relationship Forming
When an endpoint `A` learns  the VID for another endpoint `B`, say `VID_b`, through an Out-Of-Band Introduction method, the endpoint `A` MAY use the following message type to form a direct relationship with `B`. Suppose the source VID that endpoint `A` uses is `VID_a`, then the relationship A and B establishes is `(VID_a, VID_b)`.
``` text
Out-Of-Band Introduction to A: VID_b
The relationship forming message from A to B: [VID_a, VID_b, Payload]
Payload fields:
    - Type = TSP_RFI (Relationship Forming Invite)
    - Digest = TSP_DIGEST
    - Nonce_Field = Nonce
```
This `TSP_RFI` is not strictly required for forming a relationship between two *direct* endpoints. It is permissible that one endpoint which has learned a VID of the other simply starts with an application level message without first having an exchange of TSP control messages. In such cases, it is up to the application or the Out-of-Band Introduction mechanism or other means that they make acceptance decisions. Similarly, they will not have the digests embedded in the `TSP_RFI` (or `TSP-RFA`) and again, it is up to the application to create another form of identifier or their own digest.

Endpoint `B` retrieves and verifies `VID_a`, and if agrees, replies with the following:
``` text
Message: [VID_b, VID_a, Payload]
Payload fields:
    - Type = TSP_RFA (Relationship Forming Accept)
    - Digest = Digest of the corresponding `TSP_RFI`
    - Reply_Digest = TSP_DIGEST
```

The result is a bi-directional relationship `(VID_a, VID_b)` in endpoint `A` and `(VID_b, VID_a)` in endpoint `B`. The Digest is recorded by both endpoints and can be used in future messages in `<VID_a, VID_b>`, and similarly Reply_Digest for `<VID_b, VID_a>`.

If endpoint `B` fails to verify `VID_a`, it SHOULD silently drop the message and MAY direct the transport layer to disconnect or otherwise block or filter out further incoming messages from `VID_a` for a period of time..

If endpoint `B`, for any other reason, does not want to or can not engage with endpoint `A`, it MAY simply remain silent (if `B` does not want to give `A` any private information), or it MAY reply with a `TSP_RFD` message as specified in Section [7.4](#relationship-events) with proper event code (if `B` is willing to risk additional information disclosure by providing `A` some useful information). 


If endpoint `B` is OK with receiving the incoming messages from endpoint `A`, but declines to reply to endpoint `A` to establish the opposite direction relationship, it MAY simply remain silent. 

Other actions that endpoint B may take MAY be application specific and are left unspecified.

In all of the above cases, the responding party (endpoint `B`) should be careful about privacy leaks if it chooses to respond to an incoming message. The most private option is to remain silent.

#### Relationship over a Routed Path
Suppose endpoint `A` learns from another endpoint `B` through an Out-Of-Band Introduction method the VID for `B`, say `VID_b`, together with a routing path, `{ …, VID_hopk, VID_exit}`. Endpoint `A` MAY use the following control message to form a relationship with `B`. Suppose the source VID that endpoint `A` uses is `VID_a`, and optionally endpoint `A` specifies a reply path `{ …,  VID_rhopk, VID_rexit}`, then the relationship `A` and `B` establishes is `(VID_a, VID_b)`.

``` text
Out-Of-Band Introduction: VID_b, VID_hop2, …, VID_hopk, VID_exit
The relationship forming message = [VID_a, VID_b, …, VID_hopk, VID_exit, Payload]

Payload fields:
    - Type = TSP_RFI
    - Reply_Path = ..., VID_rhopk, VID_rexit
    - Digest = TSP_DIGEST
    - Nonce_Field = Nonce
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

### Parallel Relationship Forming

If endpoints `A` and `B` have a relationship `(VID_a0, VID_b0)` in `A` and `(VID_b0, VID_a0)` in `B`, they can establish a new parallel relationship using the current relationship as a means of referral.

Endpoint `A` sends to `B` this relationship forming message:

``` text
Message: [VID_a0, VID_b0, …, Payload], 
we omitted the optional route path VID list so this can either a Direct or Routed message.

Payload fields:
    - Type = TSP_RFI
    - New_VID = VID_a1
    - Reply_Path = VID_list | NULL
    - Digest = TSP_DIGEST
    - Nonce_Field = Nonce
    - New_Signature = TSP_SIGN(the preceding payload) by New_VID
```

In this procedure, `VID_a1` is the new VID for endpoint `A`. If endpoint `B` picks `VID_b1` and replies with `TSP_RFA`, then the new relationship `(VID_a1, VID_b1)` is parallel to `(VID_a0, VID_b0)` in endpoint `A`, and similarly in `B`.

If the `VID_List` is present, then `B` MUST use the routed path specified by `VID_List` to send the `TSP_RFA` message to endpoint `A` as defined in the previous section [Relationship over a Routed Path](#relationship-over-a-routed-path).

``` text
Return message: [VID_b1, VID_a1, …, Payload]
Payload fields:
    - Type = TSP_RFA
    - Digest = Digest of the corresponding `TSP_RFI`
    - Reply_Digest = TSP_DIGEST
```

### Nested Relationship Forming

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
Do we want to keep an option to provide verification information in the TSP_RFI itself?
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
    - New_VID = VID_a2
    - Reply_Path = VID_list | NULL
    - Digest = TSP_DIGEST
    - Nonce_Field = Nonce
    - New_Signature = TSP_SIGN(the preceding payload) by New_VID
```
And endpoint `B` replies with:

``` text
Return message: [VID_b0, VID_a0, ..., [VID_b2, VID_a2, Payload]]
Payload fields:
    - Type = TSP_RFA
    - Digest = Digest of the corresponding `TSP_RFI`
    - Reply_Digest = TSP_DIGEST
```

### Third Party Relationship Referral

::: issue
Consider to remove this section. Leave more complex relationship forming procedures to further study?
:::

If endpoints `A` and `B` have a relationship `(VID_a0, VID_b0)` (for brevity, we will use either one of the two directions to represent both in this section), and endpoints `A` and `C` have a relationship `(VID_a0, VID_c0)`, then `A` can help endpoints `B` and `C` establish a new relationship using their respective current relationship with `A` as a way of referral.

This referral process takes 3 steps:
- Endpoint `A` sends referral to `C` (or alternatively to `B`)
- Endpoint `C` sends relationship forming message to `B`
- Endpoint `B` replies to `C`

The last two steps use relationship forming messages already defined in previous sections. We define new control fields used in the first referral step below.

Endpoint `A` sends to `C` this message as a third party referral to invite `C` to form a relationship with `B`:

``` text
Message: [VID_a0, VID_c0, …, Payload], 
we omitted the optional route path VID list so this can either a Direct or Routed message.

Control payload fields:
    - Type = 3P_REFER_REL
    - Referred VID: VID_b0
    - Route Hop List: VID_List | NULL
```
When endpoint `C` receives this message from `A`, it treats it as an introduction, then `C` initiates a normal new relationship forming procedure as specified in Section [7.1](#relationship-forming). The resulting relationship between `B` and `C` is `(VID_b0, VID_c0)`.

If `VID_List` is present, then `C` uses the specified routed path, in part, to send the `TSP_RFI` message to endpoint `B`.


### Relationship Forming Decline or Cancel
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
    - Digest = the previously received Digest or Reply_Digest, NULL if there is none
    - Nonce_field = Nonce
```
Note that the Nonce is added here to prevent easy attacks when the Digest is NULL.

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
    - Nonce_field = Nonce
```
### Relationship Events

#### Padding Message

A padding message is a TSP message with a payload containing only a padding field besides required control fields. Such padding messages MAY be used as a mechanism to defend against traffic analysis based threats. The payload type is `TSP_PAD`.

If endpoint `A` chooses to send a padding message to `B`, the message will be as follows:

``` text
Message: [VID_a, VID_b, Payload]
Payload fields:
    - Type = TSP_PAD
    - Nonce_field = Nonce
    - Padding_field = Padding
```

The receiver SHOULD silently discard padding messages.

Note that an upper layer protocol may send their own similar messages without no real content. In that case, however, the payload type would be `TSP_GEN`.

#### Key Update

::: issue #7
Key rotation is TBD - define out-of-band only.
https://github.com/trustoverip/tswg-tsp-specification/issues/7
:::

#### Route Info

An Intermediary MAY send a TSP message to either another Intermediary or an endpoint to report route related information that MAY be useful for diagnoses or other legitimate purposes.

::: issue #8
TODO
https://github.com/trustoverip/tswg-tsp-specification/issues/8
:::

## Cryptographic Algorithms

TSP utilizes VIDs that are strongly bound to public-key pairs. The authenticity and confidentiality properties of TSP rely on public-key signature and encryption schemes based on public-key cryptography. In this section, we specify the supported cryptographic schemes and how they combine together as a TSP crypto suite. The choices we make here reflect our priorities to:
- achieve the strongest notions of security with respect to modern and efficient algorithms,
- have clear specifications in standards for interoperability,
- prefer schemes that have high quality open source implementations. 

The overall design and use of self-framed encoding allows TSP easy adaptability to future requirements, including new cryptographic schemes and the implementation of post-quantum cryptography.

TSP combines public-key authenticated encryption (PKAE) with public-key signatures. This combination is necessary for several reasons:
- In TSP, authenticity (both the identity of the sender and integrity of the message) is required for all messages while confidentiality is optional.
- PKAE schemes have weaknesses, such as Post Compromise Impersonation (PCI) attacks, which TSP aims to guard against in order to support its wider use cases.

### Public-Key Signatures
`Ed25519` is an EdDSA signature algorithm using `Curve-25519` and `SHA2-512` as defined in IETF [[spec-norm:RFC8032]]. 

Ed25519 supports a stronger sense of unforgeability, namely SUF-CMA (Strong UnForgeability under Chosen Message Attack).

TSP implementations MUST support Ed25519.

::: note
This implementor's draft only specifies one signature scheme at the moment. Future drafts will add additional signature schemes.
:::

#### Post-Quantum Signatures

This section is in early experiemental draft status. We aim for demonstrating future support of Post-Quantum Digital Signature Algorithms in TSP.

For early implementations, we recommend for ML-DSA as defined in [[FIPS204]]. ML-DSA (Module-Lattice-Based Digital Signature Algorithm) is also known as the CRYSTALS-Dilithium algorithm.


### Public-Key Authenticated Encryption

TSP uses strong public key encryption schemes that supports IND-CCA2 (Indistinguishability under Adaptive Chosen Ciphertext Attack). These schemes are also called Integrated Encryption Schemes (IES), ECIES if using Elliptic Curves, or Hybrid Public Key Encryption (HPKE) since they combine public key cryptography with the efficiency of symmetric key encryption/decryption operations. These schemes follow similar designs that incorporate a key exchange mechanism (KEM), a key derivation function (KDF), and a symmetric encryption scheme using the ephemeral derived key, or formalized as an Authenticated Encryption with Associated Data (AEAD) function. The use of AEAD also leads to the acrynym PKAE (public-key authenticated encryption). We use the term PKAE as a general term for this class of algorithms.  

#### TSP Encryption and Decryption Primitives

TSP defines a standard way to encrypt a single TSP message to a receiver's public key. The operations use the following `seal` and `open` primitives.

``` text
Ciphertext = TSP_SEAL(VID_sndr, VID_rcvr, Non_Confidential_Data, Plaintext)
Plaintext = TSP_OPEN(VID_sndr, VID_rcvr, Ciphertext)
```

This section specifies all PKAE schemes that TSP implementations MUST or optionally SHOULD support.

#### Hybrid Public Key Encryption (HPKE) 

HPKE is a draft standard defined in IETF [[spec-norm:RFC9180]] which formalizes and generalizes similar schemes and implementations that support encryption of messages for a receiver with a public-private key pair. [[spec-norm:RFC9180]] defines a framework from which we specify a subset of concrete configuration to best meet TSP requirements. HPKE uses modern cryptographic algorithms and has been studied with proofs of IND-CCA2 security. The HPKE base mode does not use sender authentication in the HPKE itself. The algorithms in a HPKE suite are KEM (Key Exchange Mechanism), KDF (Key Derivation Function), and AEAD (Authenticated Encryption with Associated Data function). Schemes that follow [[spec-norm:RFC9180]] have seen adoption in Messaging Layer Security [[spec-inform:RFC9420]] and TLS Encrypted ClientHello [[TLS-ECH]].

TSP implementations MUST support both HPKE-Auth and HPKE-Base modes.

##### HPKE Cryptographic Algorithm Suite

HPKE configuration(s) supported by TSP:

Primitive | Code | Description
----:|----:|--------:
KEM | 0x0020 | DHKEM(X25519, HKDF-SHA256)
KDF | 0x0001 | HKDF-SHA256
AEAD | 0x0003 | ChaCha20Poly1305

##### HPKE Auth Mode

In the HPKE-Auth mode, for TSP message that uses confidential payload, the ciphertext MUST generated by HPKE-Auth single-shot API defined in [[spec-norm:RFC9180]] as follows:

``` text
def TSP_SEAL(VID_sndr, VID_rcvr, Non_Confidential_Fields, Confidential_Fields_Plaintext):
    skS = VID_sndr.SK_e
    pkR = VID_rcvr.PK_e
    aad = CONCAT(VID_sndr, VID_rcvr, Non_Confidential_Data)
    info = NULL
    pt = Plaintext
    enc, ct = SealAuth(pkR, info, aad, ct, skS)
    return CONCAT(enc, ct)

Ciphertext = TSP_SEAL(VID_sndr, VID_rcvr,
                Non_Confidential_Fields, 
                Confidential_Fields_Plaintext)

```
The receiver MUST use the corresponding single-shot API to decrypt:

``` text
def TSP_OPEN(VID_sndr, VID_rcvr, Non_Confidential_Fields, Confidential_Fields_Ciphertext):
    pkS = VID_sndr.PK_e
    skR = VID_rcvr.SK_e
    aad = CONCAT(VID_sndr, VID_rcvr, Non_Confidential_Fields)
    info = NULL
    enc, ct = SPLIT(Confidential_Fields_Ciphertext)
    return OpenAuth(enc, skR, info, aad, ct, pkS)

Plaintext = TSP_OPEN(VID_sndr, VID_rcvr, 
                Non_Confidential_Fields, 
                Confidential_Fields_Ciphertext)
```

In HPKE-Auth mode, the `VID_sndr` field is not necessary in the confidential control payload (as required by [[spec:ESSR]]).

##### HPKE Base Mode

The HPKE-Base mode works similarly to HPKE-Auth except that it does not include the authentication mechanism allowing the receiver to verify that the sender possessed a given KEM private key `VID_sndr.SK_e`. Leaving this verification out MAY be acceptable because TSP also has `VID_sndr` in the encrypted payload ciphertext and a separate signature for sender authentication. For additional discussions comparing the HPKE-Base mode and HPKE-Auth mode use in TSP, please refer to Section [Security and Privacy Considerations](#security-and-privacy-considerations).

The HPKE-Base mode will also be required if, in the future, TSP supports non-authenticated KEMs.

In the HPKE-Base mode, for a TSP message that uses a confidential payload, the ciphertext MUST generated by HPKE-Base single-shot API defined in [[spec-norm:RFC9180]] as follows:

``` text
def TSP_SEAL(VID_sndr, VID_rcvr, Non_Confidential_Fields, Confidential_Fields_Plaintext):
    pkR = VID_rcvr.PK_e
    aad = CONCAT(VID_sndr, VID_rcvr, Non_Confidential_Fields)
    info = NULL
    pt = Confidential_Fields_Plaintext
    enc, ct = SealBase(pkR, info, aad, pt)
    return CONCAT(enc, ct)

Ciphertext = TSP_SEAL(VID_sndr, VID_rcvr,
                Non_Confidential_Fields, 
                Confidential_Fields_Plaintext)

```
The receiver MUST use the corresponding single-shot API to decrypt:

``` text
def TSP_OPEN(VID_sndr, VID_rcvr, Non_Confidential_Fields, Confidential_Fields_Ciphertext):
    skR = VID_rcvr.SK_e
    aad = CONCAT(VID_sndr, VID_rcvr, Non_Confidential_Fields)
    info = NULL
    enc, ct = SPLIT(Confidential_Fields_Ciphertext)
    return OpenBase(enc, skR, info, aad, ct)

Plaintext = TSP_OPEN(VID_sndr, VID_rcvr, 
                Non_Confidential_Fields, 
                Confidential_Fields_Ciphertext)
```

In HPKE-Base mode, the `VID_sndr` field MUST be present in the confidential control payload (as required by [[spec-inform:ESSR]]).

#### HPKE PQ and PQ/T Algorithms

This section is in early draft status. We aim for demonstrating potential support of Post-Quantum (PQ) and Post-Quantum and Traditional hybrid (PQ/T) algorithms within the HPKE specification framework, as (to be) defined in the ongoing work [[HPKE-PQ]].

For the early experimentation, we recommend the ML-KEM (the NIST Module-Lattice-Based Key-Encapsulation Mechanism) as defined in [[FIPS203]]. The ML-KEM is also known as the CRYSTALS-Kyber algorithm.

#### Lipsodium Sealed Box

Libsodium is a popular open source software library that is a fork of [[spec-inform:NaCl]]. Among many modern and easy-to-use cryptographic tools, it provides an implementation of a crypto\_box primitive that is essentially a non-standardized PKAE scheme. We specify a way for TSP to use the lipsodium sealed box API as a PKAE choice here because of its popularity. However, since the sealed box API is not standard alongside the fact that the Lipsodium community is also implementing HPKE options in parallel, implementors SHOULD consider migrating to one of the HPKE options. We MAY remove this option in the future.

##### Sealed Box

Per [[spec-norm:libsodium]] documentation, the combined mode API defined in `C` is as follows.

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
`crypto_box_seal_open()` decrypts the ciphertext `c` of length `clen` using the sender's public key `pk` and the receiver's secret key `sk`, and outputs the plaintext to `m`.

##### TSP Use of Sealed Box for PKAE

To use sealed box as the PKAE in TSP, for TSP message that uses confidential payload, the ciphertext MUST generated by `crypto_box_seal()` API as follows (in pseudocode) or an equivalent procedure:

``` text
def TSP_SEAL(VID_sndr, VID_rcvr, Non_Confidential_Fields, Confidential_Fields_Plaintext):
    pkR = VID_rcvr.PK_e
    pt = Confidential_Fields_Plaintext
    mlen = Length(pt)
    ciphertext = crypto_box_seal(pt, mlen, pkR)
    return ciphertext

Ciphertext = TSP_SEAL(VID_sndr, VID_rcvr,
                Non_Confidential_Fields, 
                Confidential_Fields_Plaintext)
```

The receiver MUST use the corresponding `crypto_box_seal_open()` API procedure or an equivalent to decrypt:

``` text
def TSP_OPEN(VID_sndr, VID_rcvr, Non_Confidential_Fields, Confidential_Fields_Ciphertext):
    pkS = VID_sndr.PK_e
    skR = VID_rcvr.SK_e
    ct = Confidential_Fields_Ciphertext
    clen = Length(ct)
    output = crypto_box_seal_open(ct, clen, pkS, skR)
    return output

Plaintext = TSP_OPEN(VID_sndr, VID_rcvr, 
                Non_Confidential_Fields, 
                Confidential_Fields_Ciphertext)
```

Similar to HPKE-Base mode, the sealed box API also does not have sender authentication, and therefore the `VID_sndr` field MUST be present in the Confidential Control Fields (as required by [[spec-inform:ESSR]]).

##### Sealed Box Cryptographic Algorithms

Per [[spec-norm:libsodium]] documentation, the sealed box API leverages the `crypto_box` construction which in turn uses `X25519` and `XSalsa20-Poly1305`, and uses `blake2b` for nonce. As a non-standard implementation, such information is not precisely known and is implementation specific depending on the open source development of lipsodium.

### Secure Hash and Digest Functions

All TSP implementations MUST support the following secure hash and digest functions. They can be used for nonce and digest constructions as the operator TSP_DIGEST.

- SHA2-256 [[spec-norm:RFC6234]]

- Blake2b [[spec-norm:RFC7693]]

## Serialization and Encoding

TSP uses CESR [[ref:CESR]] version 2.0 (master code table for `--AAACAA`) for message serialization and encoding. The TSP payload however may have data encoded in other formats including CBOR, JSON, and MsgPak that are compatible formats to interleave within CESR streams.

In this section, we describe the relevant CESR codes used in TSP.

### TSP Envelope Encoding
The TSP Envelope consists of four objects: TSP_Tag, TSP_Version, VID_sndr, VID_rcvr. Each VID is a VID_String. The CESR encoding of these are as follows.

Object | Description | Code | Note
----:|----:|--------:|--------:
TSP_Tag | Indicating the start of a TSP envelope | `-E##` or `-0E#####`| Use `-E##` for signable data up to 4095 quadlets/triplets, `-0E#####` for signable data up to 1,073,741,823 quadlets/triplets. The length does not include signature part.
TSP_Version | TSP protocol version | `YTSP-###` | The first version is `YTSP-AAB`
VID_String | short VID with lead pad size 0 | `4B##` | The VID string is in a variable length of either 2 Base64 size characters limited to 4095 quadlets/triplets (short VID) or 4 Base64 characters limited to 16,777,215 quadlets/triplets (long VID). In each case, there are 3 variations depending on the lead pad size of 0, 1, or 2.
 ^ | short VID with lead pad size 1 | `5B##` | ^ 
 ^ | short VID with lead pad size 2 | `6B##` | ^ 
 ^ | long VID with lead pad size 0 | `7AAB####` | ^ 
 ^ | long VID with lead pad size 1 | `8AAB####` | ^ 
 ^ | long VID with lead pad size 2 | `9AAB####` | ^ 

::: note
CESR uses a unit of 4 Base64 letters (Quadlet) to represent an equivalent unit of 3 bytes in binary (Triplet). Therefore, a two letter count code `0E##` in text domain provides a value in range of 0 to 4095 (`64 x 64 - 1`) where each unit is a quadlet/triplet. The corresponding value in actual bytes in binary is 12,285 (`4095 x 3`). Similarly, `-0E#####` provides 0 to 1,073,741,823 (`64^5 - 1`) quadlets/triplets which corresponds to 3,221,225,472 bytes in binary.
:::

### TSP Payload Encoding
TSP payload consists of a `TSP_Payload_Tag`, a number of `Payload_Field`, followed by `Confidential_Payload_Ciphertext` as specified in [TSP Payload](#tsp-payload). We first describe the encoding of this simple structure then the encodings of [Nested Messages](#nested-messages) and [Routed Messages](#routed-messages).

The payload fields include *control fields* that are required for the correct operations of TSP. Encodings of all required control fields are defined below. Higher layer application *data fields* may use broader CESR encoding mechanisms including interleaving JSON, CBOR or MsgPak encodings.

#### TSP Payload Tag
Object | Descryption | Code | Note
----:|----:|--------:|--------:
TSP Payload | short or long TSP payload | `-Z##` or `-0Z#####` | Use `-Z##` for payloads up to 4095 quadlets/triplets, `-0Z#####` for up to 1,073,741,823 quadlets/triplets

#### Payload Field Types
Following the Payload Tag is a number of payload fields. Each field is encoded with a payload type and additional data depending on the type. The top level TSP payload field types consist of the following CESR codes using the three character code table starting with `X` as defined in CESR [[ref:CESR]] version 2.0 (master code table for `--AAACAA`).

Object | Descryption | Code | Note
----:|----:|--------:|--------:
CTL | generic control payload field | `XCTL` | The CESR code for 3-character quadlets/triplets is `X`. The `CTL` type allows control messages in unrestricted generic format.
SCS | upper layer payload | `XSCS` | The acrynym "SCS" stands for `sniffable CESR stream`, which is treated as a single object that the upper layer decides how to process. Upper layer payload should be encoded as an SCS type.
HOP | a nested messge that includes a list of VID hops | `XHOP` | This type is used for nested and routed messages
PAD | variable length padding | `XPAD` | This type is used to generate messages that carry no meaningful information other than its metadata.
RFI | relationship forming invite | `XRFI` | Invitation to form a new TSP relationship
RFA | relationship forming accept | `XRFA` | Accepting a new TSP relationship in response to a RFI, thereby forming a bi-directional relationship
RFD | relationship forming decline | `XRFD` | Declinging a new TSP relationship in response to a RFI, or as an cancellation of an existing relationship

#### Higher Layer Payload

Higher layer application payload (Type = `TSP_GEN`) MUST use type encoding `XSCS` followed by a generic CESR stream including supported interleaving of JSON, CBOR, and MsgPak encoded data. 

The generic CESR stream MUST use the CESR count code `-A##` (for shorter length) or `-0A####` (for longer length).

The overall higher layer payload is as follows:

``` text
-Z## | -0Z####, XSCS, VID_sndr, Padding_field, -A## | -0A####, higher-layer-interleaved-payload-stream
```
where, ## or #### stands for a 2 or 4, respectively, character code of the length of the payload. All counts start immediately after the count code, not including the count code itself. The encoding of `VID_sndr` is specified in [VID Envelope Encoding](#vid-envelope-encoding). The encoding of the padding field is specified in [Padding Field](#padding-field).

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
To avoid confusion, the teram padding or padding field means the payload field itself while the shorter pad is the number of 0, 1 or 2 bytes of zero's added in front of the chosen padding field for encoding alignment.
:::

#### VID Hop List Field

The VID hop list field can appear in various messages. It is encoded as follows:

``` text
-J## | -0J####, VID_0, VID_1, ... 
```
Here both ## and #### still represent counts of length of the string that follows which is the concatenation of VIDs, not the number of VIDs. The encoding of each VID is specified in [TSP Envelope Encoding](#tsp-envelope-encoding).

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
HPKE Base Cipher |short length ciphertext | '4F##' | lead pad size 0
HPKE Base Cipher |short length ciphertext | '5F##' | lead pad size 1
HPKE Base Cipher |short length ciphertext | '6F##' | lead pad size 2
HPKE Base Cipher |long length ciphertext | '7AAF####' | lead pad size 0
HPKE Base Cipher |long length ciphertext | '8AAF####' | lead pad size 1
HPKE Base Cipher |long length ciphertext | '9AAF####' | lead pad size 2
HPKE Auth Cipher |short length ciphertext | '4G##' | lead pad size 0
HPKE Auth Cipher |short length ciphertext | '5G##' | lead pad size 1
HPKE Auth Cipher |short length ciphertext | '6G##' | lead pad size 2
HPKE Auth Cipher |long length ciphertext | '7AAG####' | lead pad size 0
HPKE Auth Cipher |long length ciphertext | '8AAG####' | lead pad size 1
HPKE Auth Cipher |long length ciphertext | '9AAG####' | lead pad size 2

The short length `##` counts for ciphertext up to 4095 quadlets/triplets and `#####` for up to 1,073,741,823 quadlets/triplets.

##### HPKE-Auth and HPKE-Base Mode Ciphertext
The HPKE ciphertext consists of the concatenation of the Encapuslated Key structure `enc` and the encrypted payload `ct`.

``` text
HPKE-Auth:
...
enc, ct = SealAuth(pkR, info, aad, ct, skS)
return CONCAT(enc, ct)

HPKE-Base:
...
enc, ct = SealBase(pkR, info, aad, pt)
return CONCAT(enc, ct)
```

The `enc` is defined by HPKE [[spec-norm:RFC9180]] which contains identifiers for KEM, KDF and AEAD functions and a bytestring for the encapsulated key.

Name | Data Type | Value Registry | Description
----:|----:|--------:|--------:
kem\_id | uint | HPKE KEM IDs Registry | Identifier for the KEM
kdf\_id | uint | HPKE KDF IDs Registry | Identifier for the KDF ID
aead\_id | uint | HPKE AEAD IDs Registry | Identifier for the AEAD ID
enc | bstr | NA | Encapsulated key defined by HPKE

The ID values that MUST be supported by TSP:
Primitive | Code | Descryption
----:|----:|--------:
KEM | 0x0020 | DHKEM(X25519, HKDF-SHA256)
KDF | 0x0001 | HKDF-SHA256
AEAD | 0x0003 | ChaCha20Poly1305

::: note
`SHA256` should be read as `SHA2-256`. The HPKE [[spec-norm:RFC9180]] and many other specifications still use `SHA256` to mean `SHA2-256`.
:::

::: note
This implementor's draft only specify a single configuration as above. Additional configurations will be added in the future.
:::

Example:
``` text
Todo
```
##### HPKE PQ and PQ/T Encoding

TBD

##### Lipsodium Sealed Box Encoding
See [[ref:CESR]] on X25519 Sealed Box cipher bytes encoding.

Example:
``` text
Todo
```
#### Interleaved JSON, CBOR or MsgPak Payload
Comformant TSP implementations MUST support the interleaving scheme in [[ref:CESR]] which allows interleaved payloads encoded in JSON, CBOR or MsgPak in addition to native CESR.
Because TSP supports nesting, this interleaving of different encoding methods may occur in the payload field of any nesting level.

Example:
``` text
Todo
```

#### Nested Payload
In TSP Nested Mode, the inner TSP message is carried inside a payload field of the outer TSP message. When the outer message is being parsed, the message may carry a simple application payload or a nested TSP message which will require additional processing.

The outer message MUST be encoded with payload type `XHOP`. If this is a direct relationship nested message, the overall message payload is as follows:

``` text
-Z## | -0Z####, XHOP, VID_sndr, -JAA, Padding_field, Encoded_TSP_Message
```
Because this is a message between direct neighbors, the VID hop list field is empty which is encoded as `-JAA`. The inner message can be any correctly encoded TSP message including its envelope, payload and signature. The starting payload length must count the nested message. 

#### Routed Payload
Routed payload is encoded as a nested payload with a non-empty routing hop list.

``` text
-Z## | -0Z####, XHOP, VID_sndr, -J## | -0J####, VID_1, ..., Padding_field, Encoded_TSP_Message
```
The hop list field encoding is specified in [VID Hop List Field](#vid-hop-list-field). The rest is identifical to nested payload.

#### Control Message Encoding
Control messages are composition of payload fields that are used for TSP's own control mechanisms. The following sections define these payload fields in its plaintext text mode. The actual final encoding will be in ciphertext format as described in [Confidential Payload Ciphertext](#confidential-payload-ciphertext).

##### TSP_RFI

The TSP_RFI payload is specified in [Direct Relationship Forming](#direct-relationship-forming).

```text
-Z## | -0Z####, XRFI, VID_sndr, Digest, Nonce, `4BAA`, Padding_field
```
where `4BAA` is an empty VID. This VID is `4BAA` to indicate that we are *not* signaling a *new* VID from an existing relationship. For the latter case, please see [TSP_RFI in Referal](#tsp_rfi_in_referal).

##### TSP_RFA

The TSP_RFA payload is specified in [Direct Relationship Forming](#direct-relationship-forming).

```text
-Z## | -0Z####, XRFA, VID_sndr, Digest, Reply_Digest, Padding_field
```

##### TSP_RFI in Referal

```text
-Z## | -0Z####, XRFI, VID_sndr, Digest, Nonce, VID_new, Signature_new, Padding_field
```
The `Signature_new` field is a signature signed by the VID_new's key over the fields that preceeds it: {XRFI,  VID_sndr, Digest, Nonce, VID_new}. It is then encoded in the same way as specified in [TSP Signature Encoding](#tsp-signature-encoding).

##### TSP_RFA in Referal

```text
-Z## | -0Z####, XRFA, VID_sndr, Digest, Reply_Digest, VID_new, Signature_new, Padding_field
```
The `Signature_new` field is a signature signed by the VID_new's key over the fields that preceeds it: {XRFA,  VID_sndr, Digest, Reply_Digest, VID_new}. It is then encoded in the same way as specified in [TSP Signature Encoding](#tsp-signature-encoding).

##### TSP_RFI Nested
The TSP_RFI message can be constructed by composing a TSP_RFI inside a nested outer message:

``` text
-Z## | -0Z####, XHOP, VID_sndr, -J## | -0J####, VID_HOP_1, ..., Padding_field, Encoded_TSP_Message
```
The `Encoded_TSP_Message` is in fact the `TSP_RFI` message as follows:

```text
TSP_Tag, TSP_Version, VID_sndr_new, `4BAA`, -Z## | -0Z####, XRFI, VID_sndr_new, Digest, Nonce, Padding_field, Signature_new
```
In the nested `TSP_RFI` message, the Signature_new is the signature of the new `VID_sndr_new`.

Note that the hop list will be encoded as `-JAA` if this message is nested over a direct relationship without intermediary.

##### TSP_RFI Nested

The TSP_RFA message can be constructed by composing a TSP_RFA inside a nested outer message:

``` text
-Z## | -0Z####, XHOP, VID_sndr, -J## | -0J####, VID_HOP_1, ..., Padding_field, Encoded_TSP_Message
```
The `Encoded_TSP_Message` is in fact the `TSP_RFA` message as follows:

```text
TSP_Tag, TSP_Version, VID_sndr_new, VID_rcvr_new, -Z## | -0Z####, XRFA, VID_sndr_new, VID_new, Digest, Reply_Digest, Padding_field, Signature_new
```
Note that the hop list will be encoded as `-JAA` if this message is nested over a direct relationship without intermediary.

##### TSP_RFD

The `TSP_RFD` message can be constructed as follows in a direct relationship,

```text
-Z## | -0Z####, XRFD, VID_sndr, Nonce, Digest, Padding_field
```
For nested or routed relationships, the same message is encoded as an inner message in the nested or routed outer message. The `Digest` field MUST reference the corresponding relationship formation `XRFI` or `XRFA` message's digest, respectively.

##### Generic Control Message

A TSP generic control message uses the `XCTL` code in the CESR code table and its payload can be any comformant stream, including interleaving JSON, CBOR, or MsgPak encodings.

```text
-Z## | -0Z####, XCTL, VID_sndr, Padding_field, any_payload_stream
```
##### Padding Message

A TSP padding message uses the `XPAD` code in the CESR code table. 

```text
-Z## | -0Z####, XPAD, VID_sndr, Nonce, Padding_field
```

### TSP Signature Encoding
The TSP Signature is encoded as an attachment group in CESR. TSP allows multiple signatures. The general structure is the attachment group code, followed by the indexed signature group code, then 1 or more signatures of supported types.

- Attachment group: `-C##` or `-0C####` (Attachment length up to 4,095 quadlets/triplets for `-C##` or up to 1,073,741,823 quadlets/triplets for `-0C####`)

- Indexed signature group: `-K##` or `-0K####` (Indexed signature group up to 4,095 quadlets/tripletsfor `-K##` or up to 1,073,741,823 quadlets/triplets for `-0K####`)

#### Ed25519 Signature

An Ed25519 (EdDSA) signature is always 64 bytes. It is identified by the two character code `0B`, followed by 2 padding bytes (in binary) and the 64 byte signature (in binary). The equivalent text format is 22 triplets.

#### ML-KEM Signature

TODO


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

For each transport mechanism supported, TSP implementations MUST instantiate these operations in a way that facilitates interoperability.

### Transport Mechanism Examples

::: issue #11
Decide what to include as examples. For each, complete a short section.
https://github.com/trustoverip/tswg-tsp-specification/issues/11
:::

- QUIC

- HTTPS

- Matrix

- Message Queues

- Email

- Paper Messages



## Security and Privacy Considerations

::: issue #12
We will be collecting FAQs and then provide relevant information in this section.
https://github.com/trustoverip/tswg-tsp-specification/issues/12
:::

## References

::: issue #13
The `spec` primitives are not yet working for all cases.
https://github.com/trustoverip/tswg-tsp-specification/issues/13
:::

### Normative References
[[spec-norm]]

**[[def:CESR]]**. *Composable Event Streaming Representation (CESR)*, Samuel Smith
[CESR]: https://trustoverip.github.io/tswg-cesr-specification/

[DID]. Decentralized Identifiers (DIDs) v1.0, https://www.w3.org/TR/did-1.0/

### Informational References
[[spec-inform]]

[ESSR]. Authenticated Encryption in the Public-Key Setting: Security Notations and Analyses, *Jee Hea An*, Cryptology ePrint Archive, Paper 2001/079.
[ESSR]: https://eprint.iacr.org/2001/079

[HPKE-WG]. The IETF HPKE Working Group
[HPKE-WG]: https://datatracker.ietf.org/group/hpke/about/

[HPKE-PQ]. Post-Quantum and Post-Quantum/Traditional Hybrid Algorithms for HPKE, June 2, 2025, draft-ietf-hpke-pq-00.
[HPKE-PQ]: https://datatracker.ietf.org/doc/draft-ietf-hpke-pq/

[FIPS203]. Module-Lattice-Based Key-Encapsulation Mechanism Standard, National Institute of Standards and Technology (U.S.), DOI 10.6028/nist.fips.203, August 2024
[FIPS203]: https://doi.org/10.6028/nist.fips.203

[FIPS204]. Module-Lattice-Based Digital Signature Standard, National Institute of Standards and Technology (U.S.), DOI 10.6028/nist.fips.204, August 2024
[FIPS204]: https://doi.org/10.6028/NIST.FIPS.204

[TOIP-TAS]. ToIP Technology Architecture Specification (DRAFT)
[TAS]: https://github.com/trustoverip/TechArch/blob/main/spec.md

[TLS-ECH]. TLS Encrypted Client Hello, *Rescorla, E., Oku, K., Sullivan, N., and C. A. Wood,* Work in Progress, Internet-Draft, draft-ietf-tls-esni-18, 4 March 2024.
[TLS-ECH]: https://datatracker.ietf.org/doc/html/draft-ietf-tls-esni-18

[COSE-HPKE]. Use of Hybrid Public-Key Encryption (HPKE) with CBOR Object Signing and Encryption (COSE), *H. Tschofenig, B. Moran*, draft-ietf-cose-hpke-03, 27 February 2023.
[COSE-HPKE]: https://www.ietf.org/archive/id/draft-ietf-cose-hpke-03.html

## Appendix A: Test Vectors

::: issue #14
To provide sample test vectors for a few common cases.
https://github.com/trustoverip/tswg-tsp-specification/issues/14
:::

### Test Vectors for Direct Mode TSP Message

### Test Vectors for Direct Mode Nested TSP Message

### Test Vectors for Routed Mode Message

