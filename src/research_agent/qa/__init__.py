from retrival import Retrival_Fetch 
from llm import LLM_connection 
from greounded import Grounded , check_grounded
from langgraph.graph import START , StateGraph , END 
from graph import Self
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

if __name__ == "__main__":
    print(f'the graph for question answering : {bool(qa_graph)}')
