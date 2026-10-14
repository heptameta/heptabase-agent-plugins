#!/usr/bin/env python3
"""Build the ZIP to upload to the OpenAI plugin directory.

    python3 scripts/package_openai_plugin.py              # the current commit
    python3 scripts/package_openai_plugin.py --ref main --release-notes notes.md

The ZIP holds the plugin folder as committed at the ref, with two changes that the directory requires:

- no OpenAI app registration (`.app.json` and the Codex manifest's `apps` field that points to it), because the
  directory does not accept a package that declares one;
- the plugin name that the directory gave the Heptabase plugin, in place of `heptabase`, because an upload must
  match the existing plugin.

`--release-notes` adds the text of a file as the version's release notes, which the reviewers read. The submission
form has no other place for a note to them, such as why a finding of the automated checks is expected. The notes
belong to one version, so they are not committed.

It is written to dist/heptabase-<version>-openai.zip.
"""

from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = "plugins/heptabase"
OPENAI_PLUGIN_NAME = "app-6a8df1b568f08191af42b4e26e012044"
APP_REGISTRATION_PATH = ".app.json"
CODEX_MANIFEST_PATH = ".codex-plugin/plugin.json"
MANIFEST_PATHS = ("plugin.json", CODEX_MANIFEST_PATH, ".claude-plugin/plugin.json")
OUTPUT_DIR = REPOSITORY_ROOT / "dist"
REGULAR_FILE_TYPE = 0o100000


def read_plugin_files(ref: str) -> dict[str, tuple[bytes, int]]:
    """The plugin folder's files at `ref`: content and file mode by path inside the folder."""
    completed = subprocess.run(
        ["git", "-C", str(REPOSITORY_ROOT), "archive", "--format=tar", ref, PLUGIN_DIR],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise ValueError(f"git cannot archive {ref}: {completed.stderr.decode().strip()}")

    files = {}
    with tarfile.open(fileobj=io.BytesIO(completed.stdout)) as tar:
        for member in tar.getmembers():
            if member.isfile():
                path = member.name.removeprefix(f"{PLUGIN_DIR}/")
                files[path] = (tar.extractfile(member).read(), member.mode)
    return files


def convert_to_openai_package(files: dict[str, tuple[bytes, int]], release_notes: str | None) -> None:
    files.pop(APP_REGISTRATION_PATH, None)
    for path in MANIFEST_PATHS:
        content, mode = files[path]
        manifest = json.loads(content)
        manifest["name"] = OPENAI_PLUGIN_NAME
        manifest.pop("apps", None)
        if path == CODEX_MANIFEST_PATH and release_notes is not None:
            # OpenAI reads its settings from the Codex manifest when the portable manifest has none
            openai_settings = manifest.setdefault("extensions", {}).setdefault("com.openai", {})
            openai_settings.setdefault("publication", {})["release_notes"] = release_notes
        files[path] = ((json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode(), mode)


def write_zip(files: dict[str, tuple[bytes, int]], zip_path: Path) -> None:
    """Write the files at the root of the ZIP with a fixed date, so a commit always gives the same ZIP."""
    zip_path.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(zip_path, "w") as archive:
        for path in sorted(files):
            content, mode = files[path]
            info = zipfile.ZipInfo(path)
            info.external_attr = (REGULAR_FILE_TYPE | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ref", default="HEAD", help="the commit, branch or tag to package (default: HEAD)")
    parser.add_argument("--release-notes", type=Path, help="a text file with this version's release notes")
    arguments = parser.parse_args()
    try:
        files = read_plugin_files(arguments.ref)
        release_notes = arguments.release_notes.read_text(encoding="utf-8").strip() if arguments.release_notes else None
        convert_to_openai_package(files, release_notes)
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)

    version = json.loads(files["plugin.json"][0])["version"]
    zip_path = OUTPUT_DIR / f"heptabase-{version}-openai.zip"
    write_zip(files, zip_path)
    print(f"Wrote {zip_path.relative_to(REPOSITORY_ROOT)} ({len(files)} files) from {arguments.ref}")


if __name__ == "__main__":
    main()
