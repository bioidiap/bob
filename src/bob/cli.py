"""Sets up the click plugin interface for packages to plug into."""

import click

from importlib.metadata import entry_points

import clapper.logging

from bob.click_helper import AliasedGroup
from click_plugins import with_plugins

logger = clapper.logging.setup("bob")


@with_plugins(entry_points(group="bob.cli"))
@click.group(
    cls=AliasedGroup,
    context_settings={"help_option_names": ("-?", "-h", "--help")},
)
def bob():
    """The main command line interface for bob."""
    pass
