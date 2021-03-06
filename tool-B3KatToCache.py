# import default libraries
import json
import datetime
import sys
import os
import re

# import custom library
import quickAseqGenerator

# import parallel queue handler
from pymultiprocwrapper.pyMultiprocWrapper import pyMultiprocWrapper as mwprototype

def getTimestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def logError(logLine):
    with open('error.log', 'a') as logfileDao:
        logfileDao.write(logLine + ' ' + getTimestamp() + '\n')

def go(bvId):
    # get sysid
    sysId = quickAseqGenerator._helper_getIntId.go(bvId)
    if sysId == False:
        logError(bvId + ': bad oai answer at') 
        return False

    # get present tags
    presentTags = quickAseqGenerator._helper_parseSru.go(bvId)
    if presentTags == False:
        logError(bvId + ': bad sru answer at')
        return False
    
    # get present LOWs
    presentLows = quickAseqGenerator._helper_getLows.go(bvId)
    if presentLows == False:
        logError(bvId + ': bad sru answer at')
        return False

    # create json cache entry
    cacheEntry = dict()
    cacheEntry['bvId'] = bvId
    cacheEntry['sysId'] = sysId
    cacheEntry['tagged'] = presentTags
    cacheEntry['holdings'] = presentLows
    cacheEntry['asOf'] = str(datetime.datetime.now())
    cacheLine = json.dumps(cacheEntry, indent=3)

    # write to cache
    quickAseqGenerator._helper_cacheManager.writeCacheEntry(bvId, cacheLine)

    # signal successful processing to batch handler
    return True


# TODO syntax check at begin
# TODO add help info like proper cli

# get filename from prompt
inputFileName = sys.argv[1]
blockfileName = 'block--' + re.sub(r'\W+', '', inputFileName)

# get switch for empty queue file after batch
if  sys.argv[2] == 'dodel':
    cleanupQueueAfter = True
else:
    cleanupQueueAfter = False

# get number of parallel queries, use 1 of none set
if len(sys.argv) == 4:
    parallelJobsLimit = int(sys.argv[3])
else:
    parallelJobsLimit = 1

# prepare loop objects
queueArray = list()
keepForNext = list()

# handle queue
queue = list()
with open(inputFileName, 'r') as queueFile:
    for bvId in queueFile.readlines():
        queue.append(bvId)

# function to run on every item in queue
def handleSingleBvid(bvId):
    # cleanup string
    bvId = bvId.lstrip().rstrip()
    if len(bvId) == 0:
        return False
    # handle invalid lines
    if bvId[0] == '#':
        logError(bvId + ' <- this is a comment')
        return False
    if len(bvId) != 11:
        logError(bvId + ' has invalid length')
        return False
    if bvId[0:2] != 'BV':
        logError(bvId + ' has no BV prefix')
        return False
    if bvId[2:].isdigit() == False:
        logError(bvId + ' not only digits after prefix')
        return False
    processingSucess = go(bvId)
    if processingSucess == True:
        with open('queue-processed.bvid', 'a') as processedQueue:
            processedQueue.write(bvId + '\n')
        with open('cache.log', 'a') as logfileDao:
            logfileDao.write(bvId + ' cached at ' + getTimestamp() + '\n')
    else:
        with open('queue-rescheduled.bvid', 'a') as processedQueue:
            processedQueue.write(bvId + '\n')

if __name__ == '__main__':
    mw = mwprototype()
    mw.registerQueue(queue)
    mw.setParallelLimit(parallelJobsLimit)
    mw.registerFunction(handleSingleBvid )
    mw.launch()

# reset inbox queue file if switch
if cleanupQueueAfter:
    with open(inputFileName, 'w') as queue:
        queue.write('')