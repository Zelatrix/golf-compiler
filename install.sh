check_installed() {
	DEPENDENCIES=("rply" "llvmlite")
	
	for dependency in "${DEPENDENCIES[@]}"
	do
		if ! pip freeze | grep rply > /dev/null 
		then
			echo "Installing $dependency..."
			pip install ${dependency} 
		fi
	done	
}

check_installed

#git clone https://github.com/Zelatrix/golf-compiler.git
