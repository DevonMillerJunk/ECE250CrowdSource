import shutil
import sys
import os
import argparse

GIT_REPO = "https://github.com/DevonMillerJunk/ECE250CrowdSource.git"

class TestResult:
    def __init__(self, results, diffs):
        self.results = results
        self.num_tests = len(results)
        self.num_correct = sum(results)
        self.num_wrong = self.num_tests - self.num_correct
        self.correct = list()
        self.wrong = list()
        for i, val in enumerate(results, 1):
            if val:
                self.correct.append(i)
            else:
                self.wrong.append(i)
        if(results):
            self.grade = self.num_correct / self.num_tests
        else:
            self.grade = 0
        self.diffs = diffs
    def to_string(self):
        if(not self.correct and not self.wrong):
            return "No result generated"
        if(self.grade == 1):
            return "{}/{}, {:.2%}".format(self.num_correct, self.num_tests, self.grade)
        else:
            return "{}/{}, {:.2%} mistakes were found in line(s) {}".format(self.num_correct, self.num_tests, self.grade, self.wrong)
    def diffs_to_string(self):
        for diff in self.diffs:
            print(" \t Expected: '{}', Got: '{}' ".format(diff[0], diff[1]))
parser = argparse.ArgumentParser(description='Run tests')
parser.add_argument("executable", help="this is a file that contains a compiled program i.e.(the output of g++)")
parser.add_argument("project_num",help="project number that is being tested i.e.(0,1,2,3)")
parser.add_argument("-no-purge",help="Saves the temp directory for manual inspection", action='store_true')
parser.add_argument("-input",help="Run given input file locally, dont use git, must be used in conjunction with -out")
parser.add_argument("-output",help="output file that is considered to be the 'solution' to the -in file.")

args = parser.parse_args()

if args.input and (args.output is None):
    parser.error("Provided input file without any output")
    exit()
if args.output and (args.input is None):
    parser.error("Provided output file without any input")
    exit()

exec = args.executable
project_num = args.project_num
purge = not args.no_purge



project = os.environ.get('PARKIN_PROJECT', os.getcwd()) + "/" 


if(os.path.isdir("temp")):
    os.system("rm -rf temp/*")
else:
    os.system("mkdir temp")

#TODO: ERROR CHECK if user provided files exist


def filter(line):
    index = line.find('//')
    if(index != -1):
         return line[0:index].strip()
    else:
        return line.strip()
        

def pair(input, output):
    """
    Takes to lists of input files and output files, pairs them based on the prefix
    """
    pairs = list()
    for a in input:     
        prefix = a.split('.')[0]
        for i, b in enumerate(output):
            if b.startswith(prefix):
                used_index = i
                pairs.append( (a,b) )
            used_index = None
        if(used_index):
            del output[used_index] #delete so I do not have to loop over stuff twice
    return pairs
            


def getTestsFromGit(num):
    os.system("mkdir temp/repo")
    os.system("git clone {} temp/repo".format(GIT_REPO))
    file_prefix = "temp/repo/Project{}/TestCases/".format(num)
    files = os.listdir("temp/repo/Project{}/TestCases".format(num))
    input = list()
    output = list()
    for file in files:
        if file.endswith('in'):
            input.append(file_prefix + file)
        if file.endswith('out'):
            output.append(file_prefix + file)
    input.sort()
    output.sort()
    return pair(input, output)

def getTestResults(exec, input, expected_output):
    results = list()
    diffs = list()
    user_output_file = "temp/output"
    os.system(r"{} < {} > {}".format(exec,input, user_output_file))
    with open(user_output_file, 'r') as user_output:
        with open(expected_output, 'r') as real_output:
            #TODO: this may break with empty files
            user_line = filter(user_output.readline())
            real_line = filter(real_output.readline())
            while real_line and user_line:
                result = user_line == real_line
                results.append(result)
                if(not result):
                    diffs.append( (real_line, user_line) )
                user_line = filter(user_output.readline())
                real_line = filter(real_output.readline())
            if(user_line != real_line):
                print("Program output and expected output are not the same size, not grading next lines")
    os.system("rm temp/output")
    return TestResult(results, diffs)


if(not args.input):
    test_cases = getTestsFromGit(project_num)
else:
    test_cases = [(project + args.input, project+args.output)]



for pair in test_cases:
    input_file = pair[0]
    output_file = pair[1]
    name = input_file.split('/')[-1]
    results = getTestResults(project+exec, input_file, output_file)
    #if(verbose)
    print("Results from {}: {} ".format(name, results.to_string()))
    (results.diffs_to_string())

if(purge):
    os.system("rm -rf temp")