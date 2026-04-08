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

st.set_page_config(
    page_title="Instant Resume Builder",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500;600&display=swap');

#MainMenu, footer, header,
div[data-testid="stDecoration"],
div[data-testid="stToolbar"] { display: none !important; }

.block-container {
    padding: 1.2rem 2rem 1rem 2rem !important;
    max-width: 100% !important;
}

h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    line-height: 1.2 !important;
    margin-bottom: 0 !important;
}
h3 {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.85rem !important;
    margin: 0 0 0.3rem 0 !important;
}
p, div, span, label, textarea {
    font-family: 'Inter', sans-serif !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    padding: 0.7rem 1rem !important;
    margin-bottom: 0.5rem !important;
    border-radius: 10px !important;
    border-color: #E5E7EB !important;
}

div[data-testid="stFileUploader"] section {
    padding: 0.5rem 0.75rem !important;
    min-height: unset !important;
    border-radius: 8px !important;
}
div[data-testid="stFileUploaderDropzoneInstructions"] span {
    font-size: 0.75rem !important;
}
div[data-testid="stFileUploaderDropzoneInstructions"] small {
    font-size: 0.65rem !important;
}

textarea {
    font-size: 0.8rem !important;
    line-height: 1.5 !important;
    border-radius: 8px !important;
}

.stButton > button[kind="primary"] {
    background: #4F46E5 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    height: 40px !important;
    box-shadow: 0 2px 12px rgba(79,70,229,0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #4338CA !important;
}

.stButton > button[kind="secondary"] {
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    height: 36px !important;
    border-color: #C7D2FE !important;
    color: #4F46E5 !important;
}

.stDownloadButton > button {
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.75rem !important;
    height: 36px !important;
    background: #4F46E5 !important;
    color: #fff !important;
    border: none !important;
    width: 100% !important;
}

div[data-testid="stAlert"] {
    padding: 0.4rem 0.75rem !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
}

.stCaptionContainer p {
    font-size: 0.62rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    color: #4F46E5 !important;
    text-transform: uppercase !important;
    margin-bottom: 0.1rem !important;
}

hr { margin: 0.5rem 0 !important; border-color: #F3F4F6 !important; }

.badge {
    display: inline-block;
    background: #EEF2FF;
    color: #4F46E5;
    font-size: 0.62rem;
    font-weight: 600;
    padding: 0.15rem 0.55rem;
    border-radius: 20px;
    letter-spacing: 0.05em;
    vertical-align: middle;
    margin-left: 0.5rem;
}

.empty-panel {
    min-height: 460px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────
if "generated_resume" not in st.session_state:
    st.session_state.generated_resume = ""
if "contact_info" not in st.session_state:
    st.session_state.contact_info = ""

# ── Header ────────────────────────────────────────────────────
st.markdown("# ⚡ Instant Resume Builder <span class='badge'>RAG · GPT-4o</span>",
            unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:0.8rem;color:#6B7280;margin:0.1rem 0 0.5rem 0'>"
    "Tailored to the job. Grounded in your experience.</p>",
    unsafe_allow_html=True
)
st.divider()

# ── Two column layout ─────────────────────────────────────────
left, right = st.columns([1, 1.4], gap="large")

with left:
    with st.container(border=True):
        st.caption("STEP 01")
        st.subheader("Upload Resume")
        uploaded_files = st.file_uploader(
            "upload",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        if uploaded_files and len(uploaded_files) > 3:
            st.error("Max 3 resumes allowed.")
            uploaded_files = uploaded_files[:3]
        if uploaded_files:
            for f in uploaded_files:
                st.success(f"✓  {f.name}")

    with st.container(border=True):
        st.caption("STEP 02")
        st.subheader("Paste Job Description")
        raw_jd = st.text_area(
            "jd",
            height=150,
            placeholder="Paste the full job description here...",
            label_visibility="collapsed"
        )

    # Step 03 — button only inside container
    with st.container(border=True):
        st.caption("STEP 03")
        generate_clicked = st.button(
            "⚡  Generate Tailored Resume",
            use_container_width=True,
            type="primary"
        )

# Status and pipeline run OUTSIDE the container and column
# This prevents the overlap glitch
if generate_clicked:
    if not uploaded_files:
        st.error("Upload at least one resume.")
    elif not raw_jd.strip():
        st.error("Paste a job description.")
    else:
        with st.status("Analysing your experience...", expanded=True) as status:
            st.write("📄  Extracting resume data...")
            client = chromadb.Client()
            collection = get_collection(client)
            model = get_embedding_model()

            for file in uploaded_files:
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=os.path.splitext(file.name)[1]
                ) as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name

                text = parse_resume(tmp_path)
                if file == uploaded_files[0]:
                    st.session_state.contact_info = text

                chunks = chunk_text(text)
                embeddings, metadatas = embed_chunks(
                    chunks, source_filename=file.name)
                store_embeddings(collection, chunks, embeddings, metadatas)
                os.unlink(tmp_path)

            st.write("🔍  Matching to job description...")
            clean_jd = process_job_description(raw_jd)
            query_vector = model.embed_query(clean_jd)
            retrieved_chunks = retrieve_relevant_chunks(
                collection, query_vector, k=5)

            st.write("✍️  Drafting your resume...")
            result = generate_resume(
                retrieved_chunks,
                clean_jd,
                contact_info=st.session_state.get("contact_info", "")
            )
            st.session_state.generated_resume = result
            status.update(
                label="✅  Resume ready!",
                state="complete",
                expanded=False
            )

with right:
    if st.session_state.generated_resume:
        with st.container(border=True):
            st.success("✓  Resume ready — review and edit below.")
            edited_resume = st.text_area(
                "resume_out",
                value=st.session_state.generated_resume,
                height=400,
                label_visibility="collapsed"
            )
            c1, c2 = st.columns(2, gap="small")
            with c1:
                if st.button("Prepare DOCX", use_container_width=True):
                    path = export_to_docx(edited_resume, "resume_output.docx")
                    with open(path, "rb") as f:
                        st.download_button(
                            "⬇  Download DOCX", f,
                            file_name="tailored_resume.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
            with c2:
                if st.button("Prepare PDF", use_container_width=True):
                    path = export_to_pdf(edited_resume, "resume_output.pdf")
                    with open(path, "rb") as f:
                        st.download_button(
                            "⬇  Download PDF", f,
                            file_name="tailored_resume.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
    else:
        with st.container(border=True):
            st.markdown("""
            <div class="empty-panel">
                <div style="font-size:2.5rem;opacity:0.15">📄</div>
                <p style="font-family:'Syne',sans-serif;font-weight:700;
                   font-size:0.95rem;color:#D1D5DB;margin:0">
                    Your tailored resume awaits
                </p>
                <p style="font-size:0.75rem;color:#E5E7EB;margin:0">
                    Upload a resume · Paste a JD · Click Generate
                </p>
            </div>
            """, unsafe_allow_html=True)