import asyncpg

from app.config import settings

pool: asyncpg.Pool | None = None
startup_error: str | None = None


async def connect_database() -> None:
    global pool, startup_error

    try:
        pool = await asyncpg.create_pool(
            dsn=settings.database_url,
            min_size=1,
            max_size=4,
            timeout=10,
        )
        startup_error = None
    except Exception as exc:  # pragma: no cover
        pool = None
        startup_error = f"{type(exc).__name__}: {exc}"


async def disconnect_database() -> None:
    global pool

    if pool is not None:
        await pool.close()
        pool = None


async def ping_database() -> tuple[bool, str]:
    global pool

    if pool is None:
        await connect_database()

    if pool is None:
        return False, startup_error or "Database pool is not initialized."

    try:
        async with pool.acquire() as connection:
            probe = await connection.fetchval("SELECT 1;")

        if probe == 1:
            return True, "Neon PostgreSQL reachable."

        return False, "Unexpected database probe result."
    except Exception as exc:  # pragma: no cover
        return False, f"{type(exc).__name__}: {exc}"
