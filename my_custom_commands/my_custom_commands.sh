function codeTester(){
	python3 /home/ameybrugh/Documents/programming-olympiad/C++_Solutions/tester.py $(pwd) $*
}

function setupArduino(){
	sudo chmod a+rw /dev/ttyACM0
}