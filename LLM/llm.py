# LLM connection 
import os 
from langchain_groq import ChatGroq 
from dotenv import load_dotenv 
load_dotenv()
os.getenv('GROQ_API_KEY')
LLM = ChatGroq(model='openai/gpt-oss-120b')
LLM.invoke("hii?").content