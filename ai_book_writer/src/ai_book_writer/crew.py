from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool
from dotenv import load_dotenv
load_dotenv()
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class AiBookWriter():
    """AiBookWriter crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    ollama_llms = LLM(
        model= "ollama/deepseek-r1",
        base_url="http://localhost:11434/api/generate"
    )

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def data_collector(self) -> Agent:
        return Agent(
            config=self.agents_config['data_collector'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def web_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['web_scraper'],
            verbose=True,
            tools=[ScrapeWebsiteTool()],
            llm= self.ollama_llms
        )
    
    @agent
    def ai_news_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['ai_news_writer'],
            verbose=True,
            llm= self.ollama_llms        
        )
    @agent
    def file_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['file_writer'],
            verbose=True,
            tools=[FileWriterTool()],
            
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def data_collector_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_collector_task'],
        )
    
    @task
    def web_scraper_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_scraper_task'],
        )
   
    @task
    def ai_news_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['ai_news_writer_task'],
        )
    @task
    def file_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['file_writer_task'],
        )
    

    

    @crew
    def crew(self) -> Crew:
        """Creates the AiBookWriter crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
