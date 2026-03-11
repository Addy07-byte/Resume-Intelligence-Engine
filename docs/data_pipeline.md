# Data Pipeline

## Input Formats Supported
- PDF resumes (text-based)
- Not supported yet: scanned PDFs, images, tables

## Parsing
- PyMuPDF extracts raw text from PDF files
- Text cleaned of excessive whitespace and special characters

## Chunking Strategy
Resumes divided by sections:
- Work Experience
- Projects
- Skills
- Education

Each bullet point is treated as one chunk.

Each chunk carries metadata:
- source: original filename
- section: which resume section it came from

## Embedding
- Model: text-embedding-3-small
- Embeddings generated per chunk
- Stored in ChromaDB in-memory collection

## Future Work
- Layout-aware chunking for tables and certificates
- Support for scanned PDFs via OCR