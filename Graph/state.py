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