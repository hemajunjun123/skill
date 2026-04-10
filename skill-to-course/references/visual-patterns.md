# Visual Patterns — 可视化模式参考

生成各模块 HTML 时，直接复用以下代码片段。每个模式都已体现四条设计哲学。

---

## 0. 设计哲学检查点（每次生成前默读）

```
✅ 先体验后理解：第一屏展示"结果"，原理放后面
✅ 演示不说教：文字块 ≤ 3 句，其余全部可视化
✅ 测验考实操：题目格式 = "你遇到[情况]，你会[怎么做]？"
✅ 比喻不复用：每个术语配一个只属于它自己的比喻
```

---

## 1. 模块 1 — 能力卡片（先体验：用结果开场）

开场绝对不是"这个 skill 的定义是..."，而是"你能用它做这 5 件事"。

```html
<!-- 副标题要具体，不能抽象 -->
<p class="module-subtitle">
  上传 Excel、描述你想要的结果，剩下的交给我——
  公式、格式、图表，一次搞定。
</p>

<div class="cards-grid">
  <div class="card">
    <div class="card-icon">📊</div>
    <div class="card-title">读取 & 分析数据</div>
    <!-- 描述要具体到操作，不是"支持多种功能" -->
    <div class="card-desc">上传表格，直接问"帮我统计每个城市的销售额"</div>
  </div>
  <div class="card">
    <div class="card-icon">🧮</div>
    <div class="card-title">写公式，不写死数字</div>
    <div class="card-desc">自动用 =SUM()，数据变了，结果自动跟着变</div>
  </div>
  <!-- 更多卡片... -->
</div>

<!-- 场景标签：让用户快速对号入座 -->
<p style="font-size:13px; color:var(--text-muted); margin-top:8px;">适合你，如果你经常需要：</p>
<div class="trigger-tags" style="margin-top:8px;">
  <span class="trigger-tag">月度财务汇总</span>
  <span class="trigger-tag">销售数据分析</span>
  <span class="trigger-tag">项目进度追踪</span>
</div>

<!-- ===== 知彼知己：竞品对比小节 ===== -->
<div class="divider"></div>

<h3 style="font-family:var(--font-display); font-size:22px; margin-bottom:8px;">
  🏆 相比市面产品，它强在哪？
</h3>
<p style="font-size:14px; color:var(--text-muted); margin-bottom:24px;">
  对比 2-3 个同类工具，看看这个 skill 的差异化优势
</p>

<!-- 竞品对照表：左列传统工具做法，右列该 skill 做法 -->
<div class="compare-table">
  <table>
    <thead>
      <tr>
        <th class="compare-dim">对比维度</th>
        <th class="compare-competitor">竞品A（如 Notion AI）</th>
        <th class="compare-competitor">竞品B（如 Obsidian）</th>
        <th class="compare-skill">本 Skill</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>沉淀方式</td>
        <td>手动创建页面</td>
        <td>手动写 Markdown</td>
        <td><strong>对话中自动识别+提炼</strong></td>
      </tr>
      <!-- 更多对比行... -->
    </tbody>
  </table>
</div>

<!-- 核心优势卡片（3 张） -->
<div class="cards-grid" style="grid-template-columns: repeat(3, 1fr); margin-top:24px;">
  <div class="card" style="border-left-color: #2E8B72;">
    <div class="card-icon">⚡</div>
    <div class="card-title">优势 1 标题</div>
    <div class="card-desc">具体描述这个优势为什么重要，用户能感受到的差异</div>
  </div>
  <div class="card" style="border-left-color: #2E8B72;">
    <div class="card-icon">🔍</div>
    <div class="card-title">优势 2 标题</div>
    <div class="card-desc">具体描述</div>
  </div>
  <div class="card" style="border-left-color: #2E8B72;">
    <div class="card-icon">🛡️</div>
    <div class="card-title">优势 3 标题</div>
    <div class="card-desc">具体描述</div>
  </div>
</div>

<!-- 优化建议（友好口吻） -->
<div class="cta-block" style="margin-top:24px; background:rgba(224,92,75,0.06);">
  <strong>💡 还可以做得更好</strong>
  <p>1-2 条具体的优化方向，措辞友好、建设性，不是批评</p>
</div>
```

---

## 2. 模块 2 — 对话气泡（演示触发方式，用"示范"代替"列举"）

❌ 不要这样：
```html
<ul>
  <li>帮我分析这个表格</li>
  <li>创建一个 Excel</li>
</ul>
```

✅ 要这样（先展示真实对话，再展示触发词云）：

```html
<!-- 真实对话气泡 — 在 initSkillData() 里调用 animateChat() -->
<div class="chat-container" id="trigger-chat"></div>

<!-- 触发词云放在对话下方，作为总结 -->
<p style="font-size:13px; color:var(--text-muted); margin-top:28px;">
  这些说法都能触发这个 skill：
</p>
<div class="trigger-tags">
  <span class="trigger-tag">帮我分析这个表格</span>
  <span class="trigger-tag">创建一个 Excel 报表</span>
  <span class="trigger-tag">加一列计算利润率</span>
  <!-- 更多... -->
</div>
```

**animateChat 调用示例**（在 initSkillData 里）：
```javascript
animateChat('trigger-chat', [
  { avatar: '👤', label: '你', text: '帮我把 sales.xlsx 按月份汇总，找出销售最差的那个月' },
  { avatar: '🎭', label: 'JoJo', right: true, text: '读取中… 发现 12 个月的数据，共 847 行' },
  { avatar: '🎭', label: 'JoJo', right: true, text: '7月最差，¥23.4万，比平均低 38%。已生成月度对比表和折线图。' },
  { avatar: '👤', label: '你', text: '能再帮我加一列"是否达标"（低于 30 万标红）吗？' },
  { avatar: '🎭', label: 'JoJo', right: true, text: '完成，已用条件格式标红 4 个月份，文件在 monthly_summary.xlsx' },
]);
```

---

## 3. 模块 3 — 流程步骤 + 并排对照（演示原理，比喻在这里出现）

流程步骤每条 = **动词短语标题** + **1 句通俗描述**。
比喻要嵌在描述里，自然出现，不是单独一段"解释这个比喻"。

```html
<div class="flow-steps" id="flow">
  <div class="flow-step">
    <div class="step-num">1</div>
    <div class="step-content">
      <div class="step-title">读取 skill 说明书</div>
      <!-- 比喻自然嵌入，不独立成段 -->
      <div class="step-desc">
        就像新员工入职第一天先看岗位职责手册，
        AI 先读 SKILL.md，知道接下来该用什么工具、遵守什么规范
      </div>
    </div>
  </div>
  <div class="flow-step">
    <div class="step-num">2</div>
    <div class="step-content">
      <div class="step-title">判断任务类型，选合适工具</div>
      <div class="step-desc">
        分析数据用 <span class="term" data-tip="Python 数据处理库，擅长大量数值计算和统计">pandas</span>，
        改格式写公式用 <span class="term" data-tip="Python 的 Excel 专用库，处理单元格样式和公式字符串">openpyxl</span>——
        像外科医生根据手术类型选手术刀
      </div>
    </div>
  </div>
  <!-- 更多步骤... -->
</div>

<!-- 并排对照表：行数和流程步骤对应 -->
<div class="side-by-side">
  <div class="side-col">
    <div class="side-header">⚙️ 技术描述</div>
    <div class="side-cell">Parse YAML frontmatter from SKILL.md</div>
    <div class="side-cell">Dispatch to pandas or openpyxl based on task type</div>
    <div class="side-cell">Inject Excel formula strings, not computed values</div>
    <div class="side-cell">Invoke LibreOffice headless recalc macro</div>
    <div class="side-cell">Scan JSON output for #REF! / #DIV/0! error codes</div>
  </div>
  <div class="side-col">
    <div class="side-header">🌏 通俗中文</div>
    <div class="side-cell">读取 skill 的"身份证"，知道规则和约束</div>
    <div class="side-cell">根据你要"分析数据"还是"改格式"，选不同工具</div>
    <div class="side-cell">填入 =SUM() 而不是填死数字，表格保持动态可更新</div>
    <div class="side-cell">让 LibreOffice 悄悄跑一遍计算，让公式显示出真实数字</div>
    <div class="side-cell">检查每个格子有没有红色报错，有就修复，确保你拿到的文件是干净的</div>
  </div>
</div>
```

---

## 4. 模块 4 — 工具链（从左到右依次出现，像多米诺牌倒下）

```html
<div class="tool-chain" id="tool-chain">
  <div class="tool-node">👤 你的消息</div>
  <div class="tool-arrow">→</div>
  <div class="tool-node">🧠 Claude</div>
  <div class="tool-arrow">→</div>
  <div class="tool-node">📜 SKILL.md</div>
  <div class="tool-arrow">→</div>
  <div class="tool-node">🐍 Python 脚本</div>
  <div class="tool-arrow">→</div>
  <div class="tool-node">🔄 LibreOffice</div>
  <div class="tool-arrow">→</div>
  <div class="tool-node">✅ .xlsx 文件</div>
</div>

<!-- 工具说明卡：每张卡配一句独特比喻，不重复 -->
<div class="tool-notes">
  <div class="tool-note">
    <strong>📜 SKILL.md</strong>
    <!-- 比喻：乐谱（规定每个音符怎么弹，但弹奏者还是 AI） -->
    <span>乐谱 — 规定了每个步骤怎么执行，但 AI 是演奏者</span>
  </div>
  <div class="tool-note">
    <strong>🐍 pandas</strong>
    <!-- 比喻：考古刷子（细心筛选和分类数据）-->
    <span>考古刷子 — 在海量数据里细心筛选、分类、统计</span>
  </div>
  <div class="tool-note">
    <strong>📊 openpyxl</strong>
    <!-- 比喻：印章匠（给每个格子盖上格式和公式） -->
    <span>印章匠 — 给每个单元格盖上公式和样式标记</span>
  </div>
  <div class="tool-note">
    <strong>🔄 LibreOffice</strong>
    <!-- 比喻：钟表上弦（让静止的公式字符串真正转动起来） -->
    <span>钟表上弦 — 让写好但静止的公式真正转动，算出结果</span>
  </div>
</div>
```

---

## 5. 模块 5 — 输入输出（具体例子，永远比功能列表有说服力）

每个 io-example 要满足：
- **输入**：真实的、具体的用户语句（不是"用户提供数据"）
- **输出**：具体的交付物描述（不是"生成结果"）

```html
<div class="io-example">
  <div class="io-box">
    <div class="io-label input">👤 你说</div>
    帮我分析 sales.xlsx，按城市统计总销售额，找 TOP 5
  </div>
  <div class="io-arrow">→</div>
  <div class="io-box">
    <div class="io-label output">✅ 你得到</div>
    Markdown 排名表：5 个城市、销售额、占比，附一句关键洞察
  </div>
</div>

<div class="io-example">
  <div class="io-box">
    <div class="io-label input">👤 你说</div>
    做一个季度财务报表，含收入成本利润率，专业格式
  </div>
  <div class="io-arrow">→</div>
  <div class="io-box">
    <div class="io-label output">✅ 你得到</div>
    quarterly_report.xlsx：蓝色输入项、黑色公式、利润率 =（收入-成本）/收入 自动计算
  </div>
</div>
```

---

## 6. 模块 6 — 测验（场景题模板）

**必须是情境题。永远遵循：你在[做某件事]，遇到了[具体问题]，你会[怎么做]？**

```html
<!-- ✅ 好题 — 场景式，考实操判断 -->
<div class="quiz-block">
  <div class="quiz-question">
    📋 你让 AI 生成了一个带公式的 Excel，打开后发现 =SUM() 显示 0 而不是求和结果。
    下一步你应该？
  </div>
  <div class="quiz-options">
    <div class="quiz-option" data-correct="0">
      <span class="quiz-opt-label">A</span>
      重新让 AI 生成，这次不要用公式，直接填数字
    </div>
    <div class="quiz-option" data-correct="1">
      <span class="quiz-opt-label">B</span>
      告诉 AI "公式没有计算出来，请运行 recalc.py 刷新"
    </div>
    <div class="quiz-option" data-correct="0">
      <span class="quiz-opt-label">C</span>
      手动用计算器算出结果，填进对应的格子
    </div>
  </div>
  <div class="quiz-feedback"
    data-right="对！openpyxl 写入公式时只是文字，需要 LibreOffice 的 recalc.py 跑一遍才能算出数值。让 AI 执行这一步就好。"
    data-wrong="其实 recalc.py 是专门解决这个问题的 — openpyxl 写入的公式在 LibreOffice 计算之前只是静止的字符串。告诉 AI 运行 recalc.py 就能修复。">
  </div>
</div>

<!-- ❌ 坏题示例（不要这样写）
<div class="quiz-question">openpyxl 是什么库？</div>
-->

<!-- 测验结束后的 CTA，把"学到了什么"和"怎么用"连起来 -->
<div class="cta-block" style="margin-top:40px;">
  <strong>🎉 现在你知道了…</strong>
  <p>
    xlsx skill 接管从"理解需求"到"交付文件"的全过程。
    你只需要用自然语言描述想要的结果——
    公式、格式、计算，都不需要你懂。
  </p>
  <p style="margin-top:8px;">
    想试试？直接说 <strong>"帮我创建一个销售数据表格"</strong> 就能触发。
  </p>
</div>
```

---

## 7. 比喻创作指南

Phase 2 分析 skill 时，为每个术语填写下表，Phase 3 直接引用：

| 技术术语 | 通俗解释（1句） | 专属比喻（说明为什么选这个） |
|---|---|---|
| SKILL.md | skill 的使用说明和规则手册 | 乐谱 — 规定了演奏方式，但演奏者还是 AI |
| pandas | Python 数据处理库 | 考古刷子 — 在大量数据里细心筛选分类 |
| openpyxl | Excel 专用操作库 | 印章匠 — 给每个格子盖上公式和样式 |
| LibreOffice recalc | 公式计算引擎 | 钟表上弦 — 让静止的公式真正转动起来 |

**好比喻的标准：**
1. 反映概念的**核心特征**（不是随便一个"大家懂的"事物）
2. 在同一课程里**绝不重复**
3. 读完感觉"当然就该是这个"，而不是"勉强说得通"

**禁用比喻（过度滥用）：**
- API → 餐厅点餐/服务员
- 消息传递 → 邮差
- 数据处理 → 工厂流水线
- 数据库 → 文件柜
- 认证 → 身份证

---

## 8. Tooltip 术语标注（所有技术术语第一次出现时必须标注）

```html
<!-- 格式：term 类名 + data-tip 通俗解释 -->
<span class="term" data-tip="Python 数据处理库，就像考古刷子，帮你在大量数据里细心筛选分类">pandas</span>
<span class="term" data-tip="Excel 专用操作库，帮 AI 给每个单元格盖上公式和样式">openpyxl</span>
<span class="term" data-tip="LibreOffice 的计算引擎，让写好但静止的公式真正转动起来算出结果">recalc.py</span>
```

---

## 9. 模块 0 — Skill 获取区（页面最顶部，所有课程模块之前）

位于进度条和侧边导航之后、模块 1 之前。展示 skill 的获取方式，支持四种素材组合使用。
生成时根据用户提供的素材选择性填充，未提供则不生成此区块。

```html
<!-- 获取区：根据用户提供的素材组合填充 -->
<div class="skill-download" id="skill-download">
  <div class="skill-download-card">
    <h2>📥 获取这个 Skill</h2>

    <!-- 文字描述（如有） -->
    <p class="download-desc">{DOWNLOAD_TEXT}</p>

    <!-- 图片（如有，base64 嵌入） -->
    <img class="download-image" src="data:image/png;base64,{IMAGE_BASE64}" alt="skill preview">

    <!-- 按钮区 -->
    <div class="download-actions">
      <!-- 链接按钮（如有） -->
      <a class="download-btn" href="{DOWNLOAD_LINK}" target="_blank">🔗 获取 Skill</a>
      <!-- 文件下载按钮（如有，md/zip 编码嵌入） -->
      <button class="download-btn secondary" onclick="downloadEmbeddedFile('{FILE_BASE64}', '{FILENAME}')">📁 下载 {FILENAME}</button>
    </div>
  </div>
</div>
```

**四种素材类型：**
- **链接**：显示为可点击的跳转按钮（`<a>` 标签）
- **图片**：base64 编码后直接嵌入 `<img>` 展示
- **文字描述**：直接显示在 `download-desc` 中
- **文件（md/zip）**：base64 编码嵌入 HTML，点按钮触发浏览器下载

**生成规则：**
- 只保留用户实际提供的素材对应的 HTML 元素，未提供的删除（不是隐藏）
- 如果用户未提供任何获取方式，整个获取区不生成

---

## 10. 分隔线（模块内部两个部分之间用）

```html
<div class="divider"></div>
```
