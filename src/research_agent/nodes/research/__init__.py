from research_agent.state import Self
from research_agent.llm import LLM


def research_plan(state: Self):

    topic = state.get("query", "").strip()

    prompt = f"""
You are a research planning agent.

Original Research Topic:
{topic}

Your task is to convert the original topic into a concise,
focused research direction for downstream research.

Rules:
- The original research topic is fixed.
- Do not change, broaden, or replace the topic.
- Keep the research direction directly related to the topic.
- Identify the main scope, focus, and research angle.
- Do not write the paper.
- Do not invent facts, sources, findings, or statistics.

Return ONLY the concise research direction.
"""

    result = LLM.invoke(prompt)

    return {
        "research_query": result.content.strip()
    }