def chunking(text, chunk_size=500, chunk_overlap=100):
    """
    Splits a string into fixed-size chunks with a specified overlap.
    """
    chunks = []
    
    step = chunk_size - chunk_overlap
    
    for i in range(0, len(text), step):
        chunk = text[i : i + chunk_size]
        chunks.append(chunk)
        
        # Stop if we've reached the end of the string
        if i + chunk_size >= len(text):
            break

    return chunks

# Usage
if __name__ == "__main__":
    from pdf_extractor import extract_text

    text = extract_text("notice.pdf")
    result = chunking(text)

    print(f"Total chunks created: {len(result)}")
    print(f"First 2 chunks: {result[0:2]}")