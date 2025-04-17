# models/llm_wrapper.py
from openai import OpenAI

client = OpenAI()


def ask_llm(prompt: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are a finance assistant that classifies spending."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content
