# Project Context

The source project behind this extract was built for day-to-day community operations on Discord.

The interesting part for business-facing engineering roles is not the chat surface itself. It is the mix of runtime governance, operational safety, background processing, and persistence discipline:

- slash-command driven workflows with service boundaries
- tenant-scoped runtime configuration
- SQL-first schema evolution
- worker-style reminder delivery
- guardrails for permission drift and read-only operation
- health and failure signaling that help with ongoing support

This extract avoids copying the whole project tree. A smaller set of strong artifacts is easier to review and safer to publish.
