move() {
	# Move all ZID files into a separate directory
	echo "Moving all ZID files..."
	mv *:Zone.Identifier ZIDs/
	sleep 3
	echo "ZIDs moved successfully!"
}

if [[ $(find . -maxdepth 1 -name "*:Zone.Identifier" | wc -l) == 0 ]]
	then
		echo "No ZID files in directory!"
else
	# Create a directory to store ZID files
	if [[ ! -d "ZIDs/" ]]
	then
		mkdir ZIDs/
		echo "Directory ZIDs/ created!"
		sleep 3
		move
	else
		move
	fi

	echo "Do you want to delete ZIDs/?"
	# Get input from the user
	read choice
	if [[ $choice == "y" || $choice == "Y" ]] 
	then
		echo "OK! Removing ZIDs/..."
		rm -r ZIDs/
	else if [[ $choice == "n" || $choice == "N" ]] 
	then
		echo "OK, not removing ZIDs/!"
		else
			echo "Please enter a valid choice!"
		fi
	fi
fi
