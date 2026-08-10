import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt 

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("OPENROUTER_APT_KEY not found")

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

response = client.chat.completions.create(
    model= "openrouter/free",
    messages=messages,
    temperature=0,
)

if response.usage is None:
    raise RuntimeError("RUNTIME ERROR")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens:  {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")

print(f"Response: \n{response.choices[0].message.content}")