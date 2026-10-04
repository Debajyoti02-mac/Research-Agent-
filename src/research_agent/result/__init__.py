from graph import Self
from llm import LLM 

def results_node(state: Self) -> dict:
    topic = state.get("query", "")
    methodology = state.get("methodology", "")
    raw_notes = state.get("raw_notes", "")
    context = "\n".join(state.get("context", []))

    prompt = f"""You are an academic researcher writing the Results section of a research paper.

Topic: {topic}

Methodology & Experimental Setup:
{methodology}

User's Experimental Notes / Metrics / Raw Findings:
{raw_notes}

Relevant Context:
{context}

Draft a formal, objective Results section structured strictly under these two subheadings:
1. Empirical Findings: Present data and factual performance systematically without subjective speculation.
2. Performance Metrics & Comparative Outcomes: Include structured markdown comparison tables, quantitative measurements (accuracy, runtime, error rates, benchmark scores), or ablation outcomes based on the provided notes and setup.

Maintain an unbiased, empirical tone. Output only the section content with the subheadings above.
"""
    response = LLM.invoke(prompt)
    return {"results": response.content.strip()}
