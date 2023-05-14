# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/4 22:31
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi

import os
import shutil
import tempfile
import aiofiles
from typing import List
from fastapi import APIRouter, UploadFile, HTTPException
from file_parse.process_file.file_parser import FileParser

ALLOWED_EXTENSIONS = ['.txt', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.json', '.ppt', '.pptx', '.wav', '.mp3', 'wma',
                      '.png', '.jpg', '.jpeg', '.pdf', '.md', '.html', '.htm', '.mp4']

SUMMARY = "文件解析"

POST_DESCRIPTION = ("文件解析API\n\n\n"
                    "本API接受一个或者多个文本对象，进行内容解析。</br></br>"
                    "其中支持以下文件：txt、Word、Excel、pdf、csv、json、ppt、Markdown、HTML、 图片、音频、视频。</br></br>"
                    "包括以下格式: {}".format(ALLOWED_EXTENSIONS))

fp_router = APIRouter()


async def process_file(file_path: str):
    file_reader = FileParser(file_path, supported_file_types=ALLOWED_EXTENSIONS)
    text = await file_reader.read_file()
    return text


@fp_router.post("/file_parser/", summary=SUMMARY, description=POST_DESCRIPTION, )
async def file_parser(files: List[UploadFile]):
    success_files = []
    failed_files = []
    tmp_dir = tempfile.mkdtemp()
    try:
        for uploaded_file in files:
            file_extension = os.path.splitext(uploaded_file.filename)[1]

            if file_extension not in ALLOWED_EXTENSIONS:
                failed_files.append(
                    {"code": 500, "file_name": uploaded_file.filename, "error": f"不支持的文件类型: {file_extension}"})
                continue

            # 创建临时文件
            tmp_file_path = os.path.join(tmp_dir, uploaded_file.filename)

            # 使用aiofiles模块异步写入文件
            data = await uploaded_file.read()
            async with aiofiles.open(tmp_file_path, 'wb') as out_file:
                await out_file.write(data)

            try:
                data = await process_file(tmp_file_path)
                data["file"] = uploaded_file.filename
                success_files.append({"code": 200, "data": data})
            except HTTPException as e:
                failed_files.append({"code": 500, "file_name": uploaded_file.filename, "error": e.detail})

            # 关闭和删除临时文件
            os.remove(tmp_file_path)
    except Exception as e:
        shutil.rmtree(tmp_dir)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

    return {"status_code": 200, "success_files": success_files, "failed_files": failed_files}
