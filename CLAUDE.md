# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python examples of AWS AI and Machine Learning resources (Bedrock, SageMaker, Rekognition, etc.). Uses Python 3.13 managed by `uv`.

## Commands

```bash
# Install / sync dependencies
uv sync

# Run a script
uv run main.py
uv run examples/bedrock/invoke_model.py

# Add a dependency
uv add boto3
uv add --dev pytest

# Run tests
uv run pytest

# Run a single test
uv run pytest tests/test_foo.py::test_bar
```

## Structure

As examples are added, organize them by AWS service under an `examples/` directory (e.g., `examples/bedrock/`, `examples/rekognition/`). Each example should be a self-contained runnable script.

## Boto3 Documentation

https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html

## AWS Credentials

Credentials are resolved via the standard boto3 chain: environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`), `~/.aws/credentials`, or an IAM role. Never hardcode credentials or region strings — use `boto3.session.Session()` or read from environment.
