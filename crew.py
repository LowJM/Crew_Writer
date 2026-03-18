import warnings
warnings.filterwarnings('ignore')

#Imports
import os
from crewai import Agent, Task, Process, Crew, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai_tools import SerperDevTool
from custom_tools import TitanImageTool

from dotenv import load_dotenv
load_dotenv()

# Knowledge sources
# pdfs = PDFKnowledgeSource(
#     file_paths=['article1.pdf', 
#                 # 'article2.pdf', 
#                 # 'article3.pdf'
#                 ]
# )

# LLMs
llm = LLM(
    model="bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0",
    temperature=0.4
)

titan_image = TitanImageTool()


# Creating the crew: base shows where the agents and tasks are defined
@CrewBase
class BlogWriter():
    """Crew to write a blog post"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Configuring the agents
    @agent
    def writer_style(self) -> Agent:
        return Agent(
                config=self.agents_config['writer_style'],
                verbose=1,
                llm=llm,
                # knowledge_sources=[pdfs] # Disabled until valid OpenAI API key or Bedrock embedder is provided
                )

    @agent
    def planner(self) -> Agent:
        return Agent(
        config=self.agents_config['planner'],
        verbose=True,
        # tools=[SerperDevTool()], # Disabled until valid SERPER_API_KEY is provided
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
        tools=[titan_image],
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
        config=self.tasks_config['write'],
        output_file='output/blog_post.md' # This is the file that will be contain the final blog post.
        )
    
    @task
    def edit(self) -> Task:
        return Task(
        config=self.tasks_config['edit']
        )
    
    @task
    def illustrate(self) -> Task:
        return Task(
        config=self.tasks_config['illustrate'],
        output_file='output/picture.txt' # This is the file that will contain the link to the picture's.
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the Blog Post crew"""
        return Crew(
            agents= [self.writer_style(), self.planner(), self.content_writer(), self.editor(), self.illustrator()],
            tasks= [self.style(), self.plan(), self.write(), self.edit(), self.illustrate()],
            process=Process.sequential,
            verbose=True,
            max_rpm=2  # Added to strictly limit API calls and prevent AWS Bedrock throttling
        )