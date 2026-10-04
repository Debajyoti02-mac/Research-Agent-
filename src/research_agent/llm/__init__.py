# LLM connection 
from graph import Self

import os 
from langchain_groq import ChatGroq 
from dotenv import load_dotenv 
load_dotenv()
os.getenv('GROQ_API_KEY')
LLM = ChatGroq(model='openai/gpt-oss-120b')
LLM.invoke("hii?").content

def LLM_connection(state:Self):
    prompt = f""" 
    context : {state['context']}
    question : {state['query']}
    """
    response = LLM.invoke(prompt)
    return {
        'answer':response
    }