# Future Implementation: Automated Topic Generation & RAG Pipeline

This document outlines the conceptual architecture and implementation steps required to finalize the automated data-driven content engine. Having successfully implemented the internal Fact Checker and the `main.py` dynamic batch loop, the next phase focuses entirely on data ingestion and document RAG.

## Phase 1: Data Ingestion & Topic Generation

Currently, the pipeline requires manually typing topics into a Python list in `main.py`. The goal is to fully automate this by reading from a CSV or JSON dataset.

### 1. `data_analyst` Agent
We will create a separate `TopicGeneratorCrew` that runs *before* the main `BlogWriter` loop.

Add to `config/agents.yaml`:
```yaml
data_analyst:
  role: Expert Data Trends Analyst
  goal: Read through JSON/CSV review datasets, extract key trends, and generate a list of engaging blog post topics.
  backstory: You are a sharp, data-driven analyst who specializes in reading large amounts of restaurant review data and finding the most popular trends to write about.
```

Add to `config/tasks.yaml`:
```yaml
analyze_data:
  description: >
    1. Read the provided review dataset.
    2. Identify the top trends or top-reviewed venues.
    3. Output the exact number of required blog post titles formatted strictly as a JSON array.
  expected_output: >
    A strict JSON array of blog post titles based on the dataset.
  agent: data_analyst
```

### 2. Integration into `main.py`
In `main.py`, you will instantiate the `TopicGeneratorCrew`, give the analyst a `FileReadTool` or `CSVSearchTool`, and execute it to return the Pydantic array. You will then pass that array directly into the `run_batch_pipeline(topics)` loop.

---

## Phase 2: Technical Debt & Local RAG

The current `fact_checker` relies purely on the internal intelligence of Llama 3.1 70B. For hyper-specific company datasets, we need to implement Local Retrieval-Augmented Generation (RAG).

- **PDFKnowledgeSource / CSVSearchTool**: We will ingest local documentation and provide it to the `writer_style` agent (for brand voice guidelines) and the `fact_checker` agent (for verifying proprietary claims).
- **Embeddings**: This will require finalizing a local embedding model or using an AWS Bedrock embedding equivalent (like Amazon Titan Text Embeddings) to convert your PDFs into searchable vector data.
