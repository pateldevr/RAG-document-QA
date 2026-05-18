import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from indexing import embedder as em
from vector_store import chroma_client as cc

def retrieving(query, collection_name):
    """
    Convert query into vectors and find matching vectors from collection
    """
    
    # Covert query into vectors
    query_embeddings = em.embedding([query])
    
    # find the matching record
    collection = cc.initialize(collection_name)
    result = cc.retrieve(collection, query_embeddings,3)
    
    return result['documents'][0]


# Usage
if __name__ == "__main__":
    query = "What is the recipient name?"
    
    ans = retrieving(query, "my_collection")
    
    print(ans)