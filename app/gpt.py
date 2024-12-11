import openai
import os

from icecream import ic

# Конфигурация библиотеки OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


def genarateResponse(text, prompt):
    return(openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f'{prompt}. At the end, always make text as less as you can, but informative',},
            {"role": "user", "content": f"{text}"}
        ]
    )["choices"][0]["message"]["content"]) 



