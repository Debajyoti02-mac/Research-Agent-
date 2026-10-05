from research_agent.state import Self 
from research_agent.llm import LLM

def research_plan(state: Self):
    prompt = f"""
You are a research planning agent.

Take the user's research topic and turn it into a clear,
focused research direction for the research agent.

Do not write the paper.
Do not invent facts or sources.

Return only a concise research direction.

User topic:
{state['query']}
"""

    result = LLM.invoke(prompt)

    return {
        "research_query": result.content
    }