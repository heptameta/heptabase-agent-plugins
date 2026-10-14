# Heptabase Agent Plugins

Official agent plugins for connecting AI agents to [Heptabase](https://heptabase.com).

The repository packages one portable Heptabase integration with the small host-specific adapters required for distribution. The plugin connects to Heptabase's hosted MCP server and authenticates through the standard OAuth flow; that connection does not require a local server, API key, or separate Heptabase CLI. It also carries the Explainer Studio skill, which makes explainer videos on your computer and needs no Heptabase account.

## What the plugin can do

- Search and read cards, journals, PDFs, tags, databases, and whiteboards
- Create and edit notes
- Update properties
- Place existing objects on whiteboards
- Turn teaching material into narrated, animated explainer videos with [Heptabase Explainer Studio](https://github.com/heptameta/heptabase-explainer-studio)

The exact tools available to an agent are provided by the hosted MCP server at `https://api.heptabase.com/mcp`.

## Install

### Codex

Add this repository as a marketplace:

```bash
codex plugin marketplace add heptameta/heptabase-agent-plugins
```

Then open `/plugins` and install `heptabase` from the `heptabase-agent-plugins` marketplace. The first time your agent uses Heptabase, a browser window opens for sign-in and authorization.

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
plugins/heptabase/skills/           Skills, including Explainer Studio
plugins/heptabase/README.md         Plugin description for users and listings
plugins/heptabase/LICENSE           MIT license shipped with the plugin
plugins/heptabase/.codex-plugin/    Codex-specific manifest
plugins/heptabase/.claude-plugin/   Claude Code-specific manifest and listing fields
```

The portable core contains only the shared plugin identity, MCP connection, and skills. Host-specific manifests add distribution metadata that is not part of the Agent Plugins standard. OpenAI's app registration is declared separately in `.app.json`; other hosts ignore it.

The plugin folder ships its own `README.md` and `LICENSE`, because hosts install only that folder.

## Releases

The plugin package uses Semantic Versioning. Keep the version in `plugin.json`, `.codex-plugin/plugin.json`, and `.claude-plugin/plugin.json` identical for every release:

- Patch for backward-compatible fixes or skill refinements
- Minor for backward-compatible skills, tools, or workflows
- Major for changes that require users or existing skills to migrate

Installed plugins are cached, so changing files on `main` without bumping the explicit version is not a release. Keep the hosted MCP server compatible with previously released plugin versions during a rollout. Public marketplace updates are reviewed and published separately by each host.

Claude's plugin directory picks up new commits on `main` by itself. The OpenAI plugin directory takes a ZIP: build it from the released commit with `python3 scripts/package_openai_plugin.py`, then upload `dist/heptabase-<version>-openai.zip` to the existing Heptabase plugin in the OpenAI Platform (**Plugins → Heptabase → Upload new version**). The script leaves out `.app.json` and the `apps` field, which the directory does not accept. The listing text, links, and icon come from `.codex-plugin/plugin.json`. Changes to the hosted MCP tools need no upload, because OpenAI scans the server.

## Development

Run the repository checks before opening a pull request:

```bash
python3 scripts/validate.py
```

The checks validate the portable and host-specific manifests, shared identity, version, and license, the license files, the plugin README, the Claude Code listing fields, marketplace paths, MCP endpoint, and referenced assets.

To try a change in Claude Code, start a session with `claude --plugin-dir plugins/heptabase`. For that session, it loads this folder in place of the installed plugin. To try the Explainer Studio skill with an unreleased `explainer-studio` command, first install that command as a dev build with `scripts/use_dev_build.py` in [heptameta/heptabase-explainer-studio](https://github.com/heptameta/heptabase-explainer-studio): the skill's `doctor` then finds it, and the install scripts do not run.

## Support and policies

- [Heptabase Support](https://support.heptabase.com)
- [Privacy Policy](https://heptabase.com/privacy_policy)
- [Terms of Service](https://heptabase.com/terms_of_service)

## License

The files in this repository are licensed under the [MIT License](LICENSE). Use of Heptabase itself is governed by the [Terms of Service](https://heptabase.com/terms_of_service).
