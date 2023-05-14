# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/13 17:41 
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi


from typing import Dict
from utils.common_util import cost_time
from paddlespeech.cli.asr.infer import ASRExecutor

asr = ASRExecutor()


@cost_time
async def read_speech_file(file_path) -> Dict:
    """
    读取音频文件并进行语音识别
    :return: result -- 语音识别结果
    """
    response_data = {
        "file": file_path,
        "content": asr(audio_file=file_path),
    }
    return response_data

