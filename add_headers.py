import os
import sys
import subprocess
import argparse
import re
from datetime import datetime

# Configura il tuo nome
author = "Valerio Molinari"

# Parser per gli argomenti della riga di comando
parser = argparse.ArgumentParser(description="Aggiunge header ai file specificati e ignora alcune directory.")
parser.add_argument("directory", type=str, help="Directory principale in cui eseguire lo script.")
parser.add_argument("-i", "--ignore", nargs='+', help="Cartelle da ignorare (supporta regex).", default=[])
args = parser.parse_args()

# Estensioni dei file a cui vuoi aggiungere le informazioni
file_extensions = ['.py', '.js', '.html', '.css', '.sql']


# Funzione per verificare se una directory dovrebbe essere ignorata
def should_ignore_dir(directory, ignored_dirs):
    return any(re.search(ignored_dir, directory) for ignored_dir in ignored_dirs)


# Funzione per ottenere la data di creazione su macOS
def get_creation_date(filepath):
    result = subprocess.run(['mdls', '-name', 'kMDItemFSCreationDate', '-raw', filepath], capture_output=True,
                            text=True)
    date_str = result.stdout.strip()
    try:
        creation_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z').strftime('%Y-%m-%d')
    except ValueError:
        creation_date = "Data non disponibile"
    return creation_date


for root, dirs, files in os.walk(args.directory):
    # Rimuove le directory da ignorare dalla lista dirs
    dirs[:] = [d for d in dirs if not should_ignore_dir(os.path.join(root, d), args.ignore)]

    for file in files:
        if any(file.endswith(ext) for ext in file_extensions):
            filepath = os.path.join(root, file)
            extension = os.path.splitext(file)[1]
            # Ottieni la data di creazione del file
            creation_date = get_creation_date(filepath)

            match extension:
                case '.py':
                    header = f'"""\nAutore: {author}\nData di creazione: {creation_date}\n"""\n\n'
                case '.sql':
                    header = f'-- Autore: {author}\n-- Data di creazione: {creation_date}\n\n'
                case '.html':
                    header = f'<!--\nAutore: {author}\nData di creazione: {creation_date}\n-->\n\n'
                case '.css' | '.js':
                    header = f'/*\nAutore: {author}\nData di creazione: {creation_date}\n*/\n\n'
                case _:
                    header = f'/*\nAutore: {author}\nData di creazione: {creation_date}\n*/\n\n'

            with open(filepath, 'r') as f:
                content = f.read()

            with open(filepath, 'w') as f:
                f.write(header + content)

            print(f"Added header to {filepath}")

print("Headers added to all files with creation dates!")
