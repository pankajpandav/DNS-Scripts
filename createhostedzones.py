import boto3
import os
import datetime
import json
import logging
import time
from botocore.exceptions import ClientError

# Setting up Logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m%d%Y %I:%M:%S %p')
logger = logging.getLogger("dns-ns-update")
logger.setLevel(int(os.environ.get("Logging", logging.DEBUG)))

# defining the domain names and clients required
domainnames = ['stocklandliving.com.au','siennawood.com.au','siennawood.com','stocklandhomefinance.com','vertu.com.au','stocklandretire.com.au','stocklandtownsville.com.au','ingleburnlogisticspark.com.au','macarthurgardens.com.au','stocklandinvestmentproperty.com.au'] # You can give list of domain names for which you need to update NameServers
r53 = boto3.client('route53')
#r53dns = boto3.client('route53domains')

def create_hosted_zones():
    for domainname in domainnames:
        logger.debug(f"### Creation of Hosted Zone - {domainname} ####")
        now = datetime.datetime.now()
        logger.debug(f"Current Time is {now.strftime('%Y%m%d%H%M%S')}")
        try:
            response = r53.create_hosted_zone(
                Name=str(domainname),
                CallerReference = now.strftime("%Y%m%d%H%M%S")
            )
            logger.info(json.dumps(response, default=str))
            time.sleep(1)
        except ClientError as err:
            logger.error("Error Occurred during Hosted Zone creation")
            logger.error(err)

if __name__ == "__main__":
    create_hosted_zones()
