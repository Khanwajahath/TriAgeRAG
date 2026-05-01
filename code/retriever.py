import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path='./chroma_db')  # ← fixed
collection = client.get_collection('support_corpus')

def retrieve(query: str, company: str = None, top_k: int = 5) -> list:
    embedding = model.encode(query).tolist()
    where = {'company': company} if company and company != 'None' else None
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        where=where
    )
    return results['documents'][0]