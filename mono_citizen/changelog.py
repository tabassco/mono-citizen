from mono_citizen.git import get_commits
from mono_citizen.version import Version


class Changelog:
    def __init__(self, module_path: str) -> None:
        self.path = module_path

        self.breaking_changes: list[str] = []
        self.features: list[str] = []
        self.fixes: list[str] = []

    def load_from_commits(self, last_version_hash: str) -> None:
        commits = get_commits(self.path)

        for commit in commits:
            if commit.hash == last_version_hash:
                break
            for message_line in commit.message:
                if message_line.startswith("fix"):
                    self.fixes.append(message_line.lstrip("fix:"))

                if message_line.startswith("feat"):
                    self.features.append(message_line.lstrip("feat:"))

                if (
                    message_line.startswith("BREAKING CHANGE")
                    or "feat!" in message_line
                ):
                    self.breaking_changes.append(
                        message_line.lstrip("BREAKING CHANGE:").lstrip("feat!:")
                    )

    def construct_markdown(self, new_version: Version) -> list[str]:
        changelog_lines: list[str] = [f"# Version: {new_version}"]

        if self.breaking_changes:
            changelog_lines.append("## BREAKING CHANGES:")
            for change in self.breaking_changes:
                changelog_lines.append(f"    * {change}")

        if self.features:
            changelog_lines.append("## Features:")
            for change in self.features:
                changelog_lines.append(f"    * {change}")

        if self.fixes:
            changelog_lines.append("## Bugfixes:")
            for change in self.fixes:
                changelog_lines.append(f"    * {change}")

        return changelog_lines
