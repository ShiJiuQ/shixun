from openai import OpenAI

# 1. 客户端配置
client = OpenAI(
    api_key="1b963cd2d4b04e9f96274ac4863a519e.vPENnEHX3h94LOzu", # 你的智谱 Key
    base_url="https://open.bigmodel.cn/api/paas/v4/" # 智谱的服务器
)

# 2. 建立记忆库
messages = [
    {"role": "system", "content": "你是研途Buddy，一个耐心、专业的408计算机考研助手。"}
]

print("研途 Buddy 启动成功！(输入 '退出' 结束对话)")
print("-" * 50)

while True:
    user_input = input("\n你: ")
    
    if user_input.lower() in ['退出', 'exit', 'quit', 'q']:
        print("研途 Buddy: 加油复习，保持好心态，研途璀璨，下次见！")
        break
        
    messages.append({"role": "user", "content": user_input})
    
    # 【关键修改】：这里换成智谱的免费模型名 "glm-4-flash"
    response = client.chat.completions.create(
        model="glm-4-flash", 
        messages=messages,
        stream=True  # 顺便帮你开启了流式输出（打字机效果）
    )
    
    print("\n研途 Buddy: ", end="")
    full_answer = ""
    
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            full_answer += content
            
    print()
    
    messages.append({"role": "assistant", "content": full_answer})