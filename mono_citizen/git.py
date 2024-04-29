from __future__ import annotations
import datetime
import subprocess

from dataclasses import dataclass


@dataclass
class Author:
    name: str
    mail: str

    @classmethod
    def from_string(cls, name_string: str) -> Author:
        name_string = name_string.lstrip("Author: ")
        name, mail = name_string.split("<")
        return Author(name.rstrip(" "), mail.strip("<>"))


@dataclass
class Commit:
    hash: str
    author: Author
    date: datetime.datetime
    message: list[str]

    @classmethod
    def from_dict(cls, data_dict: dict[str, str | list[str]]) -> Commit:
        return Commit(
            hash=data_dict["hash"].lstrip("commit "),
            author=Author.from_string(data_dict["author"]),
            date=datetime.datetime.strptime(
                data_dict["date"].lstrip("Date: "), "%c %z"
            ),
            message=data_dict["message"],
        )

    def __rich_repr__(self):
        yield "commit", self.hash
        yield "by", self.author
        yield "on", self.date
        yield self.message


def get_commits(path: str) -> list[Commit]:
    lines = (
        subprocess.check_output(["git", "log", "--", path], stderr=subprocess.STDOUT)
        .decode()
        .split("\n")
    )

    commits: list[Commit] = []
    commit: dict[str, str | list[str]] = {"message": []}
    for line in lines:
        if line.startswith("commit"):
            if commit.get("hash") is not None:
                commits.append(Commit.from_dict(commit))
            commit.clear()
            commit["hash"] = line
            commit["message"] = []
            continue

        if line.startswith("Merge"):
            commit.clear()
            commit["message"] = []
            continue

        if line.startswith("Author"):
            commit["author"] = line
            continue

        if line.startswith("Date"):
            commit["date"] = line
            continue

        if line != "":
            commit["message"].append(line.lstrip(" ").rstrip(" "))

    if commit.get("hash") is not None:
        commits.append(Commit.from_dict(commit))

    return commits
