from research_agent.state import Self
from research_agent.llm import LLM


def literature_review_node(state: Self) -> dict:
    topic = state.get("query", "")
    intro = state.get("introduction", "")
    context = "\n".join(state.get("context", []))

    prompt = f"""
You are an academic researcher drafting the Literature Review section
of a research paper.

RESEARCH TOPIC:
{topic}

INTRODUCTION / RESEARCH QUESTIONS:
{intro}

REFERENCE CONTEXT / INGESTED SOURCES:
{context}

STRICT TOPIC AND EVIDENCE RULES:

- The RESEARCH TOPIC is fixed and must not be changed or broadened.
- Discuss only literature directly relevant to the research topic.
- Use only the provided sources as evidence.
- Do not invent authors, studies, findings, benchmarks, statistics,
  citations, or references.
- Do not use general knowledge to fill missing evidence.
- If the provided sources do not contain enough evidence for a claim,
  do not make that claim.
- Do not introduce unrelated subjects, technologies, datasets,
  methodologies, or concepts.
- Preserve the terminology and research framing used by the provided sources.
- Clearly distinguish established findings from proposed ideas.
- Do not claim that a research finding exists unless it is supported
  by the provided sources.
- Do not write the research paper or methodology.
- Do not mention that you are an AI.
- Do not ask for additional information.

Write a structured and evidence-grounded Literature Review.

Structure it EXACTLY under these three subheadings:

1. Prior Work
Group the existing research and methodologies into relevant
themes directly supported by the provided sources.

2. Discoveries & Benchmarks
Summarize established findings, reported relationships,
benchmarks, and important results only when explicitly supported
by the provided sources.

3. Research Gap
Identify limitations, unresolved problems, methodological gaps,
or missing evidence that are explicitly supported by the provided
sources.

If the sources do not provide enough information for a subsection,
state that the available evidence is insufficient rather than
fabricating content.

Maintain an objective, analytical, academic writing style.

Output ONLY the Literature Review section with the three subheadings.
Do not add explanations, comments, or meta-information.
"""

    response = LLM.invoke(prompt)

    return {
        "literature_review": response.content.strip()
    }