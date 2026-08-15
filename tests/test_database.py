from unittest.mock import AsyncMock, patch

import pytest

from database.connection import Database


@pytest.mark.asyncio
async def test_database_connect_disconnect():
    db = Database()

    with (
        patch("asyncpg.create_pool", new_callable=AsyncMock) as mock_pool_patch,
        patch.object(Database, "_init_schema", new_callable=AsyncMock) as mock_schema,
    ):
        mock_pool = AsyncMock()
        mock_pool_patch.return_value = mock_pool

        # Connect should initialize the pool and call _init_schema
        await db.connect()
        mock_pool_patch.assert_called_once()
        mock_schema.assert_called_once()
        assert db.pool == mock_pool

        # Disconnect should close the pool
        await db.disconnect()
        mock_pool.close.assert_called_once()
