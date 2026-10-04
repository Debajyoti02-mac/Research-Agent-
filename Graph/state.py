from langgraph.graph import StateGraph , START , END 
from typing import TypedDict

class Self(TypedDict):
    query : str 
    context : list[str]
    grounded : bool 
    answer : str 
    needed_grounded : str 
    retry : int 