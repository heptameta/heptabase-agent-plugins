# Repository guidance

This public repository distributes official Heptabase agent plugins. Keep every committed file safe for public release. Never add credentials, private submission artifacts, customer data, or internal-only documentation.

The canonical plugin payload is `plugins/heptabase/`. Its root `plugin.json`, `mcp.json`, and future `skills/` follow the Agent Plugins specification. Keep the Codex and Claude Code manifests aligned with the portable manifest on plugin identity and version. Keep the endpoint in portable `mcp.json` and host-native `.mcp.json` aligned. OpenAI app registration belongs only in `.app.json`.

Skills added here must describe Heptabase workflows and concepts without assuming one agent host. Put host-specific configuration in that host's manifest instead of duplicating the skill.

Run `python3 scripts/validate.py`, `claude plugin validate --strict plugins/heptabase`, and the Codex plugin validator before shipping manifest or asset changes.
