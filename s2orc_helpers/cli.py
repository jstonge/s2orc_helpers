"""Console script for s2orc_helpers."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for s2orc_helpers."""
    click.echo("Replace this message by putting your code into "
               "s2orc_helpers.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
