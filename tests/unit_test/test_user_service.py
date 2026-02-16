from unittest.mock import MagicMock

import pytest

from src.business.models.user import CreateUserRequest, UpdateUserRequest, User
from src.business.services.user_service import UserService


@pytest.fixture
def mock_repository() -> MagicMock:
    return MagicMock()


@pytest.fixture
def user_service_with_mock(mock_repository: MagicMock) -> UserService:
    return UserService(repository=mock_repository)


def test_get_all_returns_list_from_repository(
    user_service_with_mock: UserService,
    mock_repository: MagicMock,
    sample_user: User,
    sample_user_2: User,
) -> None:
    mock_repository.get_all.return_value = [sample_user, sample_user_2]
    result = user_service_with_mock.get_all()
    assert result == [sample_user, sample_user_2]
    mock_repository.get_all.assert_called_once()


def test_get_all_returns_empty_list_when_no_users(
    user_service_with_mock: UserService,
    mock_repository: MagicMock,
) -> None:
    mock_repository.get_all.return_value = []
    result = user_service_with_mock.get_all()
    assert result == []
    mock_repository.get_all.assert_called_once()


def test_get_by_id_returns_user_when_found(
    user_service_with_mock: UserService,
    mock_repository: MagicMock,
    sample_user: User,
) -> None:
    mock_repository.get_by_id.return_value = sample_user
    result = user_service_with_mock.get_by_id(1)
    assert result == sample_user
    mock_repository.get_by_id.assert_called_once_with(1)


def test_get_by_id_returns_none_when_not_found(
    user_service_with_mock: UserService,
    mock_repository: MagicMock,
) -> None:
    mock_repository.get_by_id.return_value = None
    result = user_service_with_mock.get_by_id(999)
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)


def test_create_user_delegates_to_repository_and_returns_created_user(
    user_service_with_mock: UserService,
    mock_repository: MagicMock,
    sample_user: User,
) -> None:
    mock_repository.create.return_value = sample_user
    result = user_service_with_mock.create_user(
        name="Alice",
        email="alice@example.com",
        age=30,
    )
    assert result == sample_user
    call_args = mock_repository.create.call_args[0][0]
    assert isinstance(call_args, CreateUserRequest)
    assert call_args.name == "Alice"
    assert call_args.email == "alice@example.com"
    assert call_args.age == 30


def test_create_user_without_age(
    user_service_with_mock: UserService,
    mock_repository: MagicMock,
) -> None:
    created = User(id=1, name="Dave", email="dave@example.com", age=None)
    mock_repository.create.return_value = created
    result = user_service_with_mock.create_user(name="Dave", email="dave@example.com")
    assert result.age is None
    call_args = mock_repository.create.call_args[0][0]
    assert call_args.age is None


def test_update_user_returns_updated_user_when_found(
    user_service_with_mock: UserService,
    mock_repository: MagicMock,
    sample_user: User,
) -> None:
    updated = User(id=1, name="Alice Updated", email="alice@example.com", age=31)
    mock_repository.update.return_value = updated
    result = user_service_with_mock.update_user(1, name="Alice Updated", age=31)
    assert result == updated
    call_kwargs = mock_repository.update.call_args[1]
    assert call_kwargs["user_id"] == 1
    data = call_kwargs["data"]
    assert isinstance(data, UpdateUserRequest)
    assert data.name == "Alice Updated"
    assert data.age == 31


def test_update_user_returns_none_when_user_not_found(
    user_service_with_mock: UserService,
    mock_repository: MagicMock,
) -> None:
    mock_repository.update.return_value = None
    result = user_service_with_mock.update_user(999, name="Nobody")
    assert result is None
    mock_repository.update.assert_called_once()
