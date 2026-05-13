import os
import subprocess


def read_and_decorate_files(file_paths):
    result_text = ""

    for file_path in file_paths:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                # Aggiungi decorazione prima del contenuto del file
                result_text += f"%% {os.path.basename(file_path)}\n\n"
                result_text += content + "\n\n"
        else:
            print(f"File not found: {file_path}")

    # Copia il risultato finale in pbcopy
    subprocess.run("pbcopy", universal_newlines=True, input=result_text)
    print("Content copied to clipboard.")


if __name__ == "__main__":
    import sys

    file_paths = sys.argv[1:]  # Prendi i percorsi dei file passati da CLI
    if file_paths:
        read_and_decorate_files(file_paths)
    else:
        print("Please provide file paths as arguments.")
