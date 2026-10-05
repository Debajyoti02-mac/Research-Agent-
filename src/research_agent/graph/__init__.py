from langgraph.graph import StateGraph , START , END 
from research_agent.state import Self
# An academic Abstract is a concise, 200–250 word self-contained summary of the entire paper. It must cover four core elements 


    


# Connection [create Node]
Builder = StateGraph(Self)

from research_agent.retrieval import Retrival_Fetch 
from research_agent.llm import LLM_connection 
from research_agent.grounded import Grounded , check_grounded
from research_agent.nodes.abstract import abstract_node
from research_agent.nodes.introduction import introduction_node 
from research_agent.nodes.literature import literature_review_node 
from research_agent.nodes.methodology import methodology_node 
from research_agent.nodes.result import results_node 
from research_agent.nodes.discussion import discussion_node
from research_agent.nodes.research import research_plan
# Connection [create Node]
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
Builder.add_node('research',research_plan)


# Create Edge 
Builder.add_edge(START,'retrival')
Builder.add_edge('retrival','LLM')
Builder.add_edge('LLM','grounded')
Builder.add_conditional_edges(
    'grounded',check_grounded,
    {
        'end':'research' , 
        'retry':'retrival'
    }
)
Builder.add_edge('research','abstract')
Builder.add_edge('abstract' , 'introduction')
Builder.add_edge('introduction','literature_review')
Builder.add_edge('literature_review','methodology')
Builder.add_edge('methodology','results')
Builder.add_edge('results','discussion')
Builder.add_edge('discussion', END)

graph = Builder.compile()
graph 