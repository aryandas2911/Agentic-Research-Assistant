# Agentic Research Assistant

A multi-agent AI system that autonomously plans, researches, critiques, and synthesizes comprehensive answers to research questions. Built with Groq, SerpAPI, and Streamlit.

## Architecture

```
User Question
     │
     ▼
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Planner  │────▶│Researcher│────▶│  Critic  │────▶│  Final   │
│          │     │          │     │          │     │  Answer  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
     │                 │                 │
     │                 │          (if needs more)
     │                 └─────────────────┘
     ▼
  Research Plan ──▶ Web Search ──▶ Quality Check ──▶ Report
```

### Agents

| Agent | Role |
|-------|------|
| **Planner** | Breaks a research question into 3-5 specific, independently researchable sub-tasks |
| **Researcher** | Searches the web for each task via SerpAPI, then summarizes findings using Groq LLM |
| **Critic** | Evaluates research quality; requests additional tasks if coverage is insufficient |
| **Final Answer** | Synthesizes all findings into a structured, cited research report |

## Features

- Multi-agent pipeline with automatic quality critique
- Iterative research — critic can request follow-up rounds (up to 2 iterations)
- Web search powered by SerpAPI (Google results)
- Fast LLM inference via Groq (`qwen/qwen3.6-27b`)
- Streamlit web UI with sidebar info, research plan cards, stats, and source chips

## Prerequisites

- Python 3.10+
- [Groq API key](https://console.groq.com/)
- [SerpAPI key](https://serpapi.com/)

## Setup

```bash
# Clone the repository
git clone <repo-url>
cd "Agentic Research Assistant"

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_groq_api_key > .env
echo SERPAPI_API_KEY=your_serpapi_api_key >> .env
```

## Usage

```bash
streamlit run app.py
```

Open the browser at `http://localhost:8501`, type a research question, and click **Start Research**.

### Example Questions

- "Should businesses adopt AI agents in 2026?"
- "What are the ethical implications of autonomous AI systems?"
- "Compare retrieval-augmented generation vs. fine-tuning for enterprise LLMs"

## Project Structure

```
Agentic Research Assistant/
├── app.py                 # Streamlit UI
├── workflow.py            # Research pipeline orchestrator
├── agents/
│   ├── planner.py         # Task decomposition agent
│   ├── researcher.py      # Web search + summarization agent
│   ├── critic.py          # Quality evaluation agent
│   └── final_answer.py    # Report synthesis agent
├── tools/
│   └── search.py          # SerpAPI web search wrapper
├── prompts/               # Prompt templates
├── requirements.txt       # Python dependencies
└── .env                   # API keys (not committed)
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | API key for Groq LLM inference |
| `SERPAPI_API_KEY` | API key for SerpAPI web search |

## Tech Stack

- **LLM**: Groq — `qwen/qwen3.6-27b`
- **Search**: SerpAPI — Google organic results
- **UI**: Streamlit
- **Orchestration**: Custom multi-agent pipeline with critic-driven iteration
