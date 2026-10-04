set -e
mkdir -p src/research_agent/nodes src/research_agent/state
touch src/research_agent/__init__.py src/research_agent/nodes/__init__.py
for n in abstract introduction literature methodology result; do
  git mv paper/$n src/research_agent/nodes/$n
done
git mv paper/discussion src/research_agent/nodes/discussion
git mv src/research_agent/nodes/discussion/__init_.py src/research_agent/nodes/discussion/__init__.py
rmdir paper 2>/dev/null || true

python3 - <<'PY'
import re
p = "src/research_agent/graph/__init__.py"
s = open(p).read()
m = re.search(r"class Self\(TypedDict\):.*?references: str\n", s, re.S)
open("src/research_agent/state/__init__.py", "w").write("from typing import TypedDict\n\n\n" + m.group(0))
s = s.replace(m.group(0), "")
s = s.replace("from typing import TypedDict\n", "from research_agent.state import Self\n", 1)
open(p, "w").write(s)
PY

FILES=$(find src tests -name "*.py")
perl -pi -e '
  s/^from graph import Self/from research_agent.state import Self/;
  s/^from graph import graph/from research_agent.graph import graph/;
  s/^from retrival import/from research_agent.retrieval import/;
  s/^from greounded import/from research_agent.grounded import/;
  s/^from qus_ans import/from research_agent.qa import/;
  s/^from (llm|ingestion|security|database|pdf_engine) import/from research_agent.$1 import/;
  s/^from (abstract|introduction|literature|methodology|result) import/from research_agent.nodes.$1 import/;
  s/^from Discussion import/from research_agent.nodes.discussion import/;
' $FILES

perl -pi -e 's/key_func=_rate_limit_exceeded_handler/key_func=get_remote_address/; s#/api/v1//ask#/api/v1/ask#' src/research_agent/main/__init__.py
perl -ni -e 'print unless /^LLM\.invoke\("hii\?"\)\.content/' src/research_agent/llm/__init__.py
perl -pi -e "s#PyPDFLoader\('economics_research_reference.pdf'\)#PyPDFLoader(str(Path(__file__).resolve().parents[1] / 'economics_research_reference.pdf'))#; s#^import warnings#from pathlib import Path\nimport warnings#" src/research_agent/ingestion/__init__.py
