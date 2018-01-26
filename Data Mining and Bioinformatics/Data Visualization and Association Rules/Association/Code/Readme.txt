Needed Files: Create a folder and place all the following files in it
	1) Data File : associationruletestdata.txt
	2) Rules File : rules.txt
	3) Code : Apriori.py

Execution command : 
	python Apriori.py -f 'associationruletestdata.txt' -s 50 -c 70 -r 'rules.txt'

Help command :
	python Apriori.py -h
	
	Usage: Apriori.py [options]

	Options:
	  -h, --help            show this help message and exit
	  -f INPUT, --inputFile=INPUT
		                filename containing data
	  -s MINS, --minSupport=MINS
		                minimum support value
	  -c MINC, --minConfidence=MINC
		                minimum confidence value
	  -r RULES, --ruleFile=RULES
		                filename containing rules

