# user_notification_system/generate_grpc.py
import os
import re
import subprocess

def generate_protos():
    base_dir = os.path.dirname(__file__)
    proto_dir = os.path.join(base_dir, "..", "protos")
    output_dir = os.path.join(base_dir, "generated")
    proto_file = "user_notifications.proto"

    # 1. Run protoc
    cmd = [
        "python",
        "-m",
        "grpc_tools.protoc",
        f"--proto_path={proto_dir}",
        f"--python_out={output_dir}",
        f"--grpc_python_out={output_dir}",
        os.path.join(proto_dir, proto_file),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("=== protoc output ===")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        raise RuntimeError("Error generating gRPC code")

    # 2. Patch absolute imports
    for filename in os.listdir(output_dir):
        if filename.endswith("_pb2.py") or filename.endswith("_pb2_grpc.py"):
            path = os.path.join(output_dir, filename)
            with open(path, "r") as f:
                content = f.read()
            patched = re.sub(
                r"^(import user_notifications_pb2.*)$",
                r"from . \1",
                content,
                flags=re.MULTILINE
            )
            if patched != content:
                with open(path, "w") as f:
                    f.write(patched)
                print(f"Patched {filename}")

if __name__ == "__main__":
    generate_protos()
