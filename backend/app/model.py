# app/model.py

import os

from dotenv import load_dotenv
from openai import OpenAI


# Load variables stored in our .env file.
load_dotenv()


# Get the OpenRouter API key from the environment.
api_key = os.getenv("OPENROUTER_API_KEY")


# Create our connection to OpenRouter.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def ask_model(prompt):
    """
    Sends a prompt to the language model
    and returns the model's response.
    """

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content