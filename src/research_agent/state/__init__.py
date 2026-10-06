from typing import TypedDict


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
    relevant : bool
    research_query : str 
