# chat/utils.py
import openai
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(prompt: str) -> str:
    completion = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.5,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )
    return completion.choices[0].message.content
