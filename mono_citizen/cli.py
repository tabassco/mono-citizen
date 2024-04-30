import rich_click as click
from mono_citizen.changelog import Changelog
from rich import print


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--prev-version", default=None, help="hash of commit of last version of the package"
)
@click.option(
    "--output-path",
    default="changelog.md",
    help="filepath to the changelog markdown file",
)
@click.argument("module-path")
def changelog(prev_version, output_path, module_path) -> None:
    cl = Changelog(module_path)
    cl.load_from_commits(prev_version)
    md_changelog = cl.construct_markdown(prev_version)  # FIXME

    with open(output_path, "a+") as modified:
        modified.writelines(md_changelog)

    print(f"Updated changelog to {output_path}")


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
