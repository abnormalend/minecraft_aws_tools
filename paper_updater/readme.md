# Paper Updater

This script will automatically download a version of paper (latest if no tags set) and then update your instance tags to mark the current version.  If run on reboot it can be used to check that the deployed version is still correct, or pull a new one if desired.

## Requirements
- Python modules boto3 and requests
- Permission to read ec2instances and update tags (described below)

## Role permissions
The following CDK will grant the instance permission to update it's own tags.  If not using CDK a similar policy can be made in IAM.

    minecraft_server_arn = core.Stack.of(self).format_arn(service="ec2", resource="instance", resource_name= minecraft_server.instance_id )
        
    role.attach_inline_policy(iam.Policy(self, "EC2 self access", statements = [iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                          resources=[minecraft_server_arn],
                                          actions=["ec2:*"]),
                                          iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                          resources=["*"],
                                          actions=["ec2:Describe*"])]))
