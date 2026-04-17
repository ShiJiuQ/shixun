'''
 存放api key 数据库密码等配置信息
'''

import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class Settings:
    # 优先从环境变量读取，如果没有则报错或给默认值
    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
    ZHIPU_BASE_URL = os.getenv("ZHIPU_BASE_URL","https://open.bigmodel.cn/api/paas/v4/")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback_secret_key") 
    # (后面的 "fallback_secret_key" 是一个兜底预防，万一 .env 没写，也不会导致程序直接崩溃)
# 实例化配置对象，供整个项目使用
settings = Settings()
#print(f"====== 调试信息：我读到的 API KEY 是: {settings.ZHIPU_API_KEY} ======")