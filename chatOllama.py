import requests
import json

# 定义请求的URL
url = 'http://localhost:11434/api/chat'

# 定义要发送的JSON数据
data = {
    "model": "llama3",
    "messages": [
        {
            "role": "user",
            "content": "why is the sky blue?"
        }
    ]
}

# 发送POST请求，并设置headers以告诉服务器我们正在发送JSON数据
response = requests.post(url, json=data)
# print(response.text)
# 检查请求是否成功
replyMessage=''
if response.status_code == 200:
    for line in response.text.splitlines():
        # print(line)
        # 去除行尾的换行符（如果有的话）
        line = line.strip()
        # 尝试解析JSON字符串
        try:
            data = json.loads(line)
            # 在这里，你可以对解析后的数据执行任何操作
            # 例如，打印出每个消息的"content"字段
            # {"model": "llama3", "created_at": "2024-08-17T09:35:43.6125159Z",
            #  "message": {"role": "assistant", "content": ""}, "done_reason": "stop", "done": true,
            #  "total_duration": 114968844000, "load_duration": 5668196500, "prompt_eval_count": 16,
            #  "prompt_eval_duration": 2462947000, "eval_count": 390, "eval_duration": 106818534000}
            replyMessage=replyMessage+data['message']['content']
            # print(data['message']['content'])
        except json.JSONDecodeError:
            # 如果JSON解析失败（例如，因为该行不是有效的JSON），则打印错误信息
            print(f"Error decoding JSON on line: {line}")

    print(replyMessage)
else:
    # 打印错误信息
    print(f"请求失败，状态码：{response.status_code}")
    print(response.text)

import json

# 假设你的JSON字符串存储在一个名为'messages.txt'的文件中
file_name = 'messages.txt'
