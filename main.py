# Script to run the blog writer project
import os
import sys
from crew import BlogWriter
from custom_tools import TitanImageTool

def write_blog_post(topic: str):
    # Initialize the crew
    my_writer = BlogWriter()

    print("[START] Starting CrewAI pipeline to plan, write, and edit the blog post...")
    # Run
    result = (my_writer
              .crew()
              .kickoff(inputs = {
                  'topic': topic
                  })
    )
    print("[DONE] CrewAI text pipeline completed!")
    
    # Decoupled Image Generation
    print("[IMAGE] Running decoupled Illustrator tool...")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(BASE_DIR, 'output', 'picture.txt')
    
    if os.path.exists(prompt_path):
        with open(prompt_path, 'r', encoding='utf-8') as f:
            image_prompt = f.read().strip()
            
        print(f"[IMAGE] Extracted clean prompt. Sending to Titan...")
        
        try:
            # Manually run the image generator without masking exceptions
            image_generator = TitanImageTool()
            image_result = image_generator.generate(image_prompt)
            print(image_result)
        except Exception as e:
            print(f"[ERROR] Image generation failed: {e}")
            sys.exit(1)
    else:
        print("[ERROR] Illustrator prompt file (picture.txt) was not generated.")
        sys.exit(1)
        
    return result


if __name__ == "__main__":
    write_blog_post("Top Rated Cafes in Malaysia")