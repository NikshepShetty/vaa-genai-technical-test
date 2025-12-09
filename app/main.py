from fastapi import FastAPI, HTTPException
from app.schemas import TravelQuery, HelpResponse
from app.prompt import generate_prompt
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/help-assistant", response_model=HelpResponse)
def help_assistant(query: TravelQuery):
    """
    RAG-based help assistant endpoint (stub).
    Candidates should implement:
    1) Retrieval of relevant chunks from help_content.json via vector store
    2) Prompting the model with retrieved context
    3) Returning grounded answers with sources & confidence
    """
    try:
        print(f"🔍 Received help query: {query.query}")
        # TODO: Replace with vector store retrieval of top-k context
        retrieved_context = ""  # e.g., concatenated text from matched chunks
        prompt = generate_prompt(query.query, retrieved_context)

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful support assistant. Answer only using provided context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )
        content = completion.choices[0].message.content
        print(f"📝 OpenAI Response: {content}")
        # Placeholder response. Replace sources with actual IDs from retrieval.
        return HelpResponse(answer=content, sources=[], confidence=None)
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
