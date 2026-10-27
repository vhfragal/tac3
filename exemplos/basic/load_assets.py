import sys
import os

def get_resource_path(relative_resource_path:str):
    if getattr(sys, 'frozen', False):
        # Executável compilado com cx_Freeze
        base_path = os.path.dirname(sys.executable)
        # ou no main.py
        #os.path.split(os.path.abspath(__file__))[0]
    else:
        # Modo desenvolvimento (.py)
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_resource_path)

# Exemplo de uso no seu programa:
#caminho_logo = obter_caminho_recurso("assets/logo.png")
#caminho_banco = obter_caminho_recurso("banco.db")