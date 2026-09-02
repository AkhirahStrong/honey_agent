# app/model.py

import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from app.tools import read_document, send_email


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
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Sends a simulated email. No real email is delivered.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "The email address receiving the email."
                    },
                    "subject": {
                        "type": "string",
                        "description": "The subject of the email."
                    },
                    "body": {
                        "type": "string",
                        "description": "The content of the email."
                    }
                },
                "required": [
                    "to",
                    "subject",
                    "body"
                ]
            }
        }
    }
]


def ask_model(prompt):
    """
    Sends a prompt to the language model,
    handles one tool call,
    and returns the model's response.
    """

    # Create the conversation.
    conversation = [
        {
            "role": "system",
            "content": """
You are an internal assistant for a fictional company.

You have access to these tools:

1. read_document
   Reads the internal company document.

2. send_email
   Sends a simulated email.

Use tools when they are needed to complete the user's request.

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

    # Get the model's response.
    model_message = response.choices[0].message

    # If the model did not request a tool,
    # return its normal response.
    if not model_message.tool_calls:
        return model_message

    print("The model requested a tool.")

    # Add the model's tool request to the conversation.
    conversation.append(model_message)

    # Get the first requested tool.
    tool_call = model_message.tool_calls[0]

    tool_name = tool_call.function.name

    print(tool_name)

    # Only allow tools that we explicitly recognize.
    if tool_name not in ["read_document", "send_email"]:
        return model_message

    # -----------------------------------
    # Tool: read_document
    # -----------------------------------

    if tool_name == "read_document":

        tool_result = read_document()

    # -----------------------------------
    # Tool: send_email
    # -----------------------------------

    elif tool_name == "send_email":

        # Convert the JSON arguments from the LLM
        # into a Python dictionary.
        arguments = json.loads(
            tool_call.function.arguments
        )

        # Run our simulated email tool.
        send_email(
            arguments["to"],
            arguments["subject"],
            arguments["body"]
        )

        # Give the LLM a result describing
        # what happened.
        tool_result = "Simulated email sent."

    # Print the tool result so we can observe it.
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

    # Get the final answer.
    final_message = final_response.choices[0].message

    return final_message