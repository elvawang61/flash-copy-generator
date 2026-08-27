# 快闪打卡文案生成器

面向品牌线下快闪活动的 AI 裂变 H5 工具。用户扫码后由大模型实时生成小红书风格打卡文案，一键复制跳转发布，返回后出示核验页即可现场兑奖——将"用户不愿发、写得慢、质量差"的活动传播痛点压缩到 30 秒内闭环解决。

## 产品流程

```
扫码进入 H5 → 点击「生成打卡文案」→ AI 流式生成小红书风格文案
      ↓
自动复制文案 → 唤起小红书 App → 用户选图粘贴发布
      ↓
返回 H5 → 展示核验页（发布时间 + 文案预览）→ 出示给工作人员 → 现场兑奖
```

## 核心特性

- **流式输出**：基于 SSE 的流式交互方案，AI 文案逐字呈现，首字显示 3s 内，感知等待降低 80%+
- **Prompt 工程**：通过字数约束 + 语气引导 + 结构化模板，控制生成内容在风格、长度、话题覆盖上稳定可控
- **三态流转架构**：生成 → 文案展示 → 状态核验，配合 localStorage 持久化与 Deep Link 状态恢复
- **参数化配置**：通过 URL 参数即可适配不同品牌活动，零开发成本接入新活动
- **零成本部署**：Cloudflare Pages + Workers Serverless 架构，GitHub 推送自动构建发布

## 技术架构

```
┌─────────────────┐     POST /api/generate     ┌──────────────────────┐
│   Frontend H5   │ ──────────────────────────→ │  Cloudflare Worker   │
│  (Pages 静态托管) │ ← ─ ─ ─ ─ SSE 流式响应 ─ ─  │  (Serverless 后端)    │
└─────────────────┘                             └──────────┬───────────┘
                                                           │ stream: true
                                                           ↓
                                                  ┌──────────────────┐
                                                  │  豆包大模型 API   │
                                                  │  (doubao-lite)   │
                                                  └──────────────────┘
```

| 层级 | 技术方案 |
|------|---------|
| 前端 | 原生 HTML/CSS/JS 单文件，无框架依赖 |
| 后端 | Cloudflare Workers（JavaScript） |
| AI 模型 | 火山引擎方舟平台 · 豆包 lite |
| 部署 | Cloudflare Pages + GitHub CI/CD |
| 本地开发 | Python FastAPI（backend/） |

## 在线演示

> **Demo**: https://flash-copy-generator.pages.dev
>
> 带参数示例（迪卡侬城市运动挑战赛）：
> https://flash-copy-generator.pages.dev?name=迪卡侬城市运动挑战赛&period=8月20日-21日&location=上海静安嘉里中心&features=城市障碍赛,飞盘体验,运动市集&prize=发布笔记抽运动水壶&tone=活力健康&tags=迪卡侬城市运动挑战赛,上海周末好去处

## 项目结构

```
flash-copy-generator/
├── frontend/
│   └── index.html          # H5 单页应用（含全部前端代码）
├── backend/
│   ├── main.py             # FastAPI 本地开发服务
│   ├── config.py           # API 配置（需自行创建，已 gitignore）
│   ├── config.example.py   # 配置模板
│   └── requirements.txt
└── .gitignore
```

## 本地运行

### 1. 配置 API Key

```bash
cd backend
cp config.example.py config.py
```

编辑 `config.py`，填入豆包 API Key：

```python
DOUBAO_API_KEY = "your-api-key-here"
DOUBAO_ENDPOINT_ID = "ep-xxxxxxxxxx"
DOUBAO_API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
```

### 2. 启动后端

```bash
pip install -r requirements.txt
python main.py
```

### 3. 修改前端 API 地址

将 `frontend/index.html` 中的 `API_BASE_URL` 改为本地地址：

```javascript
const API_BASE_URL = "http://localhost:8000";
```

### 4. 打开页面

浏览器访问 `frontend/index.html`，可附带 URL 参数自定义活动信息。

## URL 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `name` | 活动名称 | 迪卡侬城市运动挑战赛 |
| `period` | 活动时间 | 8月20日-21日 |
| `location` | 活动地点 | 上海静安嘉里中心 |
| `features` | 活动特色（逗号分隔） | 城市障碍赛,飞盘体验 |
| `prize` | 参与奖品 | 发布笔记抽运动水壶 |
| `tone` | 品牌调性 | 活力健康 |
| `tags` | 必带话题（逗号分隔） | 迪卡侬城市运动挑战赛 |

## 部署说明

本项目采用 Cloudflare 免费方案部署：

- **前端**：Cloudflare Pages 连接 GitHub 仓库，Root directory 设为 `frontend/`，推送 main 分支自动构建部署
- **后端**：Cloudflare Worker 独立部署，在 Settings → Variables 中配置 `DOUBAO_API_KEY` 环境变量
- **Worker 代码**：在 Cloudflare Dashboard → Workers → Edit code 中维护（未纳入 Git 管理）
