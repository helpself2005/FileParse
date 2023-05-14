# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/13 17:41 
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi


import csv
from typing import Dict
from utils.common_util import cost_time


@cost_time
async def read_csv_file(file_path) -> Dict:
    """
    读取指定路径下的 CSV 文件内容，并返回一个列表。
    :return:  列表，其中每个元素是 CSV 文件中每一行中的数据，以列表形式存储。
    """
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        response_data = {
            "file": file_path,
            "content": [row for row in reader],
        }
    return response_data
