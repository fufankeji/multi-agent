# import nltk
# nltk.download('punkt')
#
# nltk.download('punkt_tab')

from crewai import Agent, Task

crewai_agent = Agent(
    role="Github Agent",
    goal="You take action on Github using Github APIs",
    backstory=(
        "You are AI agent that is responsible for taking actions on Github "
        "on users behalf. You need to take action on Github using Github APIs"
    ),
    verbose=True,
    tools=[],
)


task = Task(
    description="Star a repo ComposioHQ/composio on GitHub",
    agent=crewai_agent,
    expected_output="if the star happened",
)

task.execute()

