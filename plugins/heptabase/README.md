# Heptabase

Connect AI agents such as Claude to your [Heptabase](https://heptabase.com) knowledge base, and turn your material into explainer videos with Heptabase Explainer Studio.

## Heptabase MCP

This plugin adds Heptabase's hosted MCP server to your agent. You need a Heptabase account. You sign in to Heptabase in your browser and approve access. The connection does not require a local server, API key, or separate Heptabase CLI.

- Search and read cards, journals, PDFs, tags, databases, and whiteboards
- Create and edit notes
- Update properties
- Place existing objects on whiteboards
- View selected cards in an interactive reader, in clients that support MCP Apps

The tools your agent can use depend on the access you grant when you authorize. A read-only connection cannot change your notes.

## Explainer Studio

The `explainer-studio` skill turns teaching material (lecture notes, a book chapter, a paper, a design document, or a codebase) into a series of narrated, animated explainer videos, each answering one question. Ask your agent: "Make an explainer video from `<your file>`".

The videos are made on your computer, so the skill works in agents that can run commands there, such as Claude Code and Codex. You need no Heptabase account. Details are in the [Explainer Studio repository](https://github.com/heptameta/heptabase-explainer-studio).

## What the plugin runs and sends

The plugin contains no hooks, commands, or local server. It registers one remote MCP server, `https://api.heptabase.com/mcp`, and your agent sends its Heptabase tool requests there. Sign-in uses the standard OAuth flow in your browser. The plugin does not store a token or API key in its files. Content that your agent reads from Heptabase becomes part of your conversation with that AI client.

The Explainer Studio skill contains an install script for macOS and Linux and one for Windows. The first time you ask for a video, your agent asks before it runs one. The script installs the `explainer-studio` command and the tools it needs (about 1.5 GB) in your home folder, without an administrator password. Your sources and videos stay on your computer. What leaves it, such as narration text sent to the provider you choose or feedback you agree to share, is listed in [Explainer Studio's privacy notes](https://github.com/heptameta/heptabase-explainer-studio/blob/main/PRIVACY.md).

## Install

Steps for Claude Code, Codex, and Cursor are in the [repository README](https://github.com/heptameta/heptabase-agent-plugins#install).

## Support and policies

- [How to use Heptabase MCP](https://support.heptabase.com/en/articles/12679581-heptabase-mcp)
- [Explainer Studio issues](https://github.com/heptameta/heptabase-explainer-studio/issues)
- [Heptabase Support](https://support.heptabase.com)
- [Privacy Policy](https://heptabase.com/privacy_policy)
- [Terms of Service](https://heptabase.com/terms_of_service)

## License

[MIT](LICENSE)
