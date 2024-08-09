import os
import sys

# Configura il tuo nome
author = "Valerio Molinari"

# Costruisci il path dalla riga di comando
directory = os.path.join(*sys.argv[1:])

# Estensioni dei file che potrebbero aver avuto l'intestazione errata
file_extensions = ['.py', '.js', '.html', '.css', '.sql']

# Modelli di intestazione errata per ogni tipo di file
header_models = {
    '.py': f'"""\nAutore: {author}\nData di creazione: ',
    '.js': f'/*\nAutore: {author}\nData di creazione: ',
    '.css': f'/*\nAutore: {author}\nData di creazione: ',
    '.html': f'<!--\nAutore: {author}\nData di creazione: ',
    '.sql': f'-- Autore: {author}\n-- Data di creazione: '
}

any_corrected = False

for root, dirs, files in os.walk(directory):
    for file in files:
        filepath = os.path.join(root, file)
        extension = os.path.splitext(file)[1]

        if extension in file_extensions:
            with open(filepath, 'r') as f:
                content = f.read()

            header_start = header_models.get(extension)
            if extension in ['.py', '.js', '.css']:
                header_end = "*/\n\n" if extension != '.py' else '"""\n\n'
            elif extension == '.html':
                header_end = "-->\n\n"
            elif extension == '.sql':
                header_end = "\n\n"

            # Trova e rimuove l'intestazione errata
            if content.startswith(header_start):
                header_close_index = content.find(header_end)
                if header_close_index != -1:
                    new_content = content[header_close_index + len(header_end):]
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"Intestazione rimossa da {filepath}\n")
                    any_corrected = True
            else:
                print(f"Intestazione errata non completamente trovata in {filepath}, il file non è stato modificato.\n")

if any_corrected:
    print("Correzione completata!")
else:
    print("Alcuna correzione è stata eseguita!")
