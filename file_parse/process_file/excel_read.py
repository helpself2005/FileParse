# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/13 17:41 
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi


import pandas as pd
from typing import Dict
from utils.common_util import cost_time


@cost_time
async def read_excel_file(file_path) -> Dict:
    """
    读取指定路径下的 Excel 文件内容，并返回一个字典。
    :return:  字典。其中，字典的键对应 Excel 文件中的列名称，字典的值对应每列中的所有数据，以列表形式存储。
    """
    response_data = {
        "file": file_path,
        "content": pd.read_excel(file_path).to_dict('list'),
    }
    return response_data
