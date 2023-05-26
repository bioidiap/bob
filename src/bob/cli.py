"""Sets up the click plugin group for packages to plug into."""

from importlib.metadata import entry_points

import clapper.logging
import click

from clapper.click import AliasedGroup
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
