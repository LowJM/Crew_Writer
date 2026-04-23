import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

def test_model(model_id):
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    try:
        response = client.invoke_model(
            modelId=model_id,
            body='{"anthropic_version": "bedrock-2023-05-31", "max_tokens": 10, "messages": [{"role": "user", "content": "Hi"}]}',
            contentType='application/json',
            accept='application/json'
        )
        print(f"[SUCCESS] Access granted to {model_id}!")
        return True
    except ClientError as e:
        print(f"[FAILED] {model_id}: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
        return False

models_to_test = [
    "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "anthropic.claude-3-7-sonnet-20250219-v1:0",
    "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "anthropic.claude-3-5-sonnet-20241022-v2:0",
]

print("Testing Anthropic access in us-east-1...")
for m in models_to_test:
    test_model(m)
