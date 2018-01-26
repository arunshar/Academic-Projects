
************************** HAC Algorithm ******************************

Needed Files: Create a folder and place all the following files in it
	1) Data File : cho.txt, iyer.txt
	2) Code : hac.py

Execution command : 
	python hac.py -f 'cho.txt' -s 5

Usage: hac.py [options]

	Options:
	  -h, --help            show this help message and exit
	  -f INPUT, --inputFile=INPUT
		                filename containing data
	  -s CLUSTERSSIZE, --clustersSize=CLUSTERSSIZE
		                clusters count at which algorithm stops


************************** DBSCAN Algorithm ******************************

Needed Files: Create a folder and place all the following files in it
	1) Data File : cho.txt, iyer.txt
	2) Code : dbscan.py

Execution command : 
	python dbscan.py -f 'cho.txt' -s 4 -e 1.03

Usage: dbscan.py [options]

	Options:
	  -h, --help            show this help message and exit
	  -f INPUT, --inputFile=INPUT
		                filename containing data
	  -s CLUSTERSSIZE, --clustersSize=CLUSTERSSIZE
		                clusters count at which algorithm stops
	  -e EPSILONVALUE, --epsilonValue=EPSILONVALUE
		                epsilonValue

