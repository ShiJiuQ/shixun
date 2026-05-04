'''
    刷题功能
'''

from fastapi import APIRouter, Body

router = APIRouter()

@router.get("/get-question")
async def get_question(subject: str = "数据结构"):
    # 模拟从题库取题
    return {
        "id": 1024,
        "subject": subject,
        "content": "若一个栈的输入序列为1,2,3，则不可能是栈的输出序列是？",
        "options": ["A. 1,2,3", "B. 3,2,1", "C. 3,1,2", "D. 2,1,3"],
        "answer": "C"
    }

@router.post("/submit-code")
async def analyze_code(code: str = Body(..., embed=True)):
    # 模拟代码错误定位逻辑[cite: 2]
    # 提示：你可以使用 Python 的 AST 库或直接调用大模型 API 
    if "NULL" in code and "->" not in code:
        return {
            "status": "error",
            "location": "Line 12",
            "message": "检测到空指针访问风险，链表操作需先检查节点是否存在。"
        }
    return {"status": "success", "message": "逻辑基本正确，建议优化循环复杂度。"}