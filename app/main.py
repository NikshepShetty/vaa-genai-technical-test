from fastapi import FastAPI, HTTPException
from app.schemas import TravelQuery, HelpResponse
from app.prompt import generate_prompt
from openai import OpenAI
import os
from dotenv import load_dotenv
from app.vector_store import VectorStoreService
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

app = FastAPI()

vs = VectorStoreService()
vs.load_help_content()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/help-assistant", response_model=HelpResponse)
def help_assistant(query: TravelQuery) -> HelpResponse:
    """
    RAG-based help assistant endpoint.
    Candidates should implement:
    1) Retrieval of relevant chunks from help_content.json via vector store
    2) Prompting the model with retrieved context
    3) Returning grounded answers with sources & confidence
    """
    try:
        print(f"🔍 Received help query: {query.query}")

        # Category validation
        allowed_categories = vs.get_category_list()
        category_lower: str | None = None
        if query.category is not None:
            category_lower = query.category.strip().lower()
            if category_lower not in allowed_categories:
                raise HTTPException(status_code=422, detail=f"Invalid category value. \nAllowed categories: {', '.join(allowed_categories)}") # Display allowed categories as comma seperated string
        
        # Retrieve relevant chunks from ChromaDB
        search_results = vs.search(query = query.query, category = category_lower)

        # Empty result check
        if len(search_results)==0:
            return HelpResponse(
                answer="I don't have enough information in the provided help content to answer that.",
                sources=[],
                confidence=None
            )

        retrieved_context = "\n\n---\n\n".join(entry["text"] for entry in search_results)
        prompt = generate_prompt(query.query, retrieved_context)

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful support assistant. Answer only using provided context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )
        content = completion.choices[0].message.content
        print(f"📝 OpenAI Response: {content}")
        
        sources: list[str] = list(dict.fromkeys(entry["source_id"] for entry in search_results)) # Adding only unique source ids while maintaining order

        # Take cosine similarity of top chunk as the score
        raw_score: float | None = search_results[0].get("score")
        score: float | None = (raw_score * 100) if raw_score is not None else None
        
        # Tried - Weighted average for confidence scores (reciprocal)
        # weighted_sum: float = 0.0
        # weight_sum: float = 0.0
        # score: Optional[float] = None
        # for i, entry in enumerate(search_results):
        #     weight = 1.0 / (i+1) # Rank 1 will have weight 1, rank 2 = 0.5, rank 3 = 0.33 and so on
        #     weight_sum += weight # sum of weights
        #     weighted_sum += weight * entry["score"] # sum of weighted scores
        
        # if weight_sum>0:
        #     score = weighted_sum/weight_sum
        # else:
        #     score = None # Omit score if no score is retrieved

        return HelpResponse(answer=content, sources=sources, confidence=score)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@app.get("/")
def read_root() -> dict:
    return {"message": "Travel Assistant API is running"}

@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}

# Two endpoint had the same name and function, commented this one 
# @app.post("/help-assistant", response_model=HelpResponse)
# def help_assistant(query: TravelQuery):
#     """
#     TODO: Implement RAG-based help assistant endpoint
    
#     This endpoint should:
#     1. Use vector store to retrieve relevant context from seed data
#     2. Generate contextual response using retrieved information
#     3. Return structured response with sources and confidence
#     """
#     # Placeholder implementation - candidates should replace this
#     return HelpResponse(
#         answer="This is a placeholder response. Implement RAG architecture to provide real answers based on travel data.",
#         sources=["hotel_001", "flight_002"],  # Should be actual source IDs from retrieval
#         confidence=0.8
#     )
