from research_agent.retrieval import Retrival_Fetch 
from research_agent.llm import LLM_connection 
from research_agent.grounded import Grounded , check_grounded
from langgraph.graph import START , StateGraph , END 
from research_agent.state import Self

def after_llm(state: Self):
    return 'grounded' if state.get('relevant') else 'end'

qa_builder = StateGraph(Self)
qa_builder.add_node('retrival', Retrival_Fetch)
qa_builder.add_node('LLM', LLM_connection)
qa_builder.add_node('grounded', Grounded)

qa_builder.add_edge(START, 'retrival')
qa_builder.add_edge('retrival', 'LLM')
qa_builder.add_conditional_edges(
    'LLM', after_llm,
    {'grounded': 'grounded', 'end': END}
)
qa_graph = qa_builder.compile()

if __name__ == "__main__":
    print(f'the graph for question answering : {bool(qa_graph)}')
