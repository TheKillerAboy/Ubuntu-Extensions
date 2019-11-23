from sys import argv
from os.path import isdir, join, abspath
from os import system, listdir

if len(argv) < 2:
	directory = "./"
else:
	directory = argv[1]
directory = abspath(directory)

print("RENAMES INPUT DIRECTORY TOO, AND!!!! ALL SUB DIRECTORIES BE CAREFUL!!!!!!!!!!!!!!!!\n Are you sure you want to continue? (Y/n)")
if input() != 'Y':
	exit()

def rename_directory_and_all_sub_directories(dir):
	newdir = dir[:dir.rindex('/')+1] + dir[dir.rindex('/')+1:].replace(' ','_')
	if newdir != dir:
		system(f"mv \"{dir}\" \"{newdir}\"")
	if isdir(newdir):
		for sub in map(lambda f: join(newdir,f),listdir(newdir)):
			rename_directory_and_all_sub_directories(sub)

rename_directory_and_all_sub_directories(directory)


'''
	RENAMES INPUT DIRECTORY TOO, AND!!!! ALL SUB DIRECTORIES BE CAREFUL!!!!!!!!!!!!!!!!
'''