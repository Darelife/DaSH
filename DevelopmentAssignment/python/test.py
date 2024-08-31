# from transformers import pipeline

# # import torch
# from dotenv import load_dotenv
# import os
# from huggingface_hub import HfFolder

# envPath = ".env"
# load_dotenv(dotenv_path=envPath)
# API_KEY = os.getenv("API_KEY")

# # Save the API key using HfFolder
# HfFolder.save_token(API_KEY)

# pipe = pipeline(
#     "text-generation",
#     model="google/gemma-2b-it",
#     # model_kwargs={"torch_dtype": torch.bfloat16},
#     device="cpu",
#     use_auth_token=True,
# )

# messages = [
#     {"role": "user", "content": "Who are you? Please, answer in pirate-speak."},
# ]
# outputs = pipe(
#     messages, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95
# )
# assistant_response = outputs[0]["generated_text"][-1]["content"]
# print(assistant_response)
