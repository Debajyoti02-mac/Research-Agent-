from Graph.state import Self

from LLM.llm import LLM
 
def LLM_connection(state:Self):
    prompt = f""" 
    context : {state['context']}
    question : {state['query']}
    """
    response = LLM.invoke(prompt)
    return {
        'answer':response
    }