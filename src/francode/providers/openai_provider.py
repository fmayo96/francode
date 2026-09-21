from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import FunctionToolParam
from typing import Iterable
from enum import StrEnum
from francode.tools import TOOL_REGISTERY, TOOLS_OPENAI
from francode.tools import *
import json

load_dotenv()


class ReasoningEffort(StrEnum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    XHIGH = "xhigh"
    MAX = "max"


INSTRUCTIONS = """
    Sos un asistente dentro de un harness para coding.
    Usa tools cuando sea apropiado.
    No inventes resultados de las tools.
    """

OPENAI_MODELS = [model.id for model in OpenAI().models.list()]


class OpenAIProvider:
    def __init__(
        self,
        model: str = "gpt-5.6-luna",
        effort: ReasoningEffort = ReasoningEffort.MEDIUM,
        instructions: str = INSTRUCTIONS,
        tools: Iterable[FunctionToolParam] = TOOLS_OPENAI,
        tools_registry: dict = TOOL_REGISTERY,
    ):
        self.client = OpenAI()
        print(model)

        if model not in OPENAI_MODELS:
            raise ValueError("Model name does not match available models")

        self.model = model
        self.effort = effort
        self.instructions = instructions
        self.tools = tools
        self.tools_registry = tools_registry

    def get_response(self, input_items: str):
        response = self.client.responses.create(
                model=self.model,
                instructions=self.instructions,
                tools=self.tools,
                input=input_items,
            )
        return response
    
    def run_agent(self, input_items, max_steps: int = 500):
        for _ in range(max_steps):
            response = self.get_response(input_items)
            input_items += response.output

            tool_calls = [
                item for item in response.output if item.type == "function_call"
            ]

            if not tool_calls:
                return response

            for call in tool_calls:
                try:
                    args = json.loads(call.arguments)

                    if call.name not in self.tools_registry:
                        raise ValueError(f"Herramienta desconocida {call.name}")

                    print(f"Ejecutando herramienta {call.name}")
                    result = self.tools_registry[call.name](**args)

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
