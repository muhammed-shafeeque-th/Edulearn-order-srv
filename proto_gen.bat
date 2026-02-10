@echo off
@REM python -m grpc_tools.protoc -Isrc/infrastructure/grpc/protos --python_out=src/infrastructure/grpc/generated --grpc_python_out=src/infrastructure/grpc/generated src/infrastructure/grpc/protos/*.proto
@REM python -m grpc_tools.protoc -Isrc/infrastructure/grpc/protos --python_out=src/infrastructure/grpc/generated --grpc_python_out=src/infrastructure/grpc/generated src/infrastructure/grpc/protos/*.proto

python -m grpc_tools.protoc -I=proto --python_out=src/infrastructure/grpc/generated --pyi_out=src/infrastructure/grpc/generated --grpc_python_out=src/infrastructure/grpc/generated proto/*.proto proto/course/*.proto proto/course/types/*.proto