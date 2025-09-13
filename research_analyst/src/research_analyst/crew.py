from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool,ScrapeWebsiteTool
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ResearchAnalyst():
    """ResearchAnalyst crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self, output_file=None):
        self.llm = LLM(
            model=os.getenv("MODEL", "gemini/gemini-2.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY")
        )
        self.groq_llm = LLM(
            model=os.getenv("THINKING", "openrouter/qwen/qwen3-235b-a22b:free"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        
        self.output_file = output_file

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            llm=self.groq_llm,
            verbose=True,
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool()
            ],
            inject_date=True,
            reasoning=True,
            # allow_delegation=True,
            max_reasoning_attempts=10,
            max_rpm=5,
            max_iter=10
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            llm=self.groq_llm,
            verbose=True,
            # allow_delegation=True,
            reasoning=True,
            max_reasoning_attempts=10,
            max_rpm=5,
            max_iter=10
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file=self.output_file if hasattr(self, 'output_file') and self.output_file else 'research_analyst\Reports\report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ResearchAnalyst crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            max_rpm=30,
            cache=True,
            embedder={      #If you're using groq or open router keep embedder otherwise remove it
            "provider": "huggingface",
            "config": {
                "model": 'sentence-transformers/all-MiniLM-L6-v2'
                        }
            }
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
