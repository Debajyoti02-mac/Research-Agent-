from research_agent.state import Self
from research_agent.llm import LLM 

def discussion_node(state: Self) -> dict:
    topic = state.get("query", "")
    lit_review = state.get("literature_review", "")[:1200]
    methodology = state.get("methodology", "")[:1500]
    results = state.get("results", "")[:1200]
    context_chunks = state.get("context", [])[:2]
    context = "\n".join(context_chunks)

    prompt = f"""You are an academic researcher writing the Discussion and Reference section of a research paper.

RESEARCH TOPIC:
{topic}

IMPORTANT TOPIC RULES:
- Stay strictly focused on the research topic above.
- Every discussion point must directly relate to this topic.
- Do not introduce unrelated subjects, examples, technologies, datasets, or concepts.
- Use the methodology, results, and literature only to discuss this specific topic.
- Do not allow information from the context to change or broaden the research topic.
- Do not invent findings, causes, comparisons, or references.

Methodology:
{methodology}

Results:
{results}

Prior Literature Context:
{lit_review}
{context}

Draft a comprehensive Discussion section structured strictly under these four subheadings:
1. Interpretation of Results: Analyze the practical and mechanistic implications of the findings.
2. Underlying Causes: Detail why the method succeeded or where performance trade-offs emerged.
3. Literature Comparison: Contrast findings directly against prior benchmarks and baselines mentioned in the literature review.
4. Limitations & Future Work: Detail specific constraints (e.g., compute, dataset boundaries) and future research avenues.

Finally, compile a list of cited academic references (formal APA or IEEE style) derived from the reference context under the subheading:
5. References

Maintain an analytical, critical academic tone. Output only the section content with the subheadings above.
"""
    response = LLM.invoke(prompt)
    output = response.content.strip()

    # Split discussion and references if formatted separately, or store unified
    return {
        "discussion": output,
        "references": output.split("5. References")[-1].strip() if "5. References" in output else ""
    }
