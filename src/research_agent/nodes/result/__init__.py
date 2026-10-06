from research_agent.state import Self
from research_agent.llm import LLM


def results_node(state: Self) -> dict:
    topic = state.get("query", "")
    methodology = state.get("methodology", "")
    raw_notes = state.get("raw_notes", "")
    context = "\n".join(state.get("context", []))

    prompt = f"""
You are an academic researcher writing the Results section
of a research paper.

RESEARCH TOPIC:
{topic}

METHODOLOGY & EXPERIMENTAL SETUP:
{methodology}

USER'S EXPERIMENTAL NOTES / METRICS / RAW FINDINGS:
{raw_notes}

RELEVANT RESEARCH CONTEXT:
{context}

STRICT TOPIC AND EVIDENCE RULES:

- The RESEARCH TOPIC is fixed and must not be changed or broadened.
- Report only findings directly related to the research topic.
- Use only evidence explicitly provided in the experimental notes,
  methodology, or relevant research context.
- NEVER invent numbers, metrics, datasets, experiments, observations,
  benchmark scores, performance improvements, or statistical results.
- Do not convert literature benchmarks into results produced by this study.
- Do not convert evaluation targets into achieved results.
- Do not treat proposed experiments as completed experiments.
- Clearly distinguish actual observations from methodological descriptions.
- Do not explain why a result occurred. Save interpretation,
  causes, and implications for the Discussion section.
- Do not introduce unrelated findings, technologies, datasets, or concepts.
- Do not mention that you are an AI.
- Do not ask for additional information.

IMPORTANT:
If actual experimental findings are unavailable, explicitly state that
the supplied material does not contain empirical results.

If only some results are available:
- Report only those results.
- Do not fill the missing values.
- Clearly identify which evaluation information is unavailable.

Write the Results section under EXACTLY these two subheadings:

1. Empirical Findings
Present the available experimental observations and findings
in a clear and systematic manner.

2. Performance Metrics & Comparative Outcomes
Present quantitative measurements, benchmark comparisons,
runtime, accuracy, error rates, ablation results, or other
evaluation metrics ONLY when explicitly supported by the evidence.

Do not interpret the results.
Do not explain causes.
Do not claim success or improvement unless explicitly demonstrated
by the provided experimental evidence.

Maintain an objective, empirical academic writing style.

Output ONLY the Results section with the two subheadings.
Do not add explanations, comments, or meta-information.
"""

    response = LLM.invoke(prompt)

    return {
        "results": response.content.strip()
    }