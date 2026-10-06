from research_agent.state import Self
from research_agent.llm import LLM


def results_node(state: Self) -> dict:
    topic = state.get("query", "")
    methodology = state.get("methodology", "")
    raw_notes = state.get("raw_notes", "")
    context = "\n".join(state.get("context", []))

    prompt = f"""You are an academic researcher writing the Results section
of a research paper.

RESEARCH TOPIC:
{topic}

METHODOLOGY & EXPERIMENTAL SETUP:
{methodology}

USER'S EXPERIMENTAL NOTES / METRICS / RAW FINDINGS:
{raw_notes}

RELEVANT CONTEXT:
{context}

STRICT RULES:
- The research topic is fixed. Do not change or broaden it.
- Report only findings directly related to the research topic.
- Use only quantitative values explicitly provided in the
  experimental notes, methodology, or relevant context.
- NEVER invent numbers, metrics, benchmark scores, datasets,
  experiments, or performance improvements.
- If quantitative results are not provided, do not create them.
- Clearly distinguish observed results from methodological details.
- Do not explain why the results occurred. Save interpretation
  and causal analysis for the Discussion section.
- Do not introduce unrelated subjects or findings.

Draft a formal, objective Results section structured strictly
under these two subheadings:

1. Empirical Findings:
   Present the available findings and observations systematically.

2. Performance Metrics & Comparative Outcomes:
   Present available quantitative measurements, comparison tables,
   benchmark results, runtime, accuracy, error rates, or ablation
   results ONLY when supported by the provided evidence.

If no quantitative results are available, explicitly state that
quantitative evaluation data were not provided rather than
fabricating values.

Maintain an unbiased, empirical academic tone.
Output only the section content with the subheadings above.
"""

    response = LLM.invoke(prompt)

    return {
        "results": response.content.strip()
    }