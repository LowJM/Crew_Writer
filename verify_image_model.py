import boto3
import json
import base64
import os
from dotenv import load_dotenv

load_dotenv('.env')

client = boto3.client(
    'bedrock-runtime', 
    region_name='us-east-1',
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)

models = [
    ("amazon.titan-image-generator-v1", {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {"text": "A green futuristic city"},
        "imageGenerationConfig": {"numberOfImages": 1, "height": 1024, "width": 1024, "cfgScale": 8.0}
    }),
    ("amazon.titan-image-generator-v2:0", {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {"text": "A green futuristic city"},
        "imageGenerationConfig": {"numberOfImages": 1, "height": 1024, "width": 1024, "cfgScale": 8.0}
    }),
    ("amazon.nova-canvas-v1:0", {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {"text": "A green futuristic city"},
        "imageGenerationConfig": {"numberOfImages": 1, "height": 1024, "width": 1024, "cfgScale": 8.0}
    }),
    ("stability.stable-diffusion-xl-v1", {
        "text_prompts": [{"text": "A green futuristic city"}],
        "cfg_scale": 10,
        "steps": 30
    })
]

for model_id, payload in models:
    print(f"\nTrying {model_id}...")
    try:
        response = client.invoke_model(
            body=json.dumps(payload),
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        print(f"SUCCESS with {model_id}!")
        break
    except Exception as e:
        print(f"FAILED: {e}")
