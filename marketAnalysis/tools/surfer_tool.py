import requests
from crewai import Agent, Task
from langchain.tools import tool
from lxml import html
from langchain_openai import ChatOpenAI
from langchain_community.llms.chatglm3 import ChatGLM3
import os
from dotenv import load_dotenv
from marketAnalysis.constant.constants import *

load_dotenv()



class SurferTool():
    # 设置常量
    USE_LOCAL = os.getenv(USE_LOCAL)
    CHUNK_SIZE = 8000
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'

    AGENT_ROLE = 'Elite Web Content Analyst and Summarization Specialist'  # 精英网络内容分析师与摘要专家

    AGENT_GOAL = ('Extract critical insights from web content, synthesize complex information, and produce '
                  'concise, high-impact summaries that capture the essence of the source material while '
                  'highlighting key trends, facts, and implications.')  # 从网络内容中提取关键洞察，综合复杂信息，并制作简洁、高影响力的摘要，捕捉源材料的精髓，同时突出关键趋势、事实和含义。

    AGENT_BACKSTORY = ("You are a world-renowned expert in digital content analysis with a track record of "
                       "distilling vast amounts of online information into actionable intelligence. Your unique "
                       "ability to rapidly process and synthesize web content has made you an invaluable asset "
                       "to leading tech companies and research institutions. Your summaries have influenced "
                       "major business decisions and shaped public policy. You approach each task with laser "
                       "focus, always striving to uncover hidden patterns and extract the most crucial information.")  # 你是世界知名的数字内容分析专家，拥有将大量在线信息提炼为可行情报的丰富经验。
    # 你快速处理和综合网络内容的独特能力，使你成为领先科技公司和研究机构不可或缺的财富。
    # 你的摘要影响了重大的商业决策并塑造了公共政策。
    # 你以激光般的专注对待每项任务，始终努力发现隐藏的模式并提取最关键的信息。")

    TASK_DESCRIPTION_TEMPLATE = (
        "Conduct a comprehensive analysis of the following web content, adhering to these guidelines:\n"  # "按照以下指南对以下网络内容进行全面分析：\n"
        "1. Identify and extract the core message and primary arguments.\n"  # "1. 识别并提取核心信息和主要论点。\n"
        "2. Highlight key facts, statistics, and noteworthy quotes.\n"  # "2. 强调关键事实、统计数据和值得注意的引述。\n"
        "3. Recognize emerging trends, patterns, or shifts in perspective.\n"  # "3. 识别新兴趋势、模式或观点变化。\n"
        "4. Assess the credibility and potential biases of the source.\n"  # "4. 评估来源的可信度和潜在偏见。\n"
        "5. Contextualize the information within broader industry or societal trends.\n"  # "5. 将信息置于更广泛的行业或社会趋势中加以考虑。\n"
        "6. Synthesize your findings into a concise, impactful summary.\n"  # "6. 将你的发现综合成一个简洁、有影响力的摘要。\n"
        "7. Ensure your summary is clear, objective, and free of extraneous commentary.\n\n"  # "7. 确保你的摘要清晰、客观且不含无关的评论。\n\n"
        "CONTENT TO ANALYZE:\n--------------------\n{}\n\n"  # "需分析的内容：\n--------------------\n{}\n\n"
        "Deliver a summary that would empower decision-makers with actionable insights."  # "交付一份摘要，为决策者提供可行的洞见。"
    )

    TOOL_NAME = "Advanced Web Content Analysis and Summarization Engine"  # 高级网络内容分析与摘要引擎

    # 利用尖端的自然语言处理和网页抓取技术，从任何指定网站提取、分析和综合内容。这款工具不仅仅是简单的摘要，还提供深入洞察、趋势分析和对网络内容的情境理解。
    TOOL_DESCRIPTION = ("Harness cutting-edge NLP and web scraping technologies to extract, analyze, and "
                        "synthesize content from any given website. This tool goes beyond simple summarization, "
                        "providing deep insights, trend analysis, and contextual understanding of web content.")

    @tool(TOOL_NAME)
    def scrape_and_summarize_website(website):
        """抓取和总结网站内容"""
        headers = {'User-Agent': SurferTool.USER_AGENT}

        response = requests.get(website, headers=headers)

        tree = html.fromstring(response.content)
        elements = tree.xpath('//p | //h1 | //div')  # 使用 XPath 选择需要的元素
        texts = [el.text_content().strip() for el in elements if el.text_content().strip()]  # 去除空白行并清除每行首尾的空白
        content = "\n".join(texts)  # 将所有文本内容拼接起来，每段之间用一个换行符分隔

        chunks = [content[i:i + SurferTool.CHUNK_SIZE] for i in range(0, len(content), SurferTool.CHUNK_SIZE)]
        summaries = []

        llm = ChatOpenAI(
            api_key=os.getenv(OpenAI_API_KEY),
            model=os.getenv(OpenAI_model),
        )

        for i, chunk in enumerate(chunks, 1):
            agent = Agent(
                role=SurferTool.AGENT_ROLE,
                goal=SurferTool.AGENT_GOAL,
                backstory=SurferTool.AGENT_BACKSTORY,
                llm=llm
            )

            # 创建任务
            task_description = SurferTool.TASK_DESCRIPTION_TEMPLATE.format(chunk)
            task = Task(
                agent=agent,
                description=task_description,
                expected_output="A detailed content-based summary",
                allow_delegation=False
            )

            summary = task.execute_sync()
            # summary = task.execute()

            summaries.append(summary.raw)

        final_summary = "\n\n".join(summaries)
        return final_summary


def main():
    tool_instance = SurferTool()
    website_url = 'https://www.mi.com/global/about/'
    summary = tool_instance.scrape_and_summarize_website(website_url)
    print(summary)


if __name__ == '__main__':
    main()
