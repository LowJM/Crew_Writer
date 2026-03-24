import boto3
import json
import base64
import os
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
