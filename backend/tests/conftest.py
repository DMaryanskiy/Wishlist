import typing as tp

import faker
import pytest
import sqlalchemy
from fastapi import testclient
from sqlalchemy import orm

from backend import config
from backend import main

settings = config.get_settings()

sync_engine = sqlalchemy.create_engine(settings.db_url)
local_session = orm.sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

fake = faker.Faker()


@pytest.fixture(scope="session")
def client() -> tp.Generator[testclient.TestClient, tp.Any, None]:
    with testclient.TestClient(main.app) as _client:
        yield _client
    main.app.dependency_overrides = {}
    sync_engine.dispose()


@pytest.fixture
def db() -> tp.Generator[orm.session.Session, tp.Any, None]:
    session = local_session()
    yield session
    session.close()
