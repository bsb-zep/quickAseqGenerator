import json
import quickAseqGenerator
import datetime
import sys


def getTimestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def logError(logLine):
    with open('error.log', 'a') as logfileDao:
        logfileDao.write(logLine + ' ' + getTimestamp() + '\n')

def aseqFromCache(argvDao):
    bvId = argvDao[1]
    tagType = argvDao[2]
    tagStr = argvDao[3]
    jobId = argvDao[4]

    cacheResponse = quickAseqGenerator._helper_cacheManager.getFromCache(bvId)
    aseqLine = str()
    if cacheResponse == False:
        logError(bvId + ' returned cache error')
    else:
        if tagStr not in cacheResponse['tagged']:
            aseqLine += cacheResponse['sysId'] + ' 078' + tagType + '  L $$a'
            aseqLine += tagStr
            with open('jobs/' + jobId + '.aseq', 'a') as jobOutfile:
                jobOutfile.write(aseqLine + '\n')
            logError(bvId + ' will get "$' + tagType + ' ' + tagStr + '", as of')
            return True
        else:
            logError(bvId + ' already has "' + tagStr + '" as ' + tagType + ' tag, no aseq line')
            return False