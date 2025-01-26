import google
import grpc
import logging
from user_notification_system.generated import user_notifications_pb2_grpc, user_notifications_pb2

class NotificationClient:
    def __init__(self, server_address="localhost:50051"):
        self.server_address = server_address
        self.channel = grpc.insecure_channel(server_address)
        self.stub = user_notifications_pb2_grpc.NotificationServiceStub(self.channel)
        logging.info(f"NotificationClient initialized with server address: {server_address}")

    def send_message(self, client_id, message):
        try:
            response = self.stub.SendMessage(user_notifications_pb2.MessageRequest(client_id=client_id, message=message))
            logging.info(f"Client {client_id}: SendMessage response: {response.status}")
            status_response = self.stub.GetClientStatus(user_notifications_pb2.ClientStatusRequest(client_id=client_id))
            logging.info(f"Client {client_id}: Status: {status_response.statuses}")
        except grpc.RpcError as e:
            logging.error(f"Failed to send message for client {client_id}: {e.details()} (code: {e.code()})")

    def get_client_status(self, client_id):
        try:
            status_response = self.stub.GetClientStatus(user_notifications_pb2.ClientStatusRequest(client_id=client_id))
            logging.info(f"Client {client_id}: Status: {status_response.statuses}")
            print(f"Client {client_id}: Status: {status_response.statuses}")
        except grpc.RpcError as e:
            logging.error(f"Failed to get status for client {client_id}: {e.details()} (code: {e.code()})")

    def get_all_client_statuses(self):
        try:
            status_response = self.stub.GetAllClientStatuses(google.protobuf.empty_pb2.Empty())
            logging.info("All client statuses:")
            for client_id, status in status_response.statuses.items():
                logging.info(f"  {client_id}: {status}")
                print(f"  {client_id}: {status}")
        except grpc.RpcError as e:
            logging.error(f"Failed to get all client statuses: {e.details()} (code: {e.code()})")


def send_message():
    import argparse
    parser = argparse.ArgumentParser(description="Send a message to a client.")
    parser.add_argument("client_id", type=str, help="Client ID")
    parser.add_argument("message", type=str, help="Message to send")
    parser.add_argument("--server-address", type=str, default="localhost:50051", help="Address of the gRPC server")
    args = parser.parse_args()

    client = NotificationClient(args.server_address)
    client.send_message(args.client_id, args.message)

def get_client_status():
    import argparse
    parser = argparse.ArgumentParser(description="Get the status of a client.")
    parser.add_argument("client_id", type=str, help="Client ID")
    parser.add_argument("--server-address", type=str, default="localhost:50051", help="Address of the gRPC server")
    args = parser.parse_args()

    client = NotificationClient(args.server_address)
    client.get_client_status(args.client_id)

def get_all_client_statuses():
    import argparse
    parser = argparse.ArgumentParser(description="Get the statuses of all clients.")
    parser.add_argument("--server-address", type=str, default="localhost:50051", help="Address of the gRPC server")
    args = parser.parse_args()

    client = NotificationClient(args.server_address)
    client.get_all_client_statuses()