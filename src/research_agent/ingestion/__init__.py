## Import warnings 
import warnings 
warnings.filterwarnings('ignore')

# PDF loader 
from langchain_community.document_loaders import PyPDFLoader 
loader = PyPDFLoader('economics_research_reference.pdf')
pages = loader.load()

# Split data 
from langchain_text_splitters import RecursiveCharacterTextSplitter
spliter = RecursiveCharacterTextSplitter(chunk_size=1200,chunk_overlap=150)
text_split = spliter.split_documents(pages)
# chunks 
chunks = [i.page_content for i in text_split]
metadata = [i.metadata for i in text_split]

# Create unique ids 
import hashlib 
ids =[hashlib.md5(chunk.encode('utf-8')).hexdigest() for chunk in chunks]

# CromaDB create 
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

embedding_fun = DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path="./Vector_DataBase")

collection = client.get_or_create_collection(
    name="Research_agent",
    embedding_function=embedding_fun
)
if collection.count()!= len(chunks):
    collection.add(
    documents=chunks,
    ids=ids
    )

    
if __name__ == "__main__":
    print(f"Total items in DB: {collection.count()}")