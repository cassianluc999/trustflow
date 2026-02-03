# GUI_SPEC.md: Synergy Ledger Dashboard (SLD) Aesthetic Specification

**Goal:** To translate the underlying technical integrity (DVP/RGP) into a clean, minimal, and transparent visual experience, reinforcing the **Process Transparency** and **Ethical Spine** pillars.

---

## 1. Aesthetic Principles (Constraint Enforcement)

1.  **Clarity over Density:** Avoid information overload. Present only the actionable facts (Confidence, Lineage, Next Step).
2.  **Immutability Visualization:** Use subtle visual cues (e.g., hash icons, lock symbols) to signal that records are anchored.
3.  **Process-First:** The primary visual metric is **Confidence**, not 'Likes' or 'Virality.'
4.  **Dark Theme:** (Already set in `dashboard.html`) - Professional, low-fatigue environment.

---

## 2. DVP Card (Primary Visual Element)

The DVP Status Card should be the central element.

| Field | Purpose | Visualization |
| :--- | :--- | :--- |
| **Claim Text** | The formal motion. | Large, centered text. |
| **Current Confidence** | The most critical metric. | Large, dynamic percentage (0-100%) or decimal (0.00-1.00). **Color-coded:** < 0.3 (Red), 0.3-0.6 (Yellow/Orange), > 0.6 (Green). |
| **Lineage Steps** | The audit trail. | Collapsible list. Each item shows: `Process Type` (Icon), `Agent DID`, `Score Change`, `K-Factor Applied`. |
| **Next Constraint** | What the DVP needs to pass. | Clear, single instruction (e.g., "Awaiting CIG Audit"). |

---

## 3. Action Bar (User Interface)

Must provide clear entry points for verification.

| Button | Function | Required Input |
| :--- | :--- | :--- |
| **New Motion** | Calls `sl_cli.py create`. | Claim Text, Agent DID, Initial Karma. |
| **Submit Audit Pass** | Calls `sl_cli.py add_step`. | DVP ID, S-Group (EIG/FFG/CIG), Attestation URI. |
| **Submit Audit Fail** | Calls `sl_cli.py add_step` with negative score. | DVP ID, S-Group, Attestation URI. |
| **Start OSD** | Triggers an Oxford-Style Debate Process (Future: `osd_model.py`). | DVP ID, Opposing Agent DID. |

---
[End of GUI_SPEC.md]