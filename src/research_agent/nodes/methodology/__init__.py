from research_agent.state import Self
from research_agent.llm import LLM 


def methodology_node(state: Self) -> dict:
    topic = state.get("query", "")
    intro = state.get("introduction", "")
    lit_review = state.get("literature_review", "")
    context = "\n".join(state.get("context", []))

    prompt = f"""You are an academic researcher drafting the Methodology section
of a research paper.

RESEARCH TOPIC:
{topic}

RESEARCH QUESTIONS & SCOPE:
{intro}

LITERATURE REVIEW:
{lit_review}

REFERENCE CONTEXT:
{context}

STRICT TOPIC AND EVIDENCE RULES:
- The RESEARCH TOPIC is fixed and must not be changed or broadened.
- Every methodological detail must directly relate to the research topic.
- Use only information supported by the provided context and previous sections.
- Do not invent datasets, hardware, hyperparameters, algorithms,
  experimental results, or validation procedures.
- If a methodological detail is not provided, state that it is
  not specified rather than fabricating it.
- Do not introduce unrelated technologies, datasets, or methods.

Draft a comprehensive, reproducible Methodology section structured strictly
under these five subheadings:

1. Research Design:
   System architecture, pipeline stages, and overall framework.

2. Dataset / Data Collection:
   Data characteristics, acquisition, preprocessing, and splits.

3. Tools and Technologies:
   Programming languages, frameworks, libraries, and hardware infrastructure
   only when supported by the provided evidence.

4. Algorithms and Models:
   Mathematical formulation, architectural components, or algorithmic
   procedures supported by the provided evidence.

5. Experimental Setup:
   Evaluation metrics, baseline configurations, hyperparameters,
   and validation protocols only when explicitly supported.

Maintain a precise, academic, and reproducible writing style.
Output only the section content with the subheadings above.
"""

    response = LLM.invoke(prompt)

    return {
        "methodology": response.content.strip()
    }