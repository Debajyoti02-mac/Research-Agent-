from Graph.graph import graph
from pdf_engine import generate_paper_pdf

initial_state = {
    "query": "Impact of Free Capital Flows and the Policy Trilemma on Emerging Markets",
    "raw_notes": "Analyzed FX volatility across 14 emerging economies. Found a 24% reduction in monetary autonomy when capital accounts were liberalized.",
    "retry": 0
}

result = graph.invoke(initial_state)

# Debug prints to see why sections are blank
print("Available keys in result:", list(result.keys()))
print("Abstract text:", repr(result.get("abstract")))
print("Introduction text:", repr(result.get("introduction")))

pdf_stream = generate_paper_pdf(result)

output_path = "Generated_Research_Paper.pdf"
with open(output_path, "wb") as f:
    f.write(pdf_stream.getbuffer())

print(f"Paper generated successfully: {output_path}")
