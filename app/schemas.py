from pydantic import BaseModel, Field
from typing import List, Optional


class TravelQuery(BaseModel):
    """Request body schema for user travel query."""
    query: str = Field(..., min_length=1, example="Can you recommend a luxury hotel in Tokyo with good ratings and spa facilities?")
    category: Optional[str] = None # add optional category for filtering

"""Simplified schemas for help-only RAG test."""


class HelpResponse(BaseModel):
    """Structured response returned by the RAG-based Help Assistant."""
    answer: str = Field(..., description="AI-generated answer based on retrieved context")
    sources: List[str] = Field(..., description="IDs of help content used to generate the answer")
    confidence: Optional[float] = Field(None, description="Confidence score of the response")

# Legacy schema removed to keep the test focused on help-only RAG
