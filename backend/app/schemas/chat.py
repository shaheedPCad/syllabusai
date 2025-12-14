"""Chat schemas for RAG-based Q&A."""
from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User's question about course materials"
    )


class DocumentSource(BaseModel):
    """A source document chunk used to answer the question."""
    chunk_id: str = Field(..., description="ID of the document chunk")
    text: str = Field(..., description="Preview of the source text")
    similarity_score: float = Field(..., description="Relevance score (0-1)", ge=0, le=1)


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    answer: str = Field(..., description="AI-generated answer based on course materials")
    sources: List[DocumentSource] = Field(
        default=[],
        description="Source chunks used to generate answer"
    )
    confidence: str = Field(
        default="medium",
        description="Confidence level: low, medium, high"
    )
