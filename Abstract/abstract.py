# For abstract Node 
from Graph.state import Self
from Security import scrub_output
from LLM.llm import LLM

def abstract_node(state:Self):
    topic = state.get('topic',state.get('query',''))
    context = "\n".join(state.get("context", []))
    raw_notes = state.get('raw_notes',"")
    
    prompt = f"""You are an academic researcher. Write a concise, formal academic abstract (200-250 words) based on the information below.

Topic: {topic}
Key Notes / Methodology / Results: {raw_notes}
Reference Context:
{context}

The abstract must include:
1. Context & Research Problem (1-2 sentences)
2. Proposed Methodology/Approach
3. Key Findings/Outcomes (include specific metrics if available)
4. Significance and Contribution

Output only the final abstract text without any meta-commentary or markdown headers.
"""
    response = LLM.invoke(prompt)
    return {"abstract": scrub_output(response.content.strip())}
    