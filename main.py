# !/usr/bin/env python
# -*- coding:utf-8 -*-　
# @Time : 2023/5/12 20:44
# @Author : sanmaomashi
# @GitHub : https://github.com/sanmaomashi

import uvicorn
from pathlib import Path
from fastapi import FastAPI
from file_parse.api import fp_router

ROOT_PATH = Path(__file__).parent

app = FastAPI(
    title="文本解析 - API",
    openapi_url="/api/openapi.json",
    default_language="zh",
    debug=True
)


app.include_router(fp_router, prefix="/file_parse", tags=["文本解析"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1701, log_level="debug", reload=True)
