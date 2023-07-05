#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   app.py
@Contact :   

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------

"""

# Start dance your fingers
import traceback
import time
import random
import string
import sys
import os

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from algo_sdk.logging_api import insert_into_wenda_logging
from algo_sdk.feedback_api import insert_into_wenda_feedback
from utils.log import logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'algo_sdk'))
app = FastAPI()

# # ------log-------
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# fh = logging.FileHandler(filename='logs/server.log')
# formatter = logging.Formatter(
#     "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
# )
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# logger.addHandler(ch)  # 将日志输出至屏幕
# logger.addHandler(fh)  # 将日志输出至文件
#
#


@app.middleware("http")
async def log_requests(request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} client_host={request.client.host} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


# --------API---------


@app.get("/")
def read_root(request: Request):
    return {"message": "Hello World", "client_ip": request.client.host}


class Log_Item(BaseModel):
    ip_address: str
    llm_type: str
    prompt: str
    response: str
    history: object

class FB_Item(BaseModel):
    history: object
    llm_type: str
    temperature: float
    top_p: float
    score: int
    current_func: str

@app.post("/api/logging")
async def text_logging(item: Log_Item, request: Request):
    try:
        start_at = time.time()
        data = insert_into_wenda_logging(request.client.host, item.ip_address, item.llm_type, item.prompt, item.response, item.history)
        end_at = time.time()
        time_length = (end_at - start_at)
        response_data = {"resultCode": '00', "resultMessage": "操作成功!",
                         "timeConsuming": "{:.2f}秒".format(time_length),
                         "result": 'done'}
    except Exception as e:
        logger.info(traceback.format_exc())
        response_data = {"resultCode": "", "resultMessage": "失败",
                         "reason": str(e)}
        raise HTTPException(status_code=500, detail=response_data)
    return response_data

@app.post("/api/feedback")
async def text_feedback(item: FB_Item, request: Request):
    try:
        start_at = time.time()
        data = insert_into_wenda_feedback(request.client.host,request.headers.get('referer'), item.llm_type, item.temperature, item.top_p, item.score, item.history, item.current_func)
        end_at = time.time()
        time_length = (end_at - start_at)
        response_data = {"resultCode": '00', "resultMessage": "操作成功!",
                         "timeConsuming": "{:.2f}秒".format(time_length),
                         "result": 'done'}
    except Exception as e:
        logger.info(traceback.format_exc())
        response_data = {"resultCode": "", "resultMessage": "失败",
                         "reason": str(e)}
        raise HTTPException(status_code=500, detail=response_data)
    return response_data
