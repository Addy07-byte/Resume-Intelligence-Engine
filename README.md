# Resume Intelligence Engine

A RAG-powered system that ingests a user's resume, retrieves relevant experience for a job description, and generates a tailored resume grounded in the user's real work history.

## Stack
- LangChain + OpenAI GPT-4o
- ChromaDB (in-memory vector store)
- Streamlit (UI)
- PyMuPDF + python-docx (parsing)
- fpdf2 + python-docx (export)

## How It Works
1. Upload 1-3 resume PDFs
2. System parses and embeds all content
3. Paste a job description
4. System retrieves most relevant experience
5. LLM generates a tailored resume
6. Download as PDF or DOCX

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your OpenAI key to `.env`
4. Run: `streamlit run app.py`

## Project Structure
- `core/` - All pipeline modules
- `docs/` - Architecture and design decisions
- `app.py` - Streamlit entry point