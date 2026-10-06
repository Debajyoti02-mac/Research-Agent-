# For abstract Node 
from research_agent.state import Self
from research_agent.llm import LLM
from research_agent.security import scrub_output

def abstract_node(state:Self):
    topic = state.get('topic',state.get('query',''))
    context = "\n".join(state.get("context", []))
    research_query = state.get('research_query')
    
    prompt = f"""
Write the abstract for a research paper on:

Research Topic:
{topic}

Research Direction:
{research_query}

Use only the provided research evidence:
{context}

Rules:
- Stay strictly focused on the research topic.
- Summarize the purpose, methodology, key findings, and significance.
- Do not introduce unrelated subjects.
- Do not invent facts or findings.
- Keep it concise and academic.
"""
    response = LLM.invoke(prompt)
    return {"abstract": scrub_output(response.content.strip())}
    