# PROTOCOL.md: Reputational Governance Protocol (RGP) v1.0

**Mission:** To govern the creation and modification of Decentralized Verification Primitives (DVP) within the Synergy Ledger (SL), ensuring **Process Transparency** and **Distributed Verification** (Pillars 2 & 5 of the Truth Revolution Manifesto).

---

## 1. Synergy Group (S-Group) Definition

The SL requires decisions to achieve Functional Overlap, necessitating consensus across diverse groups. A qualified majority (60% default) in each required S-Group is mandatory for a DVP to be accepted as a Final Motion.

| S-Group Name | Functional Role | Epistemic Focus | Core Constraint |
| :--- | :--- | :--- | :--- |
| **Epistemic Integrity Group (EIG)** | Verifies claim evidence, logical coherence, and adherence to probabilistic modeling. | **Truth as Process** (Probabilistic Reality) | Must assess the DVP's \`lineage\` for methodological rigor. |
| **Functional Feasibility Group (FFG)** | Assesses claims based on practical implementation, resource allocation, and technical constraints. | **Coordination** (Reliability) | Must ensure the proposed action can be executed with predictable reliability. |
| **Community Impact Group (CIG)** | Evaluates claims against ethical mandate, long-term sustainability, and fairness of outcome distribution. | **Ethical Spine** (Moral Orientation) | Must ensure the proposal aligns with MTP and community values. |

---

## 2. DVP Scoring Rules (Reputational Governance)

The \`current_confidence\` score (in \`PROJECT.md\`) is a dynamic aggregate reflecting the process integrity. This score determines the DVP's actionability status.

| Event Type | Condition | Score Change (\`result_score_change\`) | Rationale (Pillar) |
| :--- | :--- | :--- | :--- |
| **OSD Victory** | A Proponent successfully persuades the undecided audience (pre-vote to post-vote shift > 5%). | **+0.10** | Rewards persuasion and steel-manning (Pillar 4: Narrative Literacy). |
| **OSD Loss** | A Proponent fails to maintain or grow support (shift < 5%). | **-0.05** | Penalizes failure to persuade or weak argument structure. |
| **Functional Audit Pass** | FFG successfully validates the feasibility of the claim/proposal. | **+0.05** | Rewards predictable reliability (Pillar 2: Process Transparency). |
| **Functional Audit Fail** | FFG identifies a critical, non-trivial constraint (failure mode). | **-0.10** | Penalizes overstating certainty (Pillar 1: Epistemic Humility). |
| **Malicious Attestation** | Proven use of a DVP to anchor an intentionally false claim (e.g., a deepfake source). | **-0.50** | Enforces Ethical Spine; Costly Lying (Truth Custody). |
| **Final Motion Approval** | DVP achieves 60% consensus across all required S-Groups. | **+0.20** | Rewards Functional Overlap and collective choice. |

---

## 3. Agent Identity and DID Staking

All participating agents (human or AI) must register a verifiable Decentralized Identifier (DID) and stake a minimal amount of governance collateral (COL).

| Rule | Requirement | Rationale |
| :--- | :--- | :--- |
| **DID Required** | All endorsements (\`lineage\`) must be signed by a DID. | Ensures immutable provenance and accountability (Pillar 5). |
| **Stake Requirement** | Agents must stake 100 COL to participate in an S-Group audit/debate. | Creates a financial incentive for responsible behavior (Incentive Disclosure). |
| **Slashing (Stake Loss)** | Stake is forfeited (slashed) if an agent is found to have committed a Malicious Attestation or knowingly voted against their S-Group's mandate *for personal gain*. | Penalizes self-interest over process integrity (Ethical Spine). |
| **Reputation System** | Agent DIDs accumulate reputation (Karma) from successful contributions (passing audits, winning debates). | Authority is earned continuously, not granted by role (Pillar 5). |

---

## 4. Karma & Non-Linear Influence Model (K-NLIM)

To ensure the Reputational Governance Protocol (RGP) resists Sybil attacks and rewards long-term, high-quality participation, all agents' DIDs maintain a **Karma Score**. The Karma Score acts as a non-linear multiplier on their influence.

| Rule | Requirement | Rationale |
| :--- | :--- | :--- |
| **Karma Accumulation** | Agents earn +1 KARMA for successful contributions (e.g., winning an OSD, successful audit pass). | Rewards competence and sustained positive contribution. |
| **Decay Rate** | Karma decays by 10% every 30 days (simulated). | Prevents legacy influence from dictating present decisions; rewards active engagement (Truth as Ongoing Work). |
| **Non-Linear Multiplier (K-Factor)** | An agent's action (\`result_score_change\`) is multiplied by their K-Factor before being applied to the DVP confidence. | Rewards high-reputation agents with greater influence, resisting Sybil attacks. |
| **K-Factor Formula (SVM)** | \`K-Factor = 1 + log10(1 + KARMA_SCORE)\` | Simple, non-linear growth that heavily rewards early, high-risk contributions but scales slowly. |

### DVP Confidence Update Formula (Revised)

\`New Confidence = Current Confidence + (result_score_change * K-Factor)\`
(Subject to 0.0 to 1.0 floor/ceiling)

---
[End of PROTOCOL.md]