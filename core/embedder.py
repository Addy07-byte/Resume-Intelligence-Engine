from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings

load_dotenv() 


def get_embedding_model() -> OpenAIEmbeddings:
    """
    Returns a configured OpenAI embedding model.
    text-embedding-3-small: 1536 dimensions, fast, cheap, high quality.
    """
    return OpenAIEmbeddings(model="text-embedding-3-small")


def embed_chunks(chunks: list[str], source_filename: str) -> tuple[list[list[float]], list[dict]]:
    """
    Takes a list of text chunks and returns:
    - embeddings: list of vectors (one per chunk)
    - metadatas: list of metadata dicts (one per chunk)

    The metadata links each vector back to its source,
    which is critical for faithfulness tracking and deduplication.
    """
    model = get_embedding_model()

    # Generate all embeddings in one batched API call (efficient)
    embeddings = model.embed_documents(chunks)

    # Build metadata for every chunk — this is what links text to vector
    metadatas = [
        {
            "source": source_filename,   # which resume this came from
            "chunk_index": i,            # position in the original document
            "text": chunk                # the actual text, stored alongside the vector
        }
        for i, chunk in enumerate(chunks)
    ]

    return embeddings, metadatas

if __name__ == "__main__":
    from core.chunker import chunk_text

    sample_text = "Led a team of 5 engineers. Built a REST API using FastAPI. Reduced latency by 40%."
    chunks = chunk_text(sample_text)

    embeddings, metadatas = embed_chunks(chunks, source_filename="test_resume.pdf")

    print(f"Number of chunks: {len(chunks)}")
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding dimensions: {len(embeddings[0])}")  # Should be 1536
    print(f"Sample metadata: {metadatas[0]}")
