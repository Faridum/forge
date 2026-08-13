import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt 
from call_functions import available_functions, call_function
import json

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("OPENROUTER_API_KEY not found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument(
    "user_prompt",
    type=str,
    help="User prompt"
)
parser.add_argument(
    "--verbose",
    action="store_true",
    help="Enable verbose output"
)

args = parser.parse_args()

messages = [
    {
        "role": "system",
        "content": system_prompt
    },

    {
        "role": "user",
        "content": args.user_prompt
    },
]

if args.verbose:
    print(f"User prompt: {args.user_prompt}")

for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    if response.usage is None:
        raise RuntimeError("RUNTIME ERROR")

    if args.verbose:
        print(f"Prompt tokens:  {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)

            if not result_message["content"]:
                raise RuntimeError("Fatal error: call_function returned empty content")

            if args.verbose:
                print(f"-> {result_message['content']}")

            messages.append(result_message)
    else:
        print(f"Response: \n{message.content}")
        break
else:
    print("Max iterations reached. The agent did not produce a final response.")
    sys.exit(1)