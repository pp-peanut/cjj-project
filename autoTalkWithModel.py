import pandas as pd
import numpy as np
import requests
import json
from uiautomation import WindowControl,MenuControl
import uvicorn
import torch
from transformers import pipeline, AutoTokenizer
from fastapi import FastAPI, Request

if __name__ == '__main__':
    model_name_or_path = 'E://workspace//AI//models//llama3-Chinese//Llama3-Chinese-8B-Instruct'
    # 这里的模型路径替换为你本地的完整模型存储路径 （一般从huggingface或者modelscope上下载到）
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=False)
    pipe = pipeline(
        "conversational",
        model_name_or_path,
        torch_dtype=torch.float16,
        device_map="auto",
        max_new_tokens=512,
        do_sample=True,
        top_p=0.9,
        temperature=0.6,
        repetition_penalty=1.1,
        eos_token_id=tokenizer.encode('<|eot_id|>')[0]
    )
    # 如果是base+sft模型需要替换<|eot_id|>为<|end_of_text|>，因为llama3 base模型里没有训练<|eot_id|>这个token

    uvicorn.run(app, host='0.0.0.0', port=20002) # 这里的端口替换为你实际想要监听的端口

def chat_ollama(message):
    data = [
            {"role": "user", "content": message}
    ]
    # 访问messages列表中的第一个字典（索引为0），并替换其content字段
    data[0]["content"] = message

    response = pipe(data)
    # breakpoint()
    print(response)
    return response[-1]["content"]


wx = WindowControl(
    Name='微信',
    #searchDepth=1
)
print(wx)

wx.SwitchToThisWindow()

hw = wx.ListControl(Name='会话')
print('search communication binding', hw)
wx.TextControl(SubName='文件传输助手').Click(simulateMove=False)
while True:
    we = hw.TextControl(searchDepth=4)

    while not we.Exists(0):
        pass
    print("search unread message", we)

    if we.Name:
        we.Click(simulateMove=False)

        last_msg = wx.ListControl(Name='消息').GetChildren()[-1].Name
        print('read the last message', last_msg)

        # replyMsg = 'hello'

        replyMsg = chat_ollama(last_msg)

        wx.SendKeys(replyMsg, waitTime=0)
        wx.SendKeys('{Enter}', waitTime=0)
        hw.TextControl(foundIndex=2).Click()
        # wx.TextControl(SubName=last_msg[:2]).RightClick()
        wx.TextControl(SubName='文件传输助手').Click(simulateMove=False)