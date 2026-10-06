from research_agent.state import Self
from research_agent.llm import LLM


def introduction_node(state: Self) -> dict:
    topic = state.get("query", "")
    abstract = state.get("abstract", "")
    context = "\n".join(state.get("context", []))

    prompt = f"""
You are an academic researcher writing the Introduction section
of a research paper.

RESEARCH TOPIC:
{topic}

ABSTRACT:
{abstract}

REFERENCE CONTEXT:
{context}

STRICT TOPIC AND EVIDENCE RULES:

- The RESEARCH TOPIC is the fixed subject of this paper.
- Write only about this research topic.
- Do not change, broaden, replace, or reinterpret the research topic.
- Every paragraph must directly contribute to understanding the topic.
- Use the provided context as the primary evidence.
- Do not introduce unrelated subjects, technologies, datasets,
  methods, examples, or concepts.
- Do not invent facts, statistics, findings, citations, or claims.
- Do not treat proposed research as completed research.
- If the provided evidence is insufficient to support a claim,
  do not fabricate information.
- Do not mention that you are an AI.
- Do not ask for additional information.

Write a clear, evidence-grounded Introduction.

Structure it EXACTLY under these four subheadings:

1. Background
Establish the context, relevance, and foundational concepts
directly supported by the research topic and provided evidence.

2. Problem Statement
Identify the central problem, limitation, or unresolved challenge
supported by the provided evidence.

3. Significance
Explain the practical, technical, or theoretical importance
of addressing the identified problem. Do not invent unsupported
benefits or impacts.

4. Research Questions
Formulate 2-3 precise research questions based strictly on
the research topic, problem statement, and available evidence.

Label the questions exactly as:
RQ1:
RQ2:
RQ3:

Maintain a formal, objective, academic writing style.

Output ONLY the Introduction section with the four subheadings.
Do not add explanations, comments, or meta-information.
"""

    response = LLM.invoke(prompt)

    return {
        "introduction": response.content.strip()
    }