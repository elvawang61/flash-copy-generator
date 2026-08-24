"""
快闪打卡文案生成器 — 后端服务
===========================
功能：接收活动信息 → 拼装 Prompt → 调豆包 API → 返回文案

启动方式：
  cd backend
  pip install -r requirements.txt
  python main.py

访问地址：http://localhost:8000
接口文档：http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
import os

from config import DOUBAO_API_KEY, DOUBAO_ENDPOINT_ID, DOUBAO_API_URL

app = FastAPI(title="快闪打卡文案生成器 API")

# ✅ 允许前端跨域调用（开发环境允许所有来源，生产环境应限制为正式域名）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 📋 请求数据模型（前端传过来的活动信息）
class GenerateRequest(BaseModel):
    name: str                    # 活动名称
    period: str                  # 活动有效期
    location: str                # 活动地点
    features: str                # 活动特色（逗号分隔）
    prize: Optional[str] = ""    # 参与奖品（选填）
    tone: Optional[str] = ""     # 品牌调性（选填）
    tags: str                    # 必带话题（逗号分隔）


# 📋 返回数据模型
class GenerateResponse(BaseModel):
    success: bool
    text: Optional[str] = None
    error: Optional[str] = None


# ✅ Prompt 模板（v1，已验证）
PROMPT_TEMPLATE = """你是一个资深小红书达人，擅长写真实感强的打卡种草文案。

请根据以下活动信息，生成一段小红书风格的打卡文案。

📋 活动信息
➡️ 活动名称：{name}
➡️ 活动时间：{period}
➡️ 活动地点：{location}
➡️ 活动特色：{features}
➡️ 参与奖品：{prize}
➡️ 品牌调性：{tone}
➡️ 必带话题：{tags}

📝 文案要求
✅ 字数 150-250 字，分段清晰，适合手机阅读
✅ 语气真实自然，像普通用户分享体验，不要像广告
✅ 开头要有吸引力，让人想继续看下去
✅ 包含具体的活动细节，让人有画面感
✅ 适当使用 emoji 增加活泼感，但不要过多（3-5个即可）
✅ 结尾附上必带话题标签，可额外补充 1-2 个相关话题
✅ 不要出现"作为AI"或任何机器痕迹"""


@app.post("/api/generate", response_model=GenerateResponse)
def generate_copy(req: GenerateRequest):
    """
    接收活动信息，调用豆包 API 生成小红书风格打卡文案。
    """
    # 1️⃣ 拼装 Prompt
    prompt = PROMPT_TEMPLATE.format(
        name=req.name,
        period=req.period,
        location=req.location,
        features=req.features,
        prize=req.prize or "无特别奖品",
        tone=req.tone or "真实自然",
        tags=req.tags
    )

    # 2️⃣ 构造请求体
    data = {
        "model": DOUBAO_ENDPOINT_ID,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {DOUBAO_API_KEY}",
        "Content-Type": "application/json"
    }

    # 3️⃣ 调用豆包 API
    try:
        response = requests.post(
            DOUBAO_API_URL,
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            text = result["choices"][0]["message"]["content"]
            return GenerateResponse(success=True, text=text)
        else:
            return GenerateResponse(
                success=False,
                error=f"豆包 API 返回错误：{response.status_code}"
            )

    except requests.exceptions.Timeout:
        return GenerateResponse(success=False, error="文案生成超时，请重试")
    except Exception as e:
        return GenerateResponse(success=False, error=f"服务异常：{str(e)}")


@app.get("/")
def root():
    """健康检查"""
    return {"status": "ok", "message": "快闪打卡文案生成器 API 运行中"}


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("🚀 快闪打卡文案生成器 — 后端服务启动")
    print("📡 接口地址：http://localhost:8000")
    print("📖 接口文档：http://localhost:8000/docs")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)
