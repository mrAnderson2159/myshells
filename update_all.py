import os
import re
import argparse


def parse_directives(file_content):
    directives = {
        'include_var': False,
        'include_import': False,
        'exclude_below': False,
        'include_custom': None,
        'exclude_custom': None,
        'include_private': False,
        'include_decorator': False,
        'export_to': None,
        'export_as': None,
        'freeze': False
    }

    directive_map = {
        "include var": lambda _: directives.update({'include_var': True}),
        "include import": lambda _: directives.update({'include_import': True}),
        "include *": lambda _: directives.update({'include_var': True, 'include_import': True}),
        "exclude below": lambda _: directives.update({'exclude_below': True}),
        "include custom": lambda line: directives.update({'include_custom': line.split("custom")[1].strip()}),
        "exclude custom": lambda line: directives.update({'exclude_custom': line.split("custom")[1].strip()}),
        "include private": lambda _: directives.update({'include_private': True}),
        "include decorator": lambda _: directives.update({'include_decorator': True}),
        "export to": lambda line: directives.update({'export_to': line.split("to")[1].strip()}),
        "export as": lambda line: directives.update({'export_as': line.split("as")[1].strip()}),
        "freeze": lambda _: directives.update({'freeze': True})
    }

    for line in file_content:
        line = line.strip()
        if line.startswith("# @"):
            for directive, action in directive_map.items():
                if directive in line:
                    action(line)
                    if directive == "freeze":
                        return directives

    return directives


def should_include(name, directives):
    if directives['exclude_below']:
        return False
    if directives['exclude_custom'] and re.match(directives['exclude_custom'], name):
        return False
    if directives['include_custom'] and not re.match(directives['include_custom'], name):
        return False
    if directives['include_private'] or not name.startswith('_'):
        return True
    return False


def process_file(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()

    if not content:
        return  # Salta i file vuoti

    directives = parse_directives(content)

    if directives['freeze']:
        return  # Se freeze è abilitato, ignora il file

    to_export = []
    skip_next_line = False

    for line in content:
        if directives['exclude_below']:
            break  # Interrompe l'elaborazione se exclude_below è abilitato

        # Salta le righe che iniziano con uno spazio (per evitare dichiarazioni innestate)
        if line.startswith(' '):
            continue

        if skip_next_line:
            skip_next_line = False
            continue

        if line.startswith("# @exclude"):
            skip_next_line = True
            continue

        # Se non ci sono esclusioni, includi sempre le classi e le funzioni
        if re.match(r'^class\s+\w+', line) or re.match(r'^def\s+\w+', line):
            name = re.split(r'\s+', line.strip())[1].split('(')[0].rstrip(':')
            # Controlla se il nome è già stato escluso da una direttiva personalizzata
            if directives['exclude_custom'] and re.match(directives['exclude_custom'], name):
                continue
            to_export.append(name)

        if directives['include_var'] and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*=', line):
            name = line.split('=')[0].strip()
            if should_include(name, directives):
                to_export.append(name)

        if directives['include_import']:
            if line.startswith('import'):
                name = line.split()[1]  # Questo cattura 'x' in 'import x'
                if should_include(name, directives):
                    to_export.append(name)
            elif line.startswith('from'):
                imported_items = line.split('import')[1].strip()  # Questo cattura tutto ciò che segue 'import'
                items = [item.strip() for item in
                         imported_items.split(',')]  # Divide gli elementi separati da virgola e rimuove gli spazi
                for name in items:
                    if should_include(name, directives):
                        to_export.append(name)

        if directives['include_decorator'] and line.strip().startswith('@'):
            name = line.split()[0].strip('@')
            if should_include(name, directives):
                to_export.append(name)

    if to_export:  # Evita di scrivere un __all__ vuoto
        filtered_content = []
        in_all_section = False
        directive_found = False

        # Prima passata: rimuove il vecchio __all__
        for line in content:
            if line.startswith('__all__'):
                in_all_section = True
                continue  # Salta la riga che inizia con __all__

            if in_all_section:
                if ']' in line:
                    in_all_section = False
                continue  # Salta tutte le righe fino a quando non si chiude __all__

            # Verifica se c'è una direttiva principale
            if not directive_found and line.startswith("# @"):
                directive_found = True
                filtered_content.append(line)
                filtered_content.append(f'\n__all__ = {to_export}\n\n\n')
                continue

            filtered_content.append(line)

        # Se non è stata trovata alcuna direttiva principale, posiziona __all__ all'inizio del file
        if not directive_found:
            with open(file_path, 'w') as f:
                f.write(f'__all__ = {to_export}\n\n\n')
                f.writelines(filtered_content)
        else:
            with open(file_path, 'w') as f:
                f.writelines(filtered_content)


def main():
    parser = argparse.ArgumentParser(
        description="Automatically update __all__ in Python files based on directives.",
        epilog="""
        Available directives:
          # @include var       : Includes variables in __all__.
          # @include import    : Includes import statements in __all__.
          # @include *         : Includes everything (classes, functions, etc.) in __all__.
          # @exclude below     : Excludes everything below this directive from __all__.
          # @include custom    : Includes custom patterns in __all__.
          # @exclude custom    : Excludes custom patterns from __all__.
          # @include private   : Includes private members (starting with '_') in __all__.
          # @include decorator : Includes decorators in __all__.
          # @export to [file]  : Exports __all__ to the specified file.
          # @export as [name]  : Exports __all__ as the specified name.
          # @freeze            : Prevents further updates to __all__.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("directory", type=str, help="The directory containing Python files.")
    parser.add_argument("--verbose", action="store_true", help="Print detailed processing information.")

    args = parser.parse_args()

    for root, _, files in os.walk(args.directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if args.verbose:
                    print(f"Processing {file_path}...")
                process_file(file_path)
                if args.verbose:
                    print(f"Updated {file_path}.")


if __name__ == "__main__":
    main()
