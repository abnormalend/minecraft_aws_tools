#!/usr/bin/python3
import boto3
import requests


instance = requests.get("http://169.254.169.254/latest/meta-data/instance-id").text
myMachine = None
myZone = None
ec2 = boto3.resource('ec2', region_name='us-east-1')
myinstance = ec2.Instance(instance)
for tag in myinstance.tags:
    if tag["Key"] == "dns_hostname":
        myMachine = tag["Value"]
    elif tag["Key"] == "dns_zone":
        myZone = tag['Value']

# If both lookups didn't work, quit
if not (myMachine and myZone):
    print("failed to read tags, unable to update DNS")
    exit(0)

myPublicIP = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4")
myCurrIP = myPublicIP.text

conn53 = boto3.client('route53')
myzone = conn53.list_hosted_zones()
myzoneid = None
for zone in myzone['HostedZones']:
    if zone['Name'] == myZone:
        myzoneid = zone['Id']
if not myzoneid:
    print("Unable to find hosted zone in route53, unable to update DNS")
    exit(1)

response = conn53.change_resource_record_sets(
    HostedZoneId=myzoneid,
    ChangeBatch={
        "Comment": "Automatic DNS update",
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": myMachine + "." + myZone,
                    "Type": "A",
                    "TTL": 180,
                    "ResourceRecords": [
                        {
                            "Value": myCurrIP
                        },
                    ],
                }
            },
        ]
    }
)

print("DNSLOG: " + myMachine + "." + myZone + " updated to " + myCurrIP)
