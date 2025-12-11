import os
from dotenv import load_dotenv
from pypdf import PdfReader
import chromadb
from openai import OpenAI

def load_environment():
    """Load environment variables and verify API key exists."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return api_key

def extract_text_from_pdf(pdf_path):
    """Extract text from all pages of a PDF file."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text

def chunk_text(text, chunk_size=1000, overlap=100):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)

    return chunks

def create_embeddings(client, text_chunk):
    """Generate embedding for a text chunk using OpenAI."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text_chunk
    )
    return response.data[0].embedding

def initialize_chromadb_and_store(chunks, openai_client):
    """Initialize ChromaDB and store embeddings."""
    print("Initializing ChromaDB and generating embeddings...")

    # Create in-memory ChromaDB client
    chroma_client = chromadb.Client()

    # Create collection
    collection = chroma_client.create_collection(name="resume_test")

    # Generate embeddings and store in ChromaDB
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        embedding = create_embeddings(openai_client, chunk)

        collection.add(
            embeddings=[embedding],
            documents=[chunk],
            ids=[f"chunk_{i}"],
            metadatas=[{"chunk_index": i}]
        )

    print(f"Stored {len(chunks)} chunks in ChromaDB.\n")
    return collection

def query_rag(question, collection, openai_client):
    """Query the RAG system with a question."""
    # Generate embedding for the question
    question_embedding = create_embeddings(openai_client, question)

    # Query ChromaDB for top 10 most relevant chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=10
    )

    # Extract the retrieved chunks
    retrieved_chunks = results['documents'][0]

    # DEBUG: Print retrieved context BEFORE sending to OpenAI
    print("\n" + "=" * 80)
    print("DEBUG: RETRIEVED CONTEXT FROM CHROMADB")
    print("=" * 80)
    for i, chunk in enumerate(retrieved_chunks):
        print(f"\n[CHUNK {i+1}]:")
        print("-" * 80)
        print(chunk)
        print("-" * 80)
    print("=" * 80)
    print()

    # Build context from retrieved chunks
    context = "\n\n".join([f"[Context {i+1}]: {chunk}" for i, chunk in enumerate(retrieved_chunks)])

    # Construct prompt
    prompt = f"""Answer the question based on the following context. If the answer cannot be found in the context, say so.

Context:
{context}

Question: {question}

Answer:"""

    # Call GPT-4o
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

def main():
    """Main function to run the RAG spike test."""
    try:
        # 1. Load environment variables
        print("Loading environment variables...")
        api_key = load_environment()
        openai_client = OpenAI(api_key=api_key)
        print("Environment loaded successfully.\n")

        # 2. Extract text from PDF
        print("Extracting text from syllabus.pdf...")
        pdf_path = "syllabus.pdf"
        text = extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(text)} characters from PDF.\n")

        # 3. Chunk the text
        print("Chunking text...")
        chunks = chunk_text(text, chunk_size=1000, overlap=100)
        print(f"Created {len(chunks)} chunks.\n")

        # 4. Initialize ChromaDB and store embeddings
        collection = initialize_chromadb_and_store(chunks, openai_client)

        # 5. Enter query loop
        print("=" * 60)
        print("RAG System Ready! You can now ask questions.")
        print("Type 'quit', 'exit', or press Ctrl+C to exit.")
        print("=" * 60)
        print()

        while True:
            try:
                question = input("Your question: ").strip()

                if question.lower() in ['quit', 'exit']:
                    print("Exiting RAG system. Goodbye!")
                    break

                if not question:
                    print("Please enter a question.\n")
                    continue

                print("\nSearching for relevant context and generating answer...\n")
                answer = query_rag(question, collection, openai_client)

                print("Answer:")
                print("-" * 60)
                print(answer)
                print("-" * 60)
                print()

            except KeyboardInterrupt:
                print("\n\nExiting RAG system. Goodbye!")
                break

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
