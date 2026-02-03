---
name: sl-dvp-tool
description: The core tool for the Synergy Ledger (SL). Used to create, update (add lineage steps), and retrieve the status of Decentralized Verification Primitives (DVP). Use this skill anytime the user references verifiable claims, process transparency, DVP, or RGP.
---

# Synergy Ledger DVP Tool

This skill is the operational interface for the Synergy Ledger (SL), our Minimum Viable Product for the Truth Revolution MTP.

It encapsulates the DVP data model and the Reputational Governance Protocol (RGP) scoring logic.

## Functions (Tool Commands)

This tool exposes three primary functions via the `src/sl_cli.py` script. All commands use the pattern:
\`\`\`bash
python src/sl_cli.py <command> <args...>
\`\`\`

### 1. Create a New DVP Claim

Use this to anchor a new declarative claim (Motion) into the Synergy Ledger. It returns the new `dvp_id`.

\`\`\`bash
python src/sl_cli.py create "<claim_text>"
# Example: python src/sl_cli.py create "This house believes the DVP is the optimal unit of trust."
\`\`\`

### 2. Add a Lineage Step (Update Confidence)

Use this to record a process step (like an OSD debate or an FFG audit) and update the DVP's `current_confidence` score based on the RGP rules.

\`\`\`bash
python src/sl_cli.py add_step <dvp_id> <process_type> <agent_did> <score_change> <attestation_uri>
# Example: python src/sl_cli.py add_step 1a2b3c OSD_VICTORY did:synergy:eig-lead 0.10 https://ledger.com/vc/123
\`\`\`
**RGP Score Change Quick Reference (from PROTOCOL.md):**
- OSD Victory: `0.10`
- Functional Audit Pass: `0.05`
- Functional Audit Fail: `-0.10`
- Malicious Attestation: `-0.50`

### 3. Retrieve DVP Status

Use this to get the full JSON structure of a DVP, including its current confidence and entire lineage.

\`\`\`bash
python src/sl_cli.py status <dvp_id>
# Example: python src/sl_cli.py status 1a2b3c
\`\`\`

## Skill Resources

- **`src/dvp_model.py`**: Core Python class with DVP data structure and RGP math.
- **`src/sl_cli.py`**: Command-line interface for tool execution.
- **`data/ledger.json`**: Simple JSON file used as the persistent, local ledger (Custody layer simulation).

**Integration Note:** The `skill-creator` tool is used to package this skill for deployment. This skill, once fully packaged, enables local, native tool usage for the Synergy Ledger.