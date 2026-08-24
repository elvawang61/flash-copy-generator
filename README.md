# 快闪打卡文案生成器

扫码 → AI生成文案 → 跳转小红书发布 → 抽奖闭环

## 项目结构

```
flash-copy-generator/
├── backend/          # 后端服务（Python FastAPI）
│   ├── main.py       # 主程序
│   ├── config.py     # 配置文件（API Key）
│   └── requirements.txt
├── frontend/         # 前端页面
│   ── index.html    # H5 单页应用
└── README.md
```

## 启动方式

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python main.py
```

后端运行在 http://localhost:8000

### 2. 打开前端

直接用浏览器打开 `frontend/index.html`，或带参数访问：

```
frontend/index.html?name=迪卡侬城市运动挑战赛&period=8月20日-21日&location=上海静安嘉里中心&features=城市障碍赛,飞盘体验,运动市集&prize=发布笔记抽运动水壶&tone=活力健康&tags=迪卡侬城市运动挑战赛,上海周末好去处
```

## 注意事项

- 运行前需在 `backend/config.py` 中填入真实的豆包 API Key
- 调用国内 API 时需关闭 VPN
- 前端 `API_BASE_URL` 默认指向 localhost，部署时改为正式域名
