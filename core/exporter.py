from docx import Document
from fpdf import FPDF
import os


def export_to_docx(text: str, output_path: str) -> str:
    """
    Exports generated resume text to a DOCX file.
    Returns the output path for confirmation.
    """
    doc = Document()

    # Add each line as a paragraph
    for line in text.split("\n"):
        doc.add_paragraph(line)

    doc.save(output_path)
    print(f"DOCX saved to: {output_path}")
    return output_path


def export_to_pdf(text: str, output_path: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)

    for line in text.split("\n"):
        safe_line = line.strip().encode("latin-1", errors="replace").decode("latin-1")
        if safe_line == "":
            pdf.ln(6)
        else:
            pdf.set_x(15)
            pdf.write(8, safe_line)
            pdf.ln(8)

    pdf.output(output_path)
    print(f"PDF saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    sample_text = """
John Doe
Senior Software Engineer

Professional Summary
Experienced engineer with a strong background in API development, 
cloud infrastructure, and leading engineering teams.

Work Experience
- Led a team of 5 engineers to build a payment processing API
- Reduced system latency by 40% through query optimization
- Designed and deployed a machine learning pipeline on AWS

Skills
- Python
- AWS
- FastAPI
- Machine Learning
"""

    export_to_docx(sample_text, "test_resume.docx")
    export_to_pdf(sample_text, "test_resume.pdf")