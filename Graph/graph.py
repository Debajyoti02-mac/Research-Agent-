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
Builder = StateGraph(Self)

# Connection [create Node]
Builder = StateGraph(Self)

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