# Governance Showcase App

Eine lokal ausführbare PySide6-Showcase-Anwendung für governance-nahe und ISMS-nahe Arbeitslogik.

Die App zeigt bewusst kein vollständiges ISMS oder GRC-System, sondern einen kleinen, nachvollziehbaren Fachprototyp mit:

- Rollen- und Guard-Logik
- Review-/Claim-/Freigabe-Workflows
- Audit- und Nachweislogik
- Health-/Change-/Drift-Sicht
- exemplarischen Findings, Maßnahmen, Verantwortlichkeiten und Restrisiko-Entscheidungen

## Scope

Der Showcase ist dafür gebaut, im Bewerbungs- oder Interviewkontext glaubwürdig zu zeigen:

- kontrollierte Zustandsübergänge
- auditierbare Entscheidungen
- Governance-Guardrails wie Read-only und Feature-Flags
- nachvollziehbare Maßnahmenverfolgung
- lokale Robustheit durch Migrationen, Seeds, Tests und Health-Checks

Bewusst **nicht** enthalten:

- vollständige ISMS-/Compliance-Plattform
- ISO-27001-Abbildung in Tiefe
- Reporting-/Export-Suite
- Multi-Tenant-Oberflächen
- Incident-Response-, SIEM-, IAM- oder Schwachstellenmanagement

## Run

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m app.main
```

Die App legt lokal eine SQLite-Datenbank mit Migrationen und Demo-Seed-Daten an.

## Tests

```bash
QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest tests
```

## Tech Stack

- Python
- PySide6
- SQLite
- pytest + pytest-qt

## Repo Notes

- [`app`](/opt/community-operations-platform-showcase/app): Anwendungscode
- [`tests`](/opt/community-operations-platform-showcase/tests): Service- und GUI-Smoke-Tests
- [`ARCHITECTURE.md`](/opt/community-operations-platform-showcase/ARCHITECTURE.md): ergänzende Architekturhinweise
- [`PROJECT_CONTEXT.md`](/opt/community-operations-platform-showcase/PROJECT_CONTEXT.md): Projektkontext

## Positioning

Die richtige Einordnung ist:

- belastbarer lokaler Showcase
- kleiner Funktionsprototyp mit produktionsnahen Mechaniken

Die falsche Einordnung ist:

- produktionsreifes Vollprodukt
- zertifizierungsfähiges ISMS-Tool
