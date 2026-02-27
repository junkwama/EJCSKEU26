import os
import subprocess
from pathlib import Path

import boto3
import docker
import pytest
from docker.errors import DockerException
from fastapi.testclient import TestClient
from testcontainers.core.container import DockerContainer
from testcontainers.mysql import MySqlContainer


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _ensure_docker_available() -> None:
    try:
        docker.from_env().ping()
    except DockerException as exc:
        pytest.skip(f"Docker daemon unavailable, skipping integration tests: {exc}")


def _build_sync_url(mysql: MySqlContainer) -> str:
    host = mysql.get_container_host_ip()
    port = mysql.get_exposed_port(3306)
    return f"mysql+pymysql://test:test@{host}:{port}/test_db"


def _build_async_url(mysql: MySqlContainer) -> str:
    host = mysql.get_container_host_ip()
    port = mysql.get_exposed_port(3306)
    return f"mysql+asyncmy://test:test@{host}:{port}/test_db"


@pytest.fixture(scope="session")
def mysql_container():
    _ensure_docker_available()
    with MySqlContainer("mysql:8.0", username="test", password="test", dbname="test_db") as mysql:
        yield mysql


@pytest.fixture(scope="session")
def localstack_container():
    _ensure_docker_available()
    container = (
        DockerContainer("localstack/localstack:3.8")
        .with_env("SERVICES", "s3")
        .with_env("AWS_DEFAULT_REGION", "us-east-1")
        .with_exposed_ports(4566)
    )
    container.start()
    try:
        host = container.get_container_host_ip()
        port = container.get_exposed_port(4566)
        endpoint_url = f"http://{host}:{port}"

        s3 = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1",
        )
        s3.create_bucket(Bucket="ejcsk-test-bucket")

        yield {
            "endpoint_url": endpoint_url,
            "bucket": "ejcsk-test-bucket",
            "region": "us-east-1",
        }
    finally:
        container.stop()


@pytest.fixture(scope="session")
def app_client(mysql_container, localstack_container):
    sync_url = _build_sync_url(mysql_container)
    async_url = _build_async_url(mysql_container)

    env = os.environ.copy()
    env["MYSQL_DB_SYNC_URL"] = sync_url
    env["MYSQL_DB_ASYNC_URL"] = async_url
    env["AWS_S3_ACCESS_KEY_ID"] = "test"
    env["AWS_S3_SECRET_ACCESS_KEY"] = "test"
    env["AWS_S3_REGION"] = localstack_container["region"]
    env["AWS_S3_BUCKET"] = localstack_container["bucket"]

    subprocess.run(
        ["alembic", "upgrade", "head"],
        check=True,
        cwd=PROJECT_ROOT,
        env=env,
    )

    os.environ.update(
        {
            "MYSQL_DB_SYNC_URL": sync_url,
            "MYSQL_DB_ASYNC_URL": async_url,
            "AWS_S3_ACCESS_KEY_ID": "test",
            "AWS_S3_SECRET_ACCESS_KEY": "test",
            "AWS_S3_REGION": localstack_container["region"],
            "AWS_S3_BUCKET": localstack_container["bucket"],
        }
    )

    import core.db as db_module

    db_module._engine = None
    db_module._SessionLocal = None

    from main import app

    with TestClient(app) as client:
        yield client
