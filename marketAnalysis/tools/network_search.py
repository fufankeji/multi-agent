import json
import os
import requests
from langchain.tools import tool
from marketAnalysis.constant.constants import *
from dotenv import load_dotenv
load_dotenv()

class SearchTools():
    # 常量
    TOP_RESULTS = 3
    SEARCH_URL = "https://google.serper.dev/search"
    NEWS_URL = "https://google.serper.dev/news"

    TOOL_SEARCH_INTERNET = "Search the Internet"
    TOOL_SEARCH_NEWS = "Search the Internet News"

    @tool(TOOL_SEARCH_INTERNET)
    def search_internet(query):
        """
        用于搜索互联网上关于给定主题的信息，并返回相关结果。

        参数:
            query (str): 用户想要搜索的主题。

        返回:
            list: 包含相关搜索结果的列表。
        """

        payload = json.dumps({"q": query})

        headers = {
            'X-API-KEY': os.getenv(SERPER_API_KEY),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", SearchTools.SEARCH_URL, headers=headers, data=payload)

        results = response.json()["organic"]

        return SearchTools._format_results(results)

    @tool(TOOL_SEARCH_NEWS)
    def search_news(query):

        """ 用于搜索关于公司、股票或任何其他主题的新闻，并返回相关结果。
        Returns:
        """

        payload = json.dumps({"q": query})

        headers = {
            'X-API-KEY': os.getenv(SERPER_API_KEY),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", SearchTools.NEWS_URL, headers=headers, data=payload)

        results = response.json()["news"]

        return SearchTools._format_results(results)


    @staticmethod
    def _format_results(results):
        string = []
        for result in results[:SearchTools.TOP_RESULTS]:
            try:
                string.append('\n'.join([
                    f"Title: {result['title']}",
                    f"Link: {result['link']}",
                    f"Snippet{result['snippet']}",
                    "\n---------------------"
                ]))
            except KeyError:
                continue
        return '\n'.join(string)


if __name__ == '__main__':
    query = "xiaomi"
    print("搜索结果如下:")
    results = SearchTools.search_internet(query)
    print(results)
    print("\n ----------这是一条分割线------------------")
    news_results = SearchTools.search_news(query)
    print(news_results)