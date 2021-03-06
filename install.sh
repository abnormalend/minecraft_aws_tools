#!/bin/bash

# Install DNS Update
cp  $MINECRAFT_TOOLS_HOME/dns_updater/crontab /etc/cron.d/dnsupdater

# Install metrics collector
cp $MINECRAFT_TOOLS_HOME/playercount_metric/crontab /etc/cron.d/minecraftmetrics

# Install paper updater
cp $MINECRAFT_TOOLS_HOME/paper_updater/crontab /etc/cron.d/paperupdater

# Install dynamic memory
cp $MINECRAFT_TOOLS_HOME/dynamic_memory/crontab /etc/cron.d/dynamicmemory
