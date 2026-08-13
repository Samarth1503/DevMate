# 🚀 DevMate — AI-Powered Developer Community & DevOps Bot

An asynchronous, event-driven Discord application designed to act as a developer assistant, integrating real-time analytics, AI-assisted debugging, GitHub activity tracking, and background jobs powered by PostgreSQL and Redis.

## 📌 System Architecture

DevMate is engineered as a layered service architecture to decouple the Discord presentation layer from core business logic, database persistence, and external APIs.

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
         +------------------+------------------+
         |                                     |
         v                                     v
+-----------------+                  +-------------------+
| Command Layer   |                  |  Event Handlers   |
| (Discord Cogs)  |                  | (Message/Guild)   |
+--------+--------+                  +---------+---------+
         |                                     |
         +------------------+------------------+
                            |
                            v
                 +--------------------+
                 |   Service Layer    |
                 +--+----+----+----+--+
                    |    |    |    |
   +----------------+    |    |    +----------------+
   |                     |    |                     |
   v                     v    v                     v
   +--------------+     +---------+  +-------------+  +------------+
   |  GitHub API  |     | AI/LLM  |  | Background  |  | Analytics  |
   | Integration  |     | Engine  |  | Worker Jobs |  | Aggregator |
   +--------------+     +---------+  +-------------+  +------------+
   |                     |    |                     |
   +------------------+  |    |  +------------------+
   |                     |    |
   v                     v    v
   +----------------------------------+
   | Persistence & Caching Layer      |
   |  - PostgreSQL (via asyncpg pool) |
   |  - Redis (via redis-py cache)    |
   +----------------------------------+


## ✨ Key Features

**📊 Real-time Developer Analytics (`/stats`)**: Asynchronous aggregation of server activity, active users, and command invocation stored in PostgreSQL via connection pooling.
**⚡ Hot-Reloading Architecture**: Built using modular `discord.py` Cogs and `cogwatch` file-system watchers, allowing live code updates without disconnecting from the Discord Gateway API.
**🤖 AI Developer Assistant**: Context-aware error analysis and stack trace debugging using LLM integration.
**🚀 GitHub Integration**: Repository metrics fetcher, commit histories, and webhook notifications for Pull Requests and Issues.
**🧠 Developer Knowledge Base**: Persistent documentation storage and vector similarity search.
**⏰ Asynchronous Background Scheduler**: Non-blocking scheduled reminders and event monitoring using async workers.


## 🛠️ Tech Stack

| ------------------------- | ------------------------------------ | --------------------------------------------------- |
| Domain                    | Technology                           | Purpose                                             |
| ------------------------- | ------------------------------------ | --------------------------------------------------- |
| **Language**              | Python 3.11+                         | Core application logic and async handling           |
| **Framework**             | `discord.py` v2                      | Asynchronous Gateway API interaction                |
| **Database**              | PostgreSQL 16                        | Relational storage for analytics & application data |
| **DB Driver**             | `asyncpg`                            | High-performance async connection pooling           |
| **Caching / Queue**       | Redis 7                              | Rate-limiting, API response caching, and job queue  |
| **Infrastructure**        | Docker & Docker Compose              | Isolated local container development                |
| **Config & Environment**  | `pydantic-settings`, `python-dotenv` | Type-safe environment validation                    |
| **Code Quality / PEP 8**  | `ruff`, `pre-commit`                 | Automated PEP 8 linting, formatting, and git hooks  |
| **Development**           | `cogwatch`                           | Live hot-reloading file watcher                     |
| ------------------------- | ------------------------------------ | --------------------------------------------------- |


## 📁 Directory Structure

DevMate/
├── .vscode/
│   └── settings.json       # Auto-format on Ctrl+S
├── cogs/                   # Presentation Layer: Commands and event listeners
│   └── analytics.py        # Metrics collection & /stats dashboard
├── core/                   # Application Core: Config, logging, and settings
│   └── config.py           # Environment settings validation
├── database/               # Persistence Layer: Connection pool and SQL queries
│   └── connection.py       # Async PostgreSQL lifecycle management
├── services/               # Business Logic Layer: External API clients
├── .pre-commit-config.yaml # Git hook for PEP 8
├── docker-compose.yml      # PostgreSQL and Redis container specs
├── main.py                 # Bot entry point and lifecycle startup
├── pyproject.toml          # PEP 8 / Ruff config
├── requirements.txt        # Python project dependencies
└── .env                    # Environment variables (excluded from git)

