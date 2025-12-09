from pydantic import BaseModel, Field
from typing import List, Optional


class TravelQuery(BaseModel):
    """Request body schema for user travel query."""
    query: str = Field(..., example="Can you recommend a luxury hotel in Tokyo with good ratings and spa facilities?")


class HotelRecommendation(BaseModel):
    name: str
    city: str
    price_per_night: float
    rating: float


class FlightRecommendation(BaseModel):
    airline: str
    from_airport: str
    to_airport: str
    price: float
    duration: str
    date: str


class ExperienceRecommendation(BaseModel):
    name: str
    city: str
    price: float
    duration: str


class HelpResponse(BaseModel):
    """Structured response returned by the RAG-based Help Assistant."""
    answer: str = Field(..., description="AI-generated answer based on retrieved context")
    sources: List[str] = Field(..., description="IDs of help content used to generate the answer")
    confidence: Optional[float] = Field(None, description="Confidence score of the response")
    
    # TODO: Implement RAG architecture to populate these fields
    # - Retrieve relevant context from vector store
    # - Generate contextual response using OpenAI
    # - Track source documents for transparency

# Legacy schema - kept for backward compatibility during migration
class TravelAdvice(BaseModel):
    """Structured response returned by the Gen-AI Travel Assistant."""
    destination: str
    reason: str
    budget: str
    tips: List[str]

    # Optional enrichments
    hotel: Optional[HotelRecommendation] = None
    flight: Optional[FlightRecommendation] = None
    experience: Optional[ExperienceRecommendation] = None
