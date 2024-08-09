from os.path import expanduser, join, splitext, exists
from shutil import move

from src.functions import get_package
from re import search

from src.globals import LOG

__PACKAGE = get_package()
__DIRECTORIES = {k:v for k,v in __PACKAGE["folders"].items() if not k.startswith(('_', 'Test'))}
__COMMANDS = {k:v for k,v in __PACKAGE["customv"].items()}
__DESKTOP = expanduser('~/Desktop')
__NOTES = __PACKAGE["folders"]["_notes"]
__REGEX = r'Schermata [\d-]+ alle ([\d.]+).png'

def key_time(s:str) -> int:
    ''' Takes a screenshot name/path in input and returns the time as an integer

    :param s: The name/path of the screenshot
    :return: The time as an integer
    :raises ValueError: If the input is not the name of a screenshot
    '''
    key = search(__REGEX, s).group(1)
    if key is None:
        raise ValueError(f"{s} non è il nome di uno screenshot.png")
    key = int(''.join(key.split('.')))
    return key

def customv(subject_command:str, name:str, *args:str) -> dict:
    ''' Moves a list os screenshots from the desktop to a subject/notes/images destination then
    prints out the latex includegraphics command for each screenshot

    :param subject_command: The command name of the subject
    :param name: The new name to give to the screenshots
    :param args: A list containing one or more screenshots. Optionally can be passed a number which
                 represents the size of the latex command
    :return: A dictionary containing the new paths of the screenshots and the latex command
    :raises ValueError: if the parameter name has not been specified
    :raises FileExistsError: if already exists an image with the same name in subject/notes/images path
    '''
    if search(__REGEX, name) is not None:
        raise ValueError(f"Il primo valore dev'essere il nome da assegnare agli screenshot, {name} non è valido")

    result = {'screenshots': [], 'latex':'\n'}

    try:
        path = join(__DESKTOP, __DIRECTORIES[__COMMANDS[subject_command]], __NOTES, 'images')
        screenshots = []
        size = 4
        for arg in args:
            if arg.isdigit():
                size = int(arg)
            else:
                screenshots.append(arg)
        screenshots = sorted(screenshots, key=key_time)
        for i, screenshot in enumerate(screenshots):
            _, ext = splitext(screenshot)
            new_name = f'{name}_{i + 1}{ext}'
            new_path = join(path, new_name)
            screenshot_path = join(__DESKTOP, screenshot)

            # j = 1
            # while exists(new_path)

            if exists(new_path):
                raise FileExistsError(f"image {new_name} already exists in {path}")

            move_args = (screenshot_path, new_path)

            move(*move_args)
            result['screenshots'].append(move_args)
            result['latex'] += f"\\begin{{center}}\n" \
                               f"\\includegraphics[scale=.{size}]{{{new_name.split(ext)[0]}}}\n" \
                               f"\\end{{center}}\n\n\n"

        print(result['latex'])
        LOG.write(f"customv:\n" + '\n'.join(map(str, result['screenshots'])) + '\n' + result["latex"])
        return result

    except KeyError:
        print(f"{subject_command} non è un comando valido, riprova scegliendo un comando nell'elenco")
        for command, subject in __COMMANDS:
            print(f'\t{command}: {subject}')
    except Exception as e:
        raise e

