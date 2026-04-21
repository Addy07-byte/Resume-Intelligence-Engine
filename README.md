# Resume Intelligence Engine

A RAG-powered system that ingests a user's resume, retrieves relevant experience for a job description, and generates a tailored resume grounded in the user's real work history.

## Stack
- LangChain + OpenAI GPT-4o
- ChromaDB (in-memory vector store)
- Streamlit (UI)
- PyMuPDF + python-docx (parsing)
- fpdf2 + python-docx (export)

## How It Works

### Deployed (v2.0)
1. User submits a query via Streamlit interface
2. OpenAI API processes query and returns response
3. App captures real token usage from API response
4. Multi-feature linear regression model (built from scratch in NumPy)
   predicts water consumption based on tokens and model type
5. Result displayed dynamically per query

### Research Pipeline (v3.0, not yet wired into deployment)
- Synthetic dataset generation using Li et al. 2023 WUE values per region
- Three models compared: linear regression (ordinal), linear regression 
  (one-hot), decision tree
- Decision tree performs best (MAE 0.000659, 72% improvement over baseline)
- Feature importance: model type (40%), tokens (38%), region (22%)
- Next step: wire the decision tree into the deployed app so predictions
  account for region

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your OpenAI key to `.env`
4. Run: `streamlit run app.py`

## Project Structure
- `core/` - All pipeline modules
- `docs/` - Architecture and design decisions
- `app.py` - Streamlit entry point