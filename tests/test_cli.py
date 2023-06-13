"""Tests the command groups are functional.

NOTE: The command names displayed here are not the same as the entry-point names
"""

from textwrap import dedent

from click.testing import CliRunner

from bob.cli import bob_config, bob_main_cli


def test_cli_main():
    """Ensure the main CLI group exists."""
    runner = CliRunner()
    result = runner.invoke(bob_main_cli)
    assert result.exit_code == 0
    assert result.output.startswith(  # Match the start as plugins can change
        dedent(
            """\
            Usage: bob-main-cli [OPTIONS] COMMAND [ARGS]...

              The main command line interface for bob.

            Options:
              -h, --help  Show this message and exit.

            Commands:
            """
        )
    )


def test_cli_config_group():
    """Ensure the config group works."""
    runner = CliRunner()
    result = runner.invoke(bob_config)
    assert result.exit_code == 0
    assert result.output.startswith(
        dedent(
            """\
            Usage: bob-config [OPTIONS] COMMAND [ARGS]...

              Allows reading and writing into the user configuration.

            Options:
              -v, --verbose  Increase the verbosity level from 0 (only error and critical)
                             messages will be displayed, to 1 (like 0, but adds warnings), 2
                             (like 1, but adds info messags), and 3 (like 2, but also adds
                             debugging messages) by adding the --verbose option as often as
                             desired (e.g. '-vvv' for debug).  [default: 0; 0<=x<=3]
              -h, --help     Show this message and exit.

            Commands:
            """
        )
    )
