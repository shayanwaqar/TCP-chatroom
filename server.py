import socket
import sys
import argparse
import threading
from datetime import datetime, timedelta

clients = {}  # clients sockets to username mapping

def broadcast(message, sender=None):
    for cl_socket in clients.keys():
        username = clients[cl_socket]

        if cl_socket != sender:
            try:
                cl_socket.sendall(message.encode())
            except:
                cl_socket.close()
                del clients[cl_socket]


def handle_client(cl_socket):
    try:
        # Receive username and passcode
        credentials = cl_socket.recv(1024)
        credentials = credentials.decode()
        credentials = credentials.strip()
        credentials = credentials.split()
        if len(credentials) != 2:
            cl_socket.sendall("Incorrect passcode".encode())
            cl_socket.close()
            return

        username, passcode = credentials
        if passcode != server_passcode:
            cl_socket.sendall("Incorrect passcode".encode())
            cl_socket.close()
            return

        # Notify all clients
        clients[cl_socket] = username
        broadcast(f"# {username} joined the chatroom")
        sys.stdout.write(f"# {username} joined the chatroom\n")
        sys.stdout.flush()

        while True:
            message = cl_socket.recv(1024).decode().strip()
            if not message:
                break

            if message == ":Exit":
                break
            elif message == ":)":
                broadcast(f"# {username}: [Feeling Joyful]", sender=cl_socket)
                sys.stdout.write(f"# {username}: [Feeling Joyful]\n")
            elif message == ":(":
                broadcast(f"# {username}: [Feeling Unhappy]", sender=cl_socket)
                sys.stdout.write(f"# {username}: [Feeling Unhappy]\n")
            elif message == ":mytime":
                current_time = datetime.now().strftime("%Y %b %d %H:%M:%S %a")
                broadcast(f"# {username}: {current_time}", sender=cl_socket)
                sys.stdout.write(f"# {username}: {current_time}\n")
            elif message == ":+1hr":
                future_time = (datetime.now() + timedelta(hours=1)).strftime("%Y %b %d %H:%M:%S %a")
                broadcast(f"# {username}: {future_time}", sender=cl_socket)
                sys.stdout.write(f"# {username}: {future_time}\n")
            elif message.startswith(":dm "):
                parts = message.split(maxsplit=2)
                if len(parts) < 3:
                    continue
                _, recipient, dm_message = parts
                for sock, user in clients.items():
                    if user == recipient:
                        sock.sendall(f"# {username}: {dm_message}".encode())
                        sys.stdout.write(f"# {username} to {recipient}: {dm_message}\n")
                        sys.stdout.flush()
                        break
            else:
                broadcast(f"# {username}: {message}", sender=cl_socket)
                sys.stdout.write(f"# {username}: {message}\n")

            sys.stdout.flush()

    except:
        pass
    finally:
        if cl_socket in clients:
            username = clients[cl_socket]
            del clients[cl_socket]
            broadcast(f"# {username} left the chatroom")
            sys.stdout.write(f"# {username} left the chatroom\n")
            sys.stdout.flush()
        cl_socket.close()


def start_server(port, passcode):
    global server_passcode
    server_passcode = passcode

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)

    sys.stdout.write(f"# Server started on port {port}. Accepting connections\n")
    sys.stdout.flush()

    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-start", action="store_true")
    parser.add_argument("-port", type=int, required=True)
    parser.add_argument("-passcode", type=str, required=True)
    args = parser.parse_args()

    start_server(args.port, args.passcode)