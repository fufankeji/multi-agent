from marketAnalysis.agent.market_observers import MarketObserverAgents
from marketAnalysis.tasks.employee_goals import AgentGoals
from crewai import Crew


class MarketAnalysis:
    def __init__(self, company):
        self.company = company
        print(f"1. Initializes the company that will perform the market analysis: {company}")

    def run(self):
        try:
            # 实例化代理的基类
            agents = MarketObserverAgents()

            # 实例化代理的目标基类
            tasks = AgentGoals()

            # 实例化研究分析员角色
            research_analyst_agent = agents.research_analyst_employee()
            # 实例化金融分析师角色
            financial_analyst_agent = agents.financial_analyst_employee()
            # 实例化投资顾问角色
            investment_advisor_agent = agents.investment_consultant_employee()

            print("2. Created agents for analysis Successful !")

            research_task = tasks.research(research_analyst_agent, self.company)
            financial_task = tasks.analyst_employee(financial_analyst_agent)
            filings_task = tasks.research_on_filling_employee(financial_analyst_agent)
            recommend_task = tasks.final_report_employee(investment_advisor_agent)

            print("3. Created tasks for analysis Successful !")

            crew = Crew(
                agents=[research_analyst_agent, financial_analyst_agent, investment_advisor_agent],
                tasks=[research_task, financial_task, filings_task, recommend_task],
                verbose=True
            )

            print("4. Initiating crew kickoff Successful !")
            result = crew.kickoff()
            print("5. Crew analysis completed successfully !")

            return result
        except Exception as e:
            print(f"An error occurred during the analysis: {str(e)}")
            raise




def run_analysis(company):
    try:
        financial_crew = MarketAnalysis(company)
        result = financial_crew.run()
        print("Analysis completed successfully")
        return result
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    report = run_analysis("xiaomi")
    print(f"report: {report}")
