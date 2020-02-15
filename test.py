import quickAseqGenerator
import json
import datetime

def getTimestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def logError(logLine):
    with open('error.log', 'a') as logfileDao:
        logfileDao.write(logLine + ' ' + getTimestamp() + '\n')
    print('line added to error log')

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

    # create json cache entry
    cacheEntry = dict()
    cacheEntry['bvId'] = bvId
    cacheEntry['sysId'] = sysId
    cacheEntry['tagged'] = presentTags
    cacheEntry['asOf'] = str(datetime.datetime.now())
    cacheLine = json.dumps(cacheEntry, indent=3)
    print(cacheLine)

    # write to cache
    quickAseqGenerator._helper_cacheManager.writeCacheEntry(bvId, cacheLine)

    # signal successful processing to batch handler
    return True


queueArray = list()
keepForNext = list()
with open('queue-inbox.bvid', 'r') as queue:
    for bvId in queue.readlines():
        bvId = bvId.lstrip().rstrip()
        if len(bvId) == 0:
            continue
        print('')
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
        # TODO validate BVID formally before trying to process
        processingSucess = go(bvId)
        if processingSucess == True:
            with open('queue-processed.bvid', 'a') as processedQueue:
                processedQueue.write(bvId + '\n')
            with open('cache.log', 'a') as logfileDao:
                logfileDao.write(bvId + ' cached at ' + getTimestamp() + '\n')
        else:
            with open('queue-rescheduled.bvid', 'a') as processedQueue:
                processedQueue.write(bvId + '\n')
