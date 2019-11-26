sudo cp ./codeTester.py ~/.codeTester.py
sudo cp ./codeTester_shell_programmer.sh ~/.codeTester_shell_programmer.sh
COMMAND_EXISTS=$(grep -c "source ~/.codeTester_shell_programmer.sh" ~/.bashrc)
if  [ $COMMAND_EXISTS -eq 0 ]; then
	printf '\nsource ~/.codeTester_shell_programmer.sh' | sudo tee -a ~/.bashrc
fi