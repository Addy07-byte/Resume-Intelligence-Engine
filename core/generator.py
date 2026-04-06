from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def build_prompt(retrieved_chunks: list[dict], job_description: str) -> str:
    """
    Builds the prompt for the LLM.
    Chunks are injected as grounded context — LLM is instructed
    to only use what's provided, never invent.
    """
    context = "\n\n".join(
        [f"- {chunk['text']}" for chunk in retrieved_chunks]
    )

    prompt = f"""
You are a professional resume writer. Your job is to write a tailored resume for the candidate below.

STRICT RULES:
- Only use the experience provided in the context below
- Do not invent, embellish, or add any skills or responsibilities not present in the context
- Every bullet point must be traceable to a provided chunk

JOB DESCRIPTION:
{job_description}

CANDIDATE EXPERIENCE (retrieved from their resume):
{context}

Write a tailored, professional resume in plain text. Include:
- A short professional summary (2-3 sentences)
- A work experience section with bullet points
- A skills section based only on what appears in the context
"""
    return prompt


def generate_resume(retrieved_chunks: list[dict], job_description: str) -> str:
    """
    Calls GPT-4o with the grounded prompt and returns the generated resume.
    """
    prompt = build_prompt(retrieved_chunks, job_description)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a professional resume writer. You only use provided context. You never hallucinate."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3  # low temperature = more consistent, less creative
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