"""
echo module
===========
Package: `src`

Module to print formatted log messages.

Classes
-------
- `LogType` (enum)
Functions
---------
- `echo`
- `echoInput`
- `echoInfo`
- `echoWarning`
- `echoError`
"""


import os
import sys
import enum
import textwrap
import rich


class LogType(enum.Enum):
    """
    LogType enum
    ============
    Defines types of log messages.

    String representation: (label, output_stream)

    Attributes:
        INPUT : Input prompt messages
        INFO : Informational messages
        WARNING : Warning messages
        ERROR : Error messages
    """
    INPUT = ("[blue3]INPT[/blue3]", sys.stdout)
    INFO = ("[turquoise2]INFO[/turquoise2]", sys.stdout)
    WARNING = ("[dark_orange3]WARN[/dark_orange3]", sys.stdout)
    ERROR = ("[bold red3]EROR[/bold red3]", sys.stderr)


def __echo(
        type: LogType,
        indent: int,
        message: str,
        /,
        *,
        end: str = "\n",
        flush: bool = True,
        ) -> None:
    """
    Print a formatted log message to the console.

    Parameters:
        type (LogType) : Type of log message
        indent (int) : Indentation level
        message (str) : Log message content
        end (str) : String appended after the message
        flush (bool) : Whether to forcibly flush the stream
    """
    prefix: str = f"[{type.value[0]}] {'    ' * indent}"
    width: int = os.get_terminal_size().columns - len(prefix.replace(type.value[0], "TEST")) - 1
    chunked_message: list[str] = textwrap.wrap(message, width=width) or [""]

    for line in chunked_message[:-1]:
        rich.print(
            prefix + line,
            end="\n",
            file=type.value[1],
            flush=flush,
        )

    rich.print(
        prefix + chunked_message[-1],
        end=end,
        file=type.value[1],
        flush=flush,
    )


def echoInput(
        message: str,
        /,
        *,
        is_one_line: bool = False,
        ) -> None:
    """
    Print an input message to the console.

    Parameters:
        message (str) : input message content
        is_one_line (bool) : Whether the input to capture is one the same line (True) or on next lines (False)
    """
    __echo(LogType.INPUT, 0, message, end="" if is_one_line else "\n", flush=True)

    rich.print(
        ": " if is_one_line else "> ",
        end="",
        file=LogType.INPUT.value[1],
        flush=True
    )


def echoInfo(
        message: str,
        /,
        *,
        indent: int = 0,
        end: str = "\n",
        flush: bool = True,
        ) -> None:
    """
    Print an informational log message to the console.

    Parameters:
        message (str) : Log message content
        indent (int) : Indentation level
        end (str) : String appended after the message
        flush (bool) : Whether to forcibly flush the stream
    """
    __echo(LogType.INFO, indent, message, end=end, flush=flush)


def echoWarning(
        message: str,
        /,
        *,
        indent: int = 0,
        end: str = "\n",
        flush: bool = True,
        ) -> None:
    """
    Print a warning log message to the console.

    Parameters:
        message (str) : Log message content
        indent (int) : Indentation level
        end (str) : String appended after the message
        flush (bool) : Whether to forcibly flush the stream
    """
    __echo(LogType.WARNING, indent, message, end=end, flush=flush)


def echoError(
        message: str,
        /,
        *,
        indent: int = 0,
        end: str = "\n",
        flush: bool = True,
        ) -> None:
    """
    Print an error log message to the console.

    Parameters:
        message (str) : Log message content
        indent (int) : Indentation level
        end (str) : String appended after the message
        flush (bool) : Whether to forcibly flush the stream
    """
    __echo(LogType.ERROR, indent, message, end=end, flush=flush)
