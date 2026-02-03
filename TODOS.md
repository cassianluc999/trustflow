# TODOS.md - Synergy Ledger (SL) Development Log

## Status: Phase I - MVP Validation Complete

| Task | Status | Priority | Rationale |
| :--- | :--- | :--- | :--- |
| **1. Define DVP Schema** | ✅ DONE | P0 | Completed: `PROJECT.md` |
| **2. Define RGP Rules** | ✅ DONE | P0 | Completed: `PROTOCOL.md` |
| **3. Build DVP Model (Python)** | ✅ DONE | P0 | Completed: `src/dvp_model.py` |
| **4. Validate RGP Logic** | ✅ DONE | P0 | Completed: `python src/dvp_model.py` |
| **5. Create SL Dashboard (Canvas)** | ⚙️ IN PROGRESS | P0 | Current objective. |

## Phase II - Protocol Expansion

| Task | Status | Priority | Rationale |
| :--- | :--- | :--- | :--- |
| **6. Implement Test Rig** | ✅ DONE | P1 | Create `test/test_rig.py` to formally assert all RGP scoring rules. |
| **7. Finalize Reputation Scoring** | ✅ DONE | P1 | Formalize the non-linear curve for Karma accumulation/decay. |
| **8. Design DID/VC Integration** | ⬜ PENDING | P2 | Integrate a library for DID generation/signing (e.g., Aries, did:web). |
| **9. Design OSD Decision Flow** | ⬜ PENDING | P2 | Create the Python class to manage the OSD decision lifecycle. |

## Knowledge Assets

| File | Status | Use Case |
| :--- | :--- | :--- |
| `knowledge/truth-revolution-manifesto.md` | ✅ READY | Core Strategic Blueprint. |
| `research/DVP_Coordination_Report.md` | ✅ READY | Architecture and OSD Validation. |
| `PROTOCOL.md` | ✅ READY | Scoring Logic. |
| `PROJECT.md` | ✅ READY | Data Schema. |
