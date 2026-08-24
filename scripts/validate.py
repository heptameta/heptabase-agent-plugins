#!/usr/bin/env python3

import json
import re
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "heptabase"
PLUGIN_NAME = "heptabase"
MCP_URL = "https://api.heptabase.com/mcp"
AGENT_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
AGENT_PLUGIN_MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"

PLUGIN_MANIFEST_PATHS = (
    PLUGIN_ROOT / "plugin.json",
    PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
    PLUGIN_ROOT / ".claude-plugin" / "plugin.json",
)
MARKETPLACE_PATHS = (
    REPOSITORY_ROOT / ".agents" / "plugins" / "marketplace.json",
    REPOSITORY_ROOT / ".claude-plugin" / "marketplace.json",
    REPOSITORY_ROOT / ".cursor-plugin" / "marketplace.json",
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(REPOSITORY_ROOT)} must contain an object")
    return value


def validate_manifest_identity() -> None:
    manifests = [load_json(path) for path in PLUGIN_MANIFEST_PATHS]
    names = {manifest.get("name") for manifest in manifests}
    versions = {manifest.get("version") for manifest in manifests}

    if names != {PLUGIN_NAME}:
        raise ValueError(f"plugin manifests disagree on name: {sorted(names)}")
    if len(versions) != 1:
        raise ValueError(f"plugin manifests disagree on version: {sorted(versions)}")

    version = next(iter(versions))
    if not isinstance(version, str) or re.fullmatch(r"\d+\.\d+\.\d+", version) is None:
        raise ValueError(f"plugin version is not strict semver: {version}")


def validate_marketplaces() -> None:
    for path in MARKETPLACE_PATHS:
        marketplace = load_json(path)
        entries = marketplace.get("plugins")
        if not isinstance(entries, list):
            raise ValueError(f"{path.relative_to(REPOSITORY_ROOT)} must contain plugins")

        entry = next(
            (candidate for candidate in entries if candidate.get("name") == PLUGIN_NAME),
            None,
        )
        if entry is None:
            raise ValueError(f"{path.relative_to(REPOSITORY_ROOT)} is missing Heptabase")

        source = entry.get("source")
        source_path = source.get("path") if isinstance(source, dict) else source
        if source_path != "./plugins/heptabase":
            raise ValueError(
                f"{path.relative_to(REPOSITORY_ROOT)} has unexpected source {source_path}"
            )


def validate_portable_manifest() -> None:
    manifest = load_json(PLUGIN_ROOT / "plugin.json")
    if manifest.get("$schema") != AGENT_PLUGIN_SCHEMA:
        raise ValueError("plugin.json must target Agent Plugins 1.0.0")


def validate_mcp() -> None:
    native_manifest = load_json(PLUGIN_ROOT / ".mcp.json")
    native_servers = native_manifest.get("mcpServers")
    native_heptabase = (
        native_servers.get(PLUGIN_NAME) if isinstance(native_servers, dict) else None
    )
    if (
        not isinstance(native_heptabase, dict)
        or native_heptabase.get("type") != "http"
        or native_heptabase.get("url") != MCP_URL
    ):
        raise ValueError(f".mcp.json must configure {MCP_URL} as HTTP")

    portable_manifest = load_json(PLUGIN_ROOT / "mcp.json")
    if portable_manifest.get("$schema") != AGENT_PLUGIN_MCP_SCHEMA:
        raise ValueError("mcp.json must target Agent Plugins 1.0.0")

    portable_servers = portable_manifest.get("mcpServers")
    portable_heptabase = (
        portable_servers.get(PLUGIN_NAME)
        if isinstance(portable_servers, dict)
        else None
    )
    if (
        not isinstance(portable_heptabase, dict)
        or portable_heptabase.get("type") != "streamable-http"
        or portable_heptabase.get("url") != MCP_URL
    ):
        raise ValueError(f"mcp.json must configure {MCP_URL} as Streamable HTTP")


def validate_codex_assets() -> None:
    manifest = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        raise ValueError("Codex plugin manifest is missing interface metadata")

    for field in ("composerIcon", "logo"):
        value = interface.get(field)
        if not isinstance(value, str) or not value.startswith("./"):
            raise ValueError(f"Codex interface.{field} must be a relative path")
        if not (PLUGIN_ROOT / value).is_file():
            raise ValueError(f"Codex interface.{field} does not exist: {value}")


def validate_no_placeholders() -> None:
    placeholder_marker = "[" + "TODO:"
    for path in REPOSITORY_ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            contents = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if placeholder_marker in contents:
            raise ValueError(f"placeholder remains in {path.relative_to(REPOSITORY_ROOT)}")


def main() -> None:
    validate_manifest_identity()
    validate_marketplaces()
    validate_portable_manifest()
    validate_mcp()
    validate_codex_assets()
    validate_no_placeholders()
    print("Plugin package validation passed.")


if __name__ == "__main__":
    main()
