import os
import importlib

pasta = './routers'
routers = []

for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        if not any(substring in arquivo for substring in [".pyc", "_"]):
            nome_modulo = os.path.splitext(arquivo)[0]
            modulo = importlib.import_module(f'.{nome_modulo}', package='routers')
            router = getattr(modulo, 'router')
            routers.append(router)