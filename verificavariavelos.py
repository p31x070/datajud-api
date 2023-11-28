import os

diretorio = os.getenv("OBSIDIAN_DIRECTORY")
if diretorio is None:
    print("A variável de ambiente OBSIDIAN_DIRECTORY não está definida.")
else:
    print("O valor da variável de ambiente OBSIDIAN_DIRECTORY é:", diretorio)
