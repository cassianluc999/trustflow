import sys
import json
import os
from src.dvp_model import DVP 

# Define the local path for the DVP ledger store
DVP_LEDGER_PATH = 'data/ledger.json'

def load_dvp_ledger():
    """Loads the entire ledger from the file system."""
    if not os.path.exists(DVP_LEDGER_PATH):
        return {}
    with open(DVP_LEDGER_PATH, 'r') as f:
        return json.load(f)

def save_dvp_ledger(ledger):
    """Saves the entire ledger to the file system."""
    os.makedirs(os.path.dirname(DVP_LEDGER_PATH), exist_ok=True)
    with open(DVP_LEDGER_PATH, 'w') as f:
        json.dump(ledger, f, indent=2)

def create_dvp_claim(claim_text: str):
    """Creates a new DVP, adds it to the ledger, and returns its ID."""
    dvp_instance = DVP(claim_text=claim_text)
    ledger = load_dvp_ledger()
    ledger[dvp_instance.id] = dvp_instance.to_json()
    save_dvp_ledger(ledger)
    print(f"DVP Created Successfully: ID={dvp_instance.id}")
    return dvp_instance.id

def add_dvp_step(dvp_id: str, process_type: str, agent_did: str, score_change: float, attestation_uri: str):
    """Adds a lineage step to an existing DVP, updating its confidence score."""
    ledger = load_dvp_ledger()
    if dvp_id not in ledger:
        print(f"Error: DVP with ID {dvp_id} not found.")
        sys.exit(1)

    dvp_data = ledger[dvp_id]
    
    # Re-hydrate DVP model to use the logic
    dvp_instance = DVP(
        claim_text=dvp_data['claim_text'],
        current_confidence=dvp_data['current_confidence'],
        lineage=dvp_data['lineage']
    )
    # The ID and creation date must be preserved from the original data
    dvp_instance.id = dvp_data['id']
    dvp_instance.created_at = dvp_data['created_at']

    step_data = {
        "step_id": f"{process_type.lower()}-{dvp_id}-{len(dvp_instance.lineage) + 1}",
        "process_type": process_type,
        "agent_did": agent_did,
        "result_score_change": score_change,
        "attestation_vc_uri": attestation_uri
    }
    
    # Use the model logic to add the step and update confidence
    dvp_instance.add_lineage_step(step_data)

    # Update ledger and save
    ledger[dvp_id] = dvp_instance.to_json()
    save_dvp_ledger(ledger)
    
    print(f"Step Added: ID={dvp_id}, Confidence Updated to {dvp_instance.current_confidence:.2f}")

def get_dvp_status(dvp_id: str):
    """Retrieves and prints the full JSON status of a DVP."""
    ledger = load_dvp_ledger()
    if dvp_id not in ledger:
        print(f"Error: DVP with ID {dvp_id} not found.")
        sys.exit(1)
    
    print(json.dumps(ledger[dvp_id], indent=2))

# --- Main CLI Dispatcher ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sl_cli.py [command] [args...]")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "create":
        if len(args) != 1:
            print("Usage: sl_cli.py create \"<claim_text>\"")
            sys.exit(1)
        create_dvp_claim(args[0])

    elif command == "add_step":
        if len(args) != 5:
            print("Usage: sl_cli.py add_step <dvp_id> <process_type> <agent_did> <score_change> <attestation_uri>")
            print("Example score changes: 0.10 (OSD Win), -0.10 (Audit Fail)")
            sys.exit(1)
        
        dvp_id = args[0]
        process_type = args[1]
        agent_did = args[2]
        try:
            score_change = float(args[3])
        except ValueError:
            print("Error: score_change must be a number.")
            sys.exit(1)
        attestation_uri = args[4]

        add_dvp_step(dvp_id, process_type, agent_did, score_change, attestation_uri)

    elif command == "status":
        if len(args) != 1:
            print("Usage: sl_cli.py status <dvp_id>")
            sys.exit(1)
        get_dvp_status(args[0])

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)