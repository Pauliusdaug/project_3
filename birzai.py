import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve your API key from environment variable named SECRET
token = os.getenv("SECRET")

# Your custom endpoint and model
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

# Initialize the OpenAI client with your endpoint and token
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# Read the content of birzai.txt as context
with open("birzai.txt", "r", encoding="utf-8") as file:
    context = file.read()

# Define the question you want to ask about Birzai
question = "Tell me about Birzai."

# Compose the chat messages payload
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"}
]

# Send the request to the chat completion endpoint
response = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=200,
    temperature=0,
)

# Extract the answer text from the response
answer = response.choices[0].message.content.strip()

# Print the answer
print("Answer:", answer)
