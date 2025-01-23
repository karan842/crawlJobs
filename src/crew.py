from src.job_manager import append_event
from src.agents import CompanyResearchAgents
from src.tasks import CompanyResearchTasks

class CompanyResearchCrew:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None
        
    def setup_crew(self, companies: list[str], positions: list[str]):
        print(f"Setting up crew for {self.job_id} and with companies {companies} and positions {positions}.")
        
        # SETUP AGENTS
        agents = CompanyResearchAgents()
        research_manager = agents.research_manageer(companies, positions)
        company_research_agent = agents.company_research_agent()
        
        # SETUP TASKS
        tasks = CompanyResearchTasks(self.job_id)
        company_research_tasks = [
            tasks.company_research(company_research_agent,company, positions) for company in companies
        ]
        manage_research(research_manager, companies,
                              positions, company_research_tasks)
        
        # CREATE CREW
        self.crew = Crew(
            agents=[research_manager, company_research_agent],
            tasks=[*company_research_tasks, manage_research],
            verbose=2
        )
    
    def kickoff(self):
        if not self.crew:
            print(f"No crew foudn for {self.job_id}")
            return 
        
        append_event(self.job_id, "CREW Started")
        try:
            print(f"Running crew for {self.job_id}")
            results = self.crew.kickoff()
            append_event(self.job_id, "CREW Complete")
            return results
        

        except Exception as e:
            append_event(self.job_id, f"An error occurred: {e}")
            return str(e)