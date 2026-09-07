import streamlit as st

from workflow import run_research


st.set_page_config(
    page_title="Agentic Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; }
        .stTextArea textarea { border-radius: 0.5rem; }
        .stButton > button {
            border-radius: 0.5rem;
            font-weight: 600;
            padding: 0.5rem 2rem;
        }
        .research-plan-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-left: 4px solid #0ea5e9;
            border-radius: 0.5rem;
            padding: 1rem 1.25rem;
            margin-bottom: 0.75rem;
        }
        .research-plan-card .plan-num {
            color: #0ea5e9;
            font-weight: 700;
            margin-right: 0.5rem;
        }
        .research-plan-card .plan-text {
            color: #e2e8f0;
        }
        .answer-box {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border: 1px solid #334155;
            border-radius: 0.75rem;
            padding: 1.5rem;
            line-height: 1.7;
            color: #f1f5f9;
        }
        .source-chip {
            display: inline-block;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 0.5rem;
            padding: 0.35rem 0.75rem;
            margin: 0.2rem;
            font-size: 0.85rem;
            color: #94a3b8;
            text-decoration: none;
            transition: all 0.2s;
        }
        .source-chip:hover {
            border-color: #0ea5e9;
            color: #e2e8f0;
        }
        .stat-card {
            background: #1e293b;
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
            text-align: center;
            border: 1px solid #334155;
        }
        .stat-card .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0ea5e9;
        }
        .stat-card .stat-label {
            font-size: 0.8rem;
            color: #64748b;
            margin-top: 0.25rem;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🤖 Agentic Research Assistant")
    st.markdown("---")
    st.markdown("""
    An AI-powered multi-agent system that autonomously:
    - **Plans** research sub-tasks
    - **Searches** the web for evidence
    - **Critiques** quality of findings
    - **Synthesizes** a final answer
    """)
    st.markdown("---")
    st.markdown("**Powered by**")
    st.markdown("- Groq (LLM inference)")
    st.markdown("- SerpAPI (web search)")
    st.markdown("- Streamlit (UI)")
    st.markdown("---")
    st.caption("Built for fast, reliable research synthesis")

st.title("Agentic Research Assistant")
st.markdown("Ask a research question and let the multi-agent system plan, research, evaluate, and synthesize a comprehensive answer.")

st.markdown("")

question = st.text_area(
    "Research Question",
    placeholder="e.g. Should businesses adopt AI agents in 2026?",
    height=110,
    label_visibility="collapsed",
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_clicked = st.button("Start Research", use_container_width=True, type="primary")

if run_clicked:

    if not question.strip():
        st.warning("Please enter a research question.")

    else:
        with st.spinner("Planning research tasks..."):
            state = run_research(question)

        st.success("Research completed!")

        st.markdown("")

        plan = state["plan"]
        research_results = state["research_results"]
        final_answer = state["final_answer"]

        sources = []
        for result in research_results:
            for source in result["sources"]:
                sources.append(source)

        unique_sources = []
        seen_urls = set()
        for s in sources:
            if s["url"] not in seen_urls:
                unique_sources.append(s)
                seen_urls.add(s["url"])

        plan_col, stats_col = st.columns([2, 1])

        with stats_col:
            st.markdown("")
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{len(plan)}</div>
                    <div class="stat-label">Research Tasks</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{len(unique_sources)}</div>
                    <div class="stat-label">Sources Found</div>
                </div>
            """, unsafe_allow_html=True)

        with plan_col:
            with st.expander("Research Plan", expanded=True):
                for index, task in enumerate(plan, start=1):
                    st.markdown(f"""
                        <div class="research-plan-card">
                            <span class="plan-num">{index}.</span>
                            <span class="plan-text">{task}</span>
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("### Final Answer")
        st.markdown(f'<div class="answer-box">{final_answer}</div>', unsafe_allow_html=True)

        if unique_sources:
            st.markdown("")
            with st.expander(f"Sources ({len(unique_sources)})", expanded=False):
                for source in unique_sources:
                    st.markdown(
                        f'<div class="source-chip">'
                        f'<a href="{source["url"]}" target="_blank">{source["title"]}</a>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
