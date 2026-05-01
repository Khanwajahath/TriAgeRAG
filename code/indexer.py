import os, glob
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path='./chroma_db')  # ← fixed
collection = client.get_or_create_collection('support_corpus')

def chunk_text(text, size=500, overlap=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        chunks.append(' '.join(words[i:i+size]))
    return chunks

for company in ['hackerrank', 'claude', 'visa']:
    for filepath in glob.glob(f'data/{company}/**/*', recursive=True):
        if not os.path.isfile(filepath): continue
        text = open(filepath).read()
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            doc_id = f'{company}_{filepath}_{i}'
            embedding = model.encode(chunk).tolist()
            collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{'company': company, 'source': filepath}]
            )
            print(f'Indexed {filepath}')
print('Indexing complete!')