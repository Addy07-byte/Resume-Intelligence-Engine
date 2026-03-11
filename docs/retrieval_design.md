# Retrieval Design

## Embedding Model
- text-embedding-3-small (OpenAI)

## Similarity Metric
- Cosine similarity

## Retrieval Method
- Top-k retrieval (k=5 default)

## Why Top-K Over Fixed Threshold
- Fixed similarity thresholds are unstable across different corpora
- Embedding similarity distributions vary per dataset
- Top-k always returns the most relevant chunks

## JD Preprocessing
- Raw job descriptions contain boilerplate (benefits, EEO statements)
- JD is preprocessed by LLM to extract only requirements and responsibilities
- Clean JD query produces more accurate embeddings and retrieval

## Reranking (Future)
- Cross-encoder reranker between retrieval and generation
- Improves relevance of chunks passed to LLM