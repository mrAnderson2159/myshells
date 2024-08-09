import os
import shutil
import sys
from os.path import expanduser, split, join, exists
from shutil import copytree, rmtree
from colors import c_cyan, c_yellow, yellow, red
from debug import debug
from src.functions import feature, get_package
from src.globals import LOG
from utils import capitalize


def appunti(query: str, subject: str = None) -> None:
    """ Transfers the "appunti" folder of a lesson's subject from the nas to the computer
        and vice versa

    :param query: the type of transfer the program should do "get" on the computer, "post" on nas
    :type query: str
    :param subject: [optional] the subject of the lesson to get or post
    :type subject: str
    :return: None
    """
    feature('Copia Appunti')
    LOG.newline()

    def query_object(query: str, paths: dict) -> dict:
        """ Creates a dictionary of paths and words, paths to be used in transfer operations
            and words to be used in input dialogs

        :param query: the type of transfer the program should do "get" on the computer, "post" on nas
        :type query: str
        :param paths: A dictionary containing the paths of nas and bins
        :type paths: dict
        :return: A dictionary of paths to use for transfers and words to use for dialogs
        :rtype: dict
        """
        if query not in ('get', 'post'):
            raise ValueError(f'Query must whether be "get" or "post", not "{query}"')

        plat = sys.platform

        def q(a, b):
            return [a, b][query == 'post']

        return {
            'bin': expanduser(paths[q('user bin', 'nas bin')][plat]),
            'src': q(paths['università'][plat], expanduser('~/Desktop')),
            'dst': q(expanduser('~/Desktop'), paths['università'][plat]),
            '$dst': q('computer', 'nas'),
            '$mv': q('scaricare', 'caricare')
        }

    def copy_and_trash(src: str, dst: str, bin: str, bin_w: str) -> None:
        """

        :param src: the path to the file to copy
        :type src: str
        :param dst: the path to the file to substitute
        :type dst: str
        :param bin: the path to the bin on the same machine of the "dst"
        :type bin: str
        :param bin_w: the name of the bin's machine
        :type bin_w: str
        :return: None
        """

        def except_errno22(src: str, dst: str) -> str:
            try:
                c = copytree(src, dst)
                # debug(c is None)
                return c
            except shutil.Error as e:
                if isinstance(e.args[0], list) and isinstance(e.args[0][0], tuple) \
                        and e.args[0][0][2].startswith('[Errno 22]'):
                    pass
                else:
                    raise e
            except FileNotFoundError as e:
                # debug(e.filename)
                if e.filename != src:
                    os.makedirs(dst)
                    return except_errno22(src, dst)

        i = 2
        dst_parent, dst_name = split(dst)
        bin_dst = join(bin, dst_name)
        t = bin_dst
        while exists(bin_dst):
            bin_dst = f'{t} {i}'
            i += 1

        sys.stdout.write(f"{c_cyan('Copio')} {c_yellow(dst)} {c_cyan('nel cestino del')} {c_yellow(bin_w)}...")
        sys.stdout.flush()
        LOG.write(f'Copio {dst} nel cestino {bin}')
        except_errno22(dst, bin_dst)
        print('OK')

        try:
            sys.stdout.write(f"{c_cyan('Elimino')} {c_yellow(dst)}...")
            sys.stdout.flush()
            LOG.write(f'Elimino {dst}')
            rmtree(dst)
            print('OK')
        except FileNotFoundError:
            LOG.write('Niente da eliminare')
            yellow('CARTELLA INESISTENTE')
        except OSError as e:
            if e.args == (16, 'Resource busy'):
                red('RISORSA OCCUPATA')
                raise KeyboardInterrupt
            else:
                raise e

        sys.stdout.write(f"{c_cyan('Copio')} {c_yellow(src)} {c_cyan('in')} {c_yellow(dst_parent)}...")
        sys.stdout.flush()
        LOG.write(f"Copio {src} in {dst_parent}")
        except_errno22(src, dst)
        print('OK\n')

    package = get_package()
    paths = package['paths']
    folders = package['folders']

    qb = query_object(query, paths)
    subject = subject and capitalize(subject)

    if subject not in folders:
        if subject:
            print(f'Purtroppo {c_yellow(subject)} non è stata riconosciuta come materia')
        fd_items = list(folders.items())
        subjs = [f'{i + 1}. {key}' for i, (key, _) in enumerate(fd_items) if not key.startswith('_')]
        subjs = '\n'.join(subjs)
        choice = int(input(f'Scegli la materia che vuoi {qb["$mv"]} sul {c_yellow(qb["$dst"])}\n{subjs}\n\n> '))
        subject = fd_items[choice - 1][0]

    print(f"{capitalize(qb['$mv'][:-3])}o {c_yellow(subject)} sul {c_yellow(qb['$dst'])}...\n")

    subject = folders[subject]
    notes = folders['_notes']
    src = join(qb['src'], subject, notes)
    dst = join(qb['dst'], subject, notes)
    bin = qb['bin']

    copy_and_trash(src, dst, bin, qb['$dst'])

    if query == 'get':
        os.system(f'open "{join(dst, "appunti.tex")}"')
