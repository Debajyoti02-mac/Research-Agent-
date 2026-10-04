from research_agent.state import Self
from research_agent.llm import LLM
 

def Grounded(state:Self):
    prompt = f"""
    Check whether the answer is supported by the provided context.

    Context:
    {state['context']}

    Question:
    {state['query']}

    Answer:
    {state['answer']}

    Return only:
    YES
    or
    NO
    """
    response = LLM.invoke(prompt).content
    result = response.strip().upper()
    
    return {
        "grounded": "YES" in result
    }

    
def check_grounded(state:Self):
    if state['grounded']:
        return 'end'
    elif state['retry']>=2:
        return 'end'
    else :
        return 'retry'
        