# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/13 17:41 
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi

import asyncio
import os
import tempfile
import cv2
import operator
import numpy as np
from fastapi import HTTPException
from typing import Dict, Tuple
from moviepy.editor import AudioFileClip
from utils.common_util import cost_time
from pydub import AudioSegment
from utils.common_util import logger
from scipy.signal import argrelextrema
from paddlenlp import Taskflow
from file_parse.process_file.img_read import read_img_file
from file_parse.process_file.speech_read import read_speech_file


similarity = Taskflow("text_similarity")


class Frame:
    def __init__(self, id, diff):
        self.id = id
        self.diff = diff

    def __lt__(self, other):
        return self.id < other.id if self.id != other.id else self.id < other.id

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        return self.id == other.id and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


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
        logger.error(f"Error extracting audio from video: {e}")
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
        raise HTTPException(status_code=500, detail=str(e))


def smooth(x, window_len=13, window='hanning'):
    s = np.r_[2 * x[0] - x[window_len:1:-1], x, 2 * x[-1] - x[-1:-window_len:-1]]
    w = np.ones(window_len, 'd') if window == 'flat' else getattr(np, window)(window_len)
    y = np.convolve(w / w.sum(), s, mode='same')
    return y[window_len - 1:-window_len + 1]


def rel_change(a, b):
    return 0 if max(a, b) == 0 else (b - a) / max(a, b)


async def keyframe_video(file_path, use_thresh=True, thresh=0.8, use_top_order=False, num_top_frames=50,
                         use_local_maxima=False):
    len_window = 50
    cap = cv2.VideoCapture(file_path)
    prev_frame = None
    frame_diffs = []
    frames = []
    success, frame = cap.read()
    i = 0

    while success:
        luv = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
        curr_frame = luv
        if curr_frame is not None and prev_frame is not None:
            diff = cv2.absdiff(curr_frame, prev_frame)
            diff_sum_mean = np.sum(diff) / (diff.shape[0] * diff.shape[1])
            frame_diffs.append(diff_sum_mean)
            frames.append(Frame(i, diff_sum_mean))
        prev_frame = curr_frame
        i += 1
        success, frame = cap.read()
    cap.release()

    keyframe_ids = set()
    if use_top_order:
        frames.sort(key=operator.attrgetter("diff"), reverse=True)
        keyframe_ids = {keyframe.id for keyframe in frames[:num_top_frames]}
    if use_thresh:
        print("Using Threshold")
        keyframe_ids.update(frames[i].id for i in range(1, len(frames)) if
                            rel_change(float(frames[i - 1].diff), float(frames[i].diff)) >= thresh)
    if use_local_maxima:
        print("Using Local Maxima")
        diff_array = np.array(frame_diffs)
        sm_diff_array = smooth(diff_array, len_window)
        frame_indexes = np.asarray(argrelextrema(sm_diff_array, np.greater))[0]
        keyframe_ids.update(frames[i - 1].id for i in frame_indexes)

    output_frames = []
    cap = cv2.VideoCapture(file_path)
    success, frame = cap.read()
    idx = 0

    while success:
        if idx in keyframe_ids:
            output_frames.append((idx, frame))
            keyframe_ids.remove(idx)
        idx += 1
        success, frame = cap.read()
    cap.release()

    return output_frames


async def extract_text_from_frame(idx_frame: Tuple[int, any]) -> Tuple[str, str]:
    idx, frame = idx_frame
    print(f"Processing frame: {idx}")
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=True) as tmp_frame:
        cv2.imwrite(tmp_frame.name, frame)
        res_frame = await read_img_file(tmp_frame.name)  # Here we call read_img_file asynchronously
        # Ensure that the res_frame has the "content" key
        text_frame = res_frame.get("content", "") if isinstance(res_frame, dict) else ""
    return str(idx).zfill(5), text_frame


async def extract_text_from_frames(frames, thresh_similarity=0.7):
    frame_to_text = []
    pre_text = None
    extracted_texts = []

    for idx_frame in frames:
        res = await extract_text_from_frame(idx_frame)
        if not pre_text:
            pre_text = res[1]
            frame_to_text.append({"frame_id": res[0], "text": res[1]})
            extracted_texts.append(res[1])
            continue

        simi = float(similarity([[res[1], pre_text]])[0]["similarity"])
        if simi > thresh_similarity:
            continue

        frame_to_text.append({"frame_id": res[0], "text": res[1]})
        extracted_texts.append(res[1])
        pre_text = res[1]

    return "\n".join(extracted_texts)


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
        audio.set_frame_rate(16000).export(audio_path, format="wav")

        result, res = await asyncio.gather(
            read_speech_file(audio_path),
            extract_text_from_frames(await keyframe_video(video_path, thresh=0.9), thresh_similarity=0.9)
        )
        # 返回语音识别结果
        response_data = {
            "file": video_path,
            "captions": result.get("content") if result else None,
            "content": res
        }
        return response_data

    except Exception as e:
        logger.error(str(f"Error recognizing speech from video: {e}"))
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 删除临时音频文件
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

