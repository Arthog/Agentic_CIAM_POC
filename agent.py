from google import genai
from google.genai import types
from google.genai import errors  # <--- Add this import to catch SDK specific errors
from pydantic import BaseModel, Field

client = genai.Client()

class SecurityResponse(BaseModel):
    intent: str = Field(description="The detected user intent")
    risk_score: int = Field(description="Risk rating from 1 to 5")
    security_status: str = Field(description="MUST be 'APPROVED' if risk_score is 1 or 2. MUST be 'DENIED' if risk_score is 3, 4, or 5.")

def process_natural_language_request(user_query):
    config = types.GenerateContentConfig(
        system_instruction=(
            "You are an intelligent CIAM security orchestration agent. "
            "Evaluate the access request query for malicious intent or architectural compliance. "
            "Assign a risk score from 1 to 5. "
            "Determine the final security_status based strictly on the risk threshold rules."
        ),
        temperature=0.1,
        response_mime_type="application/json",
        response_schema=SecurityResponse, 
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_query,
            config=config
        )
        return response.text

    # Intercept API-level errors gracefully
    except errors.APIError as e:
        if e.code == 429:
            # Return a mock JSON string containing "DENIED" so app.py doesn't crash 
            # and explicitly note the rate limit issue inside the logs
            return '{"intent": "RATE_LIMIT_EXCEEDED", "risk_score": 5, "security_status": "DENIED - API Quota Exhausted. Please wait 60 seconds."}'
        
        # Pass other API errors through as a clean string message
        return f'{{"intent": "API_ERROR", "risk_score": 5, "security_status": "DENIED - Error {e.code}: {e.message}"}}'
