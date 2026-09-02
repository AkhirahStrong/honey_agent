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


# Tools the LLM is allowed to request.
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
    Sends a prompt to the language model,
    handles a read_document tool call,
    and returns the final model response.
    """

    # Create the conversation.
    conversation = [
        {
            "role": "system",
            "content": """
You are an internal assistant for a fictional company.

You have access to a tool named read_document.

When a user asks about company policies, employee rules,
or internal company information, use the read_document tool
before answering.

After a tool result is provided, use that result to answer
the user's original question.

Do not guess company information.
"""
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    # First call to the LLM.
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=conversation,
        tools=TOOLS
    )

    # Get the model's first response.
    model_message = response.choices[0].message

    # If the model did not request a tool,
    # return its normal text response.
    if not model_message.tool_calls:
        return model_message

    print("The model requested a tool.")

    # Add the model's tool request to the conversation.
    conversation.append(model_message)

    # Get the first requested tool.
    tool_call = model_message.tool_calls[0]

    print(tool_call.function.name)

    # Only allow our known safe tool.
    if tool_call.function.name != "read_document":
        return model_message

    # Run the tool.
    tool_result = read_document()

    print(tool_result)

    # Add the tool result to the conversation.
    conversation.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_result
        }
    )

    # Send the updated conversation back to the LLM.
    final_response = client.chat.completions.create(
        model="openrouter/free",
        messages=conversation
    )

    # Return the final answer.
    final_message = final_response.choices[0].message

    return final_message