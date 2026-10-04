from research_agent.ingestion import chunks , collection
from research_agent.state import Self


from rank_bm25 import BM25Okapi 
tokens = [i.lower().split() for i in chunks]
token_corpus = BM25Okapi(tokens)

# RAG building 
def Retrival_Fetch(state:Self):
    query = state['query'] 
    
    result = collection.query(query_texts=[query],n_results=3)
    documents = result['documents'][0]
    distances = result['distances'][0]
    
    threshold = 1.0 
    
    dense_chunks = []
    for dist, doc in zip(distances, documents):
        if dist < threshold:
            dense_chunks.append(doc)
            
    scores = token_corpus.get_scores(query.lower().split())
    def get_index(score, k=10):
        indexed = list(enumerate(score))
        sorted_indices = sorted(indexed, key=lambda x: x[1], reverse=True)
        return [idx for idx, scr in sorted_indices[:k] if scr > 0]


    keyword_corpus= get_index(score=scores,k=10)
    chunks_corpus = [chunks[i] for i in keyword_corpus]
    
    rrf_tokens = {}
    for rank , doc in enumerate(dense_chunks):
        rrf_tokens[doc] = rrf_tokens.get(doc,0.0)+1.0/(rank+60)
    for rank , doc in enumerate(chunks_corpus):
        rrf_tokens[doc] = rrf_tokens.get(doc,0.0)+1.0/(rank+60) 
        
    marge = sorted(rrf_tokens.items(),key=lambda x:x[1],reverse=True)
    relevant = len(dense_chunks) > 0
    top_docs = [i for i , doc in marge[:3]] if relevant else []
    retry_time = state.get('retry',0)
    return {
        'context':top_docs ,
        'retry':retry_time+1 ,
        'relevant': relevant
    }