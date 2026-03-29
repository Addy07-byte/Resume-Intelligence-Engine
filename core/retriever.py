import chromadb
from chromadb.config import Settings


def get_collection(client: chromadb.Client, collection_name: str = "resume_chunks"):
    """
    Gets or creates a ChromaDB collection.
    Using get_or_create means calling this twice won't duplicate the collection.
    """
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}  # use cosine similarity for matching
    )


def build_ids(metadatas: list[dict]) -> list[str]:
    """
    Builds a unique ID for each chunk based on source filename and chunk index.
    Example: "test_resume.pdf_chunk_0"

    This is the deduplication key — if the same resume is uploaded again,
    the IDs will be identical and ChromaDB will skip the duplicates.
    """
    return [f"{m['source']}_chunk_{m['chunk_index']}" for m in metadatas]


def store_embeddings(
    collection,
    chunks: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict]
) -> None:
    """
    Stores chunks, their vectors, and metadata into ChromaDB.
    Uses upsert instead of add — safe to call multiple times with same data.
    Upsert = insert if new, update if ID already exists.
    """
    ids = build_ids(metadatas)

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,       # the original text — retrievable later
        metadatas=metadatas
    )

    print(f"Stored {len(chunks)} chunks into collection '{collection.name}'")


def retrieve_relevant_chunks(
    collection,
    query_embedding: list[float],
    k: int = 5
) -> list[dict]:
    """
    Queries ChromaDB with a vector and returns the top-k most similar chunks.
    Returns a list of dicts with 'text', 'source', and 'score' for each result.
    """
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    # Flatten results into a clean list of dicts
    retrieved = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        retrieved.append({
            "text": doc,
            "source": meta.get("source"),
            "score": round(1 - dist, 4)  # convert cosine distance → similarity score
        })

    return retrieved


if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from dotenv import load_dotenv
    from core.chunker import chunk_text
    from core.embedder import embed_chunks, get_embedding_model

    load_dotenv()

    # Step 1: Chunk and embed some sample text
    sample_text = """
    Led a team of 5 engineers to build a payment processing API.
    Reduced system latency by 40% through query optimization.
    Designed and deployed a machine learning pipeline on AWS.
    Managed stakeholder communication and sprint planning.
    """
    chunks = chunk_text(sample_text)
    embeddings, metadatas = embed_chunks(chunks, source_filename="test_resume.pdf")

    # Step 2: Store in ChromaDB
    client = chromadb.Client()
    collection = get_collection(client)
    store_embeddings(collection, chunks, embeddings, metadatas)

    # Step 3: Query with a job description snippet
    query = "Looking for an engineer with API development and cloud experience"
    model = get_embedding_model()
    query_vector = model.embed_query(query)

    results = retrieve_relevant_chunks(collection, query_vector, k=3)

    print("\nTop retrieved chunks:")
    for r in results:
        print(f"  Score: {r['score']} | Source: {r['source']}")
        print(f"  Text: {r['text']}\n")