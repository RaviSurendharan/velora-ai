import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_message(message, conversation=[], client=None, escort=None):
    style = escort.get("style", "friendly") if escort else "friendly"
    bio = escort.get("bio", "") if escort else ""
    services = escort.get("services", []) if escort else []
    do_not_list = escort.get("do_not_list", []) if escort else []

    context = (
        f"You are a virtual assistant replying as an escort.\n"
        f"Her personality style is: {style}.\n"
        f"Her bio: {bio}\n"
        f"Her services offered: {', '.join(services)}\n"
        f"Topics to avoid: {', '.join(do_not_list)}\n"
        "Keep responses flirty but professional if style allows. Keep it under 3 sentences.\n\n"
    )

    history = "\n".join([
        f"Client: {msg['text']}" if msg["is_client"] else f"Escort: {msg['text']}"
        for msg in conversation[-5:]
    ])

    prompt = context + history + f"\nClient: {message}\nEscort:"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error: {e}")
        return "Sorry, something went wrong. 💔"

