FROM sanmaomashi/python:3.9.16-ubuntu20.04

#gpu
#FROM sanmaomashi/python:3.9.16-ubuntu20.04-cuda11.7-cudnn8

# 设置paddlenlp
ENV PPNLP_HOME /root/.models/paddlenlp

# 设置modelscope模型路径
ENV MODELSCOPE_CACHE /root/.models/modelscope

# 设置huggingface模型路径
ENV HF_HOME /root/.models/huggingface

COPY . /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "ai_main.main:app", "--host", "0.0.0.0", "--port", "1701"]