from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

def embedding(chunks):
    """
    Convert text into vectors
    """
    embeddings = model.encode(chunks, batch_size=16)
    return embeddings


# Usage
if __name__ == "__main__":
    from pdf_extractor import extract_text
    from chunker import chunking

    # Extract Text from PDF
    text = extract_text("notice.pdf")
    
    # Spliting text into chunks
    chunks = chunking(text)
    
    # Converting chunks into vectors
    vectors = embedding(chunks)
    
    print(vectors.shape)
    
