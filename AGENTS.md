# Repository guidance

This public repository distributes official Heptabase agent plugins. Keep every committed file safe for public release. Never add credentials, private submission artifacts, customer data, or internal-only documentation.

The canonical plugin payload is `plugins/heptabase/`. Its root `plugin.json`, `mcp.json`, and future `skills/` follow the Agent Plugins specification. Keep the Codex and Claude Code manifests aligned with the portable manifest on plugin identity and version. Keep the endpoint in portable `mcp.json` and host-native `.mcp.json` aligned. OpenAI app registration belongs only in `.app.json`.

The plugin is MIT licensed. Keep `license` set to `MIT` in all three manifests, and keep `plugins/heptabase/LICENSE` identical to the root `LICENSE`. Hosts install only `plugins/heptabase/`, so the plugin README and license must live there. Keep `plugins/heptabase/README.md` accurate about what the plugin runs and sends, and update it when adding skills, hooks, commands, or scripts. Set the Claude plugin directory listing fields (`icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl`, `termsOfServiceUrl`) only in `.claude-plugin/plugin.json`.

Skills added here must describe Heptabase workflows and concepts without assuming one agent host. Put host-specific configuration in that host's manifest instead of duplicating the skill.

Run `python3 scripts/validate.py`, `claude plugin validate --strict plugins/heptabase`, and the Codex plugin validator before shipping manifest or asset changes.
