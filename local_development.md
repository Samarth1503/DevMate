# Local Development Guide — DevMate

This guide walks you through setting up a complete local development environment for DevMate, from prerequisites through running the bot, executing tests, and linting.

---

## Prerequisites

| Tool | Minimum Version | Install |
|---|---|---|
| **Git** | any | [git-scm.com](https://git-scm.com/) |
| **Python** | 3.11 | [python.org](https://www.python.org/downloads/) |
| **Docker Desktop** | any | [docker.com](https://www.docker.com/products/docker-desktop/) |
| **Docker Compose** | v2 (bundled with Docker Desktop) | included above |

> **Windows note**: run all commands in PowerShell or Command Prompt (not WSL unless you've configured Docker Desktop for WSL 2).

---

## 1. Clone the Repository

```bash
git clone https://github.com/yourorg/DevMate.git
cd DevMate
```

---

## 2. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in **every** value:

```
DISCORD_BOT_TOKEN=<your Discord bot token>
COMMAND_PREFIX=$
DATABASE_URL=postgresql://devpulse_user:devpulse_password@localhost:5432/devpulse_db
REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=<your Google AI Studio API key>
GITHUB_TOKEN=<your GitHub personal access token>
```

### How to obtain each token

#### Discord Bot Token
1. Go to [discord.com/developers/applications](https://discord.com/developers/applications).
2. Create a new application → **Bot** tab → **Reset Token**.
3. Enable **Message Content Intent** under Privileged Gateway Intents.
4. Paste the token into `.env`.

#### Gemini API Key (free tier)
1. Visit [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).
2. Click **Create API key**.
3. Paste it into `.env`.

#### GitHub Personal Access Token
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens).
2. **Generate new token (classic)** → select `public_repo` scope (add `repo` for private repos).
3. Paste it into `.env`.

> **Security**: `.env` is listed in `.gitignore` — it will never be committed.

---

## 5. Start Infrastructure (PostgreSQL + Redis)

```bash
docker compose up -d
```

This starts:
- **PostgreSQL 16** on `localhost:5432`
- **Redis 7** on `localhost:6379`

Both containers use named Docker volumes so data persists across restarts.

Verify containers are running:
```bash
docker compose ps
```

---

## 6. Run the Bot

```bash
python main.py
```

Expected startup output:
```
[INFO] root: Connecting to PostgreSQL pool...
[INFO] root: Connected to PostgreSQL pool.
[INFO] discord.gateway: Shard ID None has connected to Gateway ...
[cogwatch] Found cogs/
[cogwatch] [Cog Loaded] cogs.general
[cogwatch] [Cog Loaded] cogs.analytics
[cogwatch] [Cog Loaded] cogs.assistant
[cogwatch] [Cog Loaded] cogs.github
[INFO] root: Logged in as DevMate#XXXX (ID: ...)
[INFO] root: Bot is ready.
```

Stop the bot with `Ctrl+C`.

---

## 7. Invite the Bot to a Server

Use the OAuth2 URL Generator in the Discord Developer Portal:
- **Scopes**: `bot`
- **Bot Permissions**: `Send Messages`, `Embed Links`, `Read Message History`, `Read Messages/View Channels`

Or build the URL manually:
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=67584&scope=bot
```

---

## 8. Test Commands in Discord

Once the bot is online:

| Type this | Expected result |
|---|---|
| `$` | Command list embed |
| `$list` | Same command list embed |
| `$commands` | Same command list embed |
| `$hello` | `Hello!` |
| `$stats` | Analytics embed |
| `$ask What is Python?` | AI answer from Gemini |
| `$debug <error text>` | Stack trace analysis |
| `$repo torvalds linux` | GitHub repo info |
| `$commits torvalds linux` | Recent commits |

---

## 9. Run the Test Suite

All external services (Gemini, GitHub, ChromaDB) are mocked — **no real API keys are needed** for tests.

```bash
pytest
```

Expected output:
```
collected 7 items

tests/test_config.py .
tests/test_database.py .
tests/test_services.py .....

7 passed in X.Xs
```

---

## 10. Lint and Format

```bash
# Check for style violations
ruff check .

# Auto-fix safe violations
ruff check --fix .
```

---

## 11. Hot-Reloading (Development)

`cogwatch` watches the `cogs/` directory. While `main.py` is running, any saved change to a `.py` file in `cogs/` is automatically reloaded — no restart needed.

---

## 12. Full Docker Deployment (Optional)

To run the **entire stack** (bot + PostgreSQL + Redis) in Docker:

```bash
# Build and start everything
docker compose --profile full up --build -d

# Stream logs
docker compose logs -f bot
```

> The `Dockerfile` in the project root builds the bot image. The `docker-compose.yml` defines the `postgres` and `redis` services; the bot can be added as a third service profile for full containerisation.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `pydantic_settings.env_settings.EnvSettingsError` | Missing value in `.env` | Ensure all fields in `.env.example` are set in `.env` |
| `asyncpg.exceptions.ConnectionFailureError` | PostgreSQL not running | Run `docker compose up -d` |
| `Cannot connect to host localhost:6379` | Redis not running | Run `docker compose up -d` |
| `404 NOT_FOUND` from Gemini | Wrong model name or stale API key | Current model is `gemini-3.6-flash`; regenerate your API key |
| `401 Unauthorized` from GitHub | Expired or missing token | Regenerate token at github.com/settings/tokens |
| Bot online but not responding | Missing **Message Content Intent** | Enable it in the Discord Developer Portal → Bot settings |
| `PyNaCl is not installed` warning | Optional voice dependency | Safe to ignore unless you need voice features |
