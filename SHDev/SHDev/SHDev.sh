function SHDev(){
	case $1 in
		import)
			source "./$2"
			;;
		install)
			sudo python3 "~/.SHDev/install.py" file $2 $3
			;;
		remove)
			sudo python3 "~/.SHDev/remove.py" $2
			;;
		help)
			cat ~/.SHDev/help.txt
			;;
		install-file)
			sudo cp -vn "./$2" "~/.SHDev"
			;;
		remove-file)
			sudo rm -f "~/.SHDev/$2"
			;;
		build)
			printf "sudo cp -r -f ./$2 ~/.$2
COMMAND_EXISTS=\$(grep -c \"source ~/.${2//"/"/}/$3\" ~/.bashrc)
if  [ $COMMAND_EXISTS -eq 0 ]; then
	printf '\\nsource ~/.${2//"/"/}}/$3' | sudo tee -a ~/.bashrc
fi" >> 'install.sh'
			;;
		exec)
			sudo chmod +x "./$2"
			;;
		install-line)
			sudo python3 "~/.SHDev/install.py" line $2 $3
			;;
		remove-line)
			sudo python3 "~/.SHDev/remove.py" $2
			;;
	esac
}

