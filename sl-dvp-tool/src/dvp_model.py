import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional

# --- DVP Schema Definition (from PROJECT.md) ---
class DVP:
    def __init__(self, claim_text: str, current_confidence: float = 0.5, lineage: List[Dict[str, Any]] = None):
        self.id = self._generate_id(claim_text)
        self.claim_text = claim_text
        self.created_at = datetime.utcnow().isoformat() + 'Z'
        self.current_confidence = current_confidence
        self.lineage = lineage if lineage is not None else []

    def _generate_id(self, claim_text: str) -> str:
        """Generates a simple content-addressable hash ID for the DVP."""
        data = f"{claim_text}{datetime.utcnow().isoformat()}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def add_lineage_step(self, step_data: Dict[str, Any]):
        """
        Adds a verification step to the lineage and updates confidence based on RGP.
        
        step_data must contain:
        - step_id: Unique process ID
        - process_type: e.g., 'OxfordDebate', 'FunctionalAudit'
        - agent_did: Decentralized Identifier of the agent/group
        - result_score_change: Score modification based on PROTOCOL.md
        - attestation_vc_uri: URI to the immutable VC record
        """
        step_data['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        self.lineage.append(step_data)
        
        # Apply RGP Logic (from PROTOCOL.md)
        self.current_confidence = max(0.0, min(1.0, self.current_confidence + step_data['result_score_change']))

    def to_json(self) -> Dict[str, Any]:
        """Returns the DVP as a serializable dictionary."""
        return {
            "id": self.id,
            "claim_text": self.claim_text,
            "created_at": self.created_at,
            "current_confidence": self.current_confidence,
            "lineage": self.lineage
        }

    def save(self, filename: str):
        """Saves the DVP state to a local JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.to_json(), f, indent=2)

# --- Test Example (Simulated OSD Process) ---
if __name__ == "__main__":
    # 1. Create Initial DVP
    motion = "This house believes the Synergy Ledger architecture will solve the problem of Civil Unrest."
    dvp = DVP(claim_text=motion, current_confidence=0.5)
    print(f"Initial DVP created with ID: {dvp.id} and Confidence: {dvp.current_confidence}")

    # 2. Simulate an Oxford-Style Debate (OSD Victory: +0.10)
    osd_step = {
        "step_id": "osd-20260203-001",
        "process_type": "OxfordDebate",
        "agent_did": "did:synergy:eig-lead",
        "result_score_change": 0.10, 
        "attestation_vc_uri": "https://ledger.com/vc/osd-20260203-001"
    }
    dvp.add_lineage_step(osd_step)
    print(f"After OSD Victory: Confidence is now: {dvp.current_confidence}")
    
    # 3. Simulate a Functional Audit Fail (FFG Fail: -0.10)
    audit_fail_step = {
        "step_id": "audit-20260203-002",
        "process_type": "FunctionalAudit",
        "agent_did": "did:synergy:ffg-node-a",
        "result_score_change": -0.10, 
        "attestation_vc_uri": "https://ledger.com/vc/audit-20260203-002"
    }
    dvp.add_lineage_step(audit_fail_step)
    print(f"After FFG Fail: Confidence is now: {dvp.current_confidence}")

    # 4. Save the DVP
    dvp.save("test/test_dvp.json")
    print(f"DVP saved to: test/test_dvp.json")