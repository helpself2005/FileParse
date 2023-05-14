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
    读取指定路径下的 HTML 文件内容，并返回一个字典。
    :param tag: 指定的标签选择器
    :return: 字典，包含文件路径和匹配标签的内容。
    """
    # 打开并读取HTML文件
    with open(file_path, 'r') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'lxml')
        formatted_html = soup.prettify()
        response_data = {
            "file": file_path,
            "content": formatted_html,
        }
    return response_data
