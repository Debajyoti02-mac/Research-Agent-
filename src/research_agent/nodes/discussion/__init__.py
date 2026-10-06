from research_agent.state import Self
from research_agent.llm import LLM


def discussion_node(state: Self) -> dict:
    topic = state.get("query", "")
    lit_review = state.get("literature_review", "")
    methodology = state.get("methodology", "")
    results = state.get("results", "")
    context_chunks = state.get("context", [])

    context = "\n".join(context_chunks)

    prompt = f"""
You are an academic researcher writing the Discussion section
of a research paper.

RESEARCH TOPIC:
{topic}

LITERATURE REVIEW:
{lit_review}

METHODOLOGY:
{methodology}

RESULTS:
{results}

REFERENCE CONTEXT:
{context}

STRICT TOPIC AND EVIDENCE RULES:

- The RESEARCH TOPIC is fixed and must not be changed or broadened.
- Every discussion point must directly relate to the research topic.
- Use only the provided literature, methodology, results,
  and reference context.
- Do not invent findings, causes, comparisons, statistics,
  benchmarks, or references.
- Do not present expected or proposed results as actual findings.
- If the RESULTS section contains no empirical findings,
  explicitly acknowledge that limitation.
- Do not claim that an experiment succeeded unless the results
  provide evidence of success.
- Do not introduce unrelated subjects, technologies, datasets,
  or concepts.
- Do not use outside knowledge to fill missing evidence.
- Do not mention that you are an AI.
- Do not ask for additional information.

Write the Discussion section under EXACTLY these four subheadings:

1. Interpretation of Results
Interpret the actual findings provided in the Results section.
If actual findings are unavailable, explain what can and cannot
be concluded from the available evidence.

2. Underlying Causes
Discuss mechanisms or possible explanations only when they are
supported by the provided evidence. Clearly distinguish evidence
from interpretation.

3. Literature Comparison
Compare the reported findings with prior literature or benchmarks
only when those comparisons are explicitly supported by the
provided literature review or reference context.

4. Limitations & Future Work
Identify limitations supported by the research materials.
Describe future research directions without presenting them
as completed work.

Maintain a critical, objective, academic tone.

Output ONLY the Discussion section with the four subheadings.
Do not generate a References section.
Do not add explanations or meta-information.
"""

    response = LLM.invoke(prompt)

    return {
        "discussion": response.content.strip()
    }