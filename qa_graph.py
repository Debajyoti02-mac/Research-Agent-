from langgraph.graph import StateGraph , START , END
from Graph.state import Self
from retrival.retrival import Retrival_Fetch 
from LLM.llm_connection import LLM_connection 
from Grounded.grounded import Grounded , check_grounded
from Introduction.introduction import introduction_node 
from Abstract.abstract import abstract_node 
from Literature_review.literature_review import literature_review_node 
from Result.result import results_node 
from Methodology.methodology import methodology_node 
from Discusion.discussion import discussion_node

# --- Q&A Only Graph ---
qa_builder = StateGraph(Self)
qa_builder.add_node('retrival', Retrival_Fetch)
qa_builder.add_node('LLM', LLM_connection)
qa_builder.add_node('grounded', Grounded)

qa_builder.add_edge(START, 'retrival')
qa_builder.add_edge('retrival', 'LLM')
qa_builder.add_edge('LLM', 'grounded')
qa_builder.add_conditional_edges(
    'grounded', check_grounded,
    {'end': END, 'retry': 'retrival'}
)
qa_graph = qa_builder.compile()
