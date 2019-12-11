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

# defining the domain names and clients required
domainnames = ['everythingiknow.net'] # You can give list of domain names for which you need to update NameServers
r53 = boto3.client('route53')
r53dns = boto3.client('route53domains')

def update_dns_nameservers():
    for domainname in domainnames:
        logger.debug(f"### Hosted Zone - {domainname}  ###")
        try:
            logger.debug(f"Getting Hosted Zone ID for {domainname}")
            hostedzones = r53.list_hosted_zones_by_name(DNSName = str(domainname))
            junk,junk,hostedzoneid = (hostedzones['HostedZones'][0]['Id']).split('/')
            logger.debug(f"Hosted Zone ID is - {hostedzoneid}")
        except ClientError as err:
            logger.error("Error Getting Hosted Zone ID")
            logger.error(err)

        logger.debug(f"Getting Name Server Information from Hosted Zone ID: {hostedzoneid} for {domainname}")
        try:
            nsinfo = r53.get_hosted_zone(Id=hostedzoneid)
            logger.info(json.dumps(nsinfo, default=str))
            nservers = nsinfo['DelegationSet']['NameServers']
            logger.debug(f"Name Servers for {domainname} are : {nservers}")
        except ClientError as err:
            logger.error("Error getting Name Servers List")
            logger.error(err)
        
        logger.debug(f"Updating Registered Domain Name Server for {domainname}")
        try:
            response = r53dns.update_domain_nameservers(
                DomainName= domainname,
                Nameservers= [ {
                    'Name': str(nservers[0])},
                    {
                    'Name': str(nservers[1])},
                    {
                    'Name': str(nservers[2])},
                    {
                    'Name': str(nservers[3])
                    }]
            )
            print(response)
        except ClientError as err:
            logger.error(f"Caught Error at Updating the name servers for {domainname}")
            logger.error(err)

if __name__ == "__main__":
    update_dns_nameservers()
