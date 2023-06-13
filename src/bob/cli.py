"""Sets up the click plugin group for packages to plug into."""

from importlib.metadata import entry_points

import clapper.logging
import click

from clapper.click import AliasedGroup, user_defaults_group
from clapper.rc import UserDefaults
from click_plugins import with_plugins

logger = clapper.logging.setup("bob")


# Create the main CLI group: bob
@with_plugins(entry_points(group="bob.cli"))
@click.group(
    cls=AliasedGroup,
    context_settings={"help_option_names": ("-h", "--help")},
)
def bob_main_cli():
    """The main command line interface for bob."""
    # An entry-point `bob` is created at the package level (pyproject.toml)
    # pointing here.
    #
    # Packages that want to insert their sub-commands in `bob` have to register
    # a unique entry-point in the `bob.cli` group in their pyproject.toml:
    #   [project.entry-points."bob.cli"]
    #       custom = "bob.custom.cli:custom_command"
    # (and install with `pip install -e package_location`)
    #
    # Then, calling `bob custom` will call the `custom_command` function.
    pass


# Create the only default sub-command: config
@user_defaults_group(
    logger=logger, config=UserDefaults("bobrc.toml", logger=logger)
)
def bob_config(**kwargs):
    "Allows reading and writing into the user configuration."
    pass


bob_main_cli.add_command(bob_config, "config")
