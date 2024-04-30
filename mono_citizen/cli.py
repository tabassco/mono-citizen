import click
from mono_citizen.changelog import Changelog
from rich.pretty import pprint


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--prev-version", default=None, help="hash of commit of last version of the package"
)
@click.argument("module-path")
def changelog(prev_version, module_path) -> None:
    cl = Changelog(module_path)
    cl.load_from_commits(prev_version)
    md_changelog = cl.construct_markdown(None)  # FIXME
    pprint(md_changelog)


@cli.command()
@click.option(
    "--prev-version", default=None, help="hash of commit of last version of the package"
)
@click.argument("module-path")
def update_version(prev_version, module_path) -> None:
    cl = Changelog(module_path)
    cl.load_from_commits(prev_version)


if __name__ == "__main__":
    cli()
