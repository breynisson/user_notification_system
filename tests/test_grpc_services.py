import pytest
import grpc
import random
import asyncio
from hypothesis import given, strategies as st
from hypothesis.strategies import lists
from user_notification_system.generated import user_notifications_pb2, user_notifications_pb2_grpc


async def send_message(stub, client_id, message):
    stub.SendMessage(user_notifications_pb2.MessageRequest(client_id=client_id, message=message))

# Define a fixture for the gRPC channel
@pytest.fixture(scope="module")
def grpc_channel():
    channel = grpc.insecure_channel('localhost:50051')
    yield channel
    channel.close()

# Define a fixture for the service stub
@pytest.fixture(scope="module")
def stub(grpc_channel):
    return user_notifications_pb2_grpc.NotificationServiceStub(grpc_channel)


def test_send_hello(stub):
    response = stub.SendMessage(user_notifications_pb2.MessageRequest(client_id="test_client_1", message="Hello"))
    assert response.status == "Success"
    status_response = stub.GetClientStatus(user_notifications_pb2.ClientStatusRequest(client_id="test_client_1"))
    assert status_response.statuses["test_client_1"] == "connected"

def test_send_goodbye(stub):
    stub.SendMessage(user_notifications_pb2.MessageRequest(client_id="test_client_2", message="Hello"))
    response = stub.SendMessage(user_notifications_pb2.MessageRequest(client_id="test_client_2", message="Goodbye"))
    assert response.status == "Success"
    status_response = stub.GetClientStatus(user_notifications_pb2.ClientStatusRequest(client_id="test_client_2"))
    assert status_response.statuses["test_client_2"] == "disconnected"

def test_invalid_message(grpc_channel):
    stub = user_notifications_pb2_grpc.NotificationServiceStub(grpc_channel)
    response = stub.SendMessage(user_notifications_pb2.MessageRequest(client_id="client_1", message="Invalid"))
    assert response.status == "Invalid Message"

def test_get_all_client_statuses(stub):
    stub.SendMessage(user_notifications_pb2.MessageRequest(client_id="client_1", message="Hello"))
    stub.SendMessage(user_notifications_pb2.MessageRequest(client_id="client_2", message="Hello"))
    stub.SendMessage(user_notifications_pb2.MessageRequest(client_id="client_3", message="Hello"))
    stub.SendMessage(user_notifications_pb2.MessageRequest(client_id="client_2", message="Goodbye"))
    status_response = stub.GetClientStatus(user_notifications_pb2.ClientStatusRequest())
    assert status_response.statuses["client_1"] == "connected"
    assert status_response.statuses["client_2"] == "disconnected"
    assert status_response.statuses["client_3"] == "connected"


@pytest.mark.parametrize(
    "client_id, message, expected_status",
    [
        ("client_1", "Hello", "connected"),
        ("client_2", "Goodbye", "disconnected"),
        ("client_3", "Hello", "connected"),
    ]
)
def test_multiple_clients(stub, client_id, message, expected_status):
    stub.SendMessage(user_notifications_pb2.MessageRequest(client_id=client_id, message=message))
    status_response = stub.GetClientStatus(user_notifications_pb2.ClientStatusRequest(client_id=client_id))
    assert status_response.statuses[client_id] == expected_status


@given(client_id=st.text(min_size=1, max_size=10))
def test_random_client_ids(stub, client_id):
    response = stub.SendMessage(user_notifications_pb2.MessageRequest(client_id=client_id, message="Hello"))
    assert response.status == "Success"
    status_response = stub.GetClientStatus(user_notifications_pb2.ClientStatusRequest(client_id=client_id))
    assert status_response.statuses[client_id] == "connected"


@given(client_ids=lists(st.text(min_size=1, max_size=10), min_size=2, max_size=20, unique=True))
def test_multiple_clients_with_random_ids(stub, client_ids):
    for client_id in client_ids:
        message = random.choice(["Hello", "Goodbye"])
        stub.SendMessage(user_notifications_pb2.MessageRequest(client_id=client_id, message=message))
    status_response = stub.GetClientStatus(user_notifications_pb2.ClientStatusRequest())
    for client_id in client_ids:
        assert client_id in status_response.statuses

@pytest.mark.asyncio
async def test_concurrent_clients(stub):
    num_clients = 10
    messages = ["Hello", "Goodbye"]
    tasks = []

    for i in range(num_clients):
        client_id = f"client_{i}"
        message = random.choice(messages)
        tasks.append(send_message(stub, client_id, message))

    await asyncio.gather(*tasks)

    status_response = stub.GetClientStatus(user_notifications_pb2.ClientStatusRequest())
    for i in range(num_clients):
        client_id = f"client_{i}"
        assert client_id in status_response.statuses
        assert status_response.statuses[client_id] in ["connected", "disconnected"]