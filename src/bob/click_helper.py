import logging
import textwrap
import time
import traceback

import click

from clapper.config import load, mod_to_context, resource_keys
from click.core import ParameterSource


logger = logging.getLogger(__name__)


def bool_option(name, short_name, desc, dflt=False, **kwargs):
    """Generic provider for boolean options

    Parameters
    ----------
    name : str
        name of the option
    short_name : str
        short name for the option
    desc : str
        short description for the option
    dflt : bool or None
        Default value
    **kwargs
        All kwargs are passed to click.option.

    Returns
    -------
    ``callable``
        A decorator to be used for adding this option.
    """

    def custom_bool_option(func):
        def callback(ctx, param, value):
            ctx.meta[name.replace("-", "_")] = value
            return value

        return click.option(
            "-%s/-n%s" % (short_name, short_name),
            "--%s/--no-%s" % (name, name),
            default=dflt,
            help=desc,
            show_default=True,
            callback=callback,
            is_eager=True,
            **kwargs,
        )(func)

    return custom_bool_option


def list_float_option(name, short_name, desc, nitems=None, dflt=None, **kwargs):
    """Get option to get a list of float f

    Parameters
    ----------
    name : str
        name of the option
    short_name : str
        short name for the option
    desc : str
        short description for the option
    nitems : obj:`int`, optional
        If given, the parsed list must contains this number of items.
    dflt : :any:`list`, optional
        List of default  values for axes.
    **kwargs
        All kwargs are passed to click.option.

    Returns
    -------
    ``callable``
        A decorator to be used for adding this option.
    """

    def custom_list_float_option(func):
        def callback(ctx, param, value):
            if value is None or not value.replace(" ", ""):
                value = None
            elif value is not None:
                tmp = value.split(",")
                if nitems is not None and len(tmp) != nitems:
                    raise click.BadParameter(
                        "%s Must provide %d axis limits" % (name, nitems)
                    )
                try:
                    value = [float(i) for i in tmp]
                except Exception:
                    raise click.BadParameter("Inputs of %s be floats" % name)
            ctx.meta[name.replace("-", "_")] = value
            return value

        return click.option(
            "-" + short_name,
            "--" + name,
            default=dflt,
            show_default=True,
            help=desc + " Provide just a space (' ') to cancel default values.",
            callback=callback,
            **kwargs,
        )(func)

    return custom_list_float_option


def open_file_mode_option(**kwargs):
    """Get open mode file option

    Parameters
    ----------
    **kwargs
        All kwargs are passed to click.option.

    Returns
    -------
    ``callable``
        A decorator to be used for adding this option.
    """

    def custom_open_file_mode_option(func):
        def callback(ctx, param, value):
            if value not in ["w", "a", "w+", "a+"]:
                raise click.BadParameter("Incorrect open file mode")
            ctx.meta["open_mode"] = value
            return value

        return click.option(
            "-om",
            "--open-mode",
            default="w",
            help="File open mode",
            callback=callback,
            **kwargs,
        )(func)

    return custom_open_file_mode_option


def _prepare_entry_points(entry_point_group):
    if not entry_point_group:
        return ""
    ret = ""
    for prj_name, prj_entry_points in resource_keys(
        entry_point_group, with_project_names=True
    ).items():
        ret += f"\n\n**{prj_name}** entry points are: "
        ret += ", ".join(prj_entry_points)

    # wrap ret to 80 chars
    ret = "\n".join(
        textwrap.wrap(ret, 80, break_on_hyphens=False, replace_whitespace=False)
    )
    return ret


class ConfigCommand(click.Command):
    """A click.Command that can take options both form command line options and
    configuration files. In order to use this class, you **have to** use the
    :any:`ResourceOption` class also.

    Attributes
    ----------
    config_argument_name : str
      The name of the config argument.
    entry_point_group : str
      The name of entry point that will be used to load the config files.
    """

    def __init__(
        self, name, *args, help=None, entry_point_group=None, **kwargs
    ):
        self.entry_point_group = entry_point_group
        configs_argument_name = "CONFIG"
        # Augment help for the config file argument
        self.extra_help = """\n\nIt is possible to pass one or several Python files
(or names of ``{entry_point_group}`` entry points or module names i.e. import
paths) as {CONFIG} arguments to this command line which contain the parameters
listed below as Python variables. Available entry points are: {entry_points}
\nThe options through the command-line (see below) will
override the values of argument provided configuration files. You can run this
command with ``<COMMAND> -H example_config.py`` to create a template config
file.""".format(
            CONFIG=configs_argument_name,
            entry_point_group=entry_point_group,
            entry_points=_prepare_entry_points(entry_point_group),
        )
        help = (help or "").rstrip() + self.extra_help
        super().__init__(name, *args, help=help, **kwargs)

        # Add the config argument to the command
        def configs_argument_callback(ctx, param, value):
            config_context = load(
                value, entry_point_group=self.entry_point_group
            )
            config_context = mod_to_context(config_context)
            ctx.config_context = config_context
            logger.debug("Augmenting context with config context")
            return value

        click.argument(
            configs_argument_name,
            nargs=-1,
            callback=configs_argument_callback,
            is_eager=True,
        )(self)

        # Option for config file generation
        click.option(
            "-H",
            "--dump-config",
            type=click.File(mode="wt"),
            help="Name of the config file to be generated",
            is_eager=True,
            callback=self.dump_config,
        )(self)

    def dump_config(self, ctx, param, value):
        """Generate configuration file from parameters and context

        Parameters
        ----------
        ctx : object
            Click context
        """
        config_file = value
        if config_file is None:
            return
        logger.debug("Generating configuration file `%s'...", config_file)
        config_file.write("'''")
        config_file.write(
            "Configuration file automatically generated at "
            "%s\n%s\n" % (time.strftime("%d/%m/%Y"), ctx.command_path)
        )

        if self.help:
            h = self.help.replace("\b\n", "")
            config_file.write("\n{}".format(h.rstrip()))

        if self.epilog:
            config_file.write("\n\n{}".format(self.epilog.replace("\b\n", "")))

        config_file.write("'''\n")

        for param in self.params:
            if not isinstance(param, ResourceOption):
                continue

            config_file.write(
                "\n# %s = %s\n" % (param.name, str(param.default))
            )
            config_file.write("'''")

            if param.required:
                begin, dflt = "Required parameter", ""
            else:
                begin, dflt = (
                    "Optional parameter",
                    " [default: {}]".format(param.default),
                )
            config_file.write(
                "%s: %s (%s)%s"
                % (begin, param.name, ", ".join(param.opts), dflt)
            )

            if param.help is not None:
                config_file.write(
                    "\n%s"
                    % "\n".join(
                        textwrap.wrap(
                            param.help,
                            80,
                            break_on_hyphens=False,
                            replace_whitespace=False,
                        )
                    )
                )

            config_file.write("'''\n")
        click.echo(
            "Configuration file '{}' was written; exiting".format(
                config_file.name
            )
        )

        config_file.close()
        ctx.exit()


class CustomParamType(click.ParamType):
    name = "custom"


class ResourceOption(click.Option):
    """An extended click.Option that automatically loads resources from config
    files.

    This class comes with two different functionalities that are independent and
    could be combined:

    1. If used in commands that are inherited from :any:`ConfigCommand`, it will
       lookup inside the config files (that are provided as argument to the
       command) to resolve its value. Values given explicitly in the command
       line take precedence.

    2. If `entry_point_group` is provided, it will treat values given to it (by
       any means) as resources to be loaded. Loading is done using :any:`load`.
       See :ref:`bob.extension.config.resource` for more information. The final
       value cannot be a string.

    You may use this class in three ways:

    1. Using this class (without using :any:`ConfigCommand`) AND (providing
       `entry_point_group`).
    2. Using this class (with :any:`ConfigCommand`) AND (providing
       `entry_point_group`).
    3. Using this class (with :any:`ConfigCommand`) AND (without providing
       `entry_point_group`).

    Using this class without :any:`ConfigCommand` and without providing
    `entry_point_group` does nothing and is not allowed.

    Attributes
    ----------
    entry_point_group : str or None
        If provided, the strings values to this option are assumed to be entry
        points from ``entry_point_group`` that need to be loaded.
    string_exceptions : tuple or None
        If provided and ``entry_point_group`` is provided, the code will not
        treat strings in ``string_exceptions`` as entry points and does not try
        to load them.
    """

    def __init__(
        self,
        param_decls=None,
        show_default=False,
        prompt=False,
        confirmation_prompt=False,
        hide_input=False,
        is_flag=None,
        flag_value=None,
        multiple=False,
        count=False,
        allow_from_autoenv=True,
        type=None,
        help=None,
        entry_point_group=None,
        required=False,
        string_exceptions=None,
        **kwargs,
    ):
        # if no type, default, count, or is_flag is given, do not convert values to strings
        if (
            (type is None)
            and (kwargs.get("default") is None)
            and (count is False)
            and (is_flag is None)
        ):
            type = CustomParamType()

        self.entry_point_group = entry_point_group
        if entry_point_group is not None:
            name, _, _ = self._parse_decls(
                param_decls, kwargs.get("expose_value")
            )
            help = help or ""
            help += (
                " Can be a ``{entry_point_group}`` entry point, a module name, or "
                "a path to a Python file which contains a variable named `{name}`. "
                "Available entry points are: {entry_points}"
            )
            help = help.format(
                entry_point_group=entry_point_group,
                entry_points=_prepare_entry_points(entry_point_group),
                name=name,
            )
        super().__init__(
            param_decls=param_decls,
            show_default=show_default,
            prompt=prompt,
            confirmation_prompt=confirmation_prompt,
            hide_input=hide_input,
            is_flag=is_flag,
            flag_value=flag_value,
            multiple=multiple,
            count=count,
            allow_from_autoenv=allow_from_autoenv,
            type=type,
            help=help,
            required=required,
            **kwargs,
        )
        self.string_exceptions = string_exceptions or []

    def consume_value(self, ctx, opts):
        if (
            not hasattr(ctx, "config_context")
        ) and self.entry_point_group is None:
            raise TypeError(
                "The ResourceOption class is not meant to be used this way. "
                "Please see the docs of the class."
            )
        logger.debug("consuming resource option for %s", self.name)
        value = opts.get(self.name)

        source = ParameterSource.COMMANDLINE

        # if value is not given from command line, lookup the config files given as
        # arguments (not options).
        if value is None:
            # if this class is used with the ConfigCommand class. This is not always
            # true.
            if hasattr(ctx, "config_context"):
                value = ctx.config_context.get(self.name)

        # if not from config files, lookup the environment variables
        if value is None:
            value = self.value_from_envvar(ctx)
            source = ParameterSource.ENVIRONMENT

        # if not from environment variables, lookup the default value
        if value is None:
            value = ctx.lookup_default(self.name)
            source = ParameterSource.DEFAULT_MAP

        if value is None:
            value = self.get_default(ctx)
            source = ParameterSource.DEFAULT

        return value, source

    def type_cast_value(self, ctx, value):
        """Convert and validate a value against the option's
        ``type``, ``multiple``, and ``nargs``.
        Furthermore, if the an entry_point_group is provided, it will load it.
        """
        value = super().type_cast_value(ctx, value)

        # if the value is a string and an entry_point_group is provided, load it
        if self.entry_point_group is not None:
            while (
                isinstance(value, str) and value not in self.string_exceptions
            ):
                value = load(
                    [value],
                    entry_point_group=self.entry_point_group,
                    attribute_name=self.name,
                )

        return value


class AliasedGroup(click.Group):
    """Class that handles prefix aliasing for commands

    Basically just implements get_command that is used by click to choose the
    command based on the name.

    Example
    -------
    To enable prefix aliasing of commands for a given group,
    just set ``cls=AliasedGroup`` parameter in click.group decorator.
    """

    def get_command(self, ctx, cmd_name):
        """get_command with prefix aliasing"""
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail("Too many matches: %s" % ", ".join(sorted(matches)))


def log_parameters(logger_handle, ignore=tuple()):
    """Logs the click parameters with the logging module.

    Parameters
    ----------
    logger_handle : object
        The logger handle to write debug information into.
    ignore : tuple
        The keys in ignore will not be logged.
    """
    ctx = click.get_current_context()
    # do not sort the ctx.params dict. The insertion order is kept in Python 3
    # and is useful (but not necessary so works on Python 2 too).
    for k, v in ctx.params.items():
        if k in ignore:
            continue
        logger_handle.debug("%s: %s", k, v)


def assert_click_runner_result(result, exit_code=0, exception_type=None):
    """Helper for asserting click runner results"""
    m = (
        "Click command exited with code `{}' and exception:\n{}"
        "\nThe output was:\n{}"
    )
    exception = (
        "None"
        if result.exc_info is None
        else "".join(traceback.format_exception(*result.exc_info))
    )
    m = m.format(result.exit_code, exception, result.output)
    assert result.exit_code == exit_code, m
    if exit_code == 0:
        assert not result.exception, m
    if exception_type is not None:
        assert isinstance(result.exception, exception_type), m
