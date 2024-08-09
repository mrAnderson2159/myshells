import os
import sys
import send2trash
import click
import re
from shutil import copyfile
from time import strftime
from pathlib import Path, PosixPath
from typing import Callable, Union

sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from colors import c_cyan, c_yellow, c_red, c_green, yellow
from paths import bash_profile as bp


def bash_profile():
    return Path(bp()).expanduser()


class AliasNotFoundError(Exception):
    """Custom exception for when an alias is not found."""
    pass


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """
    The main command group for the CLI application.

    If no subcommand is invoked, it provides a helpful message for using the help option to see available commands.
    """
    if ctx.invoked_subcommand is None:
        print("Use 'python program.py --help' to see available options.")


@main.command()
def edit():
    """
    Opens this script in PyCharm for editing.
    """
    os.system(f'open -a "PyCharm" "{__file__}"')


def list_aliases(source_file: Union[str, os.PathLike, PosixPath] = bash_profile()) -> list[str]:
    """
    Lists all lines from the specified shell configuration file.

    :param source_file: The shell configuration file to read from. Defaults to the user's bash_profile.
    :type source_file: Union[str, os.PathLike, PosixPath]
    :return: A list of strings, each representing a line from the file.
    :rtype: list[str]
    """

    with open(source_file, 'r') as profile:
        return profile.readlines()


def backup_cleaner(source_file: Union[str, os.PathLike, PosixPath] = bash_profile()):
    try:
        if not isinstance(source_file, PosixPath):
            source_file = Path(source_file).expanduser()

        directory = source_file.parent
        # print('Debug backup_cleaner - directory:', directory)
        backup_name = source_file.name
        # print('Debug backup_cleaner - backup_name:', backup_name)
        # print('Debug backup_cleaner - directory.iterdir():', directory.iterdir())
        backup_files = [file for file in directory.iterdir() if
                        file.name.startswith(backup_name) and file.name.endswith('.backup')]
        # print('Debug backup_cleaner - backup_files:', backup_files)
        older_backup_files = sorted(backup_files)[:-3]
        # print('Debug backup_cleaner - older_backup_files:', older_backup_files)

        for backup_file in older_backup_files:
            try:
                send2trash.send2trash(backup_file)
                print(f"{c_yellow('Warning:')} Older backup {c_cyan(backup_file.name)} sent to trash")
            except Exception as e:
                print(f"{c_red('Error:')} sending {c_yellow(backup_file.name)} to trash: {e}")

    except Exception as e:
        print(f"{c_red('Error')} during backup cleaning: {e}")


def backup(source_file: Union[str, os.PathLike, PosixPath] = bash_profile()):
    """
    Creates a backup of the specified file.

    :param source_file: The file to back up. Defaults to the current working directory's path.
    :type source_file: Union[str, os.PathLike, PosixPath]
    """
    backup_file = f"{source_file}_{strftime('%Y%m%d%H%M%S')}.backup"
    copyfile(source_file, backup_file)
    print(f"Backup of the original aliases file created at {c_cyan(backup_file)}")
    backup_cleaner()


def update(lines: list[str], source_file: Union[str, os.PathLike, PosixPath] = bash_profile()):
    """
    Writes the given lines to the specified source file.

    :param lines: The lines to write to the file.
    :type lines: list[str]
    :param source_file: The file to be updated. Defaults to the user's bash_profile.
    :type source_file: Union[str, os.PathLike, PosixPath]
    """
    with open(source_file, 'w') as file:
        file.writelines(lines)


def split_alias(alias_line: str) -> tuple:
    pattern = re.compile(
        r"""
        ^\s*alias\s+           # Inizia con zero o più spazi seguiti dalla parola chiave 'alias' e almeno uno spazio
        ([^\s=]+)              # Gruppo 1: cattura il nome dell'alias, esclusi spazi e il carattere '='
        \s*=\s*                # Il segno '=' circondato da zero o più spazi, per gestire spazi intorno all'uguale
        (['\"]?)               # Gruppo 2: cattura una quota opzionale all'inizio del comando (singola o doppia quota)
        (.*?)                  # Gruppo 3: cattura il comando dell'alias, usando .*? per la modalità non avida
        (?(2)\2|(?=\s|$))      # Condizione: se il Gruppo 2 (quota di apertura) è stato catturato, cerca la stessa quota alla fine. Altrimenti, assicurati che ci sia uno spazio o la fine della stringa
        \s*$                   # Zero o più spazi seguiti dalla fine della linea, per gestire spazi finali
        """, re.VERBOSE)

    match = pattern.match(alias_line)
    if not match:
        raise ValueError(f"Error: The alias line '{alias_line}' does not match the expected format.")

    alias_name, _, command = match.groups()
    command = command.strip()
    if not command:
        raise ValueError(f"Error: Alias '{alias_name}' is missing a command.")

    return alias_name, command


def get_alias(alias_name: str, source_file: str = bash_profile()) -> dict:
    """
    Retrieves the latest definition of an alias from the configuration file.

    :param alias_name: The name of the alias to find.
    :type alias_name: str
    :param source_file: The configuration file to search within. Defaults to bash_profile.
    :type source_file: str
    :raises AliasNotFoundError: If the alias is not found in the file.
    :return: A dictionary with the alias's latest line position and command.
    :rtype: dict
    """

    lines = list_aliases()

    for i, line in enumerate(reversed(lines), 1):
        if line.startswith(f"alias {alias_name}="):
            try:
                # Extract the alias body from the alias equation
                alias_body = split_alias(line)[1]
                # Calculate the line position from the beginning of the file
                line_position = len(lines) - i
                return {"line": line_position, "body": alias_body}
            except ValueError as e:
                print(f"{c_red('Error splitting alias:')} {e}")
                continue

    raise AliasNotFoundError(f"Alias '{alias_name}' not found in {source_file}.")


def build_alias(alias: str, body: str) -> str:
    """
    Constructs a formatted alias definition string.

    :param alias: The name of the alias.
    :type alias: str
    :param body: The command that the alias executes.
    :type body: str
    :return: A formatted alias definition.
    :rtype: str
    """

    # Escape single quotes in the body
    body_escaped = body.replace("'", "'\\''")

    return f"alias {alias}='{body_escaped}'\n"


@main.command('new')
@click.argument('alias_name')
@click.argument('alias_body', nargs=-1)
def newalias(alias_name: str, alias_body: tuple[str]):
    """
    Adds a new alias to the shell configuration file, with an optional overwrite prompt.

    :param alias_name: The name of the new alias.
    :type alias_name: str
    :param alias_body: The command(s) that the alias will execute.
    :type alias_body: tuple[str]
    """

    alias_body_str = ' '.join(alias_body)
    alias_cmd = build_alias(alias_name, alias_body_str)  # f"alias {alias_name}='{alias_body_str}'"
    existing_alias = None

    # Check if the alias already exists
    try:
        existing_alias = get_alias(alias_name)
        # If get_alias did not raise an AliasNotFoundError, the alias exists
        overwrite = click.confirm(
            f"{c_yellow('Warning:')} The alias {c_cyan(alias_name)} already exists. Do you want to overwrite it?")
        if not overwrite:
            print(f"{c_yellow('No changes made.')}")
            return
    except AliasNotFoundError:
        # If an AliasNotFoundError was raised, the alias does not exist
        pass

    # Append the new alias to the configuration file
    try:
        backup()
        with open(bash_profile(), 'a') as bp:
            bp.write(alias_cmd)
    except IOError as e:
        print(f"{c_yellow('Error:')} Failed to write to {bash_profile()}: {c_red(e)}")
        sys.exit(1)  # Imposta l'exit code a 1 per indicare il fallimento

    print(f"Alias {c_cyan(alias_name)} {'updated' if existing_alias else 'added'} {c_green('successfully')}.")


def manage_alias_file(func: Callable):
    """
    A decorator to manage the reading and writing of the alias file.

    :param func: The function to be decorated.
    :type func: Callable
    :returns: The decorated function.
    :rtype: Callable
    """

    def wrapper(*args, **kwargs):
        lines = list_aliases()
        func(lines, *args, **kwargs)
        update(lines)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


@manage_alias_file
def modify_alias(lines: list, alias_name: str, alias_data: dict, new_body: str):
    """
    Modifies an existing alias's command within the configuration file.

    :param lines: The current lines of the configuration file.
    :type lines: list
    :param alias_name: The name of the alias to modify.
    :type alias_name: str
    :param alias_data: Information about the alias, including its line number.
    :type alias_data: dict
    :param new_body: The new command for the alias.
    :type new_body: str
    """

    lines[alias_data["line"]] = build_alias(alias_name, new_body)


@manage_alias_file
def rename_alias(lines: list, alias_data: dict, new_name: str):
    """
    Changes the name of an existing alias within the configuration file.

    :param lines: The current lines of the configuration file.
    :type lines: list
    :param alias_data: Information about the alias, including its line number.
    :type alias_data: dict
    :param new_name: The new name for the alias.
    :type new_name: str
    """

    lines[alias_data["line"]] = build_alias(new_name, alias_data['body'])


@main.command('mv')
@click.option('--name', default='')
@click.argument('alias_name', type=str, required=True)
@click.argument('body', type=str, required=False, default='')
def mvalias(alias_name: str, body: str, name: str) -> None:
    """
    Modifies an existing alias in the user's shell configuration file.
    It can change either the alias's name or its command.

    :param alias_name: The current name of the alias to modify.
    :type alias_name: str
    :param body: The new command for the alias. If not provided, the command will not be changed.
    :type body: str, optional
    :param name: The new name for the alias. If not provided, the name will not be changed.
    :type name: str, optional
    """
    try:
        alias_data = get_alias(alias_name)
    except AliasNotFoundError:
        print(f"{c_red('Error:')} Alias {c_cyan(alias_name)} not found.")
        return

    if name:
        if click.confirm(
                f"Are you sure you want to change the name of alias {c_yellow(alias_name)} to {c_cyan(name)}?"
        ):
            backup()
            rename_alias(alias_data, new_name=name)
            print(f"\nAlias {c_cyan(alias_name)} successfully renamed to {c_cyan(name)}")
        else:
            print(f"Alias {c_cyan(alias_name)} name has not been modified\n")
    elif body:
        if click.confirm(
                f"\nAre you sure you want to change the body of alias "
                f"{c_cyan(alias_name)} from \"{c_yellow(alias_data['body'])}\" to \"{c_yellow(body)}\"?"
        ):
            backup()
            modify_alias(alias_data, new_body=body)
            print(f"\nNew alias: {c_cyan(alias_name)} -> {c_yellow(body)}\nSuccessfully created\n")
        else:
            print(f"Alias {c_cyan(alias_name)} -> {c_yellow(alias_data['body'])} has not been modified\n")
    else:
        print(f"{c_yellow('No changes made.')} Please provide a new name or a new body for the alias.")


@main.command('rm')
@click.argument('alias_names', nargs=-1, required=True)
def rmalias(alias_names: tuple[str]):
    """
    Deletes one or more aliases from the user's shell configuration file.

    :param alias_names: The names of the aliases to be deleted.
    :type alias_names: tuple[str]
    """
    modified = False
    lines = list_aliases()

    for alias_name in alias_names:
        pattern = re.compile(rf"^\s*alias {alias_name}=.+$")
        new_lines = [line for line in lines if not pattern.match(line)]

        if len(lines) != len(new_lines):
            if click.confirm(f"Are you sure you want to delete alias {c_yellow(alias_name)}?"):
                print(f"Alias {c_cyan(alias_name)} has been {c_green('successfully deleted')}.")
                lines = new_lines
                modified = True
            else:
                print(f"Alias {c_cyan(alias_name)} has {c_red('not')} been deleted.")
        else:
            print(f"Alias {c_red(alias_name)} was not found.")

    if modified:
        backup()
        update(lines)
        print(f"The aliases file has been {c_green('updated')}.")
    else:
        print(f"{c_red('No aliases were deleted')}.")

