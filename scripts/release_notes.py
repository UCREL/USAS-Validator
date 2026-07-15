# /// script
# requires-python = ">=3.10, <3.15"
# ///

"""Prepares markdown release notes for GitHub releases.

Reference: adapted from PyMUSAS's release_notes.py script:
https://github.com/UCREL/pymusas/blob/main/scripts/release_notes.py
"""

import os

import usas_validator

TAG = os.environ["TAG"]

ADDED_HEADER = "### Added 🎉"
CHANGED_HEADER = "### Changed ⚠️"
FIXED_HEADER = "### Fixed ✅"
REMOVED_HEADER = "### Removed 🗑"
DEPRECATED_HEADER = "### Deprecated 👋"
SECURITY_HEADER = "### Security 🔒"


def get_change_log_notes() -> str:
    """Extracts the `TAG` release's section from `CHANGELOG.md`.

    Returns:
        The `TAG` release's changelog entries, formatted as markdown
        with emoji section headers.
    """
    in_current_section = False
    current_section_notes: list[str] = []

    with open("CHANGELOG.md") as changelog:
        for line in changelog:
            if line.startswith("## "):
                if line.startswith("## Unreleased"):
                    continue
                if line.startswith(f"## [{TAG}]"):
                    in_current_section = True
                    continue
                break

            if in_current_section:
                match line:
                    case _ if line.startswith("### Added"):
                        line = ADDED_HEADER + "\n"
                    case _ if line.startswith("### Changed"):
                        line = CHANGED_HEADER + "\n"
                    case _ if line.startswith("### Fixed"):
                        line = FIXED_HEADER + "\n"
                    case _ if line.startswith("### Removed"):
                        line = REMOVED_HEADER + "\n"
                    case _ if line.startswith("### Deprecated"):
                        line = DEPRECATED_HEADER + "\n"
                    case _ if line.startswith("### Security"):
                        line = SECURITY_HEADER + "\n"

                current_section_notes.append(line)

    assert current_section_notes
    return "## What's new\n\n" + "".join(current_section_notes).strip() + "\n"


def get_commit_history() -> str:
    """Builds a `## Commits` section listing commits in the `TAG` release.

    Returns:
        A markdown section listing, as a `git log --oneline`, every
        commit between the previous tag and the `TAG` release.
    """
    stream = os.popen(
        f"git log $(git describe --always --tags --abbrev=0 {TAG}^^)..{TAG}^ --oneline"
    )
    commit_history = "## Commits\n\n" + stream.read()
    stream.close()
    return commit_history


def main() -> None:
    """Prints the `TAG` release's changelog notes and commit history."""
    if TAG != f"v{usas_validator.__version__}":
        raise ValueError(
            f"The environment variable `TAG` `{TAG}` "
            f"is not the same as `v{usas_validator.__version__}` "
            "which it should be."
        )

    print(get_change_log_notes())
    print(get_commit_history())


if __name__ == "__main__":
    main()
