#!/bin/bash aws ec2 describe-instance-types --region=$REGION --instance-types 't3a.small' --query 'InstanceTypes[0].MemoryInfo.SizeInMiB'
