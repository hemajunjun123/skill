# skill-to-course

将任意 OpenClaw skill 转换为**美观、自包含的单页 HTML 课程页面**。

让用户在安装 skill 之前，就能真实感知：它能做什么、怎么触发、背后怎么运作。

不是说明书。是**体验**。

---

## 使用方式

直接告诉 AI：

```
帮我预览 skill：xlsx
给我看看 citadel skill 能干嘛
把这个 skill 转成课程页面
```

或者粘贴 SKILL.md 内容 / 提供路径。

## 生成内容

每个课程页面包含 6 个模块：

| 模块 | 内容 |
|---|---|
| 🎯 能做什么 | 能力卡片网格，一眼看清 skill 价值 |
| 💬 怎么触发 | 真实对话动画 + 触发词云 |
| ⚙️ 幕后原理 | 工作流程动画 + 技术/通俗对照 |
| 🔧 工具链 | 调用链依次出现动画 |
| 📦 输入/输出 | 具体示例卡片 |
| 🧪 场景测验 | 互动问答，选后即时反馈 |

## 技术特性

- **自包含 HTML**：无外部依赖（除 Google Fonts CDN）
- **纯 CSS 动画**：IntersectionObserver 驱动，进入视口才触发
- **响应式**：手机和桌面都能看
- **交互导航**：顶部进度条 + 右侧导航点

## 文件结构

```
skill-to-course/
├── SKILL.md                    # 主 skill 定义
├── README.md                   # 本文件
└── references/
    ├── html-template.md        # 完整 HTML/CSS/JS 模板系统
    └── visual-patterns.md      # 各模块组件的 HTML 代码片段
```

---

## 致谢 / Credits

本 skill 的核心思路来源于 **codebase-to-course** 项目：

> 📎 https://github.com/zarazhangrui/codebase-to-course

原项目的创意：将代码库转换为交互式课程页面，让开发者能沉浸式理解一个项目。
本 skill 将这一思路迁移到 OpenClaw skill 体系，把"理解代码库"变成"理解 skill 能力"。

感谢原作者 [@zarazhangrui](https://github.com/zarazhangrui) 的创意启发 🙏
