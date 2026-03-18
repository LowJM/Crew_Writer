# CrewAI Blog Writer (AWS Bedrock Edition)

Welcome to your AI-powered Blog Writer! This program uses the **CrewAI** framework to automate the creation of a full blog post and a custom illustration. It leverages **AWS Bedrock** (specifically Claude 3.5 Sonnet and Amazon Titan Image Generator) to act as a team of specialized AI agents working together to write, edit, and illustrate your article.

---

## 🚀 How to Run the Program from Scratch

### 1. Prerequisites
Ensure you have the following installed on your computer:
- Python 3.12+
- An AWS Account with On-Demand model access enabled for:
  - `anthropic.claude-3-5-sonnet-20241022-v2:0`
  - `amazon.titan-image-generator-v2:0`

### 2. Setup your Environment
First, open your terminal (Command Prompt or PowerShell) and navigate strictly into this project folder (`Crew_Writer`).

1. **Activate the Virtual Environment**
   ```powershell
   .\venv\Scripts\activate
   ```
2. **Install Dependencies** (if you haven't already):
   ```powershell
   pip install crewai crewai-tools python-dotenv boto3
   ```

### 3. Configure your API Keys
In the root of this folder, there is a file called `.env`. Open it and fill in your customized AWS credentials. It should look exactly like this:

```env
OPENAI_API_KEY="your_openai_api_key_here" # Not used by default, but required for CrewAI core
SERPER_API_KEY="your_serper_api_key_here" # (Optional) used if you re-enable the Serper web search tool

# AWS Bedrock Credentials
AWS_ACCESS_KEY_ID="your_aws_access_key"
AWS_SECRET_ACCESS_KEY="your_aws_secret_key"
AWS_REGION_NAME="us-east-1" # MUST be us-east-1 to support the Titan Image Generator
```

---

## ✍️ How to Input Your Topic

To change what the AI writes about, you simply edit the **`main.py`** file in your code editor.

1. Open `main.py`.
2. Scroll to the very bottom to line 26.
3. You will see this line of code:
   ```python
   write_blog_post("2026's Good news on Global warming issue")
   ```
4. **Change the text inside the quotes** to whatever topic you want! (e.g., `"The History of Roman Architecture"` or `"Why Python is great for Data Science"`).

**What can you input?**
Absolutely anything! Because we generalized the AI's instructions, you can input historical events, coding tutorials, creative stories, or news summaries. The AI will automatically research and adapt its style to your request.

---

## ▶️ Running the Program

Once your topic is set in `main.py`, run this exact command in your terminal (make sure your `(venv)` is activated):

```powershell
python main.py
```

*Note: The script is specifically configured with a strict speed limit (`max_rpm=2`) to prevent AWS from throttling your account for "Too Many Requests". Because of this, it will take roughly 5 to 10 minutes to finish writing. You will see progress logs printing in your console.*

---

## 📂 Where is the Output Placed?

Once the script completely finishes, it will automatically place two files into the **`output`** folder located inside this directory:

1. **`output/blog_post.md`**: This is your final written article formatted in Markdown. You can open this in any text editor, VS Code, or publish it directly to a blog.
2. **`output/picture.jpg`**: This is the custom illustration drawn by the Amazon Titan AI to match your topic.

**Important:** If you run the script a second time with a new topic, it will completely OVERWRITE `blog_post.md` and `picture.jpg`. If you want to keep your articles, make sure to rename them or move them somewhere else before running `python main.py` again!