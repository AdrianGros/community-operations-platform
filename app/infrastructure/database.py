from __future__ import annotations

import json
import logging
import sqlite3
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from app.domain.enums import CaseStatus

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Migration:
    version: str
    sql: str


MIGRATIONS: tuple[Migration, ...] = (
    Migration(
        "001_init",
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            display_name TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS role_bindings (
            user_id INTEGER NOT NULL,
            role_code TEXT NOT NULL,
            assigned_at TEXT NOT NULL,
            PRIMARY KEY (user_id, role_code),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS governance_policy (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            read_only_enabled INTEGER NOT NULL DEFAULT 0,
            feature_flags TEXT NOT NULL DEFAULT '{}',
            updated_at TEXT NOT NULL,
            updated_by INTEGER NULL,
            FOREIGN KEY (updated_by) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS review_cases (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            case_kind TEXT NOT NULL DEFAULT 'finding',
            risk_level TEXT NOT NULL DEFAULT 'Medium',
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            finding_status TEXT NOT NULL DEFAULT 'identified',
            control_status TEXT NOT NULL DEFAULT 'needs_attention',
            measure_title TEXT NOT NULL DEFAULT 'Document mitigation action',
            measure_status TEXT NOT NULL DEFAULT 'planned',
            measure_owner INTEGER NULL,
            due_at TEXT NULL,
            evidence_note TEXT NULL,
            claimed_by INTEGER NULL,
            claimed_at TEXT NULL,
            decision TEXT NULL,
            decision_reason TEXT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (claimed_by) REFERENCES users(id),
            FOREIGN KEY (measure_owner) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS audit_events (
            id INTEGER PRIMARY KEY,
            occurred_at TEXT NOT NULL,
            actor_user_id INTEGER NULL,
            domain TEXT NOT NULL,
            action TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            entity_id INTEGER NULL,
            payload_json TEXT NOT NULL DEFAULT '{}',
            FOREIGN KEY (actor_user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS health_check_results (
            id INTEGER PRIMARY KEY,
            check_type TEXT NOT NULL,
            ok INTEGER NOT NULL,
            message TEXT NOT NULL,
            measured_at TEXT NOT NULL
        );
        """,
    ),
    Migration(
        "002_audit_health_enrichment",
        """
        ALTER TABLE audit_events ADD COLUMN severity TEXT NOT NULL DEFAULT 'info';
        ALTER TABLE health_check_results ADD COLUMN details_json TEXT NOT NULL DEFAULT '{}';
        """,
    ),
    Migration(
        "003_review_case_governance_context",
        """
        ALTER TABLE review_cases ADD COLUMN case_kind TEXT NOT NULL DEFAULT 'finding';
        ALTER TABLE review_cases ADD COLUMN risk_level TEXT NOT NULL DEFAULT 'Medium';
        ALTER TABLE review_cases ADD COLUMN finding_status TEXT NOT NULL DEFAULT 'identified';
        ALTER TABLE review_cases ADD COLUMN control_status TEXT NOT NULL DEFAULT 'needs_attention';
        ALTER TABLE review_cases ADD COLUMN measure_title TEXT NOT NULL DEFAULT 'Document mitigation action';
        ALTER TABLE review_cases ADD COLUMN measure_status TEXT NOT NULL DEFAULT 'planned';
        ALTER TABLE review_cases ADD COLUMN measure_owner INTEGER NULL;
        ALTER TABLE review_cases ADD COLUMN due_at TEXT NULL;
        ALTER TABLE review_cases ADD COLUMN evidence_note TEXT NULL;
        """,
    ),
)


def utc_now() -> str:
    return datetime.now(tz=UTC).isoformat()


def ensure_runtime_dirs(base_dir: Path) -> tuple[Path, Path]:
    data_dir = base_dir / "var"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "governance_showcase.db", data_dir / "governance_showcase.log"


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def column_exists(conn: sqlite3.Connection, table_name: str, column_name: str) -> bool:
    if not table_exists(conn, table_name):
        return False
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(row["name"] == column_name for row in rows)


def _apply_known_migration(conn: sqlite3.Connection, migration: Migration) -> None:
    if migration.version == "002_audit_health_enrichment":
        if not column_exists(conn, "audit_events", "severity"):
            conn.execute("ALTER TABLE audit_events ADD COLUMN severity TEXT NOT NULL DEFAULT 'info'")
        if not column_exists(conn, "health_check_results", "details_json"):
            conn.execute("ALTER TABLE health_check_results ADD COLUMN details_json TEXT NOT NULL DEFAULT '{}'")
        return
    if migration.version == "003_review_case_governance_context":
        case_columns = (
            ("case_kind", "TEXT NOT NULL DEFAULT 'finding'"),
            ("risk_level", "TEXT NOT NULL DEFAULT 'Medium'"),
            ("finding_status", "TEXT NOT NULL DEFAULT 'identified'"),
            ("control_status", "TEXT NOT NULL DEFAULT 'needs_attention'"),
            ("measure_title", "TEXT NOT NULL DEFAULT 'Document mitigation action'"),
            ("measure_status", "TEXT NOT NULL DEFAULT 'planned'"),
            ("measure_owner", "INTEGER NULL"),
            ("due_at", "TEXT NULL"),
            ("evidence_note", "TEXT NULL"),
        )
        for column_name, column_def in case_columns:
            if not column_exists(conn, "review_cases", column_name):
                conn.execute(f"ALTER TABLE review_cases ADD COLUMN {column_name} {column_def}")
        return
    conn.executescript(migration.sql)


def apply_migrations(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL
        )
        """
    )
    applied = {
        row["version"]
        for row in conn.execute("SELECT version FROM schema_migrations ORDER BY version ASC").fetchall()
    }
    for migration in MIGRATIONS:
        if migration.version in applied:
            continue
        with conn:
            _apply_known_migration(conn, migration)
            conn.execute(
                "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
                (migration.version, utc_now()),
            )
        log.info("Applied migration %s", migration.version)


def seed_demo_data(conn: sqlite3.Connection) -> None:
    now = utc_now()
    with conn:
        conn.executemany(
            "INSERT OR IGNORE INTO users (id, display_name, is_active) VALUES (?, ?, ?)",
            [
                (1, "Avery Stone", 1),
                (2, "Mina Patel", 1),
                (3, "Jonas Becker", 1),
            ],
        )
        conn.executemany(
            "INSERT OR IGNORE INTO role_bindings (user_id, role_code, assigned_at) VALUES (?, ?, ?)",
            [
                (1, "ADMIN", now),
                (2, "REVIEWER", now),
                (3, "AUDITOR", now),
            ],
        )
        conn.execute(
            """
            INSERT INTO governance_policy (id, read_only_enabled, feature_flags, updated_at, updated_by)
            VALUES (1, 0, ?, ?, 1)
            ON CONFLICT(id) DO NOTHING
            """,
            (json.dumps({"review_cases": True}, sort_keys=True), now),
        )
        conn.executemany(
            """
            INSERT INTO review_cases (
                id, title, summary, case_kind, risk_level, status, priority, finding_status,
                control_status, measure_title, measure_status, measure_owner, due_at, evidence_note,
                claimed_by, claimed_at, decision, decision_reason, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO NOTHING
            """,
            [
                (
                    1,
                    "Pruefung des Lieferanten-Onboardings",
                    "Pruefe Rollenzuordnung und Nachweise vor der Freigabe.",
                    "finding",
                    "High",
                    CaseStatus.OPEN,
                    "High",
                    "identified",
                    "needs_attention",
                    "Onboarding-Nachweise sammeln und Kontroll-Owner bestaetigen.",
                    "planned",
                    2,
                    "2026-03-20T17:00:00+00:00",
                    "Erste Abweichung aus der quartalsweisen Onboarding-Kontrollpruefung erfasst.",
                    None,
                    None,
                    None,
                    None,
                    now,
                    now,
                ),
                (
                    2,
                    "Nachverfolgung einer Zugriffsabweichung",
                    "Abgelaufene Freigabeausnahme pruefen und die Abweichung schliessen.",
                    "finding",
                    "High",
                    CaseStatus.CLAIMED,
                    "High",
                    "in_progress",
                    "partially_effective",
                    "Ausnahmefreigabe erneut bestaetigen und den Nachweishinweis aktualisieren.",
                    "in_progress",
                    2,
                    "2026-03-18T17:00:00+00:00",
                    "Die Ausnahme besteht, aber der Nachweis fuer die Verlaengerung fehlt noch.",
                    2,
                    now,
                    None,
                    None,
                    now,
                    now,
                ),
                (
                    3,
                    "Antrag auf Policy-Ausnahme",
                    "Temporare Policy-Ausnahme fuer einen Finanz-Workflow pruefen.",
                    "risk",
                    "Medium",
                    CaseStatus.APPROVED,
                    "Medium",
                    "mitigated",
                    "monitored",
                    "Kompensierende Kontrolle nachhalten, bis die temporaere Ausnahme endet.",
                    "completed",
                    1,
                    "2026-03-25T17:00:00+00:00",
                    "Kompensierende Kontrolle dokumentiert und fuer begrenzte Dauer freigegeben.",
                    2,
                    now,
                    "approved",
                    "Temporare Ausnahme mit Owner dokumentiert.",
                    now,
                    now,
                ),
                (
                    4,
                    "Quartalspruefung der Kontrollnachweise",
                    "Pruefen, ob vor dem Abschluss alle Review-Notizen angehaengt wurden.",
                    "finding",
                    "Medium",
                    CaseStatus.REJECTED,
                    "Medium",
                    "identified",
                    "needs_attention",
                    "Fehlenden Nachweishinweis beim Kontroll-Owner anfordern.",
                    "planned",
                    1,
                    "2026-03-19T17:00:00+00:00",
                    "Kontrollpruefung fehlgeschlagen, weil die Nachweisnotizen unvollstaendig waren.",
                    1,
                    now,
                    "rejected",
                    "Nachweishinweis war unvollstaendig.",
                    now,
                    now,
                ),
                (
                    5,
                    "Anfrage zum Change Freeze",
                    "Pruefen, ob der Nur-Lesen-Modus fuer den Betrieb wieder aufgehoben werden kann.",
                    "control_review",
                    "Low",
                    CaseStatus.CLOSED,
                    "Low",
                    "closed",
                    "effective",
                    "Normalen Governance-Modus nach dem Freeze-Zeitraum bestaetigen.",
                    "completed",
                    1,
                    "2026-03-17T12:00:00+00:00",
                    "Change Freeze abgeschlossen und Betriebspruefung freigegeben.",
                    1,
                    now,
                    "approved",
                    "Freeze nach erfolgreicher Validierung beendet.",
                    now,
                    now,
                ),
                (
                    6,
                    "Luecke bei der Reviewer-Zuordnung",
                    "Innerhalb des Zielzeitraums hat kein Reviewer den Fall uebernommen.",
                    "finding",
                    "High",
                    CaseStatus.OPEN,
                    "Low",
                    "identified",
                    "needs_attention",
                    "Backup-Reviewer zuweisen und den Eskalationspfad dokumentieren.",
                    "planned",
                    None,
                    "2026-03-17T17:00:00+00:00",
                    "Eskalation noetig, weil die Review-Warteschlange die Zielzeit ueberschritten hat.",
                    None,
                    None,
                    None,
                    None,
                    now,
                    now,
                ),
            ],
        )
        conn.executemany(
            """
            INSERT INTO audit_events (
                occurred_at, actor_user_id, severity, domain, action, entity_type, entity_id, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [] if _has_seed_audit_event(conn) else [
                (now, 1, "info", "governance", "seeded", "policy", 1, json.dumps({"read_only_enabled": False})),
                (now, 2, "info", "review_case", "claimed", "review_case", 2, json.dumps({"status": "claimed"})),
                (now, 2, "info", "review_case", "approved", "review_case", 3, json.dumps({"decision": "approved"})),
                (now, 1, "warning", "review_case", "rejected", "review_case", 4, json.dumps({"decision": "rejected"})),
                (now, None, "info", "health", "snapshot", "health", None, json.dumps({"ok": True, "source": "seed"})),
            ],
        )
        if not _has_startup_health_snapshot(conn):
            conn.execute(
                """
                INSERT INTO health_check_results (check_type, ok, message, measured_at, details_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    "startup",
                    1,
                    "Datenbank initialisiert, Seed-Daten geladen, Schema OK.",
                    now,
                    json.dumps(
                        {
                            "checks": [
                                {"name": "schema_tables", "ok": True, "detail": "Alle erwarteten Tabellen vorhanden"},
                                {"name": "governance_policy", "ok": True, "detail": "Policy-Datensatz angelegt"},
                                {"name": "seed_users", "ok": True, "detail": "Demo-Nutzer verfuegbar"},
                            ]
                        },
                        sort_keys=True,
                    ),
                ),
            )
    log.info("Demo baseline ensured")


def _has_seed_audit_event(conn: sqlite3.Connection) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM audit_events
        WHERE domain = 'governance' AND action = 'seeded'
        LIMIT 1
        """
    ).fetchone()
    return row is not None


def _has_startup_health_snapshot(conn: sqlite3.Connection) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM health_check_results
        WHERE check_type = 'startup'
        LIMIT 1
        """
    ).fetchone()
    return row is not None


def fetch_table_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    return {str(row["name"]) for row in rows}


def expected_tables() -> set[str]:
    return {
        "schema_migrations",
        "users",
        "role_bindings",
        "governance_policy",
        "review_cases",
        "audit_events",
        "health_check_results",
    }


def reset_database(conn: sqlite3.Connection, tables: Iterable[str]) -> None:
    with conn:
        for table in tables:
            conn.execute(f"DELETE FROM {table}")
