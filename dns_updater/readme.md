# DNS Updater
This script will read a target hostname/zone from ec2 tags, and update that record with the public IP address of the instance.

## Requirements
- boto3
- requests
- permissions to read instance tags, and permission to update dns record in the zone
