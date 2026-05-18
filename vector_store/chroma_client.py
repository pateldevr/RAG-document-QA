import chromadb
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def initialize(collection_name):
    """
    Initiate the chroma db in local storage
    """
    
    client = chromadb.PersistentClient() # pass “path” as params if you want to store chromadb at different place. for ex. (path="path-of-folder")
    
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=None
    )
    
    return collection

def store(collection, chunks, vectors):
    """
    Store chunks and vectors into collection
    """
    
    collection.upsert(
        ids=[f"chunk_{i}" for i in range(1, len(chunks) + 1)],
        documents=chunks, # chunks array received from chunker file 
        embeddings=vectors, # vectors array received from embedder file
    )

def retrieve(collection, query_vector, no_of_result):
    """
    Fetch query related vectors from collection
    """
    
    result = collection.query(
        # query_texts=["what is correct recipient name?"], # we can pass "query_embeddings" as well along with text if we have embeddings.
        query_embeddings = query_vector,
        n_results=no_of_result
    )
    
    return result


# Usage
if __name__ == "__main__":
    from indexing.pdf_extractor import extract_text
    from indexing.chunker import chunking
    from indexing import embedder as em

    # Extract Text from PDF
    text = extract_text("notice.pdf")
    
    # Spliting text into chunks
    chunks = chunking(text)
    
    # Converting chunks into vectors
    vectors = em.embedding(chunks)
    
    #initialize the chroma db
    collection = initialize("my_collection")
    
    # store data in collection
    store(collection, chunks, vectors)
    
    print(f"Total documents: {collection.count()}")
