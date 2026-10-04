## Introduction Node
from research_agent.state import Self
from research_agent.llm import LLM 

def introduction_node(state:Self)->dict:
    topic = state.get('topic','')
    abstract = state.get('abstract','')
    context = "\n".join(state.get("context", [])) 
    prompt = f"""You are an academic researcher writing the Introduction section of a research paper.

Topic: {topic}
Abstract Summary: {abstract}
Reference Context:
{context}

Draft a comprehensive Introduction structured strictly under these four sub-headings:
1. Background: Establish the broader context, relevance, and foundational concepts.
2. Problem Statement: Identify the core failure mode, limitation, or unresolved challenge.
3. Significance: Explain the practical, technical, or theoretical impact of solving this problem.
4. Research Questions: Formulate 2-3 precise research questions (labeled RQ1, RQ2, RQ3).

Maintain a formal, objective academic tone. Output only the section content with the subheadings above.
"""

    response = LLM.invoke(prompt)
    return {"introduction": response.content.strip()}