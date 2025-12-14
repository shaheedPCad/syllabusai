"""
Chat Service for RAG-based question answering.
Handles semantic search and GPT-4 answer generation.
"""
import logging
from uuid import UUID
from typing import List, Tuple

from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.models import DocumentChunk, Document
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)


class ChatService:
    """Service for RAG-based chat with course materials."""

    def __init__(self):
        """Initialize chat service with OpenAI client."""
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.chat_model = "gpt-4o"  # or gpt-3.5-turbo for cost savings
        self.embedding_model = "text-embedding-3-small"

    async def ask_question(
        self,
        course_id: UUID,
        question: str,
        session: AsyncSession,
        top_k: int = 5,
        similarity_threshold: float = 0.7
    ) -> Tuple[str, List[Tuple[DocumentChunk, float]]]:
        """
        Answer a question about course materials using RAG.

        Args:
            course_id: UUID of the course
            question: User's question
            session: Async database session
            top_k: Number of relevant chunks to retrieve
            similarity_threshold: Minimum similarity score (0-1)

        Returns:
            Tuple of (answer_text, list of (chunk, similarity_score))

        Raises:
            ValueError: If no relevant documents found
            Exception: If answer generation fails
        """
        # Step 1: Generate embedding for the question
        logger.info(f"Embedding question for course {course_id}")
        query_embedding = await self._embed_question(question)

        # Step 2: Retrieve relevant chunks using pgvector similarity search
        logger.info(f"Searching for top {top_k} relevant chunks")
        chunks_with_scores = await self._search_relevant_chunks(
            course_id=course_id,
            query_embedding=query_embedding,
            session=session,
            top_k=top_k,
            similarity_threshold=similarity_threshold
        )

        if not chunks_with_scores:
            raise ValueError("No relevant course materials found for this question")

        logger.info(f"Found {len(chunks_with_scores)} relevant chunks")

        # Step 3: Construct context from retrieved chunks
        context = self._build_context(chunks_with_scores)

        # Step 4: Generate answer using GPT-4
        logger.info("Generating answer with GPT-4")
        answer = await self._generate_answer(question, context)

        return answer, chunks_with_scores

    async def _embed_question(self, question: str) -> List[float]:
        """
        Generate embedding for user's question.

        Args:
            question: User's question text

        Returns:
            Embedding vector as List[float]
        """
        # Reuse RAGService's embedding method
        embeddings = await rag_service._generate_embeddings([question])
        return embeddings[0]

    async def _search_relevant_chunks(
        self,
        course_id: UUID,
        query_embedding: List[float],
        session: AsyncSession,
        top_k: int,
        similarity_threshold: float
    ) -> List[Tuple[DocumentChunk, float]]:
        """
        Search for semantically similar document chunks using pgvector.

        Args:
            course_id: Filter to this course only
            query_embedding: Query vector
            session: Async database session
            top_k: Number of results to return
            similarity_threshold: Minimum similarity (0-1)

        Returns:
            List of (DocumentChunk, similarity_score) tuples, ordered by relevance
        """
        # Cosine similarity score: 1 - cosine_distance
        # Higher score = more similar (0-1 range)
        similarity = (1 - DocumentChunk.embedding.cosine_distance(query_embedding)).label("similarity")

        # Build query with join to filter by course
        stmt = (
            select(DocumentChunk, similarity)
            .join(Document, DocumentChunk.document_id == Document.id)
            .where(Document.course_id == course_id)
            .where(similarity >= similarity_threshold)  # Filter by threshold
            .order_by(similarity.desc())  # Highest similarity first
            .limit(top_k)
        )

        result = await session.execute(stmt)
        chunks_with_scores = result.all()

        logger.info(f"Found {len(chunks_with_scores)} chunks above threshold {similarity_threshold}")
        if chunks_with_scores:
            scores = [score for _, score in chunks_with_scores]
            logger.info(f"Similarity scores: min={min(scores):.3f}, max={max(scores):.3f}, avg={sum(scores)/len(scores):.3f}")

        return chunks_with_scores

    def _build_context(self, chunks_with_scores: List[Tuple[DocumentChunk, float]]) -> str:
        """
        Build context string from retrieved chunks.

        Args:
            chunks_with_scores: List of (chunk, score) tuples

        Returns:
            Formatted context string for GPT-4
        """
        context_parts = []
        for idx, (chunk, score) in enumerate(chunks_with_scores, 1):
            context_parts.append(
                f"[Source {idx}] (Relevance: {score:.2f})\n{chunk.text_content}\n"
            )

        return "\n".join(context_parts)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _generate_answer(self, question: str, context: str) -> str:
        """
        Generate answer using GPT-4 based on context.

        Args:
            question: User's question
            context: Retrieved context from documents

        Returns:
            Generated answer text
        """
        system_prompt = """You are a helpful teaching assistant for this course.
Your role is to answer student questions based ONLY on the provided course materials.

Guidelines:
- Answer questions clearly and concisely
- Base your answer ONLY on the provided context
- If the context doesn't contain enough information, say "I don't have enough information in the course materials to answer that question"
- If the question is unclear, ask for clarification
- Cite specific sources when possible (e.g., "According to Source 1...")
- Be helpful and encouraging"""

        user_prompt = f"""Context from course materials:

{context}

Student Question: {question}

Please provide a clear, helpful answer based on the context above."""

        response = await self.openai_client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        answer = response.choices[0].message.content
        logger.info(f"Generated answer: {answer[:100]}...")

        return answer


# Singleton instance
chat_service = ChatService()
