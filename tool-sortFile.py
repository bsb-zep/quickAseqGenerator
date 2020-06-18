import sys

# load command line parameter as input file name
inputFileName = sys.argv[1]

# prepare lists for sorting and sysid counting
duplicateCheckList = list()
sysidlist = list()

# read aseq source files
with open(inputFileName, 'r') as inputAseqLines:

    # process every source lin
    for currentSourceLine in inputAseqLines:

        # check whether identical source line was already processed
        if currentSourceLine not in duplicateCheckList:
            # if line is not know yet, append to deduplicated array
            duplicateCheckList.append(currentSourceLine)


    with open(inputFileName + '.sorted2', 'a') as jobOutfile:

        for deduplicatedLine in sorted(duplicateCheckList):
            # add sysid from accepted line to sysid list, if not yet known
            sysid = deduplicatedLine[0:9]
            if sysid not in sysidlist:
                sysidlist.append(sysid)

            # if maximum sysid parameter given, stop processing after given sysid
            if len(sys.argv) == 3:
                if len(sysidlist) == int(sys.argv[2]):
                    print('reached maximum number of changed sysids: ' + str(sys.argv[2]))
                    break
            jobOutfile.write(deduplicatedLine)
    
    # output number sysids changed
    print('total number of datasets changed: ' + str(len(sysidlist)))