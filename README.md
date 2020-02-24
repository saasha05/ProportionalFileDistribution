# Proportional File Distribution

_ACS Programming Challenge_

**Description**: A program to distribute files into node buckets in a proportional manner.
Takes input for files and their sizes, as well as nodes and their capacity.
Produces output into an output file which determines which files go into which node.

**Usage**: ProportionalFileDistribution.py -f filename.txt -n nodesname.txt -o outputfile.txt(optional)

**Input Files**
files.txt:
```
# filename size
tom.dat 1024
jerry.dat 16553
tweety.out 12345
elmerfudd.txt 987654321
```
nodes.txt:
```
# node-name available-space
node1 65536
node2 32768
```

output.txt:
```
tom.dat node1
tweety.out node1
jerry.dat node2
```
elmerfudd.txt NULL
