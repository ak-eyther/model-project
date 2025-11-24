---
name: pytest-backend-patterns
description: Backend testing with pytest including fixtures, mocking, async tests, and database testing. Use for FastAPI/Python test implementation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Pytest Backend Patterns

## Basic Test

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
```

## Fixtures

```python
@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_user(db_session):
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user

def test_get_user(test_user):
    response = client.get(f"/users/{test_user.id}")
    assert response.json()["email"] == "test@example.com"
```

## Async Tests

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/1")
    assert response.status_code == 200
```

## Database Test Isolation

```python
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
```

## Mocking External APIs

```python
from unittest.mock import patch, MagicMock

@patch('app.services.external_api.fetch_data')
def test_external_api_call(mock_fetch):
    mock_fetch.return_value = {"data": "mocked"}
    
    response = client.get("/external-data")
    assert response.json() == {"data": "mocked"}
    mock_fetch.assert_called_once()
```

## Parametrized Tests

```python
@pytest.mark.parametrize("email,expected_valid", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("@example.com", False),
])
def test_email_validation(email, expected_valid):
    is_valid = validate_email(email)
    assert is_valid == expected_valid
```
