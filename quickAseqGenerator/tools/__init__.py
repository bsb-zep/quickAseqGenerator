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
    if cacheResponse == 'notInCache':
        logError(bvId + ' was not found in cache')
    else:
        if tagStr not in cacheResponse['tagged']:
            aseqLine += cacheResponse['sysId'] + ' 078' + tagType + '  L $$a'
            aseqLine += tagStr
            if 5 in argvDao.keys():
                logError(bvId + ' will get "$' + tagType + ' ' + tagStr + '" as requested by job "' + argvDao[5] + '", as of')
            else:
                logError(bvId + ' will get "$' + tagType + ' ' + tagStr + '", as of')
            if jobId == 'pythonReturn':
                return aseqLine
            else:
                with open('jobs/' + jobId + '.aseq', 'a') as jobOutfile:
                    jobOutfile.write(aseqLine + '\n')
                return True
        else:
            if 5 in argvDao.keys():
                logError(bvId + ' already has "' + tagStr + '" as ' + tagType + ' tag as requested by job "' + argvDao[5] + '", no aseq line created')    
            else:
                logError(bvId + ' already has "$' + tagType + ' ' + tagStr + '", no aseq line created')
            return False