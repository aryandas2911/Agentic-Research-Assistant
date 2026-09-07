from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")


client = Groq(api_key=GROQ_API_KEY)


def generate_final_answer(question, research_results):

    prompt = f"""
You are an expert research report writer.

Original research question:
{question}

Research findings:
{research_results}

Using ONLY the information provided in the research findings,
write a clear and useful final research report answering the
original question.

Requirements:

1. Directly answer the original question.
2. Organize the answer using clear headings.
3. Combine information from different research tasks.
4. Do not invent facts.
5. Do not make claims that are unsupported by the research.
6. Mention important advantages, disadvantages, risks, or trade-offs
   when relevant.
7. Give a balanced conclusion.
8. Keep the writing concise but informative.

At the end, include a section called:

Sources

For each source, include its title and URL.

Return only the final research report.
"""

    response = client.chat.completions.create(
    model="qwen/qwen3.6-27b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    max_completion_tokens=800,
    reasoning_effort="none"
    )

    return response.choices[0].message.content