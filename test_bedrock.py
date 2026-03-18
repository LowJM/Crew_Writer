from crew import llm, titan_image

print("1. Testing Bedrock Claude 3.5 Sonnet Text Generation...")
response = llm.call(messages=[{"role": "user", "content": "Write exactly one sentence about 2026's good news on global warming."}])
print(f"Response: {response}\n")

print("2. Testing Bedrock Titan Image Generation...")
image_result = titan_image._run("A futuristic green city in 2026 showing good news on global warming")
print(f"Result: {image_result}")
