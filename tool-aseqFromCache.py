import json
import quickAseqGenerator
import datetime


def getTimestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def logError(logLine):
    with open('error.log', 'a') as logfileDao:
        logfileDao.write(logLine + ' ' + getTimestamp() + '\n')

bvId = 'BV019876401'
nString = 'DHB'
qString = 'DHB_IFZ_BIBLIO_2007'

cacheResponse = quickAseqGenerator._helper_cacheManager.getFromCache(bvId)
if cacheResponse == False:
    logError(bvId + ' returned cache error')
else:
    print(cacheResponse)
    aseqLines = list()
    if nString not in cacheResponse['tagged']:
        aseqLine = str()
        aseqLine += cacheResponse['sysId'] + ' 078n  L $$a'
        aseqLine += nString
        aseqLines.append(aseqLine)
    else:
        logError(bvId + 'is already tagged "' + nString + '", no aseq line')

    if qString not in cacheResponse['tagged']:
        aseqLine = str()
        aseqLine += cacheResponse['sysId'] + ' 078q  L $$a'
        aseqLine += qString
        aseqLines.append(aseqLine)
    else:
        logError(bvId + 'is already tagged "' + qString + '", no aseq line')

print(aseqLines)