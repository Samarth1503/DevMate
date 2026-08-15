import logging

from google import genai

from core.config import settings
from services.llm_provider import LLMProvider

logger = logging.getLogger(__name__)


class GeminiService(LLMProvider):
    """LLM provider implementation backed by Google Gemini (Interactions API).

    Uses model ``gemini-3.6-flash`` via the ``aio.interactions.create``
    endpoint.  Exceptions are caught and returned as plain-text messages;
    error details are written to the logger without exposing the API key.
    """

    def __init__(self):
        if not settings.gemini_api_key:
            logger.warning("GEMINI_API_KEY is not set. Gemini integration will fail.")
            self.client = None
        else:
            self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = "gemini-3.6-flash"  # stable free-tier model

    async def analyze_error(self, error_message: str, stack_trace: str) -> str:
        """Analyse an error message and stack trace, returning an explanation."""
        if not self.client:
            return "Error: Gemini API key is not configured."

        prompt = f"""\
You are an expert developer assistant. Analyze the error and stack trace,
and explain what caused it and how to fix it.

Error Message:
{error_message}

Stack Trace:
{stack_trace}
"""
        try:
            interaction = await self.client.aio.interactions.create(
                model=self.model_name, input=prompt
            )
            return interaction.output_text
        except Exception as exc:
            # Log the type and a scrubbed message – never the raw exception
            # repr which could contain the API key in some SDK versions.
            logger.error(
                "Gemini API call failed in analyze_error (%s): %s",
                type(exc).__name__,
                str(exc).split("\n")[0],  # first line only, avoids verbose traces
            )
            return (
                "An error occurred while communicating with Gemini. "
                "Please check your GEMINI_API_KEY and try again."
            )

    async def generate_response(self, prompt: str) -> str:
        """Generate a free-form response for the given prompt."""
        if not self.client:
            return "Error: Gemini API key is not configured."

        try:
            interaction = await self.client.aio.interactions.create(
                model=self.model_name, input=prompt
            )
            return interaction.output_text
        except Exception as exc:
            logger.error(
                "Gemini API call failed in generate_response (%s): %s",
                type(exc).__name__,
                str(exc).split("\n")[0],
            )
            return (
                "An error occurred while communicating with Gemini. "
                "Please check your GEMINI_API_KEY and try again."
            )


llm_service = GeminiService()
