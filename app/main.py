from fastapi import FastAPI, HTTPException
from app.schemas import TravelQuery, TravelAdvice, HelpResponse
from app.prompt import generate_prompt
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/travel-assistant", response_model=TravelAdvice)
def travel_assistant(query: TravelQuery):
    try:
        print(f"🔍 Received query: {query.query}")
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"🔑 Using API key: {api_key[:10]}..." if api_key else "❌ No API key")
        prompt = generate_prompt(query.query)
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful travel assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=150
        )
        content = completion.choices[0].message.content
        print(f"📝 OpenAI Response: {content}")
        
        # For now, return structured mock data (TODO: parse AI response properly)
        return TravelAdvice(
            destination="Tokyo",
            reason="Great culture, food, and safe for travelers.",
            budget="Moderate to High", 
            tips=[
                "Visit Senso-ji Temple early morning.",
                "Try local street food in Shibuya.", 
                "Use JR Pass for transportation."
            ]
        )
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Travel Assistant API is running"}

@app.post("/help-assistant", response_model=HelpResponse)
def help_assistant(query: TravelQuery):
    """
    TODO: Implement RAG-based help assistant endpoint
    
    This endpoint should:
    1. Use vector store to retrieve relevant context from seed data
    2. Generate contextual response using retrieved information
    3. Return structured response with sources and confidence
    """
    # Placeholder implementation - candidates should replace this
    return HelpResponse(
        answer="This is a placeholder response. Implement RAG architecture to provide real answers based on travel data.",
        sources=["hotel_001", "flight_002"],  # Should be actual source IDs from retrieval
        confidence=0.8
    )

@app.get("/health")
def health_check():
    return {"status": "healthy"}
