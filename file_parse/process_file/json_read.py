# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/13 17:41 
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi

import json
from typing import Dict
from utils.common_util import cost_time


@cost_time
async def read_json_file(file_path) -> Dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        response_data = {
            "file": file_path,
            "content": data,
        }
    return response_data