#!/bin/bash

# Install DNS Update
cp $MINECRAFT_HOME/minecraft_aws_tools/dns_updater/crontab /etc/cron.d/dnsupdater

# Install metrics collector
cp $MINECRAFT_HOME/minecraft_aws_tools/playercount_metric/crontab /etc/cron.d/minecraftmetrics

# Install paper updater
cp $MINECRAFT_HOME/minecraft_aws_tools/paper_updater/crontab /etc/cron.d/paperupdater
