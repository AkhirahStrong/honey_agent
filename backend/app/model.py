# app/model.py

import os

from dotenv import load_dotenv
from openai import OpenAI
from app.tools import read_document

# Load variables stored in our .env file.
load_dotenv()


# Get the OpenRouter API key from the environment.
api_key = os.getenv("OPENROUTER_API_KEY")


# Create our connection to OpenRouter.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_document",
            "description": "Reads the internal company document.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

def ask_model(prompt):
    """
    Sends a prompt to the language model
    and returns the model's response.
    """

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
           {
                "role": "system",
                "content": """
You are an internal assistant for a fictional company.

You have access to a tool named read_document.

When a user asks about company policies, employee rules,
or internal company information, use the read_document tool
before answering.

Do not guess company information.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        tools=TOOLS
    )

    # return response.choices[0].message.content
    message =response.choices[0].message
    # return response
    
    # 3. Check if the LLM requested a tool
    if message.tool_calls:
        print("The model requested a tool.")

        tool_call = message.tool_calls[0]

        print(tool_call.function.name)
        
        if tool_call.function.name == "read_document":
         tool_result = read_document()

        print(tool_result)


    # 4. Return the message
    return message