# 🚀 DevMate — AI-Powered Developer Community & DevOps Bot

An asynchronous, event-driven Discord application designed to act as a developer assistant, integrating real-time analytics, AI-assisted debugging, GitHub activity tracking, semantic knowledge search, and background jobs powered by PostgreSQL and Redis.

## 📌 System Architecture

DevMate is engineered as a layered service architecture to decouple the Discord presentation layer from core business logic, database persistence, and external APIs.

```
              +-------------------+
              |   Discord Users   |
              +---------+---------+
                        |
                        v
              +-------------------+
              |  DevMate Client   |
              |   (discord.py)    |
              +---------+---------+
                        |
       +----------------+-----------------+
       |                                  |
       v                                  v
+-----------------+             +-------------------+
| Command Layer   |             |  Event Handlers   |
| (Discord Cogs)  |             | (Message/Guild)   |
+--------+--------+             +---------+---------+
         |                                |
         +----------------+--------------+
                          |
                          v
               +--------------------+
               |   Service Layer    |
               +--+----+----+----+--+
                  |    |    |    |
   +--------------+    |    |    +--------------+
   |                   |    |                   |
   v                   v    v                   v
+-----------+   +---------+  +-----------+  +----------+
| GitHub API|   | AI/LLM  |  | Background|  |Analytics |
|(aiohttp)  |   | (Gemini)|  |  Workers  |  |Aggregator|
+-----------+   +---------+  +-----------+  +----------+
                     |
                     v
   +----------------------------------+
   | Persistence & Caching Layer      |
   |  - PostgreSQL (via asyncpg pool) |
   |  - Redis (via redis-py cache)    |
   |  - ChromaDB (vector embeddings)  |
   +----------------------------------+
```

## ✨ Key Features

| Feature | Command(s) | Description |
|---|---|---|
| **Command List** | `$`, `$list`, `$commands` | Shows an embed with all available commands |
| **Developer Analytics** | `$stats` | Real-time server activity, active users, and command metrics stored in PostgreSQL |
| **AI Developer Assistant** | `$ask`, `$debug` | Context-aware Q&A and stack trace analysis via Google Gemini |
| **Knowledge Base** | `$remember`, `$search` | Store and vector-search developer notes via ChromaDB |
| **GitHub Integration** | `$repo`, `$commits` | Repository info and recent commit history via GitHub REST API |
| **Hot-Reloading** | — | Live cog reloading via `cogwatch`; no bot restart needed during development |

## 🛠️ Tech Stack

| Domain | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11+ | Core application logic and async handling |
| **Framework** | `discord.py` v2 | Asynchronous Gateway API interaction |
| **AI / LLM** | Google Gemini (`gemini-3.6-flash`) | Error analysis, Q&A, Interactions API |
| **Vector DB** | ChromaDB (local) | Persistent semantic knowledge search |
| **Database** | PostgreSQL 16 | Relational storage for analytics & app data |
| **DB Driver** | `asyncpg` | High-performance async connection pooling |
| **Caching / Queue** | Redis 7 | Rate-limiting, API response caching, job queue |
| **GitHub Client** | `aiohttp` + GitHub REST API | Repository metrics, commits, rate-limit retry |
| **Infrastructure** | Docker & Docker Compose | Isolated PostgreSQL + Redis containers |
| **Config** | `pydantic-settings` | Type-safe, validated environment loading |
| **Code Quality** | `ruff`, `pre-commit` | PEP 8 linting, formatting, and git hooks |
| **Dev Tools** | `cogwatch` | Live hot-reloading file watcher |

## 📁 Directory Structure

```
DevMate/
├── cogs/                    # Presentation Layer: Commands and event listeners
│   ├── analytics.py         # $stats — metrics collection & dashboard
│   ├── assistant.py         # $ask, $debug, $remember, $search — AI & KB
│   ├── general.py           # $hello, $list, $commands — general listeners
│   └── github.py            # $repo, $commits — GitHub integration
├── core/
│   └── config.py            # pydantic-settings environment validation
├── database/
│   └── connection.py        # Async PostgreSQL lifecycle & pool management
├── services/
│   ├── gemini_service.py    # LLM provider: Google Gemini Interactions API
│   ├── github.py            # GitHub REST API client with retry logic
│   ├── chroma_service.py    # ChromaDB vector store client
│   └── llm_provider.py      # Abstract base class for LLM providers
├── tests/                   # pytest test suite (all external calls mocked)
├── .env.example             # Template for required environment variables
├── .gitignore               # Excludes .env, venv, chroma_db, __pycache__
├── .pre-commit-config.yaml  # Git hook: ruff lint on every commit
├── docker-compose.yml       # PostgreSQL + Redis container specs
├── Dockerfile               # Bot container image (for full Docker deployment)
├── main.py                  # Bot entry point and lifecycle startup
├── pyproject.toml           # Ruff configuration
└── requirements.txt         # Python project dependencies
```

## ⚙️ Environment Variables

Copy `.env.example` to `.env` and fill in all values:

```
DISCORD_BOT_TOKEN   — Discord bot token (from Discord Developer Portal)
COMMAND_PREFIX      — Bot prefix, default: $
DATABASE_URL        — PostgreSQL connection string
REDIS_URL           — Redis connection string
GEMINI_API_KEY      — Google AI Studio API key (free tier works)
GITHUB_TOKEN        — GitHub personal access token (for higher rate limits)
```

> See [local_development.md](./local_development.md) for step-by-step setup instructions.

## 🚀 Quick Start

```bash
# 1. Clone and enter the project
git clone https://github.com/yourorg/DevMate.git && cd DevMate

# 2. Create and activate a virtual environment
python -m venv venv && venv\Scripts\activate   # Windows
# python -m venv venv && source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure secrets
copy .env.example .env   # then edit .env with real values

# 5. Start infrastructure (PostgreSQL + Redis)
docker compose up -d

# 6. Run the bot
python main.py
```

## 🧪 Testing & Linting

```bash
# Run the full test suite (no real API keys needed — all calls are mocked)
pytest

# Lint and format check
ruff check .
```

## 🔐 Security Notes

- **`.env` is git-ignored** — never commit it.
- **API keys are never logged** — the logging layer is designed to scrub secrets.
- **GitHub token** is stored in request headers only; it is never written to log output.
- **Gemini exceptions** are caught and returned as generic user-facing messages; raw SDK errors (which may contain key fragments) are not forwarded to Discord.
