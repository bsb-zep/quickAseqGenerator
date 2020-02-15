import json

# configure cache dir relative to current path
cacheDir = './bvCache/'

def writeCacheEntry(bvId, cacheLine):
    with open(cacheDir + bvId, 'w') as cacheEntryDao:
        cacheEntryDao.write(cacheLine)