import os
import openai

# 设置代理端口，否则连接不上api
os.environ["http_proxy"] = "127.0.0.1:7890"  # os.environ["http_proxy"] = "http://<代理ip>:<代理端口>"
os.environ["https_proxy"] = "127.0.0.1:7890"  # os.environ["https_proxy"] = "http://<代理ip>:<代理端口>"

openai.api_key = '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'
# 将自己的api_key填进去，获取地址：https://platform.openai.com/account/api-keys
chat_history = ""
while True:
    # 获取用户输入
    user_input = input("User：")

    # 检查是否输入了 “exit”，如果是则退出聊天
    if user_input.lower() == "exit":
        print("AI：好的，再见！")
        break

    # 将用户的输入拼接到历史对话中
    chat_history += f"\nUser: {user_input}"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "user",
             "content": chat_history}
        ]
    )

    # 将AI的回答拼接到历史对话中
    chat_history += f"\n: {completion.choices[0].message['content']}"

    # 输出Ai的回答
    print("AI:", completion.choices[0].message["content"])
