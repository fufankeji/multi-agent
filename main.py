import streamlit as st
import logging
from crewai import Crew
from textwrap import dedent
from marketAnalysis.agent.market_observers import MarketObserverAgents
from marketAnalysis.tasks.employee_goals import AgentGoals
from dotenv import load_dotenv
import threading
import queue
import time
import sys
import os
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

# Load environment variables
load_dotenv()


class TeeLogger(object):
    def __init__(self, filename, mode="a", original_stream=None):
        self.file = open(filename, mode, buffering=1,  encoding='utf-8')  # Line-buffered
        self.original_stream = original_stream

    def write(self, message):
        self.file.write(message)
        self.file.flush()  # Force flush after each write
        if self.original_stream:
            self.original_stream.write(message)
            self.original_stream.flush()

    def flush(self):
        self.file.flush()
        if self.original_stream:
            self.original_stream.flush()

    def close(self):
        self.file.close()


# Configure logging
log_file = "analysis_logs.txt"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=log_file,
                    filemode='w')
logger = logging.getLogger(__name__)

# Ensure logger flushes immediately
for handler in logger.handlers:
    handler.flush = lambda: None

import re

from ansi2html import Ansi2HTMLConverter

conv = Ansi2HTMLConverter()


def read_new_logs(last_position):
    if os.path.exists(log_file):
        with open(log_file, 'r',  encoding='utf-8') as file:
            file.seek(last_position)
            new_content = file.read()
            new_position = file.tell()
        # Convert ANSI to HTML
        new_content = conv.convert(new_content)
        return new_content, new_position
    return "", 0


class MarketAnalysis:
    def __init__(self, company):
        self.company = company
        logger.info(f"初始化即将执行市场分析的公司: {company}")

    def run(self):
        try:
            agents = MarketObserverAgents()
            tasks = AgentGoals()

            research_analyst_agent = agents.research_analyst_employee()
            financial_analyst_agent = agents.financial_analyst_employee()
            investment_advisor_agent = agents.investment_consultant_employee()

            logger.info("Created agents for analysis")

            research_task = tasks.research(research_analyst_agent, self.company)
            financial_task = tasks.analyst_employee(financial_analyst_agent)
            recommend_task = tasks.final_report_employee(investment_advisor_agent)

            logger.info("Created tasks for analysis")

            crew = Crew(
                agents=[research_analyst_agent, financial_analyst_agent, investment_advisor_agent],
                tasks=[research_task, financial_task, recommend_task],
                verbose=True
            )

            logger.info("Initiating crew kickoff")
            result = crew.kickoff()
            logger.info("Crew analysis completed successfully")
            return result
        except Exception as e:
            logger.error(f"An error occurred during the analysis: {str(e)}")
            raise


def run_analysis(company):
    try:
        financial_crew = MarketAnalysis(company)
        result = financial_crew.run()
        logger.info("Analysis completed successfully")  # Add final log
        return result
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


def update_logs(log_placeholder, status_placeholder, stop_event):
    last_position = 0
    full_logs = ""
    while not stop_event.is_set():
        new_logs, last_position = read_new_logs(last_position)
        if new_logs:
            full_logs += new_logs
            log_placeholder.markdown(f"""
            <div style="height: 300px; overflow-y: scroll; background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
                <pre>{full_logs}</pre>
            </div>
            """, unsafe_allow_html=True)
        status_placeholder.text("Analysis in progress...")
        time.sleep(10)


def main():
    st.set_page_config(page_title="人工智能代理 - 动态市场分析工具", page_icon="📊", layout="wide")

    # 为了外观和更好的对齐，自定义CSS样式
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        font-weight: bold;
        height: 3em;
    }
    .log-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: white;
        height: 400px;
        overflow-y: scroll;
        padding: 10px;
        font-family: monospace;
    }
    .status-text {
        font-weight: bold;
        color: #1E90FF;
    }
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .icon-title {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # 居中对齐Header与图标
    st.markdown('<div class="icon-title">', unsafe_allow_html=True)
    st.markdown('# 📊 人工智能代理 - 动态市场分析工具')
    st.markdown('</div>', unsafe_allow_html=True)

    colored_header(label="", description="深入了解市场上使用先进人工智能代理的公司",
                   color_name="blue-70")

    add_vertical_space(2)

    st.write("在下面输入公司名称，开始由我们的人工智能代理提供全面的市场分析。")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        company = st.text_input("公司名称:", placeholder="e.g. 华为, 小米，阿里巴巴")
        start_analysis = st.button("开始进行分析")

    if start_analysis:
        if company:
            progress_bar = st.progress(0)
            status_placeholder = st.empty()
            log_placeholder = st.empty()

            # 重定向标准输出和标准错误到日志文件
            sys.stdout = TeeLogger(log_file, "w", sys.stdout)
            sys.stderr = TeeLogger(log_file, "a", sys.stderr)

            # 在单独的线程中运行分析
            result_queue = queue.Queue()
            analysis_thread = threading.Thread(target=lambda q: q.put(run_analysis(company)), args=(result_queue,))
            analysis_thread.start()

            # Update logs and status while the analysis is running
            last_position = 0
            full_logs = ""
            while analysis_thread.is_alive():
                new_logs, last_position = read_new_logs(last_position)
                if new_logs:
                    full_logs += new_logs
                    log_placeholder.markdown(f"""
                    <div class="log-container">
                        {full_logs}
                    </div>
                    """, unsafe_allow_html=True)
                status_placeholder.markdown('<p class="status-text">Analysis in progress...</p>',
                                            unsafe_allow_html=True)
                progress_bar.progress(
                    min(last_position / 1000, 1.0))  # Adjust the denominator based on expected log size
                time.sleep(1)

            # Get the final result
            result = result_queue.get()
            print(f"result: {result}")

            # Restore original stdout and stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            # Display the final result
            progress_bar.progress(1.0)
            status_placeholder.markdown('<p class="status-text">分析完成!</p>', unsafe_allow_html=True)
            st.success("成功完成市场分析!")

        #     with st.expander("查看详细分析报表", expanded=True):
        #         st.markdown(result)
        #
        #     st.download_button(
        #         label="Download Full Report",
        #         data=result,
        #         file_name=f"{company}_market_analysis.txt",
        #         mime="text/plain"
        #     )
        # else:
        #     st.warning("Please enter a company name to begin the analysis.")


if __name__ == "__main__":
    main()
