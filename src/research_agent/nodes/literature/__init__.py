from research_agent.state import Self
from research_agent.llm import LLM 


def literature_review_node(state: Self) -> dict:
    topic = state.get("query", "")
    intro = state.get("introduction", "")
    context = "\n".join(state.get("context", []))

    prompt = f"""You are an academic researcher drafting the Literature Review section.

RESEARCH TOPIC:
{topic}

INTRODUCTION & RESEARCH QUESTIONS:
{intro}

REFERENCE CONTEXT / INGESTED SOURCES:
{context}

STRICT TOPIC RULES:
- The RESEARCH TOPIC is fixed and must not be changed or broadened.
- Discuss only literature directly relevant to the research topic.
- Do not introduce unrelated subjects, technologies, datasets, or concepts.
- Use the provided sources as evidence.
- Do not invent studies, findings, benchmarks, or references.
- If the provided sources do not contain enough evidence for a claim, do not fabricate it.

Synthesize a structured Literature Review under these three subheadings:

1. Prior Work:
   Group existing methodologies and dominant frameworks thematically.

2. Discoveries & Benchmarks:
   Highlight established findings, core breakthroughs, and standard baselines
   relevant to the research topic.

3. Research Gap:
   Explicitly contrast existing works against unresolved challenges,
   operational bottlenecks, or missing methodologies that motivate this study.

Maintain an objective, analytical academic style.
Output only the section content with the subheadings above.
"""

    response = LLM.invoke(prompt)

    return {
        "literature_review": response.content.strip()
    }