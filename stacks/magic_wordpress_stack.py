from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_resourcegroups as resourcegroups,
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
                    name="public-",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="app-",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="data-",
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
            container_insights=True,
        )

        task_definition = ecs.TaskDefinition(
            self,
            "ecs-task",
            compatibility=ecs.Compatibility.EC2,
            network_mode=ecs.NetworkMode.AWS_VPC,
        )
        task_definition.add_container(
            "wordpress-container",
            image=ecs.ContainerImage.from_registry(
                "public.ecr.aws/bitnami/wordpress:latest"
            ),
        )

        # ecs.Ec2Service(
        #     self,
        #     "ecs-service",
        #     cluster=ecs_cluster,
        #     task_definition=task_definition,
        #     desired_count=1,
        # )

        resourcegroups.CfnGroup(
            self,
            "resource-group",
            name="magic-wordpress",
            resource_query=resourcegroups.CfnGroup.ResourceQueryProperty(
                type="CLOUDFORMATION_STACK_1_0",
            ),
        )
