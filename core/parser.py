import fitz
from docx import Document

def parse_resume(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError(f"Unsupported file format: {file_path}. Supported: .pdf, .docx, .txt")

