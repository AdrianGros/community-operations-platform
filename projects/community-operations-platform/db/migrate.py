from __future__ import annotations

import argparse
import asyncio
import hashlib
from pathlib import Path
from typing import Any

import asyncpg

TRACKING_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    checksum TEXT NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""


def default_migrations_path() -> Path:
    return Path(__file__).resolve().parent / "migrations"


def list_migration_files(migrations_path: str | Path | None = None) -> list[Path]:
    path = default_migrations_path() if migrations_path is None else Path(migrations_path)
    if not path.exists():
        raise RuntimeError(f"Migrations path does not exist: {path}")
    if not path.is_dir():
        raise RuntimeError(f"Migrations path is not a directory: {path}")
    return sorted(p for p in path.glob("*.sql") if p.is_file())


def compute_checksum(file_path: Path) -> str:
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


async def ensure_schema_migrations_table(conn: asyncpg.Connection) -> None:
    await conn.execute(TRACKING_TABLE_DDL)


async def get_applied_versions(conn: asyncpg.Connection) -> dict[str, dict[str, Any]]:
    await ensure_schema_migrations_table(conn)
    rows = await conn.fetch(
        """
        SELECT version, checksum, applied_at
        FROM schema_migrations
        ORDER BY applied_at ASC, version ASC
        """
    )
    return {
        str(row["version"]): {
            "checksum": str(row["checksum"]),
            "applied_at": row["applied_at"],
        }
        for row in rows
    }


async def apply_migration(conn: asyncpg.Connection, file_path: Path, *, checksum: str) -> None:
    sql = file_path.read_text(encoding="utf-8")
    async with conn.transaction():
        await conn.execute(sql)
        await conn.execute(
            """
            INSERT INTO schema_migrations (version, checksum)
            VALUES ($1, $2)
            ON CONFLICT (version) DO NOTHING
            """,
            file_path.name,
            checksum,
        )


async def detect_tampered_files(conn: asyncpg.Connection, files: list[Path]) -> list[str]:
    applied = await get_applied_versions(conn)
    tampered: list[str] = []
    for file_path in files:
        version = file_path.name
        stored = applied.get(version)
        if stored is None:
            continue
        if compute_checksum(file_path) != stored["checksum"]:
            tampered.append(version)
    return tampered


async def apply_all_migrations(pool: asyncpg.Pool, migrations_path: str | Path | None = None) -> dict[str, list[str]]:
    files = list_migration_files(migrations_path)
    summary: dict[str, list[str]] = {"applied": [], "skipped": [], "errors": [], "tampered": []}

    async with pool.acquire() as conn:
        await ensure_schema_migrations_table(conn)
        tampered = await detect_tampered_files(conn, files)
        if tampered:
            summary["tampered"] = tampered
            summary["errors"].append("checksum mismatch for applied migration(s): " + ", ".join(tampered))
            return summary

        applied = await get_applied_versions(conn)
        for file_path in files:
            if file_path.name in applied:
                summary["skipped"].append(file_path.name)
                continue
            try:
                await apply_migration(conn, file_path, checksum=compute_checksum(file_path))
            except Exception as exc:
                summary["errors"].append(f"{file_path.name}: {exc.__class__.__name__}: {exc}")
                break
            summary["applied"].append(file_path.name)

    return summary


async def get_schema_version(pool: asyncpg.Pool) -> dict[str, Any]:
    async with pool.acquire() as conn:
        await ensure_schema_migrations_table(conn)
        latest = await conn.fetchrow(
            """
            SELECT version, applied_at
            FROM schema_migrations
            ORDER BY applied_at DESC, version DESC
            LIMIT 1
            """
        )
        count = await conn.fetchval("SELECT COUNT(*) FROM schema_migrations")

    return {
        "count": int(count or 0),
        "latest_version": None if latest is None else str(latest["version"]),
        "latest_applied_at": None if latest is None else latest["applied_at"],
    }


async def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices={"status", "upgrade"})
    parser.add_argument("--database-url", required=True)
    args = parser.parse_args()

    pool = await asyncpg.create_pool(dsn=args.database_url, min_size=1, max_size=3)
    try:
        if args.command == "status":
            print(await get_schema_version(pool))
            return 0
        print(await apply_all_migrations(pool))
        return 0
    finally:
        await pool.close()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main()))
