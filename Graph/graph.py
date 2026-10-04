from langgraph.graph import StateGraph , START , END
from Graph.state import Self
from retrival.retrival import Retrival_Fetch 
from LLM.llm_connection import LLM_connection 
from Grounded.grounded import Grounded , check_grounded
Builder = StateGraph(Self)

# Connection [create Node]
Builder.add_node('retrival',Retrival_Fetch)
Builder.add_node('LLM',LLM_connection)
Builder.add_node('grounded',Grounded)

# Create Edge 
Builder.add_edge(START,'retrival')
Builder.add_edge('retrival','LLM')
Builder.add_edge('LLM','grounded')
Builder.add_conditional_edges(
    'grounded',check_grounded,
    {
        'end':END , 
        'retry':'retrival'
    }
)
graph = Builder.compile()
graph 

if __name__ == "__main__":
    print(f'the graph is ready : {bool(graph)}')