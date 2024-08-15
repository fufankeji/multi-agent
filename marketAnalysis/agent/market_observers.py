import os
from dotenv import load_dotenv
from marketAnalysis.constant.constants import *

from langchain_openai import ChatOpenAI
from langchain_community.llms.chatglm3 import ChatGLM3

from crewai import Agent

load_dotenv()


class MarketObserverAgents:
    """
      用于创建和管理具有不同角色的市场观察代理的。

      该类提供了创建具有特定角色的代理的方法，例如金融分析师、研究分析师和投资顾问。它支持基于LangChain接入在线模型or私有化部署的开源模型进行代理交互。

      属性:
      llm (Union[ChatGroq, ChatOpenAI]): 代理使用的语言模型。

    """

    def __init__(self, use_local=os.getenv(USE_LOCAL)):
        """
        初始化 MarketObserverAgents 类。

        参数:
            use_local (bool, 可选): 如果为 True，则使用 开源模型 语言模型。
                                   如果为 False，则使用 OpenAI 语言模型。
                                   默认值为 False。
        """

        # 使用在线模型
        if not use_local:
            self.llm = ChatOpenAI(
                api_key=os.getenv(OpenAI_API_KEY),
                model=os.getenv(OpenAI_model),
            )
        else:
            # 使用开源模型, 这里使用的模型引擎为glm4-9b-chat
            self.llm = ChatGLM3(
                endpoint_url=os.getenv(endpoint_url),
            )

    def research_analyst_employee(self):
        """
        创建一个研究分析师代理。

        返回:
            Agent: 配置了研究分析师角色、目标和工具的代理。
        """
        return Agent(
            role=RESEARCH_ANALYST_ROLE,
            goal=RESEARCH_ANALYST_GOAL,
            backstory=RESEARCH_ANALYST_BACKSTORY,
            verbose=True,
            llm=self.llm,
            tools=[
                # TODO
            ]
        )

    def financial_analyst_employee(self):
        """
        创建一个金融分析师代理。

        返回:
            Agent: 配置了金融分析师角色、目标和工具的代理。
        """
        return Agent(
            role=FINANCIAL_ANALYST_ROLE,
            goal=FINANCIAL_ANALYST_GOAL,
            backstory=FINANCIAL_ANALYST_BACKSTORY,
            verbose=True,
            llm=self.llm,
            tools=[
                # TODO
            ]
        )

    def investment_consultant_employee(self):
        """
        创建一个投资顾问代理。

        返回:
            Agent: 配置了投资顾问角色、目标和工具的代理。
        """
        return Agent(
            role=INVESTMENT_ADVISOR_ROLE,
            goal=INVESTMENT_ADVISOR_GOAL,
            backstory=INVESTMENT_ADVISOR_BACKSTORY,
            verbose=True,
            llm=self.llm,
            tools=[
                # TODO
            ]
        )
