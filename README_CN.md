<div align="center">

# 🤖 Mola Helper

**你的智能 Agent 助手**

*强大、可扩展的大语言模型 Agent 框架*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## ✨ 功能特性

- 🔌 **多 LLM 支持** - 无缝对接 Ollama、豆包、SiliconFlow 等多种大模型
- 📧 **邮件管理** - 简单指令即可获取、阅读、删除邮件
- 📚 **arXiv 论文搜索** - 直接搜索 arXiv 学术论文
- 🛠️ **技能扩展** - 通过技能系统轻松添加新能力
- 💾 **记忆系统** - 上下文感知的对话记忆
- 📦 **JSON 优先设计** - 结构化、可预测的工具调用

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/molamola-xtq/MolaHelper.git
cd MolaHelper
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境
在项目根目录创建 `.env` 文件：
```env
# LLM 配置
PROVIDER=siliconflow
MODEL=
URL=https://api.siliconflow.cn/v1/chat/completions
API_KEY=

# 邮箱配置（可选）
EMAILS=your_email@example.com
KEY=your_email_password #这个是邮箱的smtp的授权码
IMAP=imap.example.com
PORT=993
```

### 4. 运行 Mola Helper
```bash
python chat.py
```

## 📁 项目结构

```
Agent/
├── agent_config.py    # 配置管理
├── chat.py            # 核心聊天逻辑
├── tool_config.py     # 工具注册
├── Memory.py          # 对话记忆
├── email_utils.py     # 邮件工具
├── paper.py           # arXiv 搜索
├── caller.py          # 工具调用器
├── logo.py            # ASCII 艺术标志
└── skills/            # 可扩展技能
    ├── arxiv查询论文列表.md
    ├── 本地时间读取.md
    └── 邮箱助手.md
```

## 🎯 使用示例

| 指令 | 功能 |
|---------|--------|
| "帮我查一下最新的AI论文" | 搜索 arXiv AI 相关论文 |
| "读取最新的邮件" | 阅读最新邮件 |
| "现在几点了？" | 获取当前本地时间 |

## 🔧 添加新技能

1. 在 `skills/` 目录创建 `.md` 文件
2. 创建对应的 `.info` 文件，写入技能描述
3. 在 `tool_config.py` 中注册工具

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request！

## 👤 作者

**Tianqi Xue**

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！ ⭐**

</div>
