function SHDev(){
	case $1 in
		import)
			source "./$2"
			;;
		install)
			sudo python3 "$HOME/.SHDev/install.py" file $2 $3
			;;
		remove)
			sudo python3 "$HOME/.SHDev/remove.py" $2
			;;
		help)
			cat "$HOME/.SHDev/help.txt"
			;;
		install-file)
			sudo cp -vn "./$2" "$HOME/.SHDev"
			;;
		remove-file)
			sudo rm -f "$HOME/.SHDev/$2"
			;;
		build)
			printf "sudo cp -r -f ./$2 ~/.$2
COMMAND_EXISTS=\$(grep -c "source ~/.${2//"/"/}/$3" $HOME/.bashrc)
if  [ $COMMAND_EXISTS -eq 0 ]; then
	printf '\nsource $HOME/.${2//"/"/}}/$3' | sudo tee -a $HOME/.bashrc
fi" >> install.sh
			;;
		exec)
			sudo chmod +x "./$2"
			;;
		install-line)
			sudo python3 "$HOME/.SHDev/install.py" line $2 $3
			;;
		remove-line)
			sudo python3 "$HOME/.SHDev/remove.py" $2
			;;
	esac
}
function codeScraper(){
	/home/ameybrugh/Documents/Ubuntu-Extensions/CodeForces_Scraper/venv/bin/python /home/ameybrugh/Documents/Ubuntu-Extensions/CodeForces_Scraper/scraper.py $1
}
