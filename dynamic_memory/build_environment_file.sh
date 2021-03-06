#!/bin/bash
INSTANCE_TYPE=$(curl http://169.254.169.254/latest/meta-data/instance-type)
REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/region)

SYSTEM_MEMORY=$(aws ec2 describe-instance-types --region=$REGION --instance-types 't3a.small' --query 'InstanceTypes[0].MemoryInfo.SizeInMiB')
RESERVED_MEMORY="1024"
MAXMEM=$(expr $SYSTEM_MEMORY - $RESERVED_MEMORY)
MAXMEMUNIT="M"
MCMAXMEM=$MAXMEM$MAXMEMUNIT

echo "MCMAXMEM=$MCMAXMEM" > /opt/minecraft/server/server.conf
echo "MCMINMEM=512M"  >> /opt/minecraft/server/server.conf
echo "SHUTDOWN_DELAY=5"  >> /opt/minecraft/server/server.conf
echo "POST_SHUTDOWN_DELAY=10" >> /opt/minecraft/server/server.conf
