from crewai import Agent, LLM
import os
from crewai_tools import SerperDevTool
from src.tools.youtube_search_tools import YoutubeVideoSearchTool

class CompanyResearchAgents():
    def __init__(self, company):
        self.youtubeSearchTool = YouTubeVideoSearchTool()
        self.searhInternetTool = SerperDevTool()
        self.llm = LLM(
            model="gemini/gemini-1.5-pro-latest",
            temperature=0.4,
            goggle_api_key=os.getenv('GOOGLE_API_KEY')
        )

    
    def research_manageer(self, companies: list[str], positions: list[str]):
        return Agent(
            role="Company Research Manager",
            goal=f"""Generate a list of JSON objects containing the urls for 3 recent blog articles and
                the url and title for 3 recent YouTube interview, for each position in each company.
                
                Companies: {companies}
                Positions: {positions}
                
                Important:
                - The final list of JSON objects must be include all companies and positions. Do not leave any out.
                - If you can't find information for a specific position, fill in the informaiton with the word "MISSING".
                - Do not generate fake information. ONly return the information you find. Nothing else!
                - Do not stop researching until you find the requested information for each position in each company.
                - All the companies and positions exist so keep researching until you find the information for each one.
                - Make sure you each researched position for each company contains 3 blog articles and 3 YouTube interviews.           
                """,
            backstory="""As a Company Research Manager, you are responsible for aggregating all the researched information
                    into a list.""",
            llm=self.llm,
            tools=[self.searhInternetTool, self.youtubeSearchTool],
            verbose=True,
            allow_delegation=True
        )
    
    def company_research_agent(self):
        return Agent(
            role="Company Research Agent",
            goal="""Look up the specific positions for a given company and find urls for 3 recent blod articles and 
                the url and title for 3 reent YouTibe interview for each person in the specified positions. It is your job to return this collect
                information in a JSON object""",
            backstory="""As a Company Research Aget, you are responsible for looking up specific positions
                within a company and gathering relevant information.
                
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!
                - Make sure you find the persons name who holds the position.
                - Do not generate fake information. ONly return the information you find. Nothing else!
                """,
            tools=[self.searhInternetTool, self.youtubeSearchTool],
            llm=self.llm,
            verbose=True
        )