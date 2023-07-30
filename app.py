#!/usr/bin/env python3

import aws_cdk as cdk
import os

from stacks.magic_wordpress_stack import MagicWordpressStack


app = cdk.App()
MagicWordpressStack(
    app,
    "magic-wordpress",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    },
)

app.synth()
