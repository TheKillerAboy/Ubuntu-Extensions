print(repr('''function SHDev(){
	case $1 in
		import)
			source "$(pwd)/$1"
			;;
		install)
			sudo python3 "~/.SHDev/install.py" $1 $2
			;;
		remove)
			sudo python3 "~/.SHDev/remove.py" $1 $2
			;;
		help)
			cat ~/.SHDev/help.txt
}'''))