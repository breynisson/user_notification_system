import pytest
import grpc
from concurrent.futures import ThreadPoolExecutor
from user_notification_system.generated import user_notifications_pb2, user_notifications_pb2_grpc

# @pytest.fixture(scope="module", autouse=True)
# def grpc_server():
#     server_process = subprocess.Popen(["poetry", "run", "python", "../server.py"])
#     time.sleep(5)
#     yield
#     server_process.terminate()
#     server_process.wait()

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
