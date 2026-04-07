from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def build_prompt(retrieved_chunks: list[dict], job_description: str, contact_info: str) -> str:
    context = "\n\n".join(
        [f"- {chunk['text']}" for chunk in retrieved_chunks]
    )

    prompt = f"""
You are a professional resume writer. Your job is to write a tailored resume.

STRICT RULES — NEVER VIOLATE THESE:
- NEVER use placeholders like [Your Name] or [Your Email]
- NEVER change job titles, company names, or dates — use them exactly as provided
- NEVER invent or embellish anything not in the context
- If a detail is not provided, leave it out entirely

CANDIDATE CONTACT INFORMATION (always include exactly):
{contact_info}

JOB DESCRIPTION (always include exactly):
{job_description}

CANDIDATE EXPERIENCE (retrieved from their resume):
{context}

Write a tailored professional resume. Include:
- Candidate's real contact info from above
- A short professional summary (2-3 sentences)
- Work experience using ONLY real titles, companies and dates from the context
- Bullet points grounded only in the provided context
- Skills section based only on what appears in the context
"""
    return prompt


def generate_resume(retrieved_chunks: list[dict], job_description: str, contact_info: str = "") -> str:
    prompt = build_prompt(retrieved_chunks, job_description, contact_info)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a professional resume writer. You only use provided context. You never hallucinate. You never use placeholder text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # Simulated retrieved chunks (as if from retriever.py)
    sample_chunks = [
        {"text": "Led a team of 5 engineers to build a payment processing API", "source": "resume.pdf"},
        {"text": "Reduced system latency by 40% through query optimization", "source": "resume.pdf"},
        {"text": "Designed and deployed a machine learning pipeline on AWS", "source": "resume.pdf"},
    ]

    sample_jd = """
    We are looking for a Senior Software Engineer with experience in 
    API development, cloud infrastructure, and leading engineering teams.
    """

    result = generate_resume(sample_chunks, sample_jd)
    print(result)