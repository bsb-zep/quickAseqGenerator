import quickAseqGenerator
import sys


# import default libraries
import json
import datetime
import sys
import os
import re

# import custom library
import quickAseqGenerator

# run from repo root
# python cli-batchAseqFromCache.py [input filename] [n/q] [new field value] [job description]

# TODO syntax check at begin
# TODO add help info like proper cli

# get filename from prompt
inputFileName = sys.argv[1]
blockfileName = 'block--' + re.sub(r'\W+', '', inputFileName)

tagType = sys.argv[2]
tagStr = sys.argv[3]
jobId = sys.argv[4]

# get switch for empty queue file after batch
if sys.argv[2] == 'nodel':
    cleanupQueueAfter = False
elif sys.argv[2] == 'dodel':
    cleanupQueueAfter = True

def getTimestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def logError(logLine):
    with open('error.log', 'a') as logfileDao:
        logfileDao.write(logLine + ' ' + getTimestamp() + '\n')
    print('line added to error log')

def go(bvId):
    argvDao = dict()
    argvDao[1] = bvId
    argvDao[2] = tagType
    argvDao[3] = tagStr
    argvDao[4] = 'pythonReturn'
    argvDao[5] = jobId

    cacheResponse = quickAseqGenerator._helper_cacheManager.getFromCache(bvId)
    if cacheResponse == False:
        logError(bvId + ' is not in cache, skipping')
        return False
    if 'DHB' in cacheResponse['tagged']:
        logError(bvId + ' already has 078n $aDHB, no new 078q added in onlyFresh mode although requested by job ' + str(jobId))
    else:
        aseqLine = quickAseqGenerator.tools.aseqFromCache(argvDao)
        if aseqLine != False:
            with open('jobs/' + jobId + '.aseq', 'a') as jobOutfile:
                jobOutfile.write(aseqLine + '\n')


# set blockfile
with open(blockfileName, 'w') as blockfileDao:
    blockfileDao.write('!?')

# prepare loop objects
queueArray = list()
keepForNext = list()

# handle queue
linesResultContainer = list()
with open(inputFileName, 'r') as queue:
    for bvId in queue.readlines():
        # cleanup string
        bvId = bvId.lstrip().rstrip()
        if len(bvId) == 0:
            continue
        # handle invalid lines
        if bvId[0] == '#':
            logError(bvId + ' <- this is a comment')
            continue
        if len(bvId) != 11:
            logError(bvId + ' has invalid length')
            continue
        if bvId[0:2] != 'BV':
            logError(bvId + ' has no BV prefix')
            continue
        if bvId[2:].isdigit() == False:
            logError(bvId + ' not only digits after prefix')
            continue
        go(bvId)

os.remove(blockfileName)