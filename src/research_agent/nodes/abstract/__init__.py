from research_agent.state import Self
from research_agent.llm import LLM
from research_agent.security import scrub_output


def abstract_node(state: Self):

    topic = state.get("query", "").strip()
    research_query = state.get("research_query", "").strip()

    context = "\n".join(
        state.get("context", [])
    )

    prompt = f"""
Write a concise academic abstract for a research paper.

Research Topic:
{topic}

Research Direction:
{research_query}

Research Evidence:
{context}

Rules:
- Stay strictly focused on the research topic.
- Use only the provided research evidence.
- Summarize the research purpose.
- Summarize the methodology.
- Summarize findings only if actual findings are present in the evidence.
- If actual findings are unavailable, do not invent them.
- Mention the limitation briefly if necessary.
- Explain the significance of the research.
- Do not write instructions.
- Do not talk about being an AI.
- Do not ask the user for additional information.
- Do not say "I’m happy to help".
- Return ONLY the abstract.
"""

    response = LLM.invoke(prompt)

    return {
        "abstract": scrub_output(response.content.strip())
    }