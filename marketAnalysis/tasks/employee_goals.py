import json
from crewai import Task
from textwrap import dedent
import os

# 导航到项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

# 构造配置文件的路径
CONFIG_FILE_PATH = os.path.join(project_root, 'config', 'config.json')

# 设置角色task关键字
TASKS_KEY = 'tasks'
RESEARCH_KEY = 'research'
DESCRIPTION_KEY = 'description'
EXPECTED_OUTPUT_KEY = 'expected_output'
FINANCIAL_ANALYSIS_KEY = 'financial_analysis'
FILINGS_ANALYSIS_KEY = 'filings_analysis'
RECOMMEND_KEY = 'recommend'


class AgentGoals():
    def __init__(self):
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            self.config = json.load(config_file)

    def research(self, agent, company):
        task_config = self.config[TASKS_KEY][RESEARCH_KEY]
        # f 字符串和 dedent 的使用使任务描述更具可读性。
        return Task(
            description=dedent(f"""
            {task_config[DESCRIPTION_KEY]}
            \nSelected company by the customer: {company}
            """),
            agent=agent,
            expected_output=task_config[EXPECTED_OUTPUT_KEY]
        )

    def analyst_employee(self, agent):
        task_config = self.config[TASKS_KEY][FINANCIAL_ANALYSIS_KEY]
        # f 字符串和 dedent 的使用使任务描述更具可读性。
        return Task(
            description=dedent(f"""
            {task_config[DESCRIPTION_KEY]}
            """),
            agent=agent,
            expected_output=task_config[EXPECTED_OUTPUT_KEY]
        )

    def research_on_filling_employee(self, agent):
        task_config = self.config[TASKS_KEY][FILINGS_ANALYSIS_KEY]
        # f 字符串和 dedent 的使用使任务描述更具可读性。
        return Task(
            description=dedent(f"""
            {task_config[DESCRIPTION_KEY]}
            """),
            agent=agent,
            expected_output=task_config[EXPECTED_OUTPUT_KEY]
        )

    def final_report_employee(self, agent):
        task_config = self.config[TASKS_KEY][RECOMMEND_KEY]
        # f 字符串和 dedent 的使用使任务描述更具可读性。
        return Task(
            description=dedent(f"""
            {task_config[DESCRIPTION_KEY]}
            """),
            agent=agent,
            expected_output=task_config[EXPECTED_OUTPUT_KEY]
        )
