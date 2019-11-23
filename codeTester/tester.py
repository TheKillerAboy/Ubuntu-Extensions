from sys import argv
from os import listdir
from subprocess import PIPE, Popen
from os.path import isfile, join
from types import SimpleNamespace

HELP_INFO = \
"""Activate flags with - or -- (both do the same thing)
Flags:
	prefixOnly, p (no argument):
		requires test files to have the same name as source file
	outputNeeded, oN (no argument):
		requires output file to exist
	timeLimit_ms, tl (integer argument):
		time limit in milli seconds before program will be terminated
	inputExt, iE (string argument):
		input extension of test files
	outputExt, oE (string argument):
		output extension of test files
	showError, sE (no argument):
		displays reason for incorrect anwsers
	help, h (no argument):
		displays this message
	fileOnly, fO (string argument):
		requires test files to have the same name as fileOnly argument
	capSensitive, cS (no argument):
		enables capital sensitivity when prefixOnly or fileOnly is active
	excludeList, eL (list of string arguments):
		exclude files with any of these strings in them

List of arguments:
	starts and ends with square brackets with commmas acting as seperator, and has no spaces between items
	example - [dummy,onlytest]"""

def flagToNickname(flag, nicknames):
	if flag in nicknames:
		return nicknames[flag]
	return flag


def parseValue(value):
	if value.lower() in {"true","false","t","f"}:
		return value.lower()[0] == "t"
	try:
		value = int(value)
		return value
	except:
		pass
	if value[0] == '[':
		return value[1:-1].split(',')
	return value

def parseArgv(method, nicknames = {}, defaults = {}):
	args = iter(argv[1:])
	__args = []
	__kwargs = defaults
	while True:
		try:
			value = next(args)
			if(value[0] == '-'):
				extDis = 1
				if value[1] == '--':
					extDis = 2
				if(type(__kwargs[flagToNickname(value[extDis:],nicknames)]) == bool):
					__kwargs[flagToNickname(value[extDis:],nicknames)] = not __kwargs[flagToNickname(value[extDis:],nicknames)]
				else:
					__kwargs[flagToNickname(value[extDis:],nicknames)] = parseValue(next(args))
			else:
				__args.append(value)
		except:
			break
	if(__kwargs["help"]):
		print(HELP_INFO)
	else:
		method(*__args,**__kwargs)

def fileMeetConstraints(file, files_in_direcory,source_file,prefixOnly,inputExt,outputExt,outputNeeded,capSensitive,fileOnly = "",excludeList = [],**kwargs):
	def wordCapSensitiveEq(check, word):
		return check == word if capSensitive else check.lower() == word.lower()

	if fileOnly != '' and not wordCapSensitiveEq(fileOnly,file[:len(fileOnly)]):
		return False

	if prefixOnly and not wordCapSensitiveEq(source_file,file[:len(source_file)]) and not fileOnly:
		return False

	if inputExt not in file:
		return False

	if outputNeeded and file.replace(inputExt,outputExt) not in files_in_direcory:
		return False

	for exclude in excludeList:
		if exclude in file:
			return False

	return True

def tester(directory,source_file,*args,**kwargs):
	num_of_correct = 0
	KWARGS = SimpleNamespace(**kwargs)
	files_in_direcory = {f for f in listdir(directory) if isfile(join(directory, f))}
	if source_file not in files_in_direcory:
		print("Source file doesn't exist")
		return
	files_in_direcory = set(filter(lambda file : fileMeetConstraints(file,files_in_direcory,source_file,**kwargs),files_in_direcory))
	num_of_tests = len(files_in_direcory)
	files_in_direcory = sorted(list(files_in_direcory))
	for file in files_in_direcory:
		output_file = file.replace(KWARGS.inputExt,KWARGS.outputExt)
		p = Popen(f'timeout {KWARGS.timeLimit_ms/1000} "{directory}/{source_file}" < "{directory}/{file}" > "{directory}/{output_file}.tmp" \
			;diff -E -b -Z "{directory}/{output_file}.tmp" "{directory}/{output_file}"; rm -f "{directory}/{output_file}.tmp"', shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderr = map(lambda st : st.decode('utf-8'),p.communicate())
		terminal_return = ("Output Incorrect" if stdout != '' else "") + '\t' + ("Program Timeout" if stderr != '' else "") 
		print(file.replace(KWARGS.inputExt,''), end = '')
		if terminal_return== '\t':
			print(" Correct!")
			num_of_correct += 1
		else:
			print(" Incorrect :(")
			if KWARGS.showError:
				print("\tError Occoured: ", terminal_return)
			elif KWARGS.showDetailError:
				print("\tConsole Output: ", stdout.replace('\n',' '))
				print("\tConsole Error: ",stderr.replace('\n',' '))
	if num_of_tests > 0:
		print("Result:",f"{num_of_correct}/{num_of_tests}",f"{num_of_correct/num_of_tests:.2%}")
	else:
		print("No tests found.")

if __name__ == '__main__':
	parseArgv(tester,{'p':"prefixOnly",'oN':"outputNeeded","iE":"inputExt","oE":"outputExt","tl":"timeLimit_ms","cS":"capSensitive","sE":"showError","h":"help","fO":"fileOnly","sDE":"showDetailError","eL":"excludeList"},{"prefixOnly" : False, "timeLimit_ms" : 2000, "inputExt" : '.in', "outputExt" : '.out', "outputNeeded" : False, "capSensitive" : False, "showError" : False,"help" : False, "fileOnly" : "","showDetailError":False, "excludeList":[]})