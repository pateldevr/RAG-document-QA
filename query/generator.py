import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_client import client

def response_drafting(question, chunks):
    """
    Draft response for user based on the question and chunks
    """
    
    context = "\n\n".join(chunks)
    prompt = f"""
    You are a helpful assistant. Help me answer the question below from the content provided.

    Few points to note for answering the question:
        1. Make sure you answer the question from the context only.
        2. If you do not find any context which answer the question then reply with courtesy that context does not include the answer you are looking for.
        3. Do not try to look for the answer on internet.
        4. If you find the answer then properly format it and make sure it concise and accurate.
        
    Here is the question and context:
    """
    
    response = client.models.generate_content(
        model = "gemini-3.1-flash-lite",
        contents = prompt + f"Question: {question} \n Context: {context}"
    )
    
    return response.text


# Usage
if __name__ == "__main__":
    from retriever import retrieving
    query = "What is the recipient name?"
    
    chunks = retrieving(query, "my_collection")
    response = response_drafting(query, chunks)

    print(response)