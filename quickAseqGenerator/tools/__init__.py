import json
import quickAseqGenerator
import datetime
import sys

# create timestamp
def getTimestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# write log line with timestamp
def logError(logLine):
    with open('error.log', 'a') as logfileDao:
        logfileDao.write(logLine + ' ' + getTimestamp() + '\n')

# handle aseq enrichment line generation from cache
def aseqFromCache(lineParameters):

    # load cache data for lineParameters['bvId']
    cacheResponse = quickAseqGenerator._helper_cacheManager.getFromCache(lineParameters['bvId'])
    if cacheResponse == 'notInCache':
        logError('[CCHERR] ' + lineParameters['bvId'] + ' was not found in cache')
        return False

    # prepare string object for aseq line
    aseqLine = str()

    # check present tags for DHB_DEL
    for tag in cacheResponse['tagged']:
        if 'DHB_DEL'.lower() in tag.lower():
            print('negative tag DHB_DEL* found in ' + lineParameters['bvId'])
            return False

    # check whether desired tag is already present in dataset
    if lineParameters['tagContent'] not in cacheResponse['tagged']:

        # if tag is not yet applied, write line
        aseqLine += cacheResponse['sysId'] + ' 078' + lineParameters['tagLetter'] + '  L $$a'
        aseqLine += lineParameters['tagContent']

        # write log line for enrichment
        logError('[ENRICH] ' + lineParameters['bvId'] + 
                 ' will get "$' + lineParameters['tagLetter'] + 
                 ' ' + lineParameters['tagContent'] + 
                 '" as requested by job "' + lineParameters['jobId'] + '", as of')

        return aseqLine

    else:

        # if tag is already applied
        logError('[PRESNT] ' + lineParameters['bvId'] + ' already has "' +
                 lineParameters['tagContent'] + '" as ' +
                 lineParameters['tagLetter'] + ' tag as requested by job "' +
                 lineParameters['jobId'] + '", no aseq line created')    
        return False