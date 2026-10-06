from typing import TypedDict


class Self(TypedDict, total=False):
    query: str
    research_query: str
    context: list[str]
    sources: list[dict]
    grounded: bool
    relevant: bool
    needed_grounded: str
    retry: int
    raw_notes: str

    abstract: str
    introduction: str
    literature_review: str
    methodology: str
    results: str
    discussion: str
    references: str
    answer: str
