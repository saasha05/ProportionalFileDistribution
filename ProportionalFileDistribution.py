"""
Author: Saasha Mor

23rd February 2020
ACS Programming Challenge
Usage: FileDistribution.py -f filename.txt -n nodesname.txt -o outputfile.txt(optional)
Description: A program to distribute files into node buckets in a proportional manner.
    Takes input for files and their sizes, as well as nodes and their capacity.
    Produces output into an output file which determines which files go into which node.
"""

import re
import heapq
import sys


class HeapNode(object):
    def __init__(self, name, sizeAvail):
        self.name = name
        self.sizeAvail = int(sizeAvail)
        self.filesSizeTransferred = 0

    def addFile(self, file):
        self.filesSizeTransferred += file.size
        self.sizeAvail -= file.size

    def getTupleKey(self):
        return (self.filesSizeTransferred, 1 / float(self.sizeAvail), self)


class File(object):
    def __init__(self, name, size):
        self.name = name
        self.size = int(size)
        self.assignedNode = None

    def __lt__(self, other):
        return (self.size < other.size)

    def assignNode(self, node):
        self.assignedNode = node.name

skipLines = re.compile("^(?:\s+)*#|(?:\s+)")

def importNodes(filename):
    try:
        nodes = []
        nodeFile = open(filename, 'r')
        for line in nodeFile:
            if re.match(skipLines, line):
                continue
            group = re.split('\s+', line)
            heapNode = HeapNode(group[0], group[1])
            heapq.heappush(nodes, heapNode.getTupleKey())
        nodeFile.close()

        return nodes
    except:
        print("Error: Cannot read nodes-input from '", filename, "'")
        return -1


def importFiles(filename):
    try:
        files = list()
        inputFile = open(filename, "r")
        for line in inputFile:
            if re.match(skipLines, line):
                continue
            group = re.split('\s+', line)
            files.append(File(group[0], group[1]))

        inputFile.close()
        files = sorted(files, reverse=True)

        return files
    except:
        print("Error: Cannot read files-input from '", filename, "'")
        return -1


def planDistribution(nodes, files):
    for f in files:
        try:
            tempNodes = list()
            # Remove and return the least active storage node.
            while nodes:
                n = heapq.heappop(nodes)
                heapNode = n[2]
                tempNodes.append(heapNode)
                if heapNode.sizeAvail >= f.size:
                    heapNode.addFile(f)
                    f.assignNode(heapNode)
                    break
            for tempN in tempNodes:
                heapq.heappush(nodes, tempN.getTupleKey())
        except:
            print("Error: No storage node detected")


def reportResults(filename, nodes, files):
    if filename != None:
        try:
            outputFile = open(filename, 'w')
            for f in files:
                if f.assignedNode is None:
                    f.assignedNode = "NULL"
                outputFile.write(f.name + " " + f.assignedNode + "\n")
            outputFile.close()
        except:
            print("Error: Unable to create output file, '", filename, "'")
    else:
        for f in files:
            if f.assignedNode is None:
                f.assignedNode = "NULL"
            print(f.name + " " + f.assignedNode)

def processPromptInput(argv):
    inputFileName = None
    nodeFileName = None
    outputFileName = None

    inputError = False
    if ((len(argv) == 2 and argv[1] == '-h')
            or
            (len(argv) < 2 or len(argv) % 2 == 0 or len(argv) > 7)):
        inputError = True
    elif (len(argv) % 2 == 1):
        for i in range(1, len(argv), 2):
            inputKey = argv[i]
            inputValue = argv[i + 1]

            if not re.match("^\s+$", inputValue):
                if inputKey == '-f':
                    inputFileName = inputValue
                elif inputKey == '-n':
                    nodeFileName = inputValue
                elif inputKey == '-o':
                    outputFileName = inputValue
                else:
                    print("Error: Unrecognized option key '", inputKey, "'")
                    inputError = True
                    break
            else:
                print("Error: No filename is provided")
                inputError = True
                break

        if inputFileName == None or nodeFileName == None:
            print("Error: Both input files for 'files' and 'nodes' are required")
            inputError = True

    if inputError:
        sys.stderr.write("Usage: python -f filename.txt -n filename.txt -o filename.txt(Optional)")
        return -1
    return (inputFileName, nodeFileName, outputFileName)


def main(argv):
    fileReturnTuple = processPromptInput(argv)
    if fileReturnTuple != -1:
        inputFileName = fileReturnTuple[0]
        nodeFileName = fileReturnTuple[1]
        outputFileName = fileReturnTuple[2]

        files = importFiles(inputFileName)
        nodes = importNodes(nodeFileName)

        if nodes != -1 and files != -1:
            planDistribution(nodes, files)
            reportResults(outputFileName, nodes, files)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

