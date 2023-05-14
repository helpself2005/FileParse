# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/13 13:34 
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi

import aiofiles
import chardet
from utils.common_util import cost_time
from typing import Optional, Any, Dict, AsyncIterator

CHUNK_SIZE = 1024 * 1024


async def query_file_encoding(file_path) -> Optional[Any]:
    """获取文件编码"""
    try:
        with open(file_path, 'rb') as f:
            detected_encoding = chardet.detect(f.read(100))['encoding']
            if detected_encoding == 'ascii':
                return 'utf-8'
            return detected_encoding
    except Exception as e:
        print(f"Error detecting encoding for file {file_path}: {e}")
        return None


async def read_txt_in_chunks(file_path, encoding, chunk_size=CHUNK_SIZE) -> AsyncIterator[str]:
    """
    迭代器：分块读取大的文本文件
    :param encoding: 文件编码
    :param chunk_size: 分块大小，默认为1024
    :return: 文件内容迭代器
    """
    async with aiofiles.open(file_path, 'rb') as f:
        while True:
            chunk_data = await f.read(chunk_size)
            if not chunk_data:
                break
            yield chunk_data.decode(encoding)


async def convert_txt_file_encoding(file_path, to_encoding: str) -> None:
    """ txt编码转换 """
    file_encode = await query_file_encoding(file_path)
    with open(file_path, 'rb') as f1, open(file_path, 'w', encoding=to_encoding) as f2:
        content = f1.read().decode(file_encode)
        f2.write(content)


@cost_time
async def read_txt_file(file_path) -> Dict[str, object]:
    """
    读取文本文件
    :return: 文件内容字符串
    """
    file_encode = await query_file_encoding(file_path)
    chunks = []
    async for chunk in read_txt_in_chunks(file_path, encoding=file_encode):
        chunks.append(chunk)
    file_content = ''.join(chunks)
    response_data = {
        "file": file_path,
        "content": file_content,
    }
    return response_data
