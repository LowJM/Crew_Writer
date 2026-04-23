# CrewAI Blog Writer

> An automated content engine using CrewAI to research, write, edit, and illustrate professional blog posts, featuring dual-provider image generation (NVIDIA NIM primary, AWS Bedrock fallback).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Generating high-quality, fully illustrated blog content typically requires context switching between multiple AI chat interfaces, manual prompt wrangling, and separate image generation pipelines. The CrewAI Blog Writer eliminates this fragmentation. It orchestrates a specialized team of autonomous agents—planners, writers, editors, and illustrators—into a robust content pipeline. To ensure maximum reliability for the final illustration, the system features a decoupled image generation step using NVIDIA's NIM API as the primary engine, with AWS Bedrock's Titan image generator acting as a resilient fallback.

## Quick Start

> **Important**: This project requires a **stable Python release** (e.g., Python 3.12 or 3.13). Do **not** use pre-release versions like Python 3.14, as core dependencies (`regex`, `tiktoken`) lack pre-built wheels and will fail to compile during installation.

### Option 1: Using `uv` (Recommended)
This project includes a `pyproject.toml` and `uv.lock`. Using [uv](https://github.com/astral-sh/uv) is the fastest and most reliable way to run the pipeline, as it automatically manages the Python version and dependencies.

```bash
# Clone and enter the directory
git clone https://github.com/yourusername/crewai-blog-writer.git
cd crewai-blog-writer/Crew_Writer

# Sync dependencies and run (uv handles the virtual environment automatically)
uv sync
uv run main.py
```

### Option 2: Using standard `pip`

```bash
# Clone and enter the directory
git clone https://github.com/yourusername/crewai-blog-writer.git
cd crewai-blog-writer/Crew_Writer

# Create a virtual environment using a STABLE Python version
# (Replace python3.12 with your stable python executable)
python3.12 -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install crewai crewai-tools python-dotenv boto3 requests

# Run the pipeline
python main.py
```

## Installation

**Prerequisites**: 
- **Stable Python** (3.12 or 3.13 recommended)
- Node.js 18+ (if utilizing js tools)

### Configuration and Credentials

The system requires API keys for text generation, search, and dual-provider image generation. Create a `.env` file in the root of your `Crew_Writer` directory and securely provide your credentials:

```env
# Core CrewAI text processing
OPENAI_API_KEY="your_openai_api_key_here" 

# Primary Image Generation (NVIDIA NIM)
NVIDIA_NIM_API_KEY="your_nvidia_api_key_here"

# Fallback Image Generation (AWS Bedrock Titan)
AWS_ACCESS_KEY_ID="your_aws_access_key"
AWS_SECRET_ACCESS_KEY="your_aws_secret_key"
AWS_REGION_NAME="ap-southeast-2" # Default region, change if your model is deployed elsewhere
```

> **Warning:** Never commit your actual `.env` file or API credentials to public version control. Ensure `.env` is listed in your `.gitignore`.

## Usage

The script supports two modes: **Single-Topic Mode** (for active testing/development) and **Batch Mode** (for processing multiple topics sequentially).

### Single-Topic Mode (Active by default)

1. Open `main.py` in your code editor.
2. Scroll to the execution block at the very bottom:

```python
if __name__ == "__main__":
    # ---------------------------------------------------------
    # TESTING MODE: Generate a single topic
    # ---------------------------------------------------------
    write_blog_post("Malaysia Top Tourists Spots")
```

3. Change the string to your desired topic.
4. Execute the script:

```bash
# If using uv (Recommended):
uv run main.py

# If using standard pip (ensure your virtual environment is activated first!):
python main.py
```

### Batch Mode

To process multiple topics automatically (with built-in API rate-limit delays):

1. Open `main.py` and scroll to the bottom.
2. Comment out `write_blog_post("...")`.
3. Uncomment the `topics` array and the `run_batch_pipeline(topics)` call:

```python
    # ---------------------------------------------------------
    # BATCH MODE (Future Proofing): Generate multiple topics
    # ---------------------------------------------------------
    topics = [
        "The Best Nasi Lemak in Kuala Lumpur", 
        "Exploring the Batu Caves"
    ]
    run_batch_pipeline(topics)
```
4. Run the script using `uv run main.py` or `python main.py`.

### Pipeline Workflow

1. **Text Pipeline**: CrewAI orchestrates the `planner` and `content_writer` to draft the post.
2. **Internal Fact Checking**: A dedicated `fact_checker` agent cross-references the draft against its internal LLM knowledge base to prevent hallucinations.
3. **Editing & Illustration**: The `editor` polishes the verified text, and the `illustrator` generates an optimized image prompt.
4. **Decoupled Image Generation**:
   - The system attempts to generate the image using the **NVIDIA NIM API**.
   - If the NVIDIA API fails, it can automatically fall back to **AWS Bedrock Titan** (uncomment the fallback block in `main.py`).

### Retrieving Output

When the run completes, check the `output/` directory (created automatically if it doesn't exist). To prevent overwriting data, outputs are dynamically saved using safe filenames based on the topic (e.g., `malaysia_top_tourists_spots.md`).

- `output/[safe_filename].md`: The final written and fact-checked article.
- `output/[safe_filename].jpg`: The generated featured illustration.
- `output/[safe_filename].txt`: The isolated prompt used for image generation.

## Advanced Usage

### Customizing Agents

You can fine-tune agent behaviors, instructions, and target styles by editing the YAML configuration files:

- **`config/agents.yaml`**: Adjust the roles, backstories, and goals of each agent. For example, the `illustrator` uses a structured prompt layer approach to ensure realistic photography and adheres strictly to a < 512 character limit.
- **`config/tasks.yaml`**: Define the specific step-by-step instructions and expected outputs.

### Image Provider Overrides

In `crew.py` and `main.py`, you can manually switch the active providers by commenting/uncommenting the respective code blocks.

### Text Generator (LLM) Overrides

By default, the pipeline uses NVIDIA NIM (`llama-3.1-70b-instruct`) in `crew.py`. To fallback to AWS Bedrock (`claude-3-5-sonnet`), comment out the NVIDIA block and uncomment the AWS block:

```python
# --- AWS Bedrock Fallback (Claude 3.5 Sonnet) ---
llm = LLM(
    model="bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0",
    temperature=0.4,
    max_tokens=8192
)

# --- NVIDIA NIM Primary LLM (Llama 3.1 70B) ---
# llm = LLM(
#     model="openai/meta/llama-3.1-70b-instruct",
#     base_url="https://integrate.api.nvidia.com/v1",
#     api_key=os.environ.get("NVIDIA_NIM_API_KEY"),
#     temperature=0.4
# )
```

### Image Provider Overrides

In `main.py`, you can manually switch the active image generator. 

**To use NVIDIA NIM (Default):**
Leave the NVIDIA block uncommented and comment out the AWS Bedrock Titan block.
```python
# --- Primary: NVIDIA NIM Image Generation ---
image_generator = NvidiaImageTool()
image_result = image_generator.generate(image_prompt)
print(image_result)

# --- Fallback: AWS Bedrock Titan ---
# image_generator = TitanImageTool()
# image_result = image_generator.generate(image_prompt)
# print(image_result)
```

**To use AWS Bedrock Titan (Fallback):**
Comment out the NVIDIA block and uncomment the AWS Bedrock Titan block.
```python
# --- Primary: NVIDIA NIM Image Generation ---
# image_generator = NvidiaImageTool()
# image_result = image_generator.generate(image_prompt)
# print(image_result)

# --- Fallback: AWS Bedrock Titan ---
image_generator = TitanImageTool()
image_result = image_generator.generate(image_prompt)
print(image_result)
```

## API Reference

The project defines decoupled image generation tools in `custom_tools.py` to prevent CrewAI abstraction issues from hiding errors:

- `NvidiaImageTool.generate(prompt: str)`: Sends a request to the NVIDIA NIM API to generate an image from the provided text prompt.
- `TitanImageTool.generate(prompt: str)`: Utilizes the `boto3` Bedrock Runtime client to invoke the Amazon Titan image generator, strictly adhering to its 512-character prompt limit.

## Troubleshooting

### `ModuleNotFoundError: No module named 'crewai'`
If you encounter this error when running `python main.py`, it means the script is executing using your global system Python rather than the isolated virtual environment where the packages were installed.

**Solution**:
- If you used `uv`: Always run the script using `uv run main.py`. This tells `uv` to automatically find and use the correct virtual environment.
- If you used `pip`: Ensure you have activated your virtual environment (e.g., `.\venv\Scripts\activate`) before running `python main.py`. Your terminal prompt should show `(venv)` at the beginning of the line.

## License

MIT © [Your Name](https://github.com/yourname)