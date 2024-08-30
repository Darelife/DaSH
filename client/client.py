import socket
import random
import time
import json


def main():
    port = 6969
    client_socket = socket.socket()

    with open("input.txt", "r") as file:
        lines = file.readlines()

    server = socket.gethostname()
    # client_socket.connect(("server", port))
    client_socket.connect((server, port))

    client_id = random.randint(1, 1000)
    output = []
    # message = input("Enter your message: ")

    for message in lines:
        message = "hi"
        formatted_message = f"{client_id}: {message}"
        start = time.time()
        client_socket.send(formatted_message.encode())
        response = client_socket.recv(1024).decode()
        print(f"\033[36mServer: {response}\033[0m")
        end = time.time()
        output.append(
            {
                "Prompt": message,
                "Message": response,
                "TimeSent": start,
                "TimeRecvd": end,
                "Source": "GPT-4o",
            }
        )
        break
        # message = input("Enter your message: ")
    with open("output.json", "w") as file:
        json.dump(output, file, indent=2)
    formatted_message = f"{client_id}: exit"
    client_socket.send(formatted_message.encode())
    client_socket.close()


if __name__ == "__main__":
    main()
