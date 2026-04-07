import streamlit as st
import chromadb
import tempfile
import os
from dotenv import load_dotenv

from core.parser import parse_resume
from core.chunker import chunk_text
from core.embedder import embed_chunks, get_embedding_model
from core.retriever import get_collection, store_embeddings, retrieve_relevant_chunks
from core.jd_processor import process_job_description
from core.generator import generate_resume
from core.exporter import export_to_pdf, export_to_docx

load_dotenv()

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="Resume Intelligence Engine", layout="wide")
st.title("🧠 Resume Intelligence Engine")
st.caption("Upload your resume, paste a job description, get a tailored resume.")

# ── Session state ─────────────────────────────────────────────
if "generated_resume" not in st.session_state:
    st.session_state.generated_resume = ""

if "contact_info" not in st.session_state:
    st.session_state.contact_info = ""

st.write("DEBUG - Contact info passed:")
st.write(st.session_state.contact_info)

# ── Step 1: Resume Upload ─────────────────────────────────────
st.header("Step 1: Upload Your Resume(s)")
uploaded_files = st.file_uploader(
    "Upload up to 3 resumes (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) > 3:
    st.error("Maximum 3 resumes allowed.")
    uploaded_files = uploaded_files[:3]

# ── Step 2: Job Description ───────────────────────────────────
st.header("Step 2: Paste Job Description")
raw_jd = st.text_area("Paste the full job description here", height=200)

# ── Step 3: Generate ──────────────────────────────────────────
st.header("Step 3: Generate Tailored Resume")

if st.button("Generate Resume"):
    if not uploaded_files:
        st.error("Please upload at least one resume.")
    elif not raw_jd.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Processing..."):
            # Initialize ChromaDB
            client = chromadb.Client()
            collection = get_collection(client)
            model = get_embedding_model()

            # Parse, chunk, embed and store each resume
            for file in uploaded_files:
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=os.path.splitext(file.name)[1]
                ) as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name

                text = parse_resume(tmp_path)

                # Extract contact info from first resume only
                if file == uploaded_files[0]:
                    st.session_state.contact_info = text

                chunks = chunk_text(text)
                embeddings, metadatas = embed_chunks(chunks, source_filename=file.name)
                store_embeddings(collection, chunks, embeddings, metadatas)
                os.unlink(tmp_path)

            # Process and embed the job description
            clean_jd = process_job_description(raw_jd)
            query_vector = model.embed_query(clean_jd)

            # Retrieve top-k relevant chunks
            retrieved_chunks = retrieve_relevant_chunks(collection, query_vector, k=5)

            # Generate tailored resume
            result = generate_resume(
                retrieved_chunks,
                clean_jd,
                contact_info=st.session_state.get("contact_info", "")
            )
            st.session_state.generated_resume = result

# ── Step 4: Edit and Download ─────────────────────────────────
if st.session_state.generated_resume:
    st.header("Step 4: Review and Edit")

    edited_resume = st.text_area(
        "Edit your resume before downloading",
        value=st.session_state.generated_resume,
        height=400
    )

    st.header("Step 5: Download")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Download as DOCX"):
            path = export_to_docx(edited_resume, "resume_output.docx")
            with open(path, "rb") as f:
                st.download_button(
                    label="Click to Download DOCX",
                    data=f,
                    file_name="tailored_resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

    with col2:
        if st.button("Download as PDF"):
            path = export_to_pdf(edited_resume, "resume_output.pdf")
            with open(path, "rb") as f:
                st.download_button(
                    label="Click to Download PDF",
                    data=f,
                    file_name="tailored_resume.pdf",
                    mime="application/pdf"
                )