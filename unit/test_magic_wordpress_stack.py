import aws_cdk as core
import aws_cdk.assertions as assertions
from stacks.magic_wordpress_stack import MagicWordpressStack


def test_ecs_cluster_created():
    app = core.App()
    stack = MagicWordpressStack(app, "magic-wordpress")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::ECS::Cluster", 1)


def test_ecs_task_definition_created():
    app = core.App()
    stack = MagicWordpressStack(app, "magic-wordpress")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::ECS::TaskDefinition", 1)


# def test_ecs_service_created():
#     app = core.App()
#     stack = MagicWordpressStack(app, "magic-wordpress")
#     template = assertions.Template.from_stack(stack)

#     template.resource_count_is("AWS::ECS::Service", 1)
