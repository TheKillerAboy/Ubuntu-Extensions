from sys import argv
from os.path import abspath
from os import getenv
import json
import codecs

type_ = argv[1]
alias, code_dir = argv[2:4]
home = '/home/'+getenv("SUDO_USER")
if type_ == "file":
	code_lit = ""
	with open(abspath(code_dir),'r') as codeF:
		line = codeF.readline()
		while line:
			code_lit += line
			line = codeF.readline()
else:
	code_lit = code_dir

with open(f'{home}/.SHDev/program.json','r') as programF:
	aliases = json.load(programF)
	if alias in aliases:
		print(f"Alias {alias} already exist")
		exit()
	else:
		aliases[alias] = code_lit
with open(f'{home}/.SHDev/program.json','w') as programF:
	json.dump(aliases,programF)
with open(f'{home}/.SHDev/SHDev.sh',"w") as SHDevF:
	for value in aliases.values():
		SHDevF.write(value+'\n')