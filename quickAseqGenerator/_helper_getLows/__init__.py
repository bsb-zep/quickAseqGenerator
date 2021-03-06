import requests
from lxml import etree
import datetime
import time

# module settings
# TODO move to global config
bvbrSruUrl = 'http://bvbr.bib-bvb.de:5661/bvb01sru?version=1.1&recordSchema=marcxml&operation=searchRetrieve&maximumRecords=1&query=marcxml.idn='

def getTimestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def logError(logLine):
    with open('error.log', 'a') as logfileDao:
        logfileDao.write(logLine + ' ' + getTimestamp() + '\n')
    print('line added to error log')

def go(bvId):

    # query single dataset response from oai api
    try:
        sruResponse = requests.get(bvbrSruUrl + bvId)
    except requests.exceptions.RequestException as e:
        logError('connection error: ' + str(e) + ' at' )
        time.sleep(3)
        return False

    sruDao = etree.fromstring(sruResponse.text.encode('utf-8'))

    # loop through leader, control fields and datafield
    try:
        marcEncodedPortion = sruDao.find(".//zs:recordData", sruDao.nsmap).getchildren()[0]
    except:
        return False
    presentLows = list()
    for field in marcEncodedPortion:
        if field.get('tag') == '049' and field.get('ind1') == ' ' and field.get('ind2') == ' ':
            subfields = field.findall(".//subfield", field.nsmap)
            for subfield in subfields:
                if subfield.get('code') == 'a':
                    presentLows.append(subfield.text)
    return presentLows