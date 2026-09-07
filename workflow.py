from agents.planner import create_plan
from agents.researcher import research
from agents.critic import critique

MAX_ITERATIONS = 2


def run_research(question):

    plan = create_plan(question)

    research_results = []

    for iteration in range(MAX_ITERATIONS):

        print(f"\n{'=' * 60}")
        print(f"RESEARCH ROUND {iteration + 1}")
        print(f"{'=' * 60}")

        for index, task in enumerate(plan, start=1):

            print(f"\nResearching task {index}/{len(plan)}:")
            print(task)

            result = research(task)

            research_results.append(result)

        print("\nEvaluating research...")

        critic_result = critique(
            question,
            research_results
        )

        print("\nCRITIC RESULT:")
        print(critic_result)

        if critic_result["status"] == "PASS":

            print("\nResearch is sufficient.")

            break

        if critic_result["status"] == "NEEDS_RESEARCH":

            additional_tasks = critic_result["additional_tasks"]

            if not additional_tasks:

                print("\nCritic requested more research but provided no tasks.")

                break

            print("\nAdditional research required:")

            for task in additional_tasks:
                print(f"- {task}")

            plan = additional_tasks

    return {
        "question": question,
        "plan": plan,
        "research_results": research_results
    }


if __name__ == "__main__":

    question = "Should businesses adopt AI agents in 2026?"

    state = run_research(question)

    print("\n\n")
    print("=" * 60)
    print("FINAL RESEARCH STATE")
    print("=" * 60)

    print("\nQUESTION:")
    print(state["question"])

    print("\nTOTAL RESEARCH RESULTS:")

    for result in state["research_results"]:

        print("\n" + "-" * 60)

        print("TASK:")
        print(result["task"])

        print("\nFINDINGS:")
        print(result["findings"])

        print("\nSOURCES:")

        for source in result["sources"]:

            print(f"- {source['title']}")
            print(f"  {source['url']}")