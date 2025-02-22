import socket
import sys
import argparse
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                break
            sys.stdout.write(message + "\n")
            sys.stdout.flush()
        except:
            break



def start_client(host, port, username, passcode):
    cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cl_socket.connect((host, port))
    cl_socket.sendall(f"{username} {passcode}".encode())

    response = cl_socket.recv(1024).decode().strip()
    if response == "Incorrect passcode":
        sys.stdout.write("Incorrect passcode\n")
        sys.stdout.flush()
        cl_socket.close()
        return

    sys.stdout.write(f"# Connected to {host} on port {port}\n")
    sys.stdout.flush()

    threading.Thread(target=receive_messages, args=(cl_socket,), daemon=True).start()

    while True:
        try:
            msg = input()
            if msg.strip():
                cl_socket.sendall(msg.encode())
            if msg.strip() == ":Exit":
                break
        except:
            break

    cl_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-join", action="store_true")
    parser.add_argument("-host", type=str, required=True)
    parser.add_argument("-port", type=int, required=True)
    parser.add_argument("-username", type=str, required=True)
    parser.add_argument("-passcode", type=str, required=True)
    args = parser.parse_args()

    start_client(args.host, args.port, args.username, args.passcode)
