import json

def parseNicksDefaults(file):
	with open(file,"r") as f:
		data = json.load(f)
	return data

def nextArgv(nicknames,defaults):
	args = iter(argv[1:])
	while True:
		try:



def parseArgv(stackBoolFlags=True,singleFlag=True,nicknames = {}, defaults = {}):
	for bArg, key, value in nextArgv()