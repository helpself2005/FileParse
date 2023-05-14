# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/10 22:43 
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi

import os
from file_parse.process_file.txt_read import read_txt_file
from file_parse.process_file.md_read import read_md_file
from file_parse.process_file.docx_read import read_docx_file
from file_parse.process_file.doc_read import read_doc_file
from file_parse.process_file.excel_read import read_excel_file
from file_parse.process_file.csv_read import read_csv_file
from file_parse.process_file.json_read import read_json_file
from file_parse.process_file.ppt_read import read_ppt_file
from file_parse.process_file.speech_read import read_speech_file
from file_parse.process_file.img_read import read_img_file
from file_parse.process_file.pdf_read import read_pdf_file
from file_parse.process_file.html_read import read_html_file
from file_parse.process_file.video_read import read_video_file


class FileParser:

    def __init__(self, file_path: str, supported_file_types: list):
        self.file_paths = []
        self.file_index = 0
        self.supported_file_types = supported_file_types
        if os.path.isfile(file_path):
            self.add_supported_file(file_path)
        else:
            self.walk_and_add_files(file_path)
        self.current_file = self.file_paths[self.file_index] if self.file_index < len(self.file_paths) else None

    def add_supported_file(self, file_path):
        file_type = os.path.splitext(file_path)[-1].lower()
        if file_type in self.supported_file_types:
            self.file_paths.append(file_path)

    def walk_and_add_files(self, directory):
        for root, dirs, files in os.walk(directory, topdown=True):
            for name in files:
                self.add_supported_file(os.path.join(root, name))

    def increment_index(self) -> None:
        if self.file_index < len(self.file_paths) - 1:
            self.file_index += 1
            self.current_file = self.file_paths[self.file_index]
        else:
            self.current_file = None

    async def read_file(self):
        if not self.current_file:
            return ""
        file_type = os.path.splitext(self.current_file)[-1].lower()
        if file_type == '.txt':
            return await read_txt_file(self.current_file)
        elif file_type == '.md':
            return await read_md_file(self.current_file)
        elif file_type == '.docx':
            return await read_docx_file(self.current_file)
        elif file_type == '.doc':
            return await read_doc_file(self.current_file)
        elif file_type in ['.xls', '.xlsx']:
            return await read_excel_file(self.current_file)
        elif file_type in ['.csv']:
            return await read_csv_file(self.current_file)
        elif file_type in ['.json']:
            return await read_json_file(self.current_file)
        elif file_type in ['.ppt', '.pptx']:
            return await read_ppt_file(self.current_file)
        elif file_type in ['.wav', '.mp3', 'wma']:
            return await read_speech_file(self.current_file)
        elif file_type in ['.png', '.jpg', '.jpeg']:
            return await read_img_file(self.current_file)
        elif file_type == '.pdf':
            return await read_pdf_file(self.current_file)
        elif file_type in ['.html', '.htm']:
            return await read_html_file(self.current_file)
        elif file_type == '.mp4':
            return await read_video_file(self.current_file)
        else:
            return "Unsupported file type"

