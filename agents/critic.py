from dotenv import load_dotenv
from groq import Groq
import os
import json


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=GROQ_API_KEY)


def critique(question, research_results):
    prompt = f"""
You are a research quality critic.

Original research question:
{question}

Research findings:
{research_results}

Evaluate whether the research is sufficient to answer the original
question.

Check:
1. Are the major aspects of the question covered?
2. Are there important missing areas?
3. Is the evidence reasonably strong?
4. Are the findings relevant to the question?

If the research is sufficient, return PASS.

If important information is missing, return NEEDS_RESEARCH and provide
specific additional research tasks.

Return only valid JSON using this format:

{{
    "status": "PASS",
    "additional_tasks": []
}}

OR:

{{
    "status": "NEEDS_RESEARCH",
    "additional_tasks": [
        "Additional research task 1",
        "Additional research task 2"
    ]
}}
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

    critic_text = response.choices[0].message.content

    result = json.loads(critic_text)

    if not isinstance(result, dict):
        raise ValueError("Critic did not return a JSON object.")

    if result.get("status") not in ["PASS", "NEEDS_RESEARCH"]:
        raise ValueError("Critic returned an invalid status.")

    if not isinstance(result.get("additional_tasks"), list):
        raise ValueError("Critic additional_tasks must be a list.")

    return result