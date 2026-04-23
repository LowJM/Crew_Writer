# Imports
import os
from crewai import Agent, Task, Process, Crew, LLM
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

load_dotenv()

# --- AWS Bedrock Fallback (Claude 3.5 Sonnet) ---
# llm = LLM(
#     model="bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0",
#     temperature=0.4,
#     max_tokens=8192
# )

# --- NVIDIA NIM Primary LLM (Llama 3.1 70B) ---
llm = LLM(
    model="openai/meta/llama-3.1-70b-instruct",
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_NIM_API_KEY"),
    temperature=0.4
)

# Creating the crew: base shows where the agents and tasks are defined
@CrewBase
class BlogWriter():
    """Crew to write a blog post"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    agents_config = os.path.join(BASE_DIR, "config/agents.yaml")
    tasks_config = os.path.join(BASE_DIR, "config/tasks.yaml")

    # Configuring the agents
    @agent
    def writer_style(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_style'],
            verbose=1,
            llm=llm
        )

    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config['planner'],
            verbose=True,
            llm=llm
        )
    
    @agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_writer'],
            verbose=1,
            llm=llm
        )
        
    @agent
    def fact_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['fact_checker'],
            verbose=1,
            llm=llm
        )
    

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],
            verbose=1,
            llm=llm
        )
    
    @agent
    def illustrator(self) -> Agent:
        return Agent(
            config=self.agents_config['illustrator'],
            verbose=1,
            llm=llm
        )


    # Configuring the tasks    
    @task
    def style(self) -> Task:
        return Task(
            config=self.tasks_config['mystyle'],
        )
    
    @task
    def plan(self) -> Task:
        return Task(
            config=self.tasks_config['plan'],
        )

    @task
    def write(self) -> Task:
        return Task(
            config=self.tasks_config['write']
        )
        
    @task
    def fact_check(self) -> Task:
        return Task(
            config=self.tasks_config['fact_check']
        )
    
    
    @task
    def edit(self) -> Task:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        return Task(
            config=self.tasks_config['edit'],
            output_file=os.path.join(BASE_DIR, 'output/blog_post.md')
        )
    
    @task
    def illustrate(self) -> Task:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        return Task(
            config=self.tasks_config['illustrate'],
            output_file=os.path.join(BASE_DIR, 'output/picture.txt')
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Blog Post crew"""
        return Crew(
            agents=[self.planner(), self.content_writer(), self.fact_checker(), self.editor(), self.illustrator()],
            tasks=[self.plan(), self.write(), self.fact_check(), self.edit(), self.illustrate()],
            process=Process.sequential,
            verbose=True,
            cache=False,
            max_rpm=2  # Added to strictly limit API calls and prevent AWS Bedrock throttling
        )