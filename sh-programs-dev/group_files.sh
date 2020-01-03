function groupFiles(){
	mkdir $1
	while read i
	do
		mv -f $i "${1}/$i"
	done <<< $(ls | grep $1)
}
function removePrefix(){
	while read i
	do
		mv -f $i "${i//${1}/''}"
	done <<< $(ls | grep $1)
}