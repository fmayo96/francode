from .harness import Harness, Provider
from .providers.openai_provider import MODELS

harness = Harness(Provider.OPENAI)
harness.run()
