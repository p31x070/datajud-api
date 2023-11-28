from dotenv import load_dotenv
import os

load_dotenv()
diretorio = os.environ["OBSIDIAN_DIRECTORY"]

if diretorio is None:
    print("A variável de ambiente OBSIDIAN_DIRECTORY não está definida.")
else:
    print("O valor da variável de ambiente OBSIDIAN_DIRECTORY é:", diretorio)

# ler o arquivo 
