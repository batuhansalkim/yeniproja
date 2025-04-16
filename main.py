import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize FastAPI app
app = FastAPI()

class EmergencyMessage(BaseModel):
    message: str

def analyze_emergency(message: str) -> dict:
    """
    Analyze emergency message using Gemini API and return structured response
    """
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    You are an advanced emergency assistant. Analyze the following emergency message and provide a structured response:
    
    Message: {message}
    
    Provide your response in the following JSON format:
    {{
        "urgency": <Integer between 1-5, where 1 is lowest urgency and 5 is critical>,
        "rationale": <Brief explanation of the urgency level>,
        "suggestions": <Optional additional action or intervention suggestions>
    }}
    
    Consider the following in your analysis:
    1. Severity of symptoms
    2. Risk factors
    3. Nature of the emergency
    4. Potential for escalation
    """
    
    try:
        response = model.generate_content(prompt)
        # Extract JSON from response
        response_text = response.text
        # Find JSON in the response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        
        return json.loads(json_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing emergency message: {str(e)}")

@app.post("/analyze")
async def analyze(message: EmergencyMessage):
    """
    Endpoint to analyze emergency messages
    """
    return analyze_emergency(message.message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 