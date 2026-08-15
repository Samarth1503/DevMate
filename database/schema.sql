-- DevMate Analytics Schema

CREATE TABLE IF NOT EXISTS command_metrics (
    id SERIAL PRIMARY KEY,
    command_name VARCHAR(255) NOT NULL,
    user_id BIGINT NOT NULL,
    guild_id BIGINT,
    invoked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_activity (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    guild_id BIGINT,
    message_count INT DEFAULT 0,
    last_active TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, guild_id)
);
