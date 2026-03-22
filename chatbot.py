from groq import Groq

client = Groq(api_key="#give your api key")

def chatbot_response(message):

    if not message:
        return "Please enter a message."

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are a professional medical assistant.
- Reply in the same language as the user.
- Keep answers clear and short.
- If symptoms are given, suggest possible causes.
"""
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.5,
        )

        return completion.choices[0].message.content

    except Exception as e:
        print("GROQ ERROR:", e)
        return f"Groq Error: {str(e)}"
