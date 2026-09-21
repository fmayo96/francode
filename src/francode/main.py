from .harness import Harness, Provider

harness = Harness(Provider.OPENAI)
harness.run()
