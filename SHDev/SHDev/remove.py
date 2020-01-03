from sys import argv
from os.path import abspath
from os import getenv
import json
import codecs

alias = argv[1]
home = '/home/'+getenv("SUDO_USER")

with open(f'{home}/.SHDev/program.json','r') as programF:
	aliases = json.load(programF)
	if alias in aliases:
		del aliases[alias]
	else:
		print(f"Alias {alias} does not exist")
		exit()
with open(f'{home}/.SHDev/program.json','w') as programF:
	json.dump(aliases,programF)
with open(f'{home}/.SHDev/SHDev.sh',"w") as SHDevF:
	for value in aliases.values():
		SHDevF.write(value+'\n')