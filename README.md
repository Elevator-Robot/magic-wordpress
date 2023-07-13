# Magic WordPress

[![Tests](https://github.com/Elevator-Robot/magic-wordpress/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Elevator-Robot/magic-wordpress/actions/workflows/ci.yml)

## Architecture
![architecture](docs/images/wordpress.drawio.webp)

## Deploy a WordPress site to AWS

This project deploys a WordPress site to your AWS account using GitHub Actions & some variables that you set.

### Prerequisites

- An AWS account
- A domain name

### Setup

- pip install -r requirements.txt

### Usage
- Run `invoke list` to list the available tasks
- Run `invoke test` to run the tests
- Run `invoke deploy` to deploy the project
- Run `invoke destroy` to destroy the project
