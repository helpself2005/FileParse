# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/13 17:41 
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi

import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from file_parse.process_file.img_read import read_img_file
from fastapi import HTTPException
from utils.common_util import cost_time
from utils.common_util import logger


async def is_pdf_encrypted(file_path):
    try:
        pdf_reader = PdfReader(file_path)
        return pdf_reader.is_encrypted
    except Exception:
        return True


async def pdf_to_image_ocr(file_path):
    try:
        images = convert_from_path(file_path)
        text = ""

        for i, image in enumerate(images):
            temp_img_path = f"temp_img_{i}.png"
            try:
                image.save(temp_img_path, 'PNG')
                result = await read_img_file(temp_img_path)
                text += result["content"]
                logger.info(text)
            finally:
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)
        return text.strip()
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@cost_time
async def read_pdf_file(file_path):
    if await is_pdf_encrypted(file_path):
        raise HTTPException(status_code=400, detail="该PDF文件已加密或无法读取")

    try:
        pdf_reader = PdfReader(file_path)
        content = "".join(page.extract_text() for page in pdf_reader.pages)

        # 如果内容为空，可能是一个扫描的PDF，尝试OCR
        if not content:
            content = await pdf_to_image_ocr(file_path)

        response_data = {
            "file": file_path,
            "content": content,
        }
        return response_data
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
