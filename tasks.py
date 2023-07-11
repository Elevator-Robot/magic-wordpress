import os
from invoke import tasks


@tasks.task(
    help={
        "dev": "Install development dependencies.",
    }
)
def setup(c, dev=False):
    """
    Setup the project.

    Args:
        dev (bool): Install development dependencies.
    """
    venv_exists = os.path.exists(".venv")
    if not venv_exists:
        c.run("python3 -m venv .venv")
    c.run(".venv/bin/pip install -r requirements.txt")
    if dev:
        c.run(".venv/bin/pip install -r requirements-dev.txt")
    if not venv_exists:
        print(
            """
        To activate the virtual environment, run:
        source .venv/bin/activate
            """
        )


@tasks.task
def test(c):
    """
    Run tests.
    """
    c.run("pytest -v")


@tasks.task(
    help={
        "yes": "Skip confirmation and destroy the app.",
    }
)
def deploy(c, yes=False):
    """
    Deploy the app.
    """
    c.run("cdk synth")
    if not yes:
        user_input = input("Do you want to deploy? (y/n): ")
        if user_input.lower() != "y":
            print("Deployment canceled by user.")
            return
        print("Deploying...")
        c.run("cdk deploy --require-approval never")
    elif yes:
        print("Deploying...")
        c.run("cdk deploy --require-approval never")


@tasks.task(
    help={
        "yes": "Skip confirmation and destroy the app.",
    }
)
def destroy(c, yes=False):
    """
    Destroy the app.
    """
    if not yes:
        user_input = input(
            "Are you absolutely sure that you want to destroy your app? (y/n): "
        )
        if user_input.lower() != "y":
            print("Destroy canceled by user.")
            return
        print("Destroying...")
        c.run("cdk destroy --require-approval never --force")
    elif yes:
        print("Destroying...")
        c.run("cdk destroy --require-approval never --force")
