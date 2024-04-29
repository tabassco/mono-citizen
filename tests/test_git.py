from mono_citizen.git import Author


def test_author():
    name_string = "Author: Tim Kreitner <tim@kreitner.xyz>"
    author = Author.from_string(name_string)

    assert author.name == "Tim Kreitner"
    assert author.mail == "tim@kreitner.xyz"


def test_author_only_name():
    name_string = "Tim Kreitner <tim@kreitner.xyz>"
    author = Author.from_string(name_string)

    assert author.name == "Tim Kreitner"
    assert author.mail == "tim@kreitner.xyz"
