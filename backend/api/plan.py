# 顶部：考研倒计时
# 日历：打卡情况（完成标绿，未完成标红），点击特定日期，右侧展示当天任务
# 右侧今日任务清单：时间轴/可以拖拽的卡片
# 计划：自己制定+ai生成
# 自己指定：一些比较自我的计划
# ai如何生成计划？（复盘提醒+刷题提醒+相似题提醒） 艾宾浩斯遗忘曲线在这里给复盘提供；动态自适应，如果焦虑过度，则把刷题目标减少
# 有机会的话爬取一些计算机专业相关院校信息，做一个数据库，然后实现一个简单的升学规划功能

from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/daily-tasks")
async def get_daily_tasks(stress_level: str = "high"):
    # 艾宾浩斯复盘提醒逻辑（模拟从数据库找 1, 2, 4, 7 天前的错题）[cite: 2]
    base_tasks = [
        {"type": "user", "content": "看计网第5章视频", "done": False},
        {"type": "ai_review", "content": "复盘3天前的进程同步错题", "done": False}
    ]
    
    # 动态自适应：根据压力等级调整[cite: 2]
    if stress_level == "high":
        # 移除高强度刷题，增加疗愈任务
        base_tasks = [t for t in base_tasks if "刷题" not in t["content"]]
        base_tasks.append({"type": "healing", "content": "小精灵建议：进行3分钟深呼吸", "done": False})
    
    return {
        "countdown": 265, # 假设距离考研的天数
        "tasks": base_tasks
    }