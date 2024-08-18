import requests
from bs4 import BeautifulSoup


def fetch_website_title(url):
    try:
        # 发送HTTP GET请求
        response = requests.get(url)

        # 确保请求成功
        response.raise_for_status()

        # 尝试从响应头中获取编码
        encoding = response.encoding
        if 'charset' in response.headers.get('Content-Type', ''):
            encoding = response.headers['Content-Type'].split('charset=')[-1]
        encoding='UTF-8'
        # 使用指定的编码（或自动检测的编码）解码响应内容
        # 注意：通常response.text已经使用正确的编码解码了，这里只是为了演示
        content = response.content.decode(encoding)

        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(content, 'html.parser')

        # 查找<title>标签并获取其内容
        title = soup.title.string if soup.title else '无标题'

        # 返回网页标题
        return title
    except requests.RequestException as e:
        # 捕捉并处理请求异常
        print(f"请求发生错误: {e}")
    except AttributeError:
        # 捕捉并处理无法找到<title>标签的情况
        print("未找到网页标题")

    # 示例：抓取某个网页的标题（请替换为实际的URL）


url = "https://www.baidu.com"
title = fetch_website_title(url)
if title:
    print(f"网页标题是: {title}")