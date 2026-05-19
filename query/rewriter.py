import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_client import client


def rewrite_query(query, msgs):
    """
    Rewrite user query for RAG pipeline for continue conversation
    """
    prompt = f"""
    You are a critical thinker. From the below content, tell me exactly what user wants to ask. Make sure you follow this pattern to draft the response:
        1. Do not add any prefix or suffix in response, for ex. Sure Here is the question OR any follow up question/message.
        2. I only want final question in one line.
        3. If the current question is perfectly drafted then you do not need to rephrase it.
        4. If the current question is out of the context (from previous conversation) then return me same question without rephrasing it.
    
    Here is the previous conversation and current question:
        Previous conversation: {msgs[-10:]}
        Current Question: {query}
    """
    response = client.models.generate_content(
        model = "gemini-3.1-flash-lite",
        contents = prompt
    )
    
    return response.text


# Usage
if __name__ == "__main__":
    query = "Why that month?"
    
    msgs = [
        {'role': 'user', 'content': 'What is this all about?'},
        {'role': 'assistant', 'content': 'This content describes a travel itinerary that includes visits to various attractions, such as Warner Bros. World, Aquaventure Waterpark, and Sheikh Zayed Grand Mosque, with details on timings, transportation, and activities.'},
        {'role': 'user', 'content': 'what is plan of Day 2?'},
        {'role': 'assistant', 'content': 'Day 2 includes a visit to Burj Khalifa, the Aquarium, KidZania, and the Fountain.'},
        {'role': 'user', 'content': 'When will be the trip?'},
        {'role': 'assistant', 'content': 'The trip includes several events on the following dates:\n\n*   **January 9 (Sat)** - Day 4: Rest Day\n*   **January 10 (Sun)** - Day 5: Evening Desert Safari\n*   **January 11 (Mon)** - Day 6: Ski Dubai + Penguin Encounter + Global Village\n*   **January 12 (Tue)** - Day 7: Aquaventure Waterpark + Marina Dhow Farewell Dinner\n*   **January 13 (Wed)** - Day 8: Abu Dhabi Day Trip (Mosque + Ferrari World + WB World)'},
        {'role': 'user', 'content': 'Who is the CM of India'},
        {'role': 'assistant', 'content': 'I am sorry, but the provided context does not contain the answer to your question about who the CM of India is.'},
        {'role': 'user', 'content': 'When is Dubai trip planned? Month only'},
        {'role': 'assistant', 'content': 'The Dubai trip is planned for January.'}
    ]
    
    response = rewrite_query(query, msgs)
    print(response)