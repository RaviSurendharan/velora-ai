import openai
import os

# Get API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

def process_message(message, conversation_history=None, client_profile=None):
    """Process incoming message with AI"""
    if conversation_history is None:
        conversation_history = []
    
    if client_profile is None:
        client_profile = {"name": "Escort", "style": "friendly"}
    
    # Prepare the system message with personality style
    system_message = f"You are an AI assistant for {client_profile['name']}. "
    system_message += f"Use a {client_profile['style']} communication style. "
    system_message += "You are responding to potential clients. Be conversational and natural."
    
    # Format conversation history for the API
    messages = [{"role": "system", "content": system_message}]
    
    # Add conversation history (limited to last 5 messages to save tokens)
    for msg in conversation_history[-5:]:
        role = "user" if msg.get("is_client", False) else "assistant"
        messages.append({"role": role, "content": msg.get("content", "")})
    
    # Add the current message
    messages.append({"role": "user", "content": message})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "I'm sorry, I'm having trouble processing your request right now. Please try again later."
