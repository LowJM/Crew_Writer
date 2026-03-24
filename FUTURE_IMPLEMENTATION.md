# Future Implementation: Automated Review Data to Content Pipeline

This document outlines the conceptual architecture and implementation steps required to scale the current CrewAI setup into an automated, data-driven content engine capable of analyzing raw review data and autonomously producing batches of fact-checked blog posts.

## Architecture Concept

The goal is to transition from a manual single-topic pipeline to a multi-stage automated pipeline:
1. **Data Ingestion:** Read structured review data (e.g., JSON or CSV format).
2. **Topic Generation:** Analyze the data and programmatically generate 20 targeted blog topics.
3. **Drafting:** Research the topics using the internet and write rich articles.
4. **Fact-Checking:** Verify statements against live internet data.
5. **Editing & Illustration:** Finalize the article formatting and generate cover images.
6. **File Management:** Dynamically save the outputs to distinct files without overwritten overlaps.

---

## Required Additions to `config/agents.yaml`

To expand the Crew's intelligence, you will need two new specialist agents:

```yaml
data_analyst:
  role: Expert Data Trends Analyst
  goal: Read through JSON review datasets, extract key trends, and generate a list of 20 engaging blog post topics.
  backstory: You are a sharp, data-driven analyst who specializes in reading large amounts of restaurant review data and finding the most popular trends to write about.

fact_checker:
  role: Senior Fact Checker
  goal: Review blog drafts and use the internet to verify every date, statistic, and bold claim.
  backstory: You have an eagle eye for misinformation. You ruthlessly verify facts using the web and correct any hallucinations or outdated information made by content writers.
```

## Required Additions to `config/tasks.yaml`

You will define what exactly those new agents are assigned to do:

```yaml
analyze_data:
  description: >
    1. Read the provided review dataset.
    2. Identify the top 20 trends or top-reviewed venues.
    3. Output exactly 20 blog post titles formatted as a Python list.
  expected_output: >
    A list of 20 catchy blog post titles based on the dataset.
  agent: data_analyst

fact_check:
  description: >
    1. Read the provided draft from the Content Writer.
    2. Search the web to verify the accuracy of all businesses, dates, and claims mentioned.
    3. Adjust the text if false information is found.
  expected_output: >
    A verified, accurate markdown draft ready for final editing.
  agent: fact_checker
```

---

## Modifications to `crew.py`

You will need to import your Data Analyst and Fact-Checker into your Python code and provide them with the necessary tools:

1. **Add the Agents & Tasks:**
   Inject `@agent def data_analyst(self):` and `@agent def fact_checker(self):` into the `BlogWriter` class.
2. **Enable Web Search:**
   Uncomment `SerperDevTool()` and add it to the `tools=[]` array for both your `planner` and your `fact_checker` agents. *(Requires your 2,500 credit Serper account API key inside `.env`)*
3. **Enable File Reading:**
   Import `from crewai_tools import FileReadTool` and give it to the `data_analyst` agent so it can read your review datasets!

---

## Automation Logic in `main.py`

Currently, `main.py` runs exactly once and overwrites `output/blog_post.md`.
To safely generate 20 blogs in a single execution, you must transition to programmatic iteration.

### The New Pipeline Script
```python
import os
from crew import BlogWriter

def run_automated_pipeline():
    # 1. First, call your Data Analyst to get the 20 topics from your CSV/JSON
    # (Pseudo-code: topics = evaluate_data_task.execute())
    
    topics = [
        "2026 Top Reviewed Restaurants in New York",
        "The Rise of Vegan Diners in 2026",
        # ... 18 more topics
    ]
    
    # 2. Loop through each topic safely
    for idx, topic in enumerate(topics):
        print(f"Starting generation for Topic {idx+1}/20: {topic}")
        
        my_writer = BlogWriter()
        result = my_writer.crew().kickoff(inputs={'topic': topic})
        
        # 3. Dynamically save the outputs to prevent overwriting
        safe_filename = topic.replace(" ", "_").replace("'", "").lower()
        
        with open(f"output/{safe_filename}.md", "w", encoding="utf-8") as file:
            file.write(result.raw)
            
        print(f"✅ Successfully saved {safe_filename}.md")

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    run_automated_pipeline()
```

### AWS Bedrock Rate Limits Warning
Because generating 20 complete, fact-checked articles involving internet search requires dozens of AI steps per article, you will be making hundreds of API calls to `Claude 3.5 Sonnet`. 

1. **Throttle Your Execution:** Keep `max_rpm` enabled on your Crew.
2. **Batch Pauses:** Consider adding `import time; time.sleep(60)` between your Python loop iterations to give AWS limits time to cool down.
3. **Request a Quota Increase:** For a production pipeline running 20 articles concurrently, applying for an On-Demand quota limit increase in your AWS Console is highly recommended.

---

## Technical Debt Integration
The following partially implemented features were completely cleaned out of the main execution python scripts to improve maintainability, but they should be fully implemented safely in a future update:
- **PDFKnowledgeSource**: RAG document ingestion for the `writer_style` agent (pending finalization of local embeddings or a Bedrock equivalent).
- **SerperDevTool**: Live Google Search capabilities for the `planner` and future `fact_checker` agents (pending a valid `SERPER_API_KEY` registered in the environment).
