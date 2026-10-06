from research_agent.state import Self
from research_agent.llm import LLM


def methodology_node(state: Self) -> dict:
    topic = state.get("query", "")
    intro = state.get("introduction", "")
    lit_review = state.get("literature_review", "")
    context = "\n".join(state.get("context", []))

    prompt = f"""
You are an academic researcher drafting the Methodology section
of a research paper.

RESEARCH TOPIC:
{topic}

INTRODUCTION / RESEARCH SCOPE:
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
- If a methodological detail is not provided, explicitly state that
  it is not specified rather than fabricating it.
- Do not introduce unrelated technologies, datasets, or methods.
- Do not convert proposed methods into claims that they were actually executed.
- Clearly distinguish between completed procedures and proposed procedures.
- Do not invent research findings.

Write a detailed but evidence-grounded Methodology section.

Structure it EXACTLY under these five subheadings:

1. Research Design
Describe the system architecture, research pipeline, stages,
and overall framework supported by the evidence.

2. Dataset / Data Collection
Describe the available data characteristics, acquisition,
preprocessing, and data splits only when supported by the evidence.

3. Tools and Technologies
Describe programming languages, frameworks, libraries,
and hardware only when explicitly supported by the evidence.

4. Algorithms and Models
Describe mathematical formulations, model architecture,
algorithms, and procedures only when supported by the evidence.

5. Experimental Setup
Describe evaluation metrics, baseline configurations,
hyperparameters, and validation protocols only when explicitly supported.

If information is missing, clearly state that it is not specified.
Do not add information simply to make the methodology appear complete.

Maintain a precise, academic, and reproducible writing style.

Output ONLY the Methodology section.
Do not add explanations, comments, or meta-information.
"""

    response = LLM.invoke(prompt)

    return {
        "methodology": response.content.strip()
    }