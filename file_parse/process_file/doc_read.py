# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/4/27 09:39 
# @Author : zgf

import os
import asyncio
from utils.common_util import cost_time
from file_parse.process_file.docx_read import read_docx_file


async def convert_doc_to_docx(src_file: str, dst_dir: str) -> None:
    """
        使用LibreOffice将指定的DOC文件转为DOCX格式，并将输出文件保存到指定目录中。

        :param src_file: 要转换的DOC文件的完整路径
        :param dst_dir: 转换后的DOCX文件将被保存到的目录路径
        :return: None
    """
    cmd = ["libreoffice", "--headless", "--convert-to", "docx", "--outdir", dst_dir, src_file]

    proc = await asyncio.create_subprocess_exec(*cmd)
    await proc.communicate()


async def batch_convert_doc_to_docx(src_dir: str, dst_dir: str) -> None:
    """
    使用LibreOffice将指定目录中所有的DOC文件批量转换为DOCX格式，
    并将输出文件保存到指定目录中。

    :param src_dir: 要转换的所有DOC文件所在的目录路径
    :param dst_dir: 转换后的DOCX文件将被保存到的目录路径
    :return: None
"""
    tasks = [asyncio.create_task(convert_doc_to_docx(os.path.join(src_dir, file), dst_dir))
             for file in os.listdir(src_dir) if file.endswith('.doc')]
    await asyncio.gather(*tasks)


@cost_time
async def read_doc_file(file_path):
    """
    读取doc
    """
    try:
        await convert_doc_to_docx(file_path, os.path.dirname(file_path))
        print("{}文件转换成功！".format(file_path))
    except Exception as e:
        print("文件转换失败：", str(e))
    else:
        doc_data = await read_docx_file(file_path+"x")
        if os.path.exists(file_path + "x"):
            # 存在则删除文件
            os.remove(file_path + "x")
        return doc_data
