from langgraph.graph import StateGraph , START , END 
from typing import TypedDict
# An academic Abstract is a concise, 200–250 word self-contained summary of the entire paper. It must cover four core elements 


class Self(TypedDict):
    query : str 
    context : list[str]
    grounded : bool 
    answer : str 
    needed_grounded : str 
    retry : int 
    topic: str
    raw_notes: str
    abstract: str
    introduction : str
    literature_review : str 
    methodology: str 
    results: str  
    discussion: str    
    references: str
    


# Connection [create Node]
Builder = StateGraph(Self)

from retrival import Retrival_Fetch 
from llm import LLM_connection 
from greounded import Grounded , check_grounded
from abstract import abstract_node
from introduction import introduction_node 
from literature import literature_review_node 
from methodology import methodology_node 
from result import results_node 
from Discussion import discussion_node
# Connection [create Node]
Builder.add_node('retrival',Retrival_Fetch)
Builder.add_node('LLM',LLM_connection)
Builder.add_node('grounded',Grounded)
Builder.add_node("abstract", abstract_node)
Builder.add_node("introduction", introduction_node)
Builder.add_node("literature_review", literature_review_node)
Builder.add_node("methodology", methodology_node)
Builder.add_node("results", results_node)
Builder.add_node("discussion", discussion_node)


# Create Edge 
Builder.add_edge(START,'retrival')
Builder.add_edge('retrival','LLM')
Builder.add_edge('LLM','grounded')
Builder.add_conditional_edges(
    'grounded',check_grounded,
    {
        'end':'abstract' , 
        'retry':'retrival'
    }
)
Builder.add_edge('abstract' , 'introduction')
Builder.add_edge('introduction','literature_review')
Builder.add_edge('literature_review','methodology')
Builder.add_edge('methodology','results')
Builder.add_edge('results','discussion')
Builder.add_edge('discussion', END)

graph = Builder.compile()
graph 