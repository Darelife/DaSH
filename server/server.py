# import socket
# import requests
# import os
# from dotenv import load_dotenv


# class EnvManager:
#     def __init__(self, env_path=".env"):
#         self.env_path = env_path
#         self.load_env()

#     def load_env(self):
#         load_dotenv(dotenv_path=self.env_path)

#     def get_api_key(self):
#         return os.getenv("API_KEY")


# class ChatGPTClient:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"
#         self.headers = {
#             "x-rapidapi-key": self.api_key,
#             "x-rapidapi-host": "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com",
#             "Content-Type": "application/json",
#         }

#     def get_response(self, message, model="gpt-4o", max_tokens=100, temperature=0.9):
#         payload = {
#             "messages": [{"role": "user", "content": message}],
#             "model": model,
#             "max_tokens": max_tokens,
#             "temperature": temperature,
#         }
#         response = requests.post(self.url, json=payload, headers=self.headers)
#         return response.json()


# def main():
#     host = socket.gethostname()
#     port = 6942
#     incoming = socket.socket()
#     incoming.bind((host, port))
#     env_manager = EnvManager()
#     api_key = env_manager.get_api_key()
#     chat_client = ChatGPTClient(api_key)

#     incoming.listen(2)
#     conn, address = incoming.accept()
#     print("Connection from: " + str(address))

#     while True:
#         data = conn.recv(1024).decode()
#         if not data or data == "" or data == "exit":
#             break
#         print("\033[35m" + str(data) + "\033[0m")  # Tried to make it magenta
#         response = chat_client.get_response(data)
#         data = response["choices"][0]["message"]["content"]
#         print(
#             "\033[36m" + str(data) + "\033[0m"
#         )  # idk if it will be cyan or red...just gonna try it out -> ight it's cyan..pog
#         conn.send(data.encode())

#     conn.close()


# if __name__ == "__main__":
#     main()

import socket
import threading
import requests
import os
from dotenv import load_dotenv


class EnvManager:
    def __init__(self, env_path=".env"):
        self.env_path = env_path
        self.load_env()

    def load_env(self):
        load_dotenv(dotenv_path=self.env_path)

    def get_api_key(self):
        return os.getenv("API_KEY")


class ChatGPTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com",
            "Content-Type": "application/json",
        }

    def get_response(self, message, model="gpt-4o", max_tokens=100, temperature=0.9):
        payload = {
            "messages": [{"role": "user", "content": message}],
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        response = requests.post(self.url, json=payload, headers=self.headers)
        return response.json()


class ChatServer:
    def __init__(self, host="0.0.0.0", port=6969):
        self.host = host
        self.port = port
        self.clients = {}  # Dictionary to store client connections
        self.env_manager = EnvManager()
        self.api_key = self.env_manager.get_api_key()
        self.chat_client = ChatGPTClient(self.api_key)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                client_id, message = data.split(": ", 1)
                if message == "exit" or message == "":
                    self.close()
                    break
                print(f"\033[35m{client_id}: {message}\033[0m")
                response = self.chat_client.get_response(message)
                reply = response["choices"][0]["message"]["content"]
                print(f"\033[36mServer: {reply}\033[0m")
                client_socket.send(reply.encode())
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
            self.clients.pop(client_socket, None)

    def start(self):
        print("Server started, waiting for connections...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from: {client_address}")
            self.clients[client_socket] = client_address
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_socket,)
            )
            client_thread.start()

    def close(self):
        self.server_socket.close()


if __name__ == "__main__":
    server = ChatServer()
    server.start()
