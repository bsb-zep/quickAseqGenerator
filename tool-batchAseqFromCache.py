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

tagLetter = sys.argv[2]
tagContent = sys.argv[3]
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

def go(bvId):
    lineParameters = dict()
    lineParameters['bvId'] = bvId
    lineParameters['tagLetter'] = tagLetter
    lineParameters['tagContent'] = tagContent
    lineParameters['jobId'] = jobId
    generatedLine = quickAseqGenerator.tools.aseqFromCache(lineParameters)
    if isinstance(generatedLine, str):
        with open('jobs/' + jobId + '.aseq', 'a') as jobOutfile:
            jobOutfile.write(generatedLine + '\n')


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
        if len(bvId) == 0: # skip empty lines
            continue
        # handle invalid lines
        if bvId[0] == '#': # comment
            continue
        if len(bvId) != 11: # invalid length of BV id
            continue
        if bvId[0:2] != 'BV': # missing BV prefix
            continue
        if bvId[2:].isdigit() == False: # not numerical after prefix
            continue
        go(bvId)

# remove blockfile
os.remove(blockfileName)