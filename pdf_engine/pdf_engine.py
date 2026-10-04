import io
import re
import markdown
import weasyprint

def clean_math_and_markdown(text: str) -> str:
    """Cleans LaTeX artifacts into clean readable math blocks and converts MD to HTML."""
    if not text:
        return ""

    # 1. Clean common LaTeX equation markers to human-readable math blocks
    # Converts: D_{it} &= \pi_{0} + \pi_{1} G^{c}_{t} + ...
    cleaned = text.replace("&=", "=").replace(r"\times", "×")
    cleaned = re.sub(r"\\(?:pi|alpha|beta|gamma|theta)", lambda m: {
        r"\pi": "π", r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\theta": "θ"
    }.get(m.group(0), m.group(0)), cleaned)
    
    # Format inline subscripts/superscripts if simply written
    cleaned = re.sub(r"([A-Za-z])_\{([^}]+)\}", r"\1<sub>\2</sub>", cleaned)
    cleaned = re.sub(r"([A-Za-z])\^\{([^}]+)\}", r"\1<sup>\2</sup>", cleaned)

    # 2. Convert standard markdown (bold, headers, lists, tables) into HTML
    html = markdown.markdown(
        cleaned,
        extensions=["extra", "tables", "sane_lists"]
    )
    return html

def generate_paper_pdf(data: dict) -> io.BytesIO:
    title = data.get("query", data.get("topic", "Academic Research Paper"))
    abstract = clean_math_and_markdown(data.get("abstract", ""))
    intro = clean_math_and_markdown(data.get("introduction", ""))
    lit_review = clean_math_and_markdown(data.get("literature_review", ""))
    methodology = clean_math_and_markdown(data.get("methodology", ""))
    results = clean_math_and_markdown(data.get("results", ""))
    discussion = clean_math_and_markdown(data.get("discussion", ""))
    references = clean_math_and_markdown(data.get("references", ""))

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: A4;
    margin: 20mm 18mm 22mm 18mm;
    @top-right {{
      content: "Research Agent Preprint";
      font-size: 8pt;
      color: #666;
      font-family: 'Times New Roman', Times, serif;
    }}
    @bottom-center {{
      content: counter(page);
      font-size: 9pt;
      font-family: 'Times New Roman', Times, serif;
    }}
  }}

  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 10pt;
    line-height: 1.35;
    color: #1a1a1a;
    text-align: justify;
  }}

  /* Title & Author Block */
  .title-block {{
    text-align: center;
    margin-bottom: 18px;
    padding-bottom: 10px;
    border-bottom: 0.5pt solid #ccc;
  }}
  h1.paper-title {{
    font-size: 17pt;
    font-weight: bold;
    line-height: 1.25;
    margin: 0 0 10px 0;
    text-transform: capitalize;
  }}
  .meta-author {{
    font-size: 9pt;
    color: #444;
    margin-bottom: 4px;
  }}

  /* Abstract & Keywords (Single Column Span) */
  .abstract-container {{
    margin: 0 25px 18px 25px;
    padding: 10px 14px;
    background: #fbfbfb;
    border-left: 2.5pt solid #2c3e50;
    font-size: 9pt;
    line-height: 1.35;
  }}
  .abstract-heading {{
    font-weight: bold;
    text-transform: uppercase;
    font-size: 8.5pt;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
    color: #2c3e50;
  }}

  /* Two Column Academic Layout */
  .columns {{
    column-count: 2;
    column-gap: 16pt;
    column-rule: 0.2pt solid #e0e0e0;
  }}

  /* Academic Headings */
  h2 {{
    font-size: 10.5pt;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    font-weight: bold;
    margin-top: 14pt;
    margin-bottom: 5pt;
    border-bottom: 0.4pt solid #333;
    padding-bottom: 1pt;
    break-after: avoid;
  }}
  h3 {{
    font-size: 9.5pt;
    font-weight: bold;
    margin-top: 8pt;
    margin-bottom: 3pt;
    break-after: avoid;
  }}

  p {{
    margin: 0 0 6pt 0;
    text-indent: 10pt;
  }}
  p:first-of-type {{
    text-indent: 0;
  }}

  /* Tables & Lists */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8pt 0;
    font-size: 8pt;
    break-inside: avoid;
  }}
  th, td {{
    border: 0.5pt solid #bbb;
    padding: 4pt 5pt;
    text-align: left;
  }}
  th {{
    background-color: #f2f2f2;
    font-weight: bold;
  }}
  ul, ol {{
    margin: 3pt 0 6pt 16pt;
    padding: 0;
  }}
  li {{
    margin-bottom: 2pt;
  }}

  /* Math Equations Display */
  code, pre {{
    font-family: 'Courier New', monospace;
    background: #f7f7f7;
    font-size: 8.5pt;
  }}
  pre {{
    padding: 6pt;
    border-radius: 2pt;
    white-space: pre-wrap;
    border: 0.5pt solid #ddd;
    margin: 6pt 0;
    break-inside: avoid;
  }}

  .references-block {{
    font-size: 8pt;
    line-height: 1.25;
  }}
</style>
</head>
<body>

  <div class="title-block">
    <h1 class="paper-title">{title}</h1>
    <div class="meta-author">Autonomous Research Agent Framework</div>
    <div class="meta-author">Department of Computer Science & Quantitative Economics</div>
  </div>

  <div class="abstract-container">
    <div class="abstract-heading">Abstract</div>
    <div>{abstract}</div>
  </div>

  <div class="columns">
    <h2>1. Introduction</h2>
    {intro}

    <h2>2. Literature Review</h2>
    {lit_review}

    <h2>3. Methodology</h2>
    {methodology}

    <h2>4. Results</h2>
    {results}

    <h2>5. Discussion</h2>
    {discussion}

    <h2>References</h2>
    <div class="references-block">
      {references if references else "<p>See text for cited references.</p>"}
    </div>
  </div>

</body>
</html>"""

    buffer = io.BytesIO()
    weasyprint.HTML(string=html_content).write_pdf(buffer)
    buffer.seek(0)
    return buffer
