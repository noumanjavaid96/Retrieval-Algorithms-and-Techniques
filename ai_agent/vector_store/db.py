import chromadb
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, collection_name="documents"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def add_document(self, doc_id, text):
        embedding = self.model.encode(text)
        self.collection.add(
            embeddings=[embedding.tolist()],
            documents=[text],
            ids=[doc_id]
        )

    def search(self, query, n_results=5):
        query_embedding = self.model.encode(query)
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        return results
