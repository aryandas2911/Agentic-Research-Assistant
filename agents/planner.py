from dotenv import load_dotenv
from groq import Groq
import json
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=GROQ_API_KEY)

def create_plan(question):
    prompt = f"""
You are a research planning assistant.

Your job is to break a broad research question into 3 to 5
specific research tasks.

Original research question:
{question}

Create research tasks that together provide enough information
to answer the original question.

Each task should:
- Be specific
- Be independently researchable
- Be directly relevant to the original question
- Focus on a different important aspect of the problem

Return the result as a JSON array of strings.

Example:
[
    "Research task 1",
    "Research task 2",
    "Research task 3"
]

Return only valid JSON.
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

    plan_text = response.choices[0].message.content

    plan = json.loads(plan_text)

    if not isinstance(plan, list):
        raise ValueError("Planner did not return a list.")

    if not 3 <= len(plan) <= 5:
        raise ValueError("Planner must return between 3 and 5 tasks.")

    return plan

if __name__ == "__main__":
    question = "Should businesses adopt AI agents?"

    plan = create_plan(question)

    print("RESEARCH PLAN:")

    for index, task in enumerate(plan, start=1):
        print(f"{index}. {task}")