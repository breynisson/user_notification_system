import grpc
import asyncio
import signal
from user_notification_system.generated import user_notifications_pb2_grpc, user_notifications_pb2


class NotificationService(user_notifications_pb2_grpc.NotificationServiceServicer):
    def __init__(self):
        self.client_statuses = {}

    async def SendMessage(self, request, context):
        client_id = request.client_id
        message = request.message.lower()

        if message == "hello":
            self.client_statuses[client_id] = "connected"
            return user_notifications_pb2.MessageResponse(status="Success")
        elif message == "goodbye":
            self.client_statuses[client_id] = "disconnected"
            return user_notifications_pb2.MessageResponse(status="Success")
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid message")
            return user_notifications_pb2.MessageResponse(status="Invalid Message")

    async def GetClientStatus(self, request, context):
        if request.client_id:
            return user_notifications_pb2.ClientStatusResponse(
                statuses={request.client_id: self.client_statuses.get(request.client_id, "unknown")}
            )
        return user_notifications_pb2.ClientStatusResponse(statuses=self.client_statuses)


async def serve():
    server = grpc.aio.server()
    user_notifications_pb2_grpc.add_NotificationServiceServicer_to_server(NotificationService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("Server started on port 50051")

    # Signal handling for graceful shutdown
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def signal_handler():
        print("\nReceived shutdown signal, shutting down gracefully...")
        stop_event.set()

    loop.add_signal_handler(signal.SIGINT, signal_handler)
    loop.add_signal_handler(signal.SIGTERM, signal_handler)

    try:
        # Wait for the stop signal
        await stop_event.wait()
    finally:
        # Shutdown server gracefully
        await server.stop(5)  # Allow up to 5 seconds for ongoing calls to finish
        await server.wait_for_termination()
        print("Server shut down successfully")


def main():
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        print("Server interrupted and shutting down.")

if __name__ == "__main__":
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        print("Server interrupted and shutting down.")
