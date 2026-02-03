# PROJECT.md: Synergy Ledger (SL) - Phase I Specification

**Mission Alignment:** Operationalize The Truth Revolution Manifesto's Pillars (Process Transparency, Distributed Verification) to build an ethical, intelligent, and decentralized value system.
**Target Product:** The Synergy Ledger (SL).
**Minimum Viable Component:** The Decentralized Verification Primitive (DVP) Schema.

---

## Decentralized Verification Primitive (DVP) JSON Schema v1.0

The DVP is a non-custodial, cryptographically verifiable record of a claim's provenance and assessment process. It replaces subjective authority with auditable lineage.

\`\`\`json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Decentralized Verification Primitive (DVP)",
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique, non-sequential identifier (e.g., UUID or verifiable credential ID). Used as the canonical reference for the claim."
    },
    "claim_text": {
      "type": "string",
      "description": "The declarative statement (the Motion) being verified or proposed. Must be clear and non-ambiguous."
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp of initial DVP creation."
    },
    "current_confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "The current probabilistic confidence score (0.0 to 1.0) derived from the aggregate lineage endorsements. Models Epistemic Humility."
    },
    "lineage": {
      "type": "array",
      "description": "An immutable, ordered array of verifiable steps (endorsements, debates, audits) applied to the claim.",
      "items": {
        "type": "object",
        "properties": {
          "step_id": {
            "type": "string",
            "description": "Unique identifier for this step/process instance (e.g., Debate ID, Audit VC hash)."
          },
          "process_type": {
            "type": "string",
            "description": "The type of verification applied (e.g., 'OxfordDebate', 'FunctionalAudit', 'ZKProof-Verification')."
          },
          "agent_did": {
            "type": "string",
            "description": "The Decentralized Identifier (DID) of the agent or S-Group who executed this step (models Incentive Disclosure)."
          },
          "result_score_change": {
            "type": "number",
            "description": "The change in the confidence score resulting from this step (e.g., +0.1 for positive endorsement, -0.05 for a failed audit)."
          },
          "timestamp": {
            "type": "string",
            "format": "date-time"
          },
          "attestation_vc_uri": {
            "type": "string",
            "description": "URI pointing to the Verifiable Credential (VC) that immutably attests to this step's successful completion (e.g., a debate result)."
          }
        },
        "required": ["step_id", "process_type", "agent_did", "result_score_change", "timestamp", "attestation_vc_uri"]
      }
    }
  },
  "required": ["id", "claim_text", "created_at", "current_confidence", "lineage"]
}
\`\`\`

## Coordination Layer Framework

**Immediate Framework:** The OSD principles (clear Motion, persuasion via audience vote) will be the required interaction model for all disputes/verifications involving the **Epistemic S-Group** in the Synergy Ledger.

**Next Step:** Define the **Reputational Governance Protocol** that dictates *how* the `current_confidence` score is calculated from the endorsements in the `lineage` array. This will be the next SVM.

---
[End of PROJECT.md]