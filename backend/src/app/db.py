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


async def get_database_pool() -> asyncpg.Pool:
    global pool

    if pool is None:
        await connect_database()

    if pool is None:
        raise RuntimeError(startup_error or "Database pool is not initialized.")

    return pool


async def disconnect_database() -> None:
    global pool

    if pool is not None:
        await pool.close()
        pool = None


async def ping_database() -> tuple[bool, str]:
    try:
        database_pool = await get_database_pool()
    except RuntimeError as exc:
        return False, str(exc)

    try:
        async with database_pool.acquire() as connection:
            probe = await connection.fetchval("SELECT 1;")

        if probe == 1:
            return True, "PostgreSQL reachable."

        return False, "Unexpected database probe result."
    except Exception as exc:  # pragma: no cover
        return False, f"{type(exc).__name__}: {exc}"
