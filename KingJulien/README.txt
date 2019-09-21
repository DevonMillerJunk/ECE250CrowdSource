This script will pull all test cases in this repository and run your  executable against them. Printing out neccecary metrics

It is not required to clone the entire repository, users can also just download this individual file and invoke the script. The script always reads tests on the remote repo.

It can be invoked with python3 as such:

python3 king_julien.py <relative path to exectuable file> <project number>
or 
python3 king_julien.py <relative path to exectuable file> <project number> -input <relative path to custom input file> -output <relative path to custom output file>

It can be used to quickly test the crowd sourced test cases on github.

Requirments:

	An executable file (output of g++ ex a.out)
	Unix environment to use this script (One of the shells where you can 'cd')
	An internet conncection to connect to the remote repo

Disclaimer: This is really hacky code that was written in a day, there is no gurantee that code passing on king_julien will pass on the official grader. The creaters are not liable if such an event occurs. 
