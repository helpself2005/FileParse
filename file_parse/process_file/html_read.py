# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/13 13:34 
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi

from bs4 import BeautifulSoup
from typing import Dict
from utils.common_util import cost_time

@cost_time
async def read_html_file(file_path) -> Dict:
    """
    读取指定路径下的 HTML 文件的标题和body内容，并返回一个字典。
    :param file_path: HTML 文件路径
    :return: 字典，包含文件路径，标题和 body 内容。
    """
    # 打开并读取HTML文件
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'lxml')

        # 获取标题
        title = soup.title.string if soup.title else "No title"

        # 获取 body 内容
        body_content = soup.body.text if soup.body else "No body content"

        response_data = {
            "file": file_path,
            "content": {"title": title, "body_content": body_content},
        }
    return response_data
