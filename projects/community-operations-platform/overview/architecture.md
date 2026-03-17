# Architecture

The original system keeps Discord handlers thin and pushes stateful logic into services.

The dependency path is straightforward:

`Discord commands -> services -> repositories -> PostgreSQL`

The extract focuses on the parts that carry the most implementation value.

## Startup and wiring

- shared dependencies are created once during startup
- repositories are grouped behind a single application state object
- services depend on repositories, not on Discord handlers
- command modules read from the application state instead of constructing ad-hoc clients

## Runtime governance

- role checks live in one place instead of being repeated across commands
- read-only mode and feature flags live in runtime config because they are governance, not deploy-time config
- owner and admin overrides are handled explicitly to avoid bootstrap lockout during setup

## Persistence

- migrations are plain SQL files
- applied migrations are tracked with checksums
- checksum drift is treated as a hard stop
- runtime schema checks exist so long-running bot processes can surface drift early

## Background processing

- reminder dispatch and scheduled embeds use claim fields in the database
- the worker claims jobs before sending side effects
- stale claims can be recovered by another instance
- this keeps duplicate sends from becoming the default failure mode

## Monitoring

- health checks cover DB connectivity and schema compatibility
- critical runtime failures can be forwarded into the platform itself
- audit logging exists as a separate concern, not as scattered log lines
