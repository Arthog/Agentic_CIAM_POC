# security_engine.py

USER_DIRECTORY = {
    "user_123": {
        "name": "Alex",
        "role": "Product Manager",
        "department": "Finance",
        "clearance": "Level_3",
        "device_trusted": True,
        "location": "UK"
    },
    # Let's add a compromised version of Alex to simulate a risk event
    "user_123_compromised": {
        "name": "Alex (Attacker Profile)",
        "role": "Product Manager",
        "department": "Finance",
        "clearance": "Level_3",
        "device_trusted": False,  # Untrusted device!
        "location": "Unknown"     # Suspicious location!
    },
    "user_789": {
        "name": "Sam",
        "role": "Contractor",
        "department": "Marketing",
        "clearance": "Level_1",
        "device_trusted": False,
        "location": "US"
    }
}

def evaluate_abac_policy(user_id: str, resource: str) -> dict:
    user_attributes = USER_DIRECTORY.get(user_id)
    
    if not user_attributes:
        return {"status": "DENIED", "reason": "User ID not found in system."}
        
    if resource == "financial_ledger":
        # Base ABAC Rule: Must be Finance and Level 3
        if user_attributes["department"] == "Finance" and user_attributes["clearance"] == "Level_3":
            
            # DYNAMIC RISK CONSTRAINTS (The core of ABAC)
            if not user_attributes["device_trusted"] or user_attributes["location"] == "Unknown":
                return {
                    "status": "STEP_UP_REQUIRED", 
                    "reason": "Department rules met, but untrusted device/location detected. Triggering Multi-Factor Authentication (MFA)."
                }
                
            return {"status": "APPROVED", "reason": "Access granted based on Department, Clearance, and Device Trust matching."}
        else:
            return {"status": "DENIED", "reason": "Insufficient clearance or incorrect department for this asset."}
            
    return {"status": "DENIED", "reason": "Requested resource is unmapped or restricted."}