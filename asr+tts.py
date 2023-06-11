import speech_recognition as sr
import requests
import json
from urllib.parse import quote
import playsound
import urllib3
import openai
from aip import AipSpeech
import os
import time

os.environ["http_proxy"] = "127.0.0.1:7890"
os.environ["https_proxy"] = "127.0.0.1:7890"

openai.api_key = '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'

# 百度语音识别
APP_ID = '34122501'
API_KEY = 'AuhNeDedTUgcHnNDpmqNvMrH'
SECRET_KEY = 'HTQ0jfOAdQwG1lvWqqRX10Zpz96VoF3z'

urllib3.disable_warnings()

# 初始化语音识别器
r = sr.Recognizer()

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def recognize_speech():
    with sr.Microphone() as source:
        print("请开始说话...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    audio_data = audio.get_wav_data(convert_rate=16000)
    print("\n正在分析语音...")

    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1537,  # 普通话(支持简单的语音识别)
    })

    try:
        text = result['result'][0]
    except Exception as e:
        print(e)
        text = ""

    return text


def text_to_speech(text):
    # 设置百度语音合成的 API 密钥
    api_key = 'rvOIA1UnsW747kol4rHIykUE'
    secret_key = 'PSB2qrFCPipPEaD8yil1BQdxPClf4lD3'

    # 设置请求 URL
    url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'. \
        format(api_key, secret_key)

    # 获取 Access Token
    response1 = requests.get(url, verify=False)
    access_token = json.loads(response1.text)['access_token']

    # 设置语音合成 API 的请求 URL
    url = 'https://tsn.baidu.com/text2audio?tex={}&lan=zh&cuid=1234567890&ctp=1&tok={}'.format(quote(text),
                                                                                               access_token)

    # 发送请求并保存语音文件
    response2 = requests.get(url, verify=False)
    with open('output.mp3', 'wb') as f:
        f.write(response2.content)

    # 播放生成的语音
    playsound.playsound('output.mp3')


chat_history = "假设你现在是一个星巴克的柜台服务员，我是前来购买的顾客，请你针对我的问题进行简要的回答，不用解释。" \
               "现在你将开始见面第一句话，和我打招呼。直接回答就好，前面不用在引入role" \
               "或者答。"
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0301",
    messages=[
        {"role": "user",
         "content": chat_history}
    ]
)

# 将AI的回答拼接到历史对话中
chat_history += f"\n: {response.choices[0].message['content']}"

# 输出Ai的回答
print("AI:", response.choices[0].message["content"])

response_text = response.choices[0].message["content"]

# 进行语音合成
text_to_speech(response_text)

flag = False
# 语音识别和语音合成循环
while not flag:
    # 进行语音识别
    input_text = recognize_speech()
    print("user:", input_text)

    if input_text == "停止":
        print("AI：好的，再见！")
        break

    # 将用户的输入拼接到历史对话中
    chat_history += f"\nUser: {input_text}"

    print("正在处理...")
    # 进行文本处理和生成回应
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "user",
             "content": chat_history}
        ]
    )

    # 将AI的回答拼接到历史对话中
    chat_history += f"\n: {response.choices[0].message['content']}"

    # 输出Ai的回答
    print("AI:", response.choices[0].message["content"])

    response_text = response.choices[0].message["content"]

    i = 1
    # 进行语音合成
    text_to_speech(response_text)
    i += 1

print(chat_history)

"""
请问有什么推荐的吗？

"""
