import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("NVIDIA_NIM_API_KEY")

url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-schnell"
payload = {
    "prompt": "A majestic lion standing on a cliff",
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

resp = requests.post(url, headers=headers, json=payload)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    resp_data = resp.json()
    if "image" in resp_data:
        print("Found base64 image!")
    else:
        print("Response data:", str(resp_data)[:200])
else:
    print(f"Response: {resp.text[:200]}")
