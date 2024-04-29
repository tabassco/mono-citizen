from __future__ import annotations

import datetime
import tomllib

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Version:
    major: int
    minor: int
    patch: int
    rc: bool = False

    @classmethod
    def from_string(cls, version: str) -> Version:
        is_rc = "rc" in version
        version, *_ = version.split("rc")
        major, minor, patch, *_ = version.rstrip("._-").split(".")

        return Version(int(major), int(minor), int(patch), is_rc)

    def new_patch(self) -> Version:
        return Version(self.major, self.minor, self.patch + 1)

    def new_minor(self) -> Version:
        return Version(self.major, self.minor + 1, 0)

    def new_major(self) -> Version:
        return Version(self.major + 1, 0, 0)

    def __str__(self) -> str:
        version_string = f"{self.major}.{self.minor}.{self.patch}"
        if self.rc:
            version_string = (
                f"{version_string}-.{datetime.datetime.now(datetime.UTC).isoformat()}"
            )
        return version_string


def get_current_version(path: str) -> Version:
    proj_path = Path(path) / "pyproject.toml"

    with open(proj_path, "rb") as f:
        data = tomllib.load(f)

    current_version = data.get("project").get("version")

    return Version.from_string(current_version)


def update_to_new_version(path: str, new_version: Version) -> None: ...
