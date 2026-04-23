import boto3
import json
import base64
import os
import requests
from botocore.config import Config

# Amazon Titan Image Generator v2 has a 512-character limit on the prompt
TITAN_MAX_PROMPT_CHARS = 512

class TitanImageTool:
    """Standalone image generation tool utilizing AWS Bedrock."""
    
    def generate(self, topic: str) -> str:
        # Truncate prompt to Titan's 512-character limit
        if len(topic) > TITAN_MAX_PROMPT_CHARS:
            print(f"[IMAGE] Prompt too long ({len(topic)} chars), truncating to {TITAN_MAX_PROMPT_CHARS}...")
            topic = topic[:TITAN_MAX_PROMPT_CHARS]

        # Explicit timeouts to prevent infinite hangs
        boto_config = Config(
            read_timeout=120,
            connect_timeout=10
        )

        # Utilize boto3 default credential provider chain (no explicit kwargs)
        client = boto3.client(
            'bedrock-runtime', 
            region_name='us-east-1',
            config=boto_config
        )
        
        # Specific payload for Amazon Titan Image Generator
        request_body = json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": topic
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 1024,
                "width": 1024,
                "cfgScale": 8.0,
            }
        })
        
        # Exceptions will rightfully bubble up to the caller
        response = client.invoke_model(
            body=request_body,
            modelId="amazon.titan-image-generator-v2:0",
            accept="application/json",
            contentType="application/json"
        )
        
        response_body = json.loads(response.get("body").read())
        base64_image = response_body.get("images")[0]
        
        # Save the image robustly
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(BASE_DIR, "output")
        os.makedirs(output_dir, exist_ok=True)
        image_path = os.path.join(output_dir, "picture.jpg")
        
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(base64_image))
            
        return f"Success: Image generated and saved locally to {image_path}"

class NvidiaImageTool:
    """Tool to generate images using NVIDIA NIM (Flux.1-schnell)."""
    
    def generate(self, prompt: str) -> str:
        api_key = os.environ.get("NVIDIA_NIM_API_KEY")
        if not api_key or api_key == "your_nvidia_key_here":
            raise ValueError("NVIDIA_NIM_API_KEY is missing or invalid in .env")

        invoke_url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-schnell"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": prompt
        }

        print("[NVIDIA] Requesting image generation from Flux.1-schnell...")
        response = requests.post(invoke_url, headers=headers, json=payload)

        if response.status_code == 200:
            response_body = response.json()
            # The base64 image data is typically in artifacts[0].base64
            artifacts = response_body.get("artifacts", [])
            base64_image = artifacts[0].get("base64") if artifacts else None
            
            if base64_image:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                output_path = os.path.join(base_dir, "output", "picture.jpg")
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, "wb") as fh:
                    fh.write(base64.b64decode(base64_image))
                return f"Successfully generated and saved image at {output_path}"
            else:
                raise Exception("Failed to extract base64 image data from NVIDIA response.")
        else:
            raise Exception(f"NVIDIA API Error {response.status_code}: {response.text}")
