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

The plugin follows the portable [Agent Plugins specification](https://agent-plugins.org/) supported by Cursor. Public marketplace installation will be documented after publication.

To preview the package from GitHub:

1. Open **Customize → Plugins → Add → From GitHub Repository**.
2. Enter `https://github.com/heptameta/heptabase-agent-plugins`, choose **User** scope, and import it.
3. Find the `heptabase` package from this repository and click **Add**. If the older CLI package is also installed, choose the entry whose description mentions the hosted MCP server.
4. Open the installed package and authenticate its Heptabase MCP connection.

The GitHub import, OAuth authorization, search, create, read, and update workflows were verified in a live Cursor session on September 25, 2026 using a disposable note.

For local development, Cursor also documents copying the package into `~/.cursor/plugins/local/heptabase/` and reloading the app. The destination must contain `plugin.json` and `mcp.json` directly, and local imports must be allowed by your team's settings. An installed marketplace plugin with the same name takes precedence. See [Cursor's local plugin instructions](https://cursor.com/docs/plugins#test-plugins-locally).

### Grok Bot

Grok Bot [supports the same MCP servers, plugins, and skills as Cursor](https://x.ai/bot/guides/grok-bot-101). After the personal Cursor import and installation above, the hosted Heptabase plugin appeared under **Marketplace → Your plugins**. Open the entry from this repository and complete its Heptabase authorization.

## Repository layout

```text
.agents/plugins/marketplace.json    Codex marketplace
.claude-plugin/marketplace.json     Claude Code marketplace
.cursor-plugin/marketplace.json     Cursor marketplace
LICENSE                             MIT license for this repository
plugins/heptabase/plugin.json       Portable Agent Plugins manifest
plugins/heptabase/mcp.json          Portable MCP configuration
plugins/heptabase/README.md         Plugin description for users and listings
plugins/heptabase/LICENSE           MIT license shipped with the plugin
plugins/heptabase/.codex-plugin/    Codex-specific manifest
plugins/heptabase/.claude-plugin/   Claude Code-specific manifest and listing fields
```

The portable core contains only the shared plugin identity, MCP connection, and future skills. Host-specific manifests add distribution metadata that is not part of the Agent Plugins standard. OpenAI's app registration is declared separately in `.app.json`; other hosts ignore it.

The plugin folder ships its own `README.md` and `LICENSE`, because hosts install only that folder.

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

The checks validate the portable and host-specific manifests, shared identity, version, and license, the license files, the plugin README, the Claude Code listing fields, marketplace paths, MCP endpoint, and referenced assets.

## Support and policies

- [Heptabase Support](https://support.heptabase.com)
- [Privacy Policy](https://heptabase.com/privacy_policy)
- [Terms of Service](https://heptabase.com/terms_of_service)

## License

The files in this repository are licensed under the [MIT License](LICENSE). Use of Heptabase itself is governed by the [Terms of Service](https://heptabase.com/terms_of_service).
