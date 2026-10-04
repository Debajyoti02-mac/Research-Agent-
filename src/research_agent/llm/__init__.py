# LLM connection 
from research_agent.state import Self

import os 
from langchain_groq import ChatGroq 
from dotenv import load_dotenv 
load_dotenv()
os.getenv('GROQ_API_KEY')
LLM = ChatGroq(model='openai/gpt-oss-120b')

def LLM_connection(state:Self):
    prompt = f"""
    Reply with ONE short line, maximum 15 words: the answer, then the key figure.
    Example: Russia, roughly 17.1 million km²
    No explanation, no markdown, no notes, no follow-up.
    Use the context if it is relevant; otherwise answer from general knowledge.

    context : {state['context']}
    question : {state['query']}
    """
    response = LLM.invoke(prompt)
    return {'answer': response.content.strip()}
    