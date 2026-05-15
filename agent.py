# agent.py
# agent.py
from pydantic import BaseModel, Field
from google import genai
from security_engine import evaluate_abac_policy

client = genai.Client()

class AccessRequest(BaseModel):
    user_id: str = Field(description="The unique ID of the user. Map 'Alex' to 'user_123'. If the prompt mentions a suspicious device, an unknown location, or an attack scenario for Alex, map to 'user_123_compromised'. Map 'Sam' to 'user_789'.")
    resource: str = Field(description="The system resource requested. Map anything ledger/budget to 'financial_ledger'.")

def process_natural_language_request(user_prompt: str):
    print(f"\n[User Prompt]: '{user_prompt}'")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Extract the access request details: {user_prompt}",
        config={
            'response_mime_type': 'application/json',
            'response_schema': AccessRequest,
        }
    )
    
    parsed_request = AccessRequest.model_validate_json(response.text)
    print(f"[Agent Extract]: User ID: '{parsed_request.user_id}', Resource: '{parsed_request.resource}'")
    
    security_verdict = evaluate_abac_policy(parsed_request.user_id, parsed_request.resource)
    print(f"[Security Engine Decision]: {security_verdict}\n")