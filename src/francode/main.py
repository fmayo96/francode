from dotenv import load_dotenv
from openai import OpenAI
import json
import os

load_dotenv()

client = OpenAI()

MODEL = "gpt-5.6-luna"
INSTRUCTIONS = """
    Sos un asistente dentro de un harness para coding.
    Usa tools cuando sea apropiado.
    No inventes resultados de las tools.
"""


def get_weather(city: str):
    return {"city": city, "weather": f"El clima en {city} es una mierda"}


def list_files(path: str):
    return os.listdir(path)


def read_file(path: str):
    content = ""
    with open(path, "r") as f:
        for line in f:
            content += line + "\n"
    return content


def write_file(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)


TOOL_REGISTERY = {
    "get_weather": get_weather,
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
}

TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Obtiene el clima actual de una ciudad",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Ciudad de la que se quiere saber el clima",
                }
            },
            "required": ["city"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "list_files",
        "description": "Lists all the files and directories in the selected directory",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "path to the directory to be listed",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "read_file",
        "description": "reads the contents of a file given the filepath",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "path to the file to be read",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "write_file",
        "description": "writes some content provided as argument into a file with path provided also as an argument",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "path to the file to be written",
                },
                "content": {
                    "type": "string",
                    "description": "content to be written in the file",
                },
            },
            "required": ["path", "content"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def run_agent(input_items, max_steps: int = 10) -> str:

    for step in range(max_steps):
        response = client.responses.create(
            model=MODEL, instructions=INSTRUCTIONS, tools=TOOLS, input=input_items
        )
        input_items += response.output

        tool_calls = [item for item in response.output if item.type == "function_call"]

        if not tool_calls:
            return response.output_text

        for call in tool_calls:
            try:
                args = json.loads(call.arguments)

                if call.name not in TOOL_REGISTERY:
                    raise ValueError(f"Herramienta desconocida {call.name}")

                print(f"Ejecutando herramienta {call.name}")
                result = TOOL_REGISTERY[call.name](**args)

                tool_output = {"ok": True, "result": result}
                print(f"Herramienta ejecutada correctamente")
            except Exception as error:
                tool_output = {"ok": False, "error": str(error)}

            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(tool_output, ensure_ascii=False),
                }
            )
    raise RuntimeError(f"El agente superó el máximo de {max_steps} pasos")


input_items = []

while True:
    user_input = input("> ")
    if user_input in ["exit", "quit", "cerrar"]:
        exit()
    input_items.append({"role": "user", "content": user_input})
    answer = run_agent(input_items)
    print(answer)
