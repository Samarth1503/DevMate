import asyncio
import logging

import aiohttp

from core.config import settings

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3
_RATE_LIMIT_STATUSES = {403, 429}


class GitHubService:
    """Client for the GitHub REST API with automatic retry on rate-limit responses.

    Retries up to ``_MAX_RETRIES`` times with an exponential back-off sleep
    (2 s, 4 s, 8 s) on HTTP 403 / 429 responses.  The ``Authorization``
    header is set from ``GITHUB_TOKEN`` but is never written to log output.
    """

    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if settings.github_token:
            # Token is stored in the header dict only; never logged.
            self.headers["Authorization"] = f"Bearer {settings.github_token}"
        else:
            logger.warning(
                "GITHUB_TOKEN is not set. GitHub API requests may be rate-limited."
            )

    async def get_repository(self, owner: str, repo: str) -> dict:
        """Return repository metadata for ``owner/repo``."""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            for attempt in range(1, _MAX_RETRIES + 1):
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status in _RATE_LIMIT_STATUSES:
                        if attempt == _MAX_RETRIES:
                            logger.error(
                                "GitHub rate limit exceeded for %s after %d attempts.",
                                url,
                                _MAX_RETRIES,
                            )
                            return {"error": "Rate limit exceeded or access forbidden."}
                        wait = 2**attempt
                        logger.warning(
                            "GitHub rate-limit (HTTP %d, attempt %d/%d). "
                            "Sleeping %d s.",
                            response.status,
                            attempt,
                            _MAX_RETRIES,
                            wait,
                        )
                    elif response.status == 404:
                        return {"error": "Repository not found."}
                    else:
                        text = await response.text()
                        logger.error(
                            "GitHub API error %d fetching repository: %s",
                            response.status,
                            text,
                        )
                        return {"error": f"API error: {response.status}"}
                await asyncio.sleep(2**attempt)
        return {"error": "Rate limit exceeded or access forbidden."}

    async def get_recent_commits(self, owner: str, repo: str, limit: int = 5) -> list:
        """Return the ``limit`` most recent commits for ``owner/repo``."""
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {"per_page": limit}
        async with aiohttp.ClientSession(headers=self.headers) as session:
            for attempt in range(1, _MAX_RETRIES + 1):
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status in _RATE_LIMIT_STATUSES:
                        if attempt == _MAX_RETRIES:
                            logger.error(
                                "GitHub rate limit exceeded fetching commits "
                                "after %d attempts.",
                                _MAX_RETRIES,
                            )
                            return []
                        wait = 2**attempt
                        logger.warning(
                            "GitHub rate-limit (HTTP %d, attempt %d/%d). "
                            "Sleeping %d s.",
                            response.status,
                            attempt,
                            _MAX_RETRIES,
                            wait,
                        )
                    else:
                        logger.error(
                            "GitHub API error %d fetching commits.",
                            response.status,
                        )
                        return []
                await asyncio.sleep(2**attempt)
        return []


github_service = GitHubService()
