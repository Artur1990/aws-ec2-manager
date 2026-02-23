# EC2 Manager CLI (ec2mgr)

Production-ready AWS EC2 management CLI built with Python and boto3.
Designed as a real-world DevOps portfolio project with clean architecture, automated tests, and CI pipeline.

This tool allows safe and convenient management of EC2 instances directly from the command line.

---

## Features

* List EC2 instances in a region
* Start instance
* Stop instance
* Reboot instance
* Show detailed instance status
* Set Name tag
* Dry-run mode for safe execution
* Clean architecture (CLI layer + AWS layer)
* Fully tested with pytest
* Automated CI with GitHub Actions
* Works on Linux, macOS, and Windows

---

## Architecture

```
CLI (argparse)
   ↓
Service Layer
   ↓
AWS API (boto3)
   ↓
EC2
```

Separation of concerns allows easy testing and maintenance.

---

## Requirements

* Python 3.11+
* AWS account
* AWS credentials configured

Install AWS CLI if not installed:

```
sudo apt install awscli      # Ubuntu/Debian
```

Configure credentials:

```
aws configure
```

---

## Installation

Clone repository:

```
git clone https://github.com/YOUR_USERNAME/aws-ec2-manager.git
cd aws-ec2-manager
```

Create virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

Install project:

```
pip install -e .
```

---

## Usage

List instances:

```
ec2mgr list
```

Check instance status:

```
ec2mgr status i-1234567890abcdef0
```

Start instance:

```
ec2mgr start i-1234567890abcdef0
```

Stop instance:

```
ec2mgr stop i-1234567890abcdef0
```

Reboot instance:

```
ec2mgr reboot i-1234567890abcdef0
```

Set Name tag:

```
ec2mgr tag i-1234567890abcdef0 Name=my-server
```

Use dry-run mode (safe testing):

```
ec2mgr --dry-run stop i-1234567890abcdef0
```

Use specific region:

```
ec2mgr --region us-east-1 list
```

Use AWS profile:

```
ec2mgr --profile dev list
```

---

## Running Tests

Run tests:

```
pytest -q
```

Run lint:

```
ruff check .
```

---

## CI Pipeline

GitHub Actions automatically runs:

* Lint checks
* Unit tests

on every push and pull request.

---

## Example Output

```
InstanceId        Name        State     Type      PublicIP     PrivateIP
---------------------------------------------------------------------------
i-1234567890      web-server  running   t3.micro  54.12.34.56  10.0.0.5
```

---

## Safety

Supports AWS DryRun mode to prevent accidental changes.

Example:

```
ec2mgr --dry-run stop i-1234567890abcdef0
```

---

## Technologies Used

* Python
* boto3
* pytest
* GitHub Actions
* argparse
* Ruff (lint)

---

## Why this project exists

This project demonstrates real DevOps skills:

* AWS automation
* Infrastructure management
* CLI tools development
* Testing and CI
* Production-level project structure

---

## License

MIT

---

## Docker

You can run the tool inside a Docker container.

Build the image:

```bash
docker build -t ec2mgr .
```

Run help:

```bash
docker run --rm ec2mgr --help
```

Run with AWS credentials (Linux/macOS):

```bash
docker run --rm -v ~/.aws:/root/.aws:ro ec2mgr list
```

Run with AWS credentials (Windows PowerShell):

```powershell
docker run --rm -v $env:USERPROFILE\.aws:/root/.aws:ro ec2mgr list
```

---