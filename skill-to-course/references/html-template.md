# HTML Template System

生成课程 HTML 时，使用以下模板系统。整个课程是**单一自包含 HTML 文件**。

## 文件整体结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SKILL_NAME} — 技能课程</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Noto+Sans+SC:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    /* === CSS 变量 === */
    :root {
      --bg: #FAF8F5;
      --bg-alt: #F2EFE9;
      --text: #2C2825;
      --text-muted: #7A7269;
      --accent: {ACCENT_COLOR};       /* 每个 skill 选一个：珊瑚 #E05C4B / 靛青 #2D6A9F / 松绿 #2E8B72 */
      --accent-light: {ACCENT_LIGHT}; /* accent 的 15% 透明度版 */
      --code-bg: #1E1E2E;
      --card-shadow: 0 2px 12px rgba(44,40,37,0.08);
      --radius: 12px;
      --font-display: 'Noto Serif SC', serif;
      --font-body: 'Noto Sans SC', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    /* === 重置与基础 === */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      font-size: 16px;
      line-height: 1.7;
    }

    /* === 导航 === */
    .nav-sidebar {
      position: fixed;
      right: 24px;
      top: 50%;
      transform: translateY(-50%);
      z-index: 100;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .nav-dot {
      width: 10px; height: 10px;
      border-radius: 50%;
      background: var(--text-muted);
      opacity: 0.3;
      cursor: pointer;
      border: none;
      transition: all 0.3s ease;
      position: relative;
    }
    .nav-dot.active { opacity: 1; background: var(--accent); transform: scale(1.4); }
    .nav-dot:hover { opacity: 0.7; }
    /* Tooltip on hover */
    .nav-dot::after {
      content: attr(data-label);
      position: absolute;
      right: 18px;
      top: 50%;
      transform: translateY(-50%);
      background: var(--text);
      color: #fff;
      font-family: var(--font-body);
      font-size: 12px;
      padding: 3px 8px;
      border-radius: 4px;
      white-space: nowrap;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s;
    }
    .nav-dot:hover::after { opacity: 1; }

    /* === 模块通用 === */
    .module {
      min-height: 100dvh;
      min-height: 100vh;
      padding: 80px 48px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      max-width: 960px;
      margin: 0 auto;
      opacity: 0;
      transform: translateY(24px);
      transition: opacity 0.6s ease, transform 0.6s ease;
    }
    .module.visible { opacity: 1; transform: translateY(0); }
    .module:nth-child(even) { background: var(--bg-alt); max-width: 100%; padding: 80px calc(50% - 432px); }

    /* 标题系统 */
    .module-tag {
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 12px;
    }
    .module-title {
      font-family: var(--font-display);
      font-size: clamp(28px, 4vw, 48px);
      font-weight: 700;
      line-height: 1.2;
      margin-bottom: 20px;
    }
    .module-subtitle {
      font-size: 18px;
      color: var(--text-muted);
      margin-bottom: 40px;
      max-width: 600px;
    }

    /* === 能力卡片网格 === */
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin: 32px 0;
    }
    .card {
      background: #fff;
      border-radius: var(--radius);
      padding: 24px;
      box-shadow: var(--card-shadow);
      border-left: 4px solid var(--accent);
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .card:hover { transform: translateY(-3px); box-shadow: 0 6px 24px rgba(44,40,37,0.12); }
    .card-icon { font-size: 28px; margin-bottom: 12px; }
    .card-title { font-weight: 700; margin-bottom: 6px; }
    .card-desc { font-size: 14px; color: var(--text-muted); }

    /* === 对话气泡 === */
    .chat-container {
      background: #fff;
      border-radius: var(--radius);
      padding: 24px;
      max-width: 580px;
      box-shadow: var(--card-shadow);
    }
    .chat-bubble {
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
      opacity: 0;
      transform: translateX(-12px);
      transition: opacity 0.4s ease, transform 0.4s ease;
    }
    .chat-bubble.right { flex-direction: row-reverse; transform: translateX(12px); }
    .chat-bubble.show { opacity: 1; transform: translateX(0); }
    .bubble-avatar {
      width: 36px; height: 36px;
      border-radius: 50%;
      background: var(--accent-light);
      display: flex; align-items: center; justify-content: center;
      font-size: 18px;
      flex-shrink: 0;
    }
    .bubble-text {
      background: var(--bg-alt);
      border-radius: 16px;
      padding: 10px 16px;
      font-size: 14px;
      max-width: 80%;
    }
    .chat-bubble.right .bubble-text {
      background: var(--accent);
      color: #fff;
    }
    .bubble-label {
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 4px;
      font-weight: 600;
    }

    /* === 并排对照表 === */
    .side-by-side {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0;
      border-radius: var(--radius);
      overflow: hidden;
      box-shadow: var(--card-shadow);
      margin: 32px 0;
    }
    .side-col {
      padding: 0;
    }
    .side-header {
      padding: 12px 20px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }
    .side-col:first-child .side-header {
      background: var(--code-bg);
      color: #a6adc8;
    }
    .side-col:last-child .side-header {
      background: var(--accent);
      color: #fff;
    }
    .side-row {
      display: contents;
    }
    .side-cell {
      padding: 16px 20px;
      font-size: 14px;
      border-bottom: 1px solid rgba(44,40,37,0.06);
    }
    .side-col:first-child .side-cell {
      background: #252535;
      color: #cdd6f4;
      font-family: var(--font-mono);
      font-size: 13px;
    }
    .side-col:last-child .side-cell {
      background: #fff;
      color: var(--text);
    }

    /* === 竞品对比表 === */
    .compare-table {
      margin: 24px 0;
      border-radius: var(--radius);
      overflow: hidden;
      box-shadow: var(--card-shadow);
    }
    .compare-table table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }
    .compare-table thead tr {
      background: var(--code-bg);
    }
    .compare-table th {
      padding: 12px 16px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-align: left;
      border-bottom: 2px solid rgba(44,40,37,0.08);
    }
    .compare-table .compare-dim {
      color: #a6adc8;
      width: 18%;
    }
    .compare-table .compare-competitor {
      color: #a6adc8;
      width: 27%;
    }
    .compare-table .compare-skill {
      color: var(--accent);
      width: 28%;
      font-weight: 800;
    }
    .compare-table td {
      padding: 14px 16px;
      border-bottom: 1px solid rgba(44,40,37,0.06);
      background: #fff;
      vertical-align: top;
    }
    .compare-table tbody tr:last-child td {
      border-bottom: none;
    }
    .compare-table td:first-child {
      font-weight: 600;
      color: var(--text-muted);
      background: rgba(44,40,37,0.02);
    }
    .compare-table td:last-child {
      background: rgba(46,139,114,0.04);
      color: var(--text);
    }
    .compare-table td:last-child strong {
      color: #2E8B72;
    }

    /* === 流程动画 === */
    .flow-steps {
      display: flex;
      flex-direction: column;
      gap: 0;
      margin: 32px 0;
      position: relative;
    }
    .flow-steps::before {
      content: '';
      position: absolute;
      left: 20px;
      top: 20px;
      bottom: 20px;
      width: 2px;
      background: var(--accent-light);
    }
    .flow-step {
      display: flex;
      gap: 16px;
      align-items: flex-start;
      padding: 16px 0;
      opacity: 0;
      transform: translateX(-16px);
      transition: opacity 0.5s ease, transform 0.5s ease;
    }
    .flow-step.show { opacity: 1; transform: translateX(0); }
    .step-num {
      width: 40px; height: 40px;
      border-radius: 50%;
      background: var(--accent);
      color: #fff;
      display: flex; align-items: center; justify-content: center;
      font-weight: 700;
      flex-shrink: 0;
      position: relative;
      z-index: 1;
    }
    .step-content { padding-top: 6px; }
    .step-title { font-weight: 700; margin-bottom: 4px; }
    .step-desc { font-size: 14px; color: var(--text-muted); }

    /* === 工具调用链 === */
    .tool-chain {
      display: flex;
      align-items: center;
      gap: 0;
      flex-wrap: wrap;
      margin: 32px 0;
    }
    .tool-node {
      background: #fff;
      border: 2px solid var(--accent);
      border-radius: 8px;
      padding: 10px 16px;
      font-size: 13px;
      font-weight: 600;
      white-space: nowrap;
      opacity: 0;
      transition: opacity 0.4s ease;
    }
    .tool-node.show { opacity: 1; }
    .tool-arrow {
      color: var(--accent);
      font-size: 20px;
      padding: 0 8px;
      opacity: 0;
      transition: opacity 0.4s ease 0.2s;
    }
    .tool-arrow.show { opacity: 1; }

    /* === 输入输出示例 === */
    .io-example {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      gap: 16px;
      align-items: center;
      background: #fff;
      border-radius: var(--radius);
      padding: 24px;
      box-shadow: var(--card-shadow);
      margin: 16px 0;
    }
    .io-box {
      background: var(--bg-alt);
      border-radius: 8px;
      padding: 16px;
      font-size: 14px;
    }
    .io-label {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 8px;
    }
    .io-label.input { color: #7A7269; }
    .io-label.output { color: var(--accent); }
    .io-arrow { font-size: 24px; color: var(--accent); text-align: center; }

    /* === 测验 === */
    .quiz-block {
      background: #fff;
      border-radius: var(--radius);
      padding: 28px;
      box-shadow: var(--card-shadow);
      margin: 20px 0;
    }
    .quiz-question {
      font-weight: 700;
      font-size: 17px;
      margin-bottom: 20px;
    }
    .quiz-options {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .quiz-option {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 16px;
      border: 2px solid var(--bg-alt);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 14px;
    }
    .quiz-option:hover { border-color: var(--accent); background: var(--accent-light); }
    .quiz-option.correct { border-color: #2E8B72; background: #f0faf7; }
    .quiz-option.wrong { border-color: #E05C4B; background: #fdf3f2; }
    .quiz-feedback {
      margin-top: 16px;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 14px;
      display: none;
    }
    .quiz-feedback.show { display: block; }
    .quiz-feedback.correct { background: #f0faf7; color: #2E8B72; border-left: 4px solid #2E8B72; }
    .quiz-feedback.wrong { background: #fdf3f2; color: #E05C4B; border-left: 4px solid #E05C4B; }

    /* === Tooltip 术语提示 === */
    .term {
      border-bottom: 1px dashed var(--accent);
      cursor: help;
      position: relative;
    }
    .term::after {
      content: attr(data-tip);
      position: absolute;
      bottom: calc(100% + 6px);
      left: 50%;
      transform: translateX(-50%);
      background: var(--text);
      color: #fff;
      font-size: 12px;
      padding: 6px 10px;
      border-radius: 6px;
      white-space: nowrap;
      max-width: 220px;
      white-space: normal;
      text-align: center;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s;
      z-index: 200;
    }
    .term:hover::after { opacity: 1; }

    /* === 进度条 === */
    .progress-bar {
      position: fixed;
      top: 0; left: 0;
      height: 3px;
      background: var(--accent);
      transition: width 0.2s ease;
      z-index: 200;
    }

    /* === 代码块 === */
    .code-block {
      background: var(--code-bg);
      border-radius: 8px;
      padding: 16px 20px;
      font-family: var(--font-mono);
      font-size: 13px;
      color: #cdd6f4;
      overflow-x: auto;
      margin: 16px 0;
    }
    .code-comment { color: #6c7086; }
    .code-keyword { color: #cba6f7; }
    .code-string { color: #a6e3a1; }
    .code-var { color: #89b4fa; }

    /* === Skill 获取区 === */
    .skill-download {
      max-width: 960px;
      margin: 0 auto;
      padding: 40px 48px 32px;
    }
    .skill-download-card {
      background: #fff;
      border-radius: var(--radius);
      padding: 28px 32px;
      box-shadow: var(--card-shadow);
      border-left: 4px solid var(--accent);
    }
    .skill-download-card h2 {
      font-family: var(--font-display);
      font-size: 22px;
      font-weight: 700;
      margin: 0 0 16px;
    }
    .download-desc {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.7;
      margin-bottom: 16px;
    }
    .download-image {
      max-width: 100%;
      border-radius: 10px;
      margin-bottom: 16px;
      box-shadow: 0 2px 8px rgba(44,40,37,0.1);
    }
    .download-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 8px;
    }
    .download-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 10px 20px;
      background: var(--accent);
      color: #fff;
      border: none;
      border-radius: 8px;
      font-family: var(--font-body);
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: opacity 0.2s;
    }
    .download-btn:hover { opacity: 0.85; }
    .download-btn.secondary {
      background: transparent;
      color: var(--accent);
      border: 2px solid var(--accent);
    }
    .download-btn.secondary:hover { background: var(--accent); color: #fff; }

    /* === 响应式 === */
    @media (max-width: 640px) {
      .module { padding: 60px 20px; }
      .side-by-side { grid-template-columns: 1fr; }
      .compare-table { overflow-x: auto; }
      .compare-table table { min-width: 520px; }
      .io-example { grid-template-columns: 1fr; }
      .io-arrow { transform: rotate(90deg); }
      .nav-sidebar { display: none; }
      .skill-download { padding: 24px 20px 20px; }
    }
  </style>
</head>
<body>

<!-- 进度条 -->
<div class="progress-bar" id="progress"></div>

<!-- 侧边导航 -->
<nav class="nav-sidebar" id="nav">
  <!-- 动态生成，每个模块一个点 -->
  <!-- <button class="nav-dot active" data-target="module-1" data-label="这是什么"></button> -->
</nav>

<!-- ==================== Skill 获取区 ==================== -->
{DOWNLOAD_SECTION}

<!-- ==================== 模块 1：这是什么 ==================== -->
<section class="module" id="module-1">
  <div class="module-tag">🎯 第一章</div>
  <h1 class="module-title">{SKILL_NAME}<br>能做什么？</h1>
  <p class="module-subtitle">{ONE_LINE_DESC}</p>

  <div class="cards-grid">
    <!-- 循环生成能力卡片 -->
    <!-- <div class="card">
      <div class="card-icon">📊</div>
      <div class="card-title">能力名称</div>
      <div class="card-desc">一句话描述这个能力</div>
    </div> -->
  </div>
</section>

<!-- ==================== 模块 2：怎么触发 ==================== -->
<section class="module" id="module-2">
  <div class="module-tag">💬 第二章</div>
  <h2 class="module-title">怎么告诉我<br>你想用它？</h2>
  <p class="module-subtitle">这些说法都能触发这个 skill</p>

  <div class="chat-container" id="trigger-chat">
    <!-- 对话气泡动态展示 -->
  </div>
</section>

<!-- ==================== 模块 3：怎么运作 ==================== -->
<section class="module" id="module-3">
  <div class="module-tag">⚙️ 第三章</div>
  <h2 class="module-title">幕后发生了<br>什么？</h2>
  <p class="module-subtitle">从你说话到拿到结果，中间的每一步</p>

  <!-- 流程步骤 -->
  <div class="flow-steps" id="flow">
    <!-- 动态生成 flow-step -->
  </div>

  <!-- 并排对照 -->
  <div class="side-by-side">
    <div class="side-col">
      <div class="side-header">技术描述</div>
      <!-- side-cell 行 -->
    </div>
    <div class="side-col">
      <div class="side-header">通俗中文</div>
      <!-- side-cell 行 -->
    </div>
  </div>
</section>

<!-- ==================== 模块 4：背后用了什么 ==================== -->
<section class="module" id="module-4">
  <div class="module-tag">🔧 第四章</div>
  <h2 class="module-title">它调用了<br>哪些工具？</h2>
  <p class="module-subtitle">skill 背后的工具调用链</p>

  <div class="tool-chain" id="tool-chain">
    <!-- 动态生成 tool-node + tool-arrow -->
  </div>
</section>

<!-- ==================== 模块 5：输入输出 ==================== -->
<section class="module" id="module-5">
  <div class="module-tag">📦 第五章</div>
  <h2 class="module-title">你给什么<br>得到什么？</h2>
  <p class="module-subtitle">真实的使用示例</p>

  <!-- 多个 io-example -->
</section>

<!-- ==================== 模块 6：小测验 ==================== -->
<section class="module" id="module-6">
  <div class="module-tag">🧪 第六章</div>
  <h2 class="module-title">测一测<br>你学到了什么</h2>
  <p class="module-subtitle">不是记忆题，是应用题</p>

  <!-- 2-3 个 quiz-block -->
</section>

<script>
  // ===== 导航点生成 =====
  const modules = document.querySelectorAll('.module');
  const nav = document.getElementById('nav');
  const LABELS = {NAV_LABELS}; // JSON array of labels

  modules.forEach((mod, i) => {
    const btn = document.createElement('button');
    btn.className = 'nav-dot' + (i === 0 ? ' active' : '');
    btn.dataset.target = mod.id;
    btn.dataset.label = LABELS[i] || `第${i+1}章`;
    btn.addEventListener('click', () => {
      mod.scrollIntoView({ behavior: 'smooth' });
    });
    nav.appendChild(btn);
  });

  // ===== 进度条 =====
  const progress = document.getElementById('progress');
  function updateProgress() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progress.style.width = pct + '%';
  }

  // ===== IntersectionObserver：进入视口触发动画 =====
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');

        // 更新导航点
        const id = entry.target.id;
        document.querySelectorAll('.nav-dot').forEach(dot => {
          dot.classList.toggle('active', dot.dataset.target === id);
        });

        // 流程步骤依次显示
        if (entry.target.id === 'module-3') {
          document.querySelectorAll('.flow-step').forEach((step, i) => {
            setTimeout(() => step.classList.add('show'), i * 200);
          });
        }

        // 工具链依次显示
        if (entry.target.id === 'module-4') {
          document.querySelectorAll('.tool-node, .tool-arrow').forEach((el, i) => {
            setTimeout(() => el.classList.add('show'), i * 150);
          });
        }
      }
    });
  }, { threshold: 0.2 });

  modules.forEach(m => observer.observe(m));
  window.addEventListener('scroll', updateProgress);

  // ===== 对话气泡动画 =====
  function animateChat(containerId, bubbles) {
    const container = document.getElementById(containerId);
    if (!container) return;
    bubbles.forEach((b, i) => {
      const div = document.createElement('div');
      div.className = 'chat-bubble' + (b.right ? ' right' : '');
      div.innerHTML = `
        <div class="bubble-avatar">${b.avatar}</div>
        <div>
          <div class="bubble-label">${b.label}</div>
          <div class="bubble-text">${b.text}</div>
        </div>
      `;
      container.appendChild(div);
      setTimeout(() => div.classList.add('show'), i * 600 + 400);
    });
  }

  // ===== 测验逻辑 =====
  document.querySelectorAll('.quiz-option').forEach(opt => {
    opt.addEventListener('click', () => {
      const block = opt.closest('.quiz-block');
      if (block.dataset.answered) return;

      const isCorrect = opt.dataset.correct === '1';

      // 清除之前的错误标记，允许重试
      block.querySelectorAll('.quiz-option.wrong').forEach(el => el.classList.remove('wrong'));

      opt.classList.add(isCorrect ? 'correct' : 'wrong');

      // 只有答对才锁定，不揭示正确答案
      if (isCorrect) {
        block.dataset.answered = '1';
      }

      const feedback = block.querySelector('.quiz-feedback');
      if (feedback) {
        feedback.classList.remove('show', 'correct', 'wrong');
        feedback.classList.add('show', isCorrect ? 'correct' : 'wrong');
        feedback.textContent = isCorrect
          ? '✅ ' + (feedback.dataset.right || '正确！')
          : '❌ ' + (feedback.dataset.wrong || '再想想~');
      }
    });
  });

  // ===== 文件下载（嵌入式 base64 文件） =====
  function downloadEmbeddedFile(b64, filename) {
    const bin = atob(b64);
    const arr = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
    const blob = new Blob([arr]);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename; a.click();
    URL.revokeObjectURL(url);
  }

  // ===== 初始化 =====
  updateProgress();

  // 调用具体 skill 的数据初始化函数（下方 SKILL_DATA 块注入）
  if (typeof initSkillData === 'function') initSkillData();
</script>

<!-- ===== SKILL_DATA: 在此注入 skill 特定数据 ===== -->
<script>
function initSkillData() {
  // 示例：
  // animateChat('trigger-chat', [
  //   { avatar: '👤', label: '你说', text: '帮我把这个 Excel 分析一下' },
  //   { avatar: '🤖', label: 'AI', right: true, text: '好的，读取文件中...' },
  // ]);
}
</script>

</body>
</html>
```

## 使用指南

生成 HTML 时：

1. 替换 `{SKILL_NAME}`、`{ONE_LINE_DESC}`、`{ACCENT_COLOR}`、`{ACCENT_LIGHT}`、`{NAV_LABELS}`
2. 替换 `{DOWNLOAD_SECTION}`：如用户提供了获取方式，填入获取区 HTML；否则留空
3. 按 skill 分析结果填充各模块内容
4. 在 `initSkillData()` 函数中注入对话气泡数据
5. 确保所有动态元素都用 `data-*` 属性驱动，不内联 JS 逻辑

## 颜色预设

| 主题 | accent | accent-light | 适合场景 |
|---|---|---|---|
| 珊瑚红 | `#E05C4B` | `rgba(224,92,75,0.12)` | 数据处理、文档类 |
| 靛青蓝 | `#2D6A9F` | `rgba(45,106,159,0.12)` | 通信、API、集成类 |
| 松绿 | `#2E8B72` | `rgba(46,139,114,0.12)` | 分析、知识、查询类 |
| 琥珀橙 | `#C97B1A` | `rgba(201,123,26,0.12)` | 自动化、工具类 |
