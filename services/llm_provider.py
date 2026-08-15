from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def analyze_error(self, error_message: str, stack_trace: str) -> str:
        """Analyze an error message and stack trace to provide debugging help."""
        pass

    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        """Generate a general response from a prompt."""
        pass
