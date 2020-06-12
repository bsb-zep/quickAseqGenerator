import sys


inputFileName = sys.argv[1]

duplicateCheckList = list()
with open(inputFileName, 'r') as inputAseqLines:
    for currentSourceLine in inputAseqLines:
        if currentSourceLine not in duplicateCheckList:
            duplicateCheckList.append(currentSourceLine)

with open(inputFileName + '.sorted2', 'a') as jobOutfile:
    for line in sorted(duplicateCheckList):
        jobOutfile.write(line)