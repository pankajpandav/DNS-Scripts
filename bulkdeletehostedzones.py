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
domainnames = ['cardinalrsvp.com.au','caloundrasouthhallscreek.com.au','cardinalfreeman.com.au','vertu.com.au','riverstonecrossing.com.au','stocklandretire.com.au','mccauleysbeach.com.au','valewa.com.au','townside.com.au','oceansidekawana.com.au','oceansidekawana.com','oceansidesunshinecoast.com','farringtongrove.com.au','northlakesbusiness.com.au','northlakesbusinesspark.com.au','stocklandcardinalfreeman.com.au','whitemanedge.com.au','backyardbonus.com','pointcook.com.au','stocklandtownsville.com.au','watersidecorporate.com.au','ingleburnlogisticspark.com.au','stocklandcorporatereporting2014.com.au','corimbia.com.au','stockland-iscope.com.au','willowdaleretire.com.au','siennawoods.com.au','hundredhills.com.au','sandonpointplanning.com.au','waterfrontpl.com.au','arvehomes.com','stocklandpointlonsdale.com','stocklandcammeray.com.au','macarthurgardens.com.au','stocklandpointlonsdale.com.au','stocklandinvestmentproperty.com.au','portadelaidedc.com.au'] # You can give list of domain names for which you need to update NameServers
r53 = boto3.client('route53')
#r53dns = boto3.client('route53domains')

def delete_hosted_zones():
    for domainname in domainnames:
        logger.debug(f"### Deletion of Hosted Zone - {domainname} ###")
        try:
            logger.debug(f"Getting Hosted Zone ID for {domainname}")
            hostedzones = r53.list_hosted_zones_by_name(DNSName = str(domainname))
            junk,junk,hostedzoneid = (hostedzones['HostedZones'][0]['Id']).split('/')
            logger.debug(f"Hosted Zone ID is - {hostedzoneid}")
            response = r53.delete_hosted_zone(
                Id=hostedzoneid
            )
            logger.info(json.dumps(response, default=str))
        except ClientError as err:
            logger.error(f"Problem deleting the hosted zone - {domainname}")
            logger.error(err)

if __name__ == "__main__":
    delete_hosted_zones()