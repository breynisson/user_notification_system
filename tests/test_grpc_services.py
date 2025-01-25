import pytest
import grpc
from user_notification_system.generated import user_notifications_pb2, user_notifications_pb2_grpc

# @pytest.fixture(scope="module", autouse=True)
# def grpc_server():
#     server_process = subprocess.Popen(["poetry", "run", "python", "../server.py"])
#     time.sleep(5)
#     yield
#     server_process.terminate()
#     server_process.wait()

@pytest.fixture(scope="module")
def grpc_channel():
    channel = grpc.insecure_channel('localhost:50051')
    yield channel
    channel.close()

def test_send_hello(grpc_channel):
    stub = user_notifications_pb2_grpc.NotificationServiceStub(grpc_channel)
    response = stub.SendMessage(user_notifications_pb2.MessageRequest(client_id="client_1", message="Hello"))
    assert response.status == "Success"

def test_send_goodbye(grpc_channel):
    stub = user_notifications_pb2_grpc.NotificationServiceStub(grpc_channel)
    response = stub.SendMessage(user_notifications_pb2.MessageRequest(client_id="client_1", message="Goodbye"))
    assert response.status == "Success"


def test_invalid_message(grpc_channel):
    stub = user_notifications_pb2_grpc.NotificationServiceStub(grpc_channel)
    response = stub.SendMessage(user_notifications_pb2.MessageRequest(client_id="client_1", message="Invalid"))
    assert response.status == "Invalid Message"