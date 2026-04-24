from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()




def process_job_description(raw_jd: str) -> str:
    """
    Takes a raw job description and uses an LLM to strip boilerplate.
    Returns only the skills, responsibilities, and requirements.
    This clean output is used as the query for ChromaDB retrieval.

    """
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a job description parser. "
                    "Your job is to extract only the required skills, "
                    "responsibilities, and experience from a job description. "
                    "Remove all boilerplate: benefits, salary, EEO statements, "
                    "company culture, and perks. "
                    "Return a clean, concise summary in plain text only."
                )
            },
            {
                "role": "user",
                "content": f"Extract the requirements and responsibilities from this job description:\n\n{raw_jd}"
            }
        ],
        temperature=0.0  # zero creativity — this is extraction, not generation
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    sample_jd = """
    About Us:
    We are a fast-growing fintech startup with a ping pong table and free snacks.
    We offer competitive salary, health benefits, and flexible work from home policy.
    We are an equal opportunity employer.

    Role: Senior Software Engineer
    
    Responsibilities:
    - Design and build scalable REST APIs
    - Lead a team of 3-5 engineers
    - Optimize database queries for performance
    - Deploy and monitor services on AWS

    Requirements:
    - 5+ years of software engineering experience
    - Strong proficiency in Python
    - Experience with AWS and cloud infrastructure
    - Familiarity with machine learning pipelines

    Compensation:
    - $150,000 - $180,000 base salary
    - equity package
    - 401k matching
    """

    cleaned = process_job_description(sample_jd)
    print("Cleaned JD:")
    print(cleaned)