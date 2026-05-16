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

RESOURCE_ALIASES = {
    "budget": "financial_ledger",
    "financial budget": "financial_ledger",
    "financial ledger": "financial_ledger",
    "ledger": "financial_ledger",
    "q4 financial budget spreadsheet": "financial_ledger",
}

USER_ALIASES = {
    "alex": "user_123",
    "alex compromised": "user_123_compromised",
    "sam": "user_789",
}


def resolve_user_id(user_reference: str) -> str:
    normalized_reference = user_reference.strip().lower()
    return USER_ALIASES.get(normalized_reference, user_reference)


def resolve_resource_id(resource_reference: str) -> str:
    normalized_reference = resource_reference.strip().lower()
    return RESOURCE_ALIASES.get(normalized_reference, resource_reference)

def evaluate_abac_policy(user_id: str, resource: str) -> dict:
    resolved_user_id = resolve_user_id(user_id)
    resolved_resource = resolve_resource_id(resource)
    user_attributes = USER_DIRECTORY.get(resolved_user_id)
    
    if not user_attributes:
        return {
            "status": "DENIED",
            "reason": "User ID not found in system.",
            "user_id": resolved_user_id,
            "resource": resolved_resource,
        }
        
    if resolved_resource == "financial_ledger":
        # Base ABAC Rule: Must be Finance and Level 3
        if user_attributes["department"] == "Finance" and user_attributes["clearance"] == "Level_3":
            
            # DYNAMIC RISK CONSTRAINTS (The core of ABAC)
            if not user_attributes["device_trusted"] or user_attributes["location"] == "Unknown":
                return {
                    "status": "STEP_UP_REQUIRED", 
                    "reason": "Department rules met, but untrusted device/location detected. Triggering Multi-Factor Authentication (MFA).",
                    "user_id": resolved_user_id,
                    "resource": resolved_resource,
                }
                
            return {
                "status": "APPROVED",
                "reason": "Access granted based on Department, Clearance, and Device Trust matching.",
                "user_id": resolved_user_id,
                "resource": resolved_resource,
            }
        else:
            return {
                "status": "DENIED",
                "reason": "Insufficient clearance or incorrect department for this asset.",
                "user_id": resolved_user_id,
                "resource": resolved_resource,
            }
            
    return {
        "status": "DENIED",
        "reason": "Requested resource is unmapped or restricted.",
        "user_id": resolved_user_id,
        "resource": resolved_resource,
    }
