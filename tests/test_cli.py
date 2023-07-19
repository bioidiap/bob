"""Tests the command groups are functional.

NOTE: The command names displayed here are not the same as the entry-point names
"""

from pathlib import Path
from textwrap import dedent

from click.testing import CliRunner

from bob.cli import bob_config, bob_main_cli, legacy_rc_checker


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


def test_cli_legacy_rc(monkeypatch):
    """Test the relocation of a legacy bobrc."""
    runner = CliRunner()
    with runner.isolated_filesystem() as tmp_dir:
        temp_dir = Path(tmp_dir)
        config_home = temp_dir / ".config"
        config_home.mkdir()
        assert not (config_home / "bobrc.toml").is_file()
        with open(temp_dir / ".bobrc", "w") as legacy_f:
            legacy_f.write(
                """{"test.section": "value", "test.part": "value"}"""
            )

        monkeypatch.setenv("XDG_CONFIG_HOME", config_home.as_posix())

        @legacy_rc_checker
        def dummy():
            pass

        dummy()

        assert (temp_dir / ".bobrc").is_file()
        assert (config_home / "bobrc.toml").is_file()


def test_cli_legacy_both_rc(monkeypatch):
    """Test when both a legacy and a new bobrc are present."""
    runner = CliRunner()
    dummy_toml_content = dedent(
        """\
        [section]
        key = "value"
        """
    )
    with runner.isolated_filesystem() as tmp_dir:
        temp_dir = Path(tmp_dir)
        config_home = temp_dir / ".config"
        config_home.mkdir()
        with open(temp_dir / ".bobrc", "w") as legacy_f:
            legacy_f.write(
                """{"test.section": "value", "test.part": "value"}"""
            )
        with open(config_home / "bobrc.toml", "w") as new_f:
            new_f.write(dummy_toml_content)

        monkeypatch.setenv("XDG_CONFIG_HOME", config_home.as_posix())

        @legacy_rc_checker
        def dummy():
            pass

        dummy()

        assert (temp_dir / ".bobrc").is_file()
        assert (config_home / "bobrc.toml").is_file()
        with open(config_home / "bobrc.toml", "r") as new_f:
            assert new_f.read() == dummy_toml_content


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
