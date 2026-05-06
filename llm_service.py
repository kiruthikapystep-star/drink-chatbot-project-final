from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_llm_response(user_message):

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return response.choices[0].message.content

    except Exception:
        return "Fallback response system active."
