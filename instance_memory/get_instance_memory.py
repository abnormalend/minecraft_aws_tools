#!/usr/bin/python3

import boto3

region = requests.get("http://169.254.169.254/latest/meta-data/placement/region").text
ec2 = boto3.resource('ec2', region_name=region)

response = ec2.client.describe_instance_types(
            InstanceTypes=['t3a.small'],
            Filters=[memory-info.size-in-mib],
            MaxResults = 1))

print(response)
  
