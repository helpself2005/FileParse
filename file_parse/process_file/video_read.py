# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/13 17:41 
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi

import asyncio
import os
import tempfile
from fastapi import HTTPException
from typing import Dict
from moviepy.editor import AudioFileClip
from utils.common_util import cost_time
from pydub import AudioSegment
from utils.common_util import logger
from file_parse.process_file.speech_read import read_speech_file


async def extract_audio_from_video(video_path: str) -> str:
    """
    从视频文件中提取音频，并返回音频文件的临时路径
    :param video_path: 视频文件路径
    :return: 音频文件的临时路径
    """
    audio_path = None
    try:
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            audio_path = temp_audio.name

        # 提取音频
        audioclip = AudioFileClip(video_path)
        audioclip.write_audiofile(audio_path)
        audioclip.close()

        # 返回音频文件的临时路径
        return audio_path

    except Exception as e:
        print(f"Error extracting audio from video: {e}")
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
        raise HTTPException(status_code=500, detail=str(e))


@cost_time
async def read_video_file(video_path: str) -> Dict:
    """
    从视频文件中提取音频，并进行语音识别
    :param video_path: 视频文件路径
    :return: 语音识别结果
    """
    audio_path = await extract_audio_from_video(video_path)

    if audio_path is None:
        logger.error(str(f"Failed to extract audio from {video_path}"))
        raise HTTPException(status_code=500, detail=str(f"Failed to extract audio from {video_path}"))

    try:
        # 自动转换音频采样率为 16000Hz
        audio = AudioSegment.from_file(audio_path)
        audio = audio.set_frame_rate(16000)
        audio.export(audio_path, format="wav")

        # 语音识别
        result = await read_speech_file(audio_path)

        # 返回语音识别结果
        response_data = {
            "file": video_path,
            "video_speech": result.get("content") if result else None,
        }
        return response_data

    except Exception as e:
        logger.error(str(f"Error recognizing speech from video: {e}"))
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 删除临时音频文件
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
