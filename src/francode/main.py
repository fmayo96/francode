from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = '''
    Sos un asistente que responde preguntas de manera eficiente y concisa. No das vueltas.
'''

messages = []

def add_system_message(messages,content):
    messages.append({
        "role": "system",
        "content": content
    })

def add_assistant_message(messages,content):
    messages.append(content)

def add_user_message(messages,content):
    messages.append({
        "role": "user",
        "content": content
    })

def chat():
    add_system_message(messages, SYSTEM_PROMPT)
    message = input("> ")
    add_user_message(messages, message)
    response = client.responses.create(
        model="gpt-4o",
        input=messages,
        tools=tools
    )    
    for item in response.output:
        if item.type != "function_call":
            print("Not a tool call")
            continue
        if item.name == "get_weather":
            print("Got here")
            args = json.loads(item.arguments)
            result = get_weather(**args)
            messages.append(
            {
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": result,
            }
        )
        print("after tool call")
        response = client.responses.create(
            model="gpt-4o",
            input=messages,
            tools=tools
    )
    print("after last message")
    messages.append(response.output)
    print(response.output_text)
    
def get_weather(city: str, unit: str | None = "celsius"):
    print("tool running")
    return f"El clima en {city} es una mierda"

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g. 'Paris'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["city", "unit"],
            "additionalProperties": False
        },
        "strict": True
    }
    
]

while True:
    chat()
