import logging

import asyncpg

from core.config import settings


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        if not self.pool:
            logging.info("Connecting to PostgreSQL pool...")
            self.pool = await asyncpg.create_pool(dsn=settings.database_url)
            logging.info("Connected to PostgreSQL pool.")
            await self._init_schema()

    async def _init_schema(self):
        logging.info("Initializing database schema...")
        try:
            with open("database/schema.sql") as f:
                schema_sql = f.read()
            async with self.pool.acquire() as conn:
                await conn.execute(schema_sql)
            logging.info("Database schema initialized successfully.")
        except FileNotFoundError:
            logging.warning("schema.sql not found, skipping schema initialization.")

    async def disconnect(self):
        if self.pool:
            logging.info("Closing PostgreSQL pool...")
            await self.pool.close()
            logging.info("PostgreSQL pool closed.")


db = Database()
