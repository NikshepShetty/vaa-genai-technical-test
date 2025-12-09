def generate_prompt(user_query: str) -> str:
    # TODO: Update this function for RAG implementation
    # - Add retrieved_context parameter
    # - Include context in the prompt
    # - Handle cases where no relevant context is found
    return f"""
You are a travel assistant.

A user has asked: "{user_query}"

Respond with:
- A recommended destination
- A reason for the recommendation
- A rough budget category
- 3 tips or suggestions
"""

def generate_rag_prompt(user_query: str, retrieved_context: str) -> str:
    """
    TODO: Implement RAG-enhanced prompt generation
    
    This function should:
    1. Take the user query and retrieved context
    2. Create a prompt that instructs the AI to answer based on the context
    3. Handle cases where context is insufficient
    4. Ensure responses are grounded in the provided information
    
    Args:
        user_query: The user's question
        retrieved_context: Relevant context from vector store
        
    Returns:
        Formatted prompt for OpenAI API
    """
    pass
