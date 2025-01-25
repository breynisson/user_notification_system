# tests/conftest.py

import pytest
import subprocess
import time
import socket


def is_port_in_use(port, host="127.0.0.1"):
    """Check if a given port on the host is already bound/occupied."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


@pytest.fixture(scope="session", autouse=True)
def run_grpc_server():
    """
    Start the gRPC server in a separate process before any tests run
    and shut it down afterwards.
    """
    # 1. Start the server using subprocess
    server_process = subprocess.Popen(
        ["python", "user_notification_system/server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # 2. Wait until the server is up (or time out)
    timeout = 10  # seconds
    for _ in range(timeout):
        if is_port_in_use(50051):
            break
        time.sleep(1)
    else:
        # If we never broke out of the loop, kill and raise an error
        server_process.terminate()
        server_process.wait()
        raise RuntimeError("Server did not start within the given timeout")

    print("Server is running...")

    # 3. Yield control back to the test suite
    yield

    # 4. Teardown: stop the server
    print("Terminating server...")
    server_process.terminate()
    server_process.wait()
    print("Server terminated.")
