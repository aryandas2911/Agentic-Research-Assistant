import streamlit as st

from workflow import run_research


st.set_page_config(
    page_title="Agentic Research Assistant",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 Agentic Research Assistant")

st.write(
    "Ask a research question and let the agent plan, "
    "research, evaluate, and synthesize the answer."
)


question = st.text_area(
    "Research Question",
    placeholder="Example: Should businesses adopt AI agents in 2026?",
    height=120
)


if st.button("🔍 Start Research"):

    if not question.strip():

        st.warning("Please enter a research question.")

    else:

        with st.spinner("Researching..."):

            state = run_research(question)

        st.success("Research completed!")

        st.header("Research Plan")

        for index, task in enumerate(state["plan"], start=1):

            st.write(f"**{index}.** {task}")

        st.header("Final Answer")

        st.write(state["final_answer"])

        st.header("Sources")

        sources = []

        for result in state["research_results"]:

            for source in result["sources"]:

                sources.append(source)


        for source in sources:

            st.markdown(
                f"- [{source['title']}]({source['url']})"
            )