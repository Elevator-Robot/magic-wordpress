import os
from invoke import tasks


@tasks.task
def setup(c):
    venv_exists = os.path.exists(".venv")
    if not venv_exists:
        c.run("python3 -m venv .venv")
    c.run(".venv/bin/pip install -r requirements.txt")
    if not venv_exists:
        print(
            """
        To activate the virtual environment, run:
        source .venv/bin/activate
            """
        )


@tasks.task
def test(c):
    c.run("pytest -v")


@tasks.task
def deploy(c):
    c.run("cdk synth")
    user_input = input("Do you want to deploy? (y/n): ")
    if user_input.lower() == "y":
        c.run("cdk deploy --require-approval never")
    else:
        print("Deployment canceled by user.")


@tasks.task
def destroy(c):
    c.run("cdk destroy --require-approval never")
