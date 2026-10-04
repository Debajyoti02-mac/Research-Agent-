from research_agent.state import Self
from research_agent.llm import LLM 

def methodology_node(state: Self) -> dict:
    topic = state.get("query", "")
    intro = state.get("introduction", "")
    lit_review = state.get("literature_review", "")
    context = "\n".join(state.get("context", []))

    prompt = f"""You are an academic researcher drafting the Methodology section of a research paper.

Topic: {topic}
Research Questions & Scope (from Introduction):
{intro}

Baseline Literature & Technical Context:
{lit_review}
{context}

Draft a comprehensive, reproducible Methodology section structured strictly under these five subheadings:
1. Research Design: System architecture, pipeline stages, and overall framework.
2. Dataset / Data Collection: Data characteristics, acquisition, preprocessing, and splits.
3. Tools and Technologies: Programming languages, frameworks, libraries, and hardware infrastructure.
4. Algorithms and Models: Mathematical formulation, architectural components, or algorithmic procedures.
5. Experimental Setup: Evaluation metrics, baseline configurations, hyperparameters, and validation protocols.

Maintain a precise, academic, and reproducible writing style. Output only the section content with the subheadings above.
"""
    response = LLM.invoke(prompt)
    return {"methodology": response.content.strip()}
