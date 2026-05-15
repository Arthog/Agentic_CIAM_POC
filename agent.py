from google import genai
from google.genai import types
from pydantic import BaseModel, Field # Keep these!

client = genai.Client()

# Keep your schema definition
class SecurityResponse(BaseModel):
    intent: str = Field(description="The detected user intent")
    risk_score: int = Field(description="Risk rating from 1 to 5")

def process_natural_language_request(user_query):
    config = types.GenerateContentConfig(
        system_instruction="Analyze the CIAM request.",
        temperature=0.1,
        # This tells the Gemini gateway to validate against your Pydantic schema
        response_mime_type="application/json",
        response_schema=SecurityResponse, 
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_query,
        config=config
    )
    return response.text
