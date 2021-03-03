#!/usr/bin/python3

import requests
import boto3
from os import listdir
from os.path import isfile, join
import re

def install_paper(mc_version, paper_build):
    """This will download the paper jar"""
    url = "https://papermc.io/api/v2/projects/paper"
    mc_version = requests.get(url).json()['versions'][-1] if mc_version is None or mc_version is "latest" else mc_version
    paper_build = requests.get("{url}/versions/{version}".format(url = url, version = mc_version)).json()['builds'][-1] if paper_build is None or paper_build is "latest" else paper_build
    download = requests.get("{url}/versions/{version}/builds/{build}/downloads/paper-{version}-{build}.jar".format(url = url, version = mc_version, build = paper_build))
    open(join(minecraft_path,"paper-{version}-{build}.jar".format(version = mc_version, build = paper_build)), 'wb').write(download.content)
    
    # Now update the tags
    response = instance.create_tags(Tags=[
            {'Key': 'mc_version', 'Value': mc_version },
            {'Key': 'mc_paper_build', 'Value': str(paper_build) }])
    

minecraft_path = "/opt/minecraft/server"
instance_id = requests.get("http://169.254.169.254/latest/meta-data/instance-id").text
region = requests.get(" http://169.254.169.254/latest/meta-data/placement/region").text
ec2 = boto3.resource('ec2', region_name = region)
instance = ec2.Instance(instance_id)

# Search the tags for the minecraft version we are targetting
try:
    target_minecraft_version = next(t["Value"] for t in instance.tags if t["Key"] == "mc_version")
except StopIteration:
    target_minecraft_version = None

# Check and see if we've already got a build defined.
try:
    current_paper_build = next(t["Value"] for t in instance.tags if t["Key"] == "mc_paper_build")
except StopIteration:
    current_paper_build = None

# Get the filename of paper on the system
try:  
    paper_file = next(f for f in listdir(minecraft_path) if isfile(join(minecraft_path, f)) and "paper" in f and "jar" in f)
except StopIteration:
    paper_file = None
    
if not paper_file:
    # Hey, we don't have a paper file installed, so this must be a new build of the minecraft server!
    print("New paper install")
    install_paper(target_minecraft_version, current_paper_build)
else:
    # We've already got a file, so we're going to look at what we need to do.
    print("Paper already installed, let's see if we need to re-install anything")
    p = re.compile(r'paper-(?P<version>[0-9.]+)-(?P<build>[0-9]+).jar')
    m = p.search(paper_file)
    installed_version = m.group('version')
    installed_build =  m.group('build')
    
    if target_minecraft_version == installed_version:
        # We already have the same version, let's see if we need to do anything with the build
        print("minecraft version is current")
        if current_paper_build == installed_build:
            print("paper build is current, nothing to do")
        else:
            print("paper build is NOT current, updating the build")
            install_paper(target_minecraft_version, current_paper_build)
    else:
        # The version isn't the same, we need to download a new one
        print("minecraft version is NOT current")
        install_paper(target_minecraft_version, current_paper_build)
        
    

    
