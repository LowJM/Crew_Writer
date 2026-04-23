# Script to run the blog writer project
import os
import sys
import time
from crew import BlogWriter
from custom_tools import TitanImageTool, NvidiaImageTool

def write_blog_post(topic: str):
    # Initialize the crew
    my_writer = BlogWriter()

    print(f"[START] Starting CrewAI pipeline for: {topic}")
    # Run
    result = (my_writer
              .crew()
              .kickoff(inputs = {
                  'topic': topic
                  })
    )
    print(f"[DONE] CrewAI text pipeline completed for: {topic}")
    
    # Decoupled Image Generation
    print("[IMAGE] Running decoupled Illustrator tool...")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(BASE_DIR, 'output', 'picture.txt')
    
    safe_filename = topic.replace(" ", "_").replace("'", "").lower()
    
    if os.path.exists(prompt_path):
        with open(prompt_path, 'r', encoding='utf-8') as f:
            image_prompt = f.read().strip()
            
        print(f"[IMAGE] Extracted clean prompt. Sending to NVIDIA NIM...")
        
        try:
            # --- Primary: NVIDIA NIM Image Generation ---
            image_generator = NvidiaImageTool()
            image_result = image_generator.generate(image_prompt)
            print(image_result)
        except Exception as e:
            print(f"[ERROR] Image generation failed: {e}")
            # We don't exit here so the text file still gets saved
    else:
        print("[ERROR] Illustrator prompt file (picture.txt) was not generated.")
        
    # Rename outputs safely to avoid overwrites
    blog_output = os.path.join(BASE_DIR, 'output', 'blog_post.md')
    pic_output = os.path.join(BASE_DIR, 'output', 'picture.jpg')
    
    safe_blog_output = os.path.join(BASE_DIR, 'output', f'{safe_filename}.md')
    safe_pic_output = os.path.join(BASE_DIR, 'output', f'{safe_filename}.jpg')
    safe_txt_output = os.path.join(BASE_DIR, 'output', f'{safe_filename}.txt')

    # Note: Windows os.rename throws an error if destination exists, so we replace instead
    if os.path.exists(blog_output):
        os.replace(blog_output, safe_blog_output)
        print(f"✅ Saved article: {safe_blog_output}")
        
    if os.path.exists(pic_output):
        os.replace(pic_output, safe_pic_output)
        print(f"✅ Saved image: {safe_pic_output}")
        
    if os.path.exists(prompt_path):
        os.replace(prompt_path, safe_txt_output)

    return result

def run_batch_pipeline(topics: list):
    for idx, topic in enumerate(topics):
        print(f"\n==============================================")
        print(f"Processing Topic {idx+1}/{len(topics)}: {topic}")
        print(f"==============================================\n")
        
        write_blog_post(topic)
        
        # Pause to prevent API rate limit issues
        if idx < len(topics) - 1:
            print("Sleeping for 60 seconds to respect API limits...")
            time.sleep(60)

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    
    # ---------------------------------------------------------
    # TESTING MODE: Generate a single topic
    # ---------------------------------------------------------
    write_blog_post("Malaysia Top Tourists Spots")
    
    # ---------------------------------------------------------
    # BATCH MODE (Future Proofing): Generate multiple topics
    # ---------------------------------------------------------
    # topics = [
    #     "The Best Nasi Lemak in Kuala Lumpur", 
    #     "Exploring the Batu Caves"
    # ]
    # run_batch_pipeline(topics)