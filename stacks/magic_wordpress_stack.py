from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
)


class MagicWordpressStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            "vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public-subnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="app-subnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="data-subnet",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24,
                ),
            ],
            nat_gateways=1,
        )

        ecs_cluster = ecs.Cluster(
            self,
            "ecs-cluster",
            vpc=vpc,
            cluster_name="magic-wordpress",
            capacity=ecs.AddCapacityOptions(
                instance_type=ec2.InstanceType("t3.micro"),
                desired_capacity=1,
                min_capacity=1,
                max_capacity=2,
                vpc_subnets=ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
            ),
        )

        task_definition = ecs.TaskDefinition(
            self,
            "wordpress-task",
            compatibility=ecs.Compatibility.EC2,
            network_mode=ecs.NetworkMode.AWS_VPC,
        )
        task_definition.add_container(
            "wordpress-container",
            image=ecs.ContainerImage.from_registry("bitnami/wordpress"),
            memory_limit_mib=1024,
        )

        ecs.Ec2Service(
            self,
            "wordpress-service",
            cluster=ecs_cluster,
            task_definition=task_definition,
            desired_count=1,
        )
