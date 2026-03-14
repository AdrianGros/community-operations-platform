# Feature Matrix

| Area | Visible artifact | Why it matters |
|---|---|---|
| Startup wiring | `app/excerpts/startup_wiring.py` | Shows dependency boundaries and a single composition root. |
| App state | `app/state.py` | Makes shared runtime dependencies explicit instead of implicit globals. |
| Migration discipline | `db/migrate.py`, `db/migrations/*` | Shows SQL-first schema handling and checksum-based drift protection. |
| Governance / RBAC | `bot/excerpts/guards_extract.py`, `db/migrations/026_governance_extract.sql` | Shows runtime permission control beyond basic command decorators. |
| Background processing | `bot/excerpts/session_loop_extract.py`, `db/migrations/028_jobs_extract.sql` | Shows job claiming, retry windows, and worker-style thinking. |
| Monitoring | `bot/excerpts/health_extract.py`, `bot/excerpts/error_notify_extract.py` | Shows health visibility and failure routing inside the platform. |
| Operations mindset | `ARCHITECTURE.md`, `SANITIZATION.md`, `RELEASE_NOTES.md` | Shows the system was treated as software that has to run, not just code that compiles. |
