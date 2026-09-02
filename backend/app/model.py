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
    allows multiple tool calls,
    and returns the final model response.
    """

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

Use tools when needed to complete the user's request.

If a task requires multiple tools, use them in sequence.

After receiving a tool result, continue working until the
user's request is complete.

Do not guess company information.
"""
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    # Prevent the agent from looping forever.
    max_tool_steps = 5

    for step in range(max_tool_steps):

        # Ask the model what to do next.
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=conversation,
            tools=TOOLS
        )

        model_message = response.choices[0].message

        # If the model does not request a tool,
        # the task is complete.
        if not model_message.tool_calls:
            return model_message

        print("The model requested a tool.")

        # Save the model's tool request.
        conversation.append(model_message)

        # A model can request more than one tool.
        for tool_call in model_message.tool_calls:

            tool_name = tool_call.function.name

            print(tool_name)

            # -----------------------------
            # Tool: read_document
            # -----------------------------
            if tool_name == "read_document":

                tool_result = read_document()

            # -----------------------------
            # Tool: send_email
            # -----------------------------
            elif tool_name == "send_email":

                arguments = json.loads(
                    tool_call.function.arguments
                )

                send_email(
                    arguments["to"],
                    arguments["subject"],
                    arguments["body"]
                )

                tool_result = "Simulated email sent."

            # -----------------------------
            # Unknown tool
            # -----------------------------
            else:

                tool_result = (
                    f"Tool '{tool_name}' is not allowed."
                )

            print(tool_result)

            # Give the tool result back to the model.
            conversation.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                }
            )

    # If we reach this point, the model used
    # too many tool steps.
    return model_message