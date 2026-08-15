from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.chroma_service import ChromaService
from services.gemini_service import GeminiService
from services.github import GitHubService

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_session_mock(responses: list):
    """
    Build a mock aiohttp.ClientSession whose .get() context manager yields
    responses from ``responses`` in sequence.  Each item in ``responses``
    is a dict with ``status`` and optional ``json`` / ``text`` keys.
    """
    call_count = 0

    class _ResponseCM:
        async def __aenter__(self):
            nonlocal call_count
            data = responses[min(call_count, len(responses) - 1)]
            call_count += 1
            resp = AsyncMock()
            resp.status = data["status"]
            resp.json = AsyncMock(return_value=data.get("json", {}))
            resp.text = AsyncMock(return_value=data.get("text", ""))
            resp.release = AsyncMock()
            return resp

        async def __aexit__(self, *args):
            pass

    class _SessionCM:
        async def __aenter__(self):
            session = MagicMock()
            session.get = MagicMock(return_value=_ResponseCM())
            return session

        async def __aexit__(self, *args):
            pass

    return _SessionCM()


# ---------------------------------------------------------------------------
# GitHub service tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_github_service_get_repo(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "fake_token")
    github_service = GitHubService()

    with patch(
        "aiohttp.ClientSession",
        return_value=_make_session_mock(
            [{"status": 200, "json": {"full_name": "test/repo"}}]
        ),
    ):
        repo = await github_service.get_repository("test", "repo")

    assert repo["full_name"] == "test/repo"


@pytest.mark.asyncio
async def test_github_service_retries_on_rate_limit(monkeypatch):
    """First request returns 429; second returns 200 — service should succeed."""
    monkeypatch.setenv("GITHUB_TOKEN", "fake_token")
    github_service = GitHubService()

    responses = [
        {"status": 429},
        {"status": 200, "json": {"full_name": "test/repo"}},
    ]

    with (
        patch(
            "aiohttp.ClientSession",
            return_value=_make_session_mock(responses),
        ),
        patch("asyncio.sleep", new_callable=AsyncMock),  # skip real sleep
    ):
        repo = await github_service.get_repository("test", "repo")

    assert repo["full_name"] == "test/repo"


# ---------------------------------------------------------------------------
# Gemini service tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_gemini_service_generate_response(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake_key")
    gemini_service = GeminiService()

    gemini_service.client = AsyncMock()

    mock_interaction = AsyncMock()
    mock_interaction.output_text = "Mocked AI response"
    gemini_service.client.aio.interactions.create.return_value = mock_interaction

    response = await gemini_service.generate_response("hello")
    assert response == "Mocked AI response"


@pytest.mark.asyncio
async def test_gemini_service_error_is_scrubbed(monkeypatch):
    """Errors returned to callers must not include raw exception repr."""
    monkeypatch.setenv("GEMINI_API_KEY", "fake_key")
    gemini_service = GeminiService()
    gemini_service.client = AsyncMock()
    gemini_service.client.aio.interactions.create.side_effect = RuntimeError(
        "secret_api_key_abc123"
    )

    response = await gemini_service.generate_response("hello")
    assert "secret_api_key_abc123" not in response
    assert "Gemini" in response


# ---------------------------------------------------------------------------
# ChromaDB service tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_chroma_service_search():
    with patch("chromadb.PersistentClient") as mock_client:
        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            "ids": [["doc1"]],
            "documents": [["Test document"]],
            "metadatas": [[{}]],
        }
        mock_client.return_value.get_or_create_collection.return_value = mock_collection

        chroma_service = ChromaService(persist_directory="./test_db")
        results = await chroma_service.search("test")

        assert len(results) == 1
        assert results[0]["id"] == "doc1"
        assert results[0]["document"] == "Test document"
