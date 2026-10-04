from graph import Self
from llm import LLM 


def literature_review_node(state: Self) -> dict:
    topic = state.get("query", "")
    intro = state.get("introduction", "")
    context = "\n".join(state.get("context", []))

    prompt = f"""You are an academic researcher drafting the Literature Review section of a research paper.

Topic: {topic}
Introduction & Research Questions:
{intro}

Reference Context / Ingested Sources:
{context}

Synthesize a structured Literature Review under these three subheadings:
1. Prior Work: Group existing methodologies and dominant frameworks thematically.
2. Discoveries & Benchmarks: Highlight established findings, core breakthroughs, and standard baselines.
3. Research Gap: Explicitly contrast existing works against unresolved challenges, operational bottlenecks, or missing methodologies that motivate this study.

Maintain an objective, analytical academic style. Output only the section content with the subheadings above.
"""
    response = LLM.invoke(prompt)
    return {"literature_review": response.content.strip()}