from agents.planner import create_plan
from agents.researcher import research

def run_research(question):
    plan = create_plan(question)

    research_results = []

    for index, task in enumerate(plan, start=1):
        print(f"\nResearching task {index}/{len(plan)}:")
        print(task)

        result = research(task)

        research_results.append(result)

    return {
        "plan": plan,
        "research_results": research_results
    }

if __name__ == "__main__":
    question = "Should businesses adopt AI agents in 2026?"

    state = run_research(question)

    print("\nRESEARCH PLAN:\n")

    for index, task in enumerate(state["plan"], start=1):
        print(f"{index}. {task}")

    print("\n\nRESEARCH RESULTS:\n")

    for result in state["research_results"]:
        print("=" * 60)

        print("TASK:")
        print(result["task"])

        print("\nFINDINGS:")
        print(result["findings"])

        print("\nSOURCES:")

        for source in result["sources"]:
            print(f"- {source['title']}")
            print(f"  {source['url']}")

        print()