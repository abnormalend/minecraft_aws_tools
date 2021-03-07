#!/bin/bash

backup_src="/opt/minecraft/server/backups"
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
INSTANCE_TYPE=$(curl -s http://169.254.169.254/latest/meta-data/instance-type)
REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/region)

latestbackup=$(ls -Art $backup_src | tail -n 1)
s3_src=$(aws ec2 describe-instances --region=$REGION --instance-ids $INSTANCE_ID --query 'Reservations[].Instances[].Tags[?Key==`s3_backup_url`].Value' --output text)
backup_name=$(aws ec2 describe-instances --region=$REGION --instance-ids $INSTANCE_ID --query 'Reservations[].Instances[].Tags[?Key==`dns_hostname`].Value' --output text)
aws s3 cp $s3_src/$backup_name.zip /tmp/$backup_name.zip
unzip -u /tmp/$backup_name.zip -d /opt/minecraft/server
