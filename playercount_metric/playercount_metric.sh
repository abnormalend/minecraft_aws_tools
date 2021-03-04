#!/bin/bash
REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/region)
active_players=$(/usr/local/bin/mcstatus localhost status|grep players|sed -e 's/^players: \([0-9]*\)\/\([0-9]*\).*/\1/g')
max_players=$(/usr/local/bin/mcstatus localhost status|grep players|sed -e 's/^players: \([0-9]*\)\/\([0-9]*\).*/\2/g')
aws --region $REGION cloudwatch put-metric-data --metric-name active_players --namespace Minecraft --unit Count --value $active_players --dimensions minecraft_server=minecraft/JavaSurvival-1
aws --region $REGION cloudwatch put-metric-data --metric-name max_players --namespace Minecraft --unit Count --value $max_players --dimensions minecraft_server=minecraft/JavaSurvival-1
