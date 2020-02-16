import json

# configure cache dir relative to current path
cacheDir = './bvCache/'

def writeCacheEntry(bvId, cacheLine):
    with open(cacheDir + bvId, 'w') as cacheEntryDao:
        cacheEntryDao.write(cacheLine)

def getFromCache(bvId):
    try:
        with open(cacheDir + bvId, 'r') as cacheEntryDao:
            cacheContent = json.load(cacheEntryDao)
        return cacheContent
    except FileNotFoundError:
        print('bvId not in cache')
        return False