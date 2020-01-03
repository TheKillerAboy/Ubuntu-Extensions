sudo rm -f -r ~/.SHDev
sudo cp -r -f ./SHDev ~/.SHDev
COMMAND_EXISTS=$(grep -c "source ~/.SHDev/SHDev.sh" ~/.bashrc)
if  [ $COMMAND_EXISTS -eq 0 ]; then
	printf '\nsource ~/.SHDev/SHDev.sh' | sudo tee -a ~/.bashrc
fi