from dotenv import load_dotenv
from groq import Groq
import os

from tools.search import search_web

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=GROQ_API_KEY)


def research(task):
    search_results = search_web(task)

    if not search_results:
        return {
            "task": task,
            "findings": "No search results were found.",
            "sources": []
        }

    prompt =  f"""
You are a research assistant.

Research task:
{task}

Search results:
{search_results}

Analyze the search results and identify the most useful information
for answering the research task.

Summarize the important findings accurately in 4-6 concise bullet points.
Do not invent information.
Only use information supported by the search results.
Do not include unnecessary explanations.
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

    summary = response.choices[0].message.content

    sources = []

    for result in search_results:
        sources.append({
            "title": result["title"],
            "url": result["url"]
        })

    return {
        "task": task,
        "findings": summary,
        "sources": sources
    }