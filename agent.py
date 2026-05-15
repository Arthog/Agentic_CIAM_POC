from google import genai
from google.genai import types
from pydantic import BaseModel, Field

client = genai.Client()

# Update the data schema contract to include the field your app.py is checking for
class SecurityResponse(BaseModel):
    intent: str = Field(description="The detected user intent")
    risk_score: int = Field(description="Risk rating from 1 to 5")
    security_status: str = Field(description="MUST be 'APPROVED' if risk_score is 1 or 2. MUST be 'DENIED' if risk_score is 3, 4, or 5.")

def process_natural_language_request(user_query):
    config = types.GenerateContentConfig(
        system_instruction=(
            "You are an intelligent CIAM security orchestration agent. "
            "Evaluate the access request query for malicious intent or architectural compliance. "
            "Assign a risk score from 1 (completely benign/safe) to 5 (critical risk or unauthorized access path). "
            "Determine the final security_status based strictly on the risk threshold rules provided in the schema descriptions."
        ),
        temperature=0.1,
        response_mime_type="application/json",
        response_schema=SecurityResponse, 
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_query,
        config=config
    )
    return response.text
