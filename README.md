# Heptabase Agent Plugins

Official agent plugins for connecting AI agents to [Heptabase](https://heptabase.com).

The repository packages one portable Heptabase integration with the small host-specific adapters required for distribution. The current plugin connects to Heptabase's hosted MCP server and authenticates through the standard OAuth flow. It does not require a local server, API key, or separate Heptabase CLI.

## What the plugin can do

- Search and read cards, journals, PDFs, tags, databases, and whiteboards
- Create and edit notes
- Update properties
- Place existing objects on whiteboards

The exact tools available to an agent are provided by the hosted MCP server at `https://api.heptabase.com/mcp`.

## Install

### Codex

Add this repository as a marketplace:

```bash
codex plugin marketplace add heptameta/heptabase-agent-plugins
```

Then open `/plugins` and install `heptabase` from the `heptabase-agent-plugins` marketplace. A browser window will open for Heptabase sign-in and authorization.

### Claude Code

Add this repository as a marketplace:

```text
/plugin marketplace add heptameta/heptabase-agent-plugins
```

Then install the plugin:

```text
/plugin install heptabase@heptabase-agent-plugins
```

### Cursor

The plugin follows the portable [Agent Plugins specification](https://agent-plugins.org/) supported by Cursor. Public installation will be documented here when the plugin is published to the Cursor Marketplace.

## Repository layout

```text
.agents/plugins/marketplace.json    Codex marketplace
.claude-plugin/marketplace.json     Claude Code marketplace
.cursor-plugin/marketplace.json     Cursor marketplace
plugins/heptabase/plugin.json       Portable Agent Plugins manifest
plugins/heptabase/mcp.json          Portable MCP configuration
plugins/heptabase/.codex-plugin/    Codex-specific manifest
plugins/heptabase/.claude-plugin/   Claude Code-specific manifest
```

The portable core contains only the shared plugin identity, MCP connection, and future skills. Host-specific manifests add distribution metadata that is not part of the Agent Plugins standard. OpenAI's app registration is declared separately in `.app.json`; other hosts ignore it.

## Releases

The plugin package uses Semantic Versioning. Keep the version in `plugin.json`, `.codex-plugin/plugin.json`, and `.claude-plugin/plugin.json` identical for every release:

- Patch for backward-compatible fixes or skill refinements
- Minor for backward-compatible skills, tools, or workflows
- Major for changes that require users or existing skills to migrate

Installed plugins are cached, so changing files on `main` without bumping the explicit version is not a release. Keep the hosted MCP server compatible with previously released plugin versions during a rollout. Public marketplace updates are reviewed and published separately by each host.

## Development

Run the repository checks before opening a pull request:

```bash
python3 scripts/validate.py
```

The checks validate the portable and host-specific manifests, shared identity and version, marketplace paths, MCP endpoint, and referenced assets.

## Support and policies

- [Heptabase Support](https://support.heptabase.com)
- [Privacy Policy](https://heptabase.com/privacy_policy)
- [Terms of Service](https://heptabase.com/terms_of_service)
