#!/usr/bin/env python3

import aws_cdk as cdk

from stacks.magic_wordpress_stack import MagicWordpressStack


app = cdk.App()
MagicWordpressStack(app, "magic-wordpress")

app.synth()
