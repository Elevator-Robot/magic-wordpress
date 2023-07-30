from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_resourcegroups as resourcegroups,
    # CfnParameter,
    CfnOutput,
    aws_rds as rds,
    aws_iam as iam,
    # aws_secretsmanager as secretsmanager,
)


class MagicWordpressStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Setup any Parameters
        # tag_env_param = CfnParameter(
        #     self,
        #     "env-parameter",
        #     type="String",
        #     description="Environment name to be used for tagging",
        #     default="dev",
        #     allowed_values=["dev", "qa", "prod"],
        # )
        # tag_project_param = CfnParameter(
        #     self,
        #     "project-parameter",
        #     type="String",
        #     description="Environment name to be used for tagging",
        #     default="MagicWordpress",
        # )

        # Setup Tags

        # self.tags.set_tag("Environment", tag_env_param.value_as_string)
        # self.tags.set_tag("Project", tag_project_param.value_as_string)

        # Setup ResourceGroup for tagging and organizing resources
        resourcegroups.CfnGroup(
            self,
            "resource-group",
            name="magic-wordpress",
            resource_query=resourcegroups.CfnGroup.ResourceQueryProperty(
                type="CLOUDFORMATION_STACK_1_0",
            ),
        )

        # Setup VPC

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

        secrets = rds.Credentials.from_generated_secret(
            username="pgadmin",
            secret_name="postgressCredentials",
        )

        db_cluster = rds.DatabaseCluster(
            self,
            "Database",
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.VER_15_2
            ),
            credentials=secrets,
            default_database_name="wordpress",
            writer=rds.ClusterInstance.serverless_v2("writer"),
            readers=[
                rds.ClusterInstance.serverless_v2("reader"),
            ],
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                one_per_az=True,
            ),
            vpc=vpc,
        )

        # ecs_cluster = ecs.Cluster(
        #     self,
        #     "ecs-cluster",
        #     vpc=vpc,
        #     cluster_name="magic-wordpress",
        #     capacity=ecs.AddCapacityOptions(
        #         instance_type=ec2.InstanceType("t3.micro"),
        #         vpc_subnets=ec2.SubnetSelection(
        #             subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
        #             one_per_az=True,
        #         ),
        #     ),
        #     container_insights=True,
        # )

        # secrets.grant_read(ecs_cluster.task_execution_role)

        # task_definition = ecs.TaskDefinition(
        #     self,
        #     "ecs-task",
        #     compatibility=ecs.Compatibility.EC2,
        #     network_mode=ecs.NetworkMode.AWS_VPC,
        # )
        # container = task_definition.add_container(
        #     "wordpress-container",
        #     image=ecs.ContainerImage.from_registry(
        #         # "public.ecr.aws/bitnami/wordpress:latest"
        #         "public.ecr.aws/bitnami/nginx:latest"
        #     ),
        #     memory_reservation_mib=512,
        #     cpu=256,
        #     logging=ecs.LogDrivers.aws_logs(
        #         stream_prefix="wordpress-container"
        #     ),
        #     secrets={
        #         "WORDPRESS_DATABASE_HOST": ecs.Secret.from_secrets_manager(
        #             secrets, "host"
        #         ),
        #         "WORDPRESS_DATABASE_NAME": ecs.Secret.from_secrets_manager(
        #             secrets, "dbname"
        #         ),
        #         "WORDPRESS_DATABASE_USER": ecs.Secret.from_secrets_manager(
        #             secrets, "username"
        #         ),
        #         "WORDPRESS_DATABASE_PASSWORD": ecs.Secret.from_secrets_manager(
        #             secrets, "password"
        #         ),
        #     },
        # )
        # container.add_port_mappings(
        #     ecs.PortMapping(container_port=8080, host_port=8080)
        # )
        # container.add_port_mappings(
        #     ecs.PortMapping(container_port=8443, host_port=8443)
        # )

        # ecs.Ec2Service(
        #     self,
        #     "ecs",
        #     cluster=ecs_cluster,
        #     task_definition=task_definition,
        #     desired_count=1,
        # )

        CfnOutput(
            self,
            "database-endpoint",
            value=db_cluster.cluster_endpoint.hostname,
            description="Database Endpoint",
        )
