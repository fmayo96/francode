from enum import StrEnum
from .providers import OpenAIProvider


class Provider(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class Harness:
    def __init__(self, provider: Provider):
        if provider == Provider.OPENAI:
            self.provider = OpenAIProvider()

    def run(self):
        input_items = []
        while True:
            user_input = input("> ")
            if user_input in ["exit", "quit", "cerrar"]:
                exit()
            input_items.append({"role": "user", "content": user_input})
            answer = self.provider.run_agent(input_items)
            input_items.append(answer)
            print(answer.output_text)
