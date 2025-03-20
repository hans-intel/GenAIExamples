import argparse
import json
import uuid
import os

import requests

host_ip = os.environ["host_ip"]
port = 8888

# Define the URL and headers
url = f"http://{host_ip}:{port}/v1/chatqna"
headers = {
        "Content-Type": "application/json"
        }

# Define the payload
data = {
        "messages": "What is the revenue of Nike in 2023?"
        }

# Make the POST request
response = requests.post(url, headers=headers, json=data, stream=False)

# Print the response
print(response.status_code)  # HTTP status code
print("Headers:", response.headers)

if response.headers.get("Content-Type") == "text/event-stream; charset=utf-8":
    print("Streaming response detected. Processing chunks...")
    full_response=""
    for chunk in response.iter_lines(decode_unicode=True):
        if chunk:  # Skip empty lines
            if chunk == "[DONE]":  # End of the stream
                break
            # Remove the "data: " prefix and add the chunk to the full response
            chunk_content = chunk.replace("data: ", "").strip()
            #print(f"chunk_content {chunk_content}")
            if (chunk_content.startswith("b'") and chunk_content.endswith("'")) or (chunk_content.startswith('b"') and chunk_content.endswith('"')):
                # If the content looks like a byte string (e.g., b'hello'), strip the b'' and decode it
                chunk_content = eval(chunk_content).decode("utf-8")
            full_response += chunk_content
            #print("Mid response:", full_response.strip())

    # Print the final sentence
    print("Final response:", full_response.strip())
else:
    print("Non-streaming response detected.")
    print(response.text)
