# Heptabase

Connect AI agents such as Claude to your [Heptabase](https://heptabase.com) knowledge base.

This plugin adds Heptabase's hosted MCP server to your agent. You need a Heptabase account. You sign in to Heptabase in your browser and approve access. The plugin does not require a local server, API key, or separate Heptabase CLI.

## What you can do

- Search and read cards, journals, PDFs, tags, databases, and whiteboards
- Create and edit notes
- Update properties
- Place existing objects on whiteboards
- View selected cards in an interactive reader, in clients that support MCP Apps

The tools your agent can use depend on the access you grant when you authorize. A read-only connection cannot change your notes.

## What the plugin runs and sends

The plugin contains no scripts, hooks, commands, or local server. It registers one remote MCP server, `https://api.heptabase.com/mcp`, and your agent sends its tool requests there.

Sign-in uses the standard OAuth flow in your browser. The plugin does not store a token or API key in its files. Content that your agent reads from Heptabase becomes part of your conversation with that AI client.

## Install

Steps for Claude Code, Codex, and Cursor are in the [repository README](https://github.com/heptameta/heptabase-agent-plugins#install).

## Support and policies

- [How to use Heptabase MCP](https://support.heptabase.com/en/articles/12679581-heptabase-mcp)
- [Heptabase Support](https://support.heptabase.com)
- [Privacy Policy](https://heptabase.com/privacy_policy)
- [Terms of Service](https://heptabase.com/terms_of_service)

## License

[MIT](LICENSE)
