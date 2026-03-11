# Architecture

## Flow
Resume Upload (1-3 PDFs)
      ↓
Document Parsing (PyMuPDF)
      ↓
Section-Based Chunking (by bullet point)
      ↓
Embedding Generation (text-embedding-3-small)
      ↓
Vector Storage (ChromaDB in-memory, per session)
      ↓
Job Description Preprocessing (extract requirements)
      ↓
Similarity Search (cosine similarity)
      ↓
Top-K Retrieval (across all uploaded resumes)
      ↓
LLM Generation (GPT-4o, grounded in retrieved chunks)
      ↓
Export (PDF + DOCX)

## Key Decisions

### Chunking
- Section-based chunking instead of fixed character chunking
- Each bullet point treated as a single chunk
- Chunks tagged with source filename for traceability

### Vector Store
- ChromaDB in-memory per session (no persistence needed)
- Each session gets one collection containing chunks from all uploaded resumes
- Cleared when session ends

### Retrieval
- Top-k retrieval over fixed similarity threshold
- Fixed thresholds are unstable across different corpora
- Top-k always returns the most relevant chunks regardless of score distribution

### Multi-resume Support
- Minimum 1 resume required
- Maximum 3 resumes per session
- All chunks pooled into one collection
- Retrieval pulls best chunks across all resumes

### Output
- Plain text displayed in UI
- Downloadable as PDF and DOCX