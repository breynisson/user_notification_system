# User Notification System

## Description

## Usage

## Generate protobuf files

```bash
poetry run python -m grpc_tools.protoc -I. --python_out=./generated --grpc_python_out=./generated user_notifications.proto
``` 