from core.config import Settings


def test_config_loads_from_env(monkeypatch):
    monkeypatch.setenv("DISCORD_BOT_TOKEN", "test_token")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost/db")
    monkeypatch.setenv("REDIS_URL", "redis://localhost")
    monkeypatch.setenv("COMMAND_PREFIX", "!")
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini")
    monkeypatch.setenv("GITHUB_TOKEN", "test_github")

    settings = Settings(_env_file=None)
    assert settings.discord_bot_token == "test_token"
    assert settings.command_prefix == "!"
    assert settings.database_url == "postgresql://user:pass@localhost/db"
    assert settings.redis_url == "redis://localhost"
    assert settings.gemini_api_key == "test_gemini"
    assert settings.github_token == "test_github"
