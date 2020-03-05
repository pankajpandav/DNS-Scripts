import boto3
import os
import datetime
import json
import logging
from botocore.exceptions import ClientError

# Setting up Logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m%d%Y %I:%M:%S %p')
logger = logging.getLogger("dns-ns-update")
logger.setLevel(int(os.environ.get("Logging", logging.DEBUG)))
# Setting up Clients
r53 = boto3.client('route53')
r53dns = boto3.client('route53domains', region_name='us-east-1')

def getDomainList():
    try:
        logger.debug(f'### Trying to get the Registered Domains List from Route 53 ###')
        domainlist = []
        p = r53dns.get_paginator('list_domains')
        for page in p.paginate():
            for i in page['Domains']:
                domainname = i['DomainName']
                domainlist.append(domainname)
        logger.debug(" Got the list")
        return domainlist
    except ClientError as err:
        logger.error("Error getting Registered Domain List")

def checkNameServers():
    tocorrectlist = []
    domainlist = getDomainList()
    for d in domainlist:
        dom = r53dns.get_domain_detail(DomainName=d)
        if 'partnerconsole' in dom['Nameservers'][0]['Name']:
            logger.debug(f"{d} has Name Server {dom['Nameservers'][0]['Name']}")
            tocorrectlist.append(d)
    if len(tocorrectlist) > 0:
        logger.debug(" Domain Scanning Completed. Here is the list of domains with incorrect NameServers")
        for i in tocorrectlist:
            print(i)
    else:
        logger.debug("All Good !!")


if __name__ == "__main__":
    checkNameServers()