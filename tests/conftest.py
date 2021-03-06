import pytest
from sanic import Sanic
from sanic.testing import SanicTestClient

from src.main import app as sanic_app


@pytest.fixture
def app() -> Sanic:
    yield sanic_app


@pytest.fixture
def test_cli(loop, app, sanic_client) -> SanicTestClient:
    cli = loop.run_until_complete(sanic_client(app))
    cli.server.after_server_stop = []
    return cli
