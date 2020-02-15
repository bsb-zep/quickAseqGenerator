import requests
from lxml import etree

# module settings
# TODO move to global config
bvbrOaiUrl = 'http://bvbr.bib-bvb.de:8991/aleph-cgi/oai/oai_opendata.pl?verb=GetRecord&metadataPrefix=marc21&identifier='

def go(bvId):

    # query single dataset response from oai api
    oaiResponse = requests.get(bvbrOaiUrl + bvId)
    oaiDao = etree.fromstring(oaiResponse.text.encode('utf-8'))

    # loop through leader, control fields and datafield
    try:
        marcEncodedPortion = oaiDao.find(".//metadata", oaiDao.nsmap).getchildren()[0]
    except:
        return False
    
    # only attempts processing if api return seemed valid
    for field in marcEncodedPortion:
        # TODO provide per-field hook
        pass

    # get oai header and extract aleph sys id
    oaiHeader = oaiDao.find('.//header', oaiDao.nsmap)
    rawAlephSysId = oaiHeader.find('identifier', oaiHeader.nsmap).text
    alephSysId = rawAlephSysId[rawAlephSysId.find('BVB01-')+len('BVB01-'):]
    if alephSysId.isdigit():
        return alephSysId
    else:
        return False