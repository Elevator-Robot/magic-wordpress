from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)


class MagicWordpressStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, 'vpc',
            cidr = '10.0.0.0/16',
            max_azs = 2,
            enable_dns_hostnames = True,
            enable_dns_support = True, 
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name = 'public-subnet',
                    subnet_type = ec2.SubnetType.PUBLIC,
                    cidr_mask = 24
                ),
                ec2.SubnetConfiguration(
                    name = 'app-subnet',
                    subnet_type = ec2.SubnetType.PRIVATE,
                    cidr_mask = 24
                ),
                ec2.SubnetConfiguration(
                    name = 'data-subnet',
                    subnet_type = ec2.SubnetType.ISOLATED,
                    cidr_mask = 24
                )
            ],
            nat_gateways = 1,
        )

        
