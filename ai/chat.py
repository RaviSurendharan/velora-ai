import openai

def process_message(message, conversation=None, client=None):
    system_prompt = "You are a seductive, flirty, and clever text assistant for an independent escort. " \
                    "Your job is to respond to potential clients via SMS. You should be playful and engaging, " \
                    "but also filter out time-wasters, vague inquiries, or explicit demands. Be human-like and " \
                    "match the client's chosen style (friendly, professional, flirty, or luxury). Keep boundaries. " \
                    "Your goal is to warm up the lead and pass it on to the escort only if they seem serious."

    if client:
        system_prompt += f"\nEscort Style: {client.get('style', 'friendly')}"
        system_prompt += f"\nDo Not Engage With: {', '.join(client.get('do_not_list', []))}"
        system_prompt += f"\nServices Offered: {', '.join(client.get('services', []))}"

    messages = [{"role": "system", "content": system_prompt}]

    if conversation:
        for msg in conversation[-5:]:  # last 5 messages
            messages.append({
                "role": "user" if msg["is_client"] else "assistant",
                "content": msg["content"]
            })

    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message["content"]

