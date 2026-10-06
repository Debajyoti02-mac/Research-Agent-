## Introduction Node
from research_agent.state import Self
from research_agent.llm import LLM 

def introduction_node(state: Self) -> dict:
    topic = state.get("query", "")
    abstract = state.get("abstract", "")
    context = "\n".join(state.get("context", []))

    prompt = f"""You are an academic researcher writing the Introduction section.

RESEARCH TOPIC:
{topic}

ABSTRACT:
{abstract}

REFERENCE CONTEXT:
{context}

STRICT TOPIC RULES:
- The RESEARCH TOPIC is the fixed subject of this paper.
- Write ONLY about this topic.
- Do not change, broaden, or replace the research topic.
- Every paragraph must directly contribute to understanding this topic.
- Use the context only as supporting evidence.
- Do not introduce unrelated subjects, examples, technologies, datasets,
  or concepts unless they are directly relevant to the research topic.
- Do not invent facts or claims.

Draft a comprehensive Introduction structured strictly under these four
sub-headings:

1. Background: Establish the broader context, relevance, and foundational concepts.
2. Problem Statement: Identify the core failure mode, limitation, or unresolved challenge.
3. Significance: Explain the practical, technical, or theoretical impact of solving this problem.
4. Research Questions: Formulate 2-3 precise research questions (labeled RQ1, RQ2, RQ3).

Maintain a formal, objective academic tone.
Output only the section content with the subheadings above.
"""

    response = LLM.invoke(prompt)

    return {
        "introduction": response.content.strip()
    }