"""
RAG Service for processing documents into vector embeddings.
Handles PDF text extraction, chunking, and embedding generation.
"""
import io
import logging
from uuid import UUID
from typing import List

from openai import AsyncOpenAI
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tenacity import retry, stop_after_attempt, wait_exponential
from sqlmodel import Session

from app.core.config import settings
from app.models import Document, DocumentChunk
from app.services.storage import s3_service

logger = logging.getLogger(__name__)


class RAGService:
    """Service for processing documents into vector embeddings."""

    def __init__(self):
        """Initialize RAG service with OpenAI client."""
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.embedding_model = "text-embedding-3-small"
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    async def process_document(self, document_id: UUID, session: Session) -> int:
        """
        Process a document: extract text, chunk, generate embeddings, save to DB.

        Args:
            document_id: UUID of the document to process
            session: Synchronous database session (for Celery task)

        Returns:
            Number of chunks created

        Raises:
            ValueError: If document not found
            Exception: If processing fails
        """
        # Step 1: Fetch Document from database
        logger.info(f"Processing document {document_id}")
        document = session.get(Document, document_id)
        if not document:
            raise ValueError(f"Document {document_id} not found")

        logger.info(f"Found document: {document.filename} (s3_key: {document.s3_key})")

        # Step 2: Download file from MinIO
        try:
            file_content = s3_service.download_file(document.s3_key)
            logger.info(f"Downloaded {len(file_content)} bytes from S3")
        except Exception as e:
            logger.error(f"Failed to download file: {e}")
            raise

        # Step 3: Extract text from PDF
        try:
            text = self._extract_text_from_pdf(file_content)
            logger.info(f"Extracted {len(text)} characters from PDF")
        except Exception as e:
            logger.error(f"Failed to extract text: {e}")
            raise

        # Step 4: Split text into chunks
        chunks = self.text_splitter.split_text(text)
        logger.info(f"Split text into {len(chunks)} chunks")

        # Step 5: Generate embeddings for each chunk
        try:
            embeddings = await self._generate_embeddings(chunks)
            logger.info(f"Generated {len(embeddings)} embeddings")
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise

        # Step 6: Save chunks to database
        try:
            for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
                chunk = DocumentChunk(
                    document_id=document_id,
                    text_content=chunk_text,
                    chunk_index=idx,
                    embedding=embedding
                )
                session.add(chunk)

            session.commit()
            logger.info(f"Saved {len(chunks)} chunks to database")
            return len(chunks)
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save chunks: {e}")
            raise

    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """
        Extract text from PDF file content.

        Args:
            file_content: PDF file as bytes

        Returns:
            Extracted text as string
        """
        file_stream = io.BytesIO(file_content)
        reader = PdfReader(file_stream)

        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        full_text = "\n\n".join(text_parts)
        return full_text

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text chunks with retry logic.

        Args:
            texts: List of text chunks to embed

        Returns:
            List of embedding vectors (each is List[float])
        """
        # OpenAI allows batch embedding requests
        response = await self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=texts
        )

        embeddings = [item.embedding for item in response.data]
        return embeddings


# Singleton instance
rag_service = RAGService()
