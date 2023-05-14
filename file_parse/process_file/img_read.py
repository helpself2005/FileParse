# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/13 17:41 
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi


from typing import Dict
from utils.common_util import cost_time
from paddleocr import PaddleOCR


ocr = PaddleOCR(use_angle_cls=True, use_gpu=True, lang="ch")


@cost_time
async def read_img_file(file_path) -> Dict:
    """Read a img file"""
    results = ocr.ocr(file_path)
    img_data = ''
    for line in results[0]:
        img_data += line[1][0] + "/n"
    response_data = {
        "file": file_path,
        "content": img_data.strip(),
    }
    return response_data
