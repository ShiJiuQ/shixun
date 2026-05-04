# 个人画像接口
# 头像
# 名字
# 账号
# 语言？
# 可以展示各科目的雷达图，有没有可能通过刷题的错题标签等方面整合出一种算法，计算出来不同科目的掌握程度
# 学习状态：可以根据疗愈系统在这里的一个总结（疗愈系统放的是详细的内容数据啥的）
# 刷题总数：可以是对刷题系统的一个总结


from fastapi import APIRouter, Depends, HTTPException
from app.core.deps import get_current_user  # 假设你已有这个获取当前用户的工具
from app.models.user import User            # 用户数据库模型

router = APIRouter()

@router.get("/info")
async def get_profile_info(current_user: User = Depends(get_current_user)):
    # 这里的 current_user 就是通过 Token 识别出来的当前登录用户对象
    
    # 模拟从数据库根据该用户 ID 实时计算的数据[cite: 2]
    # 实际开发中会用到：db.query(PracticeRecord).filter_by(user_id=current_user.id)
    radar_data = [
        {"subject": "数据结构", "score": 70}, 
        {"subject": "计组", "score": 65},
        {"subject": "操作系统", "score": 80},
        {"subject": "计网", "score": 45}
    ]

    return {
        "user": {
            "name": current_user.username,  # 动态返回当前登录的用户名
            "avatar": "https://api.multiavatar.com/kaining.png",
            "account": current_user.id,     # 返回真实的账号 ID
            "language": "zh-CN"
        },
        "mastery_radar": radar_data,
        "learning_status": "努力冲刺中", 
        "total_practice": 520             # 这里后续对接真实的刷题统计[cite: 2]
    }