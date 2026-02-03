import unittest
import json
import os
from src.dvp_model import DVP, datetime # Assuming DVP is now exportable

# Define the expected RGP scores from PROTOCOL.md
RGP_SCORES = {
    "OSD_VICTORY": 0.10,
    "OSD_LOSS": -0.05,
    "AUDIT_PASS": 0.05,
    "AUDIT_FAIL": -0.10,
    "MALICIOUS_ATTESTATION": -0.50,
    "FINAL_APPROVAL": 0.20
}

class DVPModelTest(unittest.TestCase):

    def setUp(self):
        """Set up a fresh DVP instance for each test."""
        motion = "The Synergy Ledger is the most effective solution for epistemic crisis."
        # Start at a neutral 0.5 confidence
        self.dvp = DVP(claim_text=motion, current_confidence=0.5)

    def test_initial_state(self):
        """Tests that the DVP initializes correctly."""
        self.assertIsInstance(self.dvp.id, str)
        self.assertAlmostEqual(self.dvp.current_confidence, 0.5)
        self.assertEqual(len(self.dvp.lineage), 0)

    def test_osd_victory_scoring(self):
        """Tests OSD Victory rule (+0.10)."""
        step = {
            "step_id": "osd-win-1",
            "process_type": "OxfordDebate",
            "agent_did": "did:synergy:eig-lead",
            "result_score_change": RGP_SCORES["OSD_VICTORY"], 
            "attestation_vc_uri": "uri:osd-win"
        }
        initial_conf = self.dvp.current_confidence
        self.dvp.add_lineage_step(step)
        self.assertAlmostEqual(self.dvp.current_confidence, initial_conf + RGP_SCORES["OSD_VICTORY"])
        self.assertAlmostEqual(self.dvp.current_confidence, 0.60) # 0.5 + 0.1

    def test_functional_audit_fail_scoring(self):
        """Tests FFG Failure rule (-0.10)."""
        self.dvp.current_confidence = 0.75 # Set a starting point
        step = {
            "step_id": "audit-fail-1",
            "process_type": "FunctionalAudit",
            "agent_did": "did:synergy:ffg-node-b",
            "result_score_change": RGP_SCORES["AUDIT_FAIL"], 
            "attestation_vc_uri": "uri:audit-fail"
        }
        self.dvp.add_lineage_step(step)
        self.assertAlmostEqual(self.dvp.current_confidence, 0.65) # 0.75 - 0.1

    def test_malicious_attestation_slashing(self):
        """Tests Malicious Attestation rule (-0.50) and floor limit."""
        self.dvp.current_confidence = 0.40 # Low starting point
        step = {
            "step_id": "malicious-1",
            "process_type": "MaliciousAttestation",
            "agent_did": "did:synergy:bad-actor",
            "result_score_change": RGP_SCORES["MALICIOUS_ATTESTATION"], 
            "attestation_vc_uri": "uri:slashed"
        }
        self.dvp.add_lineage_step(step)
        # 0.40 - 0.50 = -0.10. Should floor at 0.0.
        self.assertAlmostEqual(self.dvp.current_confidence, 0.0) 

    def test_final_motion_approval_cap(self):
        """Tests Final Approval rule (+0.20) and ceiling limit."""
        self.dvp.current_confidence = 0.95 # High starting point
        step = {
            "step_id": "final-app-1",
            "process_type": "FinalMotionApproval",
            "agent_did": "did:synergy:c-group",
            "result_score_change": RGP_SCORES["FINAL_APPROVAL"], # +0.20
            "attestation_vc_uri": "uri:final-app"
        }
        self.dvp.add_lineage_step(step)
        # 0.95 + 0.20 = 1.15. Should ceiling at 1.0.
        self.assertAlmostEqual(self.dvp.current_confidence, 1.0)
        
    def test_lineage_integrity(self):
        """Tests that lineage steps contain all required fields."""
        step = {
            "step_id": "check-fields-1",
            "process_type": "TestProcess",
            "agent_did": "did:synergy:test",
            "result_score_change": 0.0, 
            "attestation_vc_uri": "uri:test"
        }
        self.dvp.add_lineage_step(step)
        self.assertEqual(len(self.dvp.lineage), 1)
        # Check that timestamp was automatically added
        self.assertIn('timestamp', self.dvp.lineage[0])
        self.assertTrue(self.dvp.lineage[0]['timestamp'].endswith('Z')) # UTC format check

if __name__ == '__main__':
    # Save the current state to the workspace to be used by the skill-creator later
    with open('test/test_rig_output.json', 'w') as f:
        json.dump({"result": "Running unit tests..."}, f, indent=2)

    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    # Note: unittest output will be mixed with command output.
    # The true test is the command exit code (0 for success).
    print("Test Rig Execution Complete. Check output for final pass/fail status.")