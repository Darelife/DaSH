# import requests
# import json
# import os
# from dotenv import load_dotenv

# envPath = ".env"
# load_dotenv(dotenv_path=envPath)
# API_KEY = os.getenv("API_KEY")

# url = "https://api.aimlapi.com/messages"
# headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
# payload = {
#     # "model": "claude-3-5-sonnet-20240620",
#     "model": "togethercomputer/Llama-2-7B-32K-Instruct",
#     "max_tokens": 1024,
#     "tools": [
#         {
#             "name": "get_weather",
#             "description": "Get the current weather in a given location",
#             "input_schema": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "The city and state, e.g. San Francisco, CA",
#                     }
#                 },
#             },
#         }
#     ],
#     "messages": [
#         {"role": "user", "content": "What is the weather like in San Francisco?"}
#     ],
#     "stream": False,
# }
# response = requests.post(url, json=payload, headers=headers)
# print(response.json())

# # url = "https://api.aimlapi.com/chat/completions"
# # headers = {
# #     "Authorization": f"Bearer {API_KEY}",
# #     "Content-Type": "application/json",
# # }

# # data = {
# #     "model": "google/gemma-7b",
# #     "messages": [{"role": "user", "content": "What is 2+2?"}],
# #     "max_tokens": 512,
# #     "stream": False,
# # }

# # try:
# #     response = requests.post(url, headers=headers, data=json.dumps(data))
# #     response.raise_for_status()  # Raise an error for bad status codes
# #     response_data = response.json()
# #     print(json.dumps(response_data, indent=2))  # Pretty print the JSON response
# # except requests.exceptions.RequestException as e:
# #     print(f"Request failed: {e}")
# # except json.JSONDecodeError:
# #     print("Failed to decode JSON response")


# import requests

# url = "https://cortex4.p.rapidapi.com/get-labeled-data"

# querystring = {
#     "page": "1",
#     "q": '{"object_analysis": {"$elemMatch": {"$elemMatch": {"classname": "cat"}}}, "width": {"$gt": 100}, "label_quality_estimation": {"$gt": 0.5}}',
# }

# headers = {
#     "x-rapidapi-key": "8c3a79fe88msh343b92940df333cp16299bjsn59f748d93498",
#     "x-rapidapi-host": "cortex4.p.rapidapi.com",
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())

# import requests import os from dotenv import load_dotenv

# envPath = ".env"
# load_dotenv(dotenv_path=envPath)
# API_KEY = os.getenv("API_KEY")

# url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"

# message = "What is 2+2?"

# payload = { "messages": [{"role": "user", "content": message}], "model": "gpt-4o", "max_tokens": 100, "temperature": 0.9, } headers = { "x-rapidapi-key": API_KEY, "x-rapidapi-host": "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com", "Content-Type": "application/json", }

# response = requests.post(url, json=payload, headers=headers)

# print(response.json()["choices"][0]["message"]["content"])

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


def main():
    env_manager = EnvManager()
    api_key = env_manager.get_api_key()

    chat_client = ChatGPTClient(api_key)
    message = "What is 2+2?"
    try:
        response = chat_client.get_response(message)
        print(response["choices"][0]["message"]["content"])
    except:
        print("Failed to get response")


if __name__ == "__main__":
    main()
