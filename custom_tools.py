import boto3
import json
import base64
import os
from crewai.tools import BaseTool

class TitanImageTool(BaseTool):
    name: str = "Generate Image"
    description: str = "Useful to generate an image from a detailed text description."
    
    def _run(self, topic: str) -> str:
        try:
            # We explicitly use us-east-1 because ap-southeast-2 doesn't have the image model
            client = boto3.client(
                'bedrock-runtime', 
                region_name='us-east-1',
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
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
            
            response = client.invoke_model(
                body=request_body,
                modelId="amazon.titan-image-generator-v2:0",
                accept="application/json",
                contentType="application/json"
            )
            
            response_body = json.loads(response.get("body").read())
            base64_image = response_body.get("images")[0]
            
            # Save the image directly to the output folder
            os.makedirs("output", exist_ok=True)
            image_path = "output/picture.jpg"
            with open(image_path, "wb") as f:
                f.write(base64.b64decode(base64_image))
                
            return f"Success: Image generated and saved locally to {image_path}"
        except Exception as e:
            return f"Error Failed to generate image: {str(e)}"
