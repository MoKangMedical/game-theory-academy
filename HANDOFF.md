# 博弈研究院 (Game Theory Academy) — Codex 交接文档

> **项目名称**：博弈研究院 v1.0.0  
> **本地路径**：`~/Desktop/OPC/game-theory-academy/`  
> **创建日期**：2026-05-16  
> **交接日期**：2026-05-17  
> **当前状态**：本地完整，**未推送到 GitHub**，需创建仓库并部署

---

## 一、项目概览

### 一句话定位
用博弈论的科学框架，帮用户在商业竞争、谈判策略和个人决策中找到最优解。

### 核心能力矩阵
| 能力模块 | 功能 | 覆盖课程 |
|---------|------|---------|
| **纳什均衡** | 策略定位、均衡求解 | 第1-12课 |
| **进化博弈论** | ESS判定、复制动态、种群演化 | 第13-18课 |
| **行为博弈论** | 有限理性、前景理论、认知偏差 | 第19-24课 |
| **机制设计** | 拍卖理论、VCG、激励相容 | 第25-30课 |
| **应用博弈** | 经济学/政治/日常/前沿 | 第31-50课 |

### 8（实为9）位 AI 辩论专家
| 专家 | 角色 | 触发关键词 |
|------|------|----------|
| 🔷 **约翰·纳什** | 博弈均衡大师 | 囚徒/困境/均衡 |
| 🟠 **托马斯·谢林** | 冲突策略家 | 冲突/威慑/承诺/核 |
| 🟢 **罗伯特·阿克塞尔罗德** | 合作演化专家 | 合作/以牙还牙/进化 |
| 🟣 **莱因哈德·泽尔腾** | 子博弈完美大师 | 完美/子博弈/精炼 |
| 🩷 **埃莉诺·奥斯特罗姆** | 公共资源治理 | 公地/公共/资源/治理 |
| 🟦 **冯·诺依曼** | 博弈论之父 | 零和/极小极大/数学/基础 |
| 🟧 **丹尼尔·卡尼曼** | 行为经济学视角 | 行为/心理/偏见/损失/非理性 |
| 🟪 **里奥尼德·赫维茨** | 机制设计师 | 拍卖/机制/激励/设计/VCG |
| 🔵 **约翰·梅纳德·史密斯** | 进化博弈先驱 | 进化稳定/ESS |

---

## 二、文件结构

```
game-theory-academy/                  (302MB，其中音频301MB)
├── README.md                         # 项目说明 + 经典博弈模型表
├── BUSINESS_PLAN.md                  # 商业化方案（定价/用户群/产品线）
├── VERSION.md                        # 版本信息 + 设计规范(CSS变量) + 功能模块
├── batch_tts.py                      # 批量TTS音频生成脚本(223行)
│
├── docs/                             # 前端页面（无框架，纯HTML+CSS+JS）
│   ├── index.html                    # 主页 — 单页滚动（29KB, 441行）
│   ├── courses.html                  # 课程展示页（38KB）
│   ├── knowledge-graph.html          # 知识图谱 — 力导向图（40KB）
│   ├── roundtable.html               # 🆕 圆桌列表页（18KB, 307行）
│   │     ├── 9个辩论议题 + 发起新辩论 + 统计面板
│   │     └── 模态框：选题/阶段/背景描述
│   ├── roundtable-detail.html        # 🆕 辩论详情页 — 聊天式（28KB, 471行）
│   │     ├── 键盘输入 → 关键词匹配 → 对应专家回复
│   │     ├── 4阶段进度：问题提出→策略分析→均衡求解→实践应用
│   │     ├── localStorage 持久化消息
│   │     └── typing indicator + 快速提示
│   └── user.html                     # 用户中心（24KB）
│         ├── 登录/注册双表单
│         ├── 仪表盘：头像+会员等级+学习进度
│         └── 完全离线 mock（localStorage）
│
├── docs/courses/                     # 51门课程 MD（908KB）
│   ├── 00-课程总览.md
│   ├── 01-博弈论基础.md
│   ├── ...
│   └── 50-终极整合.md
│
├── audio/                            # 51个课程音频 MP3 + _chunks
│   ├── 01-博弈论基础.mp3
│   ├── ...
│   └── _chunks/
│       └── 37-选举博弈/
│
├── data/                             # JSON 数据文件
│   ├── game-matrices.json            # 博弈矩阵数据（3.7KB）
│   └── knowledge-graph.json          # 知识图谱节点+边（10.9KB）
│
├── web/                              # 空目录（预留交互查询系统）
│   └── (空)                          # 原计划放 index.html + app.js
│
└── scripts/                          # 空目录（预留脚本）
    └── (空)
```

---

## 三、设计系统

### 颜色变量（深色主题 + 蓝色学术）
```css
--bg: #09090b        /* 主背景 */
--bg2: #0f0f13       /* 次背景 */
--bg3: #18181b       
--card: #1c1c21      /* 卡片背景 */
--card2: #222228     
--border: #27272a    
--text: #fafafa      /* 主文字 */
--text2: #a1a1aa     /* 次文字 */
--text3: #71717a     /* 辅助文字 */
--blue: #4f8de2      /* 主强调色 */
--blue2: #7aafe8     /* 次蓝色 */
--green: #22c55e     /* 成功/Starter */
--purple: #a78bfa    /* Premium */
--orange: #f59e0b    /* 警告/热门 */
```

### 字体
- **标题**：Noto Serif SC（衬线体，学术感）
- **正文**：Inter（无衬线体，国际化）

### 布局参数
- 最大宽度：1200px
- 圆角：16px（大）、10px（小）
- 间距：24px（标准）、32px（大）
- 响应式断点：768px

---

## 四、商业化方案（BUSINESS_PLAN.md）

| 层级 | 产品 | 定价 |
|------|------|------|
| **引流** | 博弈60秒短视频系列 + 博弈矩阵计算器小程序 | 免费 |
| **入门** | 《博弈思维》6节录播（30min/节） | ¥99 |
| **进阶** | 《博弈策略大师》12周训练营 + 直播/案例 | ¥999 |
| **企业** | 《商业博弈与竞争策略》工作坊 + 定制 | ¥6999起 |

目标用户：创业者>管理者>职场人>金融从业者>学生

---

## 五、课程体系（51门课，9个Phase）

| Phase | 范围 | 主题 |
|-------|------|------|
| 1 | 第1-5课 | 博弈论基础（定义、均衡、囚徒困境、协调、零和） |
| 2 | 第6-12课 | 经典博弈理论（重复博弈、谢林点、子博弈精炼、贝叶斯、完美贝叶斯、序贯、颤抖手） |
| 3 | 第13-18课 | 进化博弈论（ESS、复制动态、鹰鸽、信号、空间演化、文化演化） |
| 4 | 第19-24课 | 行为博弈论（有限理性、前景理论、最后通牒、信任、认知偏差、神经博弈） |
| 5 | 第25-30课 | 机制设计（导论、拍卖、VCG、匹配市场、投票、合同理论） |
| 6 | 第31-36课 | 经济学博弈（寡头竞争、产业组织、信息经济学、金融、国际贸易、公共经济） |
| 7 | 第37-42课 | 政治博弈（选举、立法、国际关系、反恐、谈判冲突、政治制度） |
| 8 | 第43-48课 | 日常生活博弈（谈判策略、婚姻、育儿、职场、社交网络、日常决策） |
| 9 | 第49-50课 | 前沿探索（AI博弈论、终极整合） |

**状态**：51门课全部有 MD + MP3，全量完成 ✅

---

## 六、部署任务清单

### 🔴 第一优先级：创建 GitHub 仓库并推送
```bash
# 1. 创建 repo
cd ~/Desktop/OPC/game-theory-academy
git init
git add -A
git commit -m "feat: 博弈研究院 v1.0.0 — 51门课+音频+9位专家圆桌辩论"

# 2. 推送到 GitHub（需先创建 MoKangMedical/game-theory-academy）
gh repo create MoKangMedical/game-theory-academy --public --push \
  --source=. --remote=origin
```

**注意**：302MB 大文件（主要是 audio/ 下 51 个 MP3），GitHub 限制 100MB 单文件，单个 MP3 约 6MB 没问题，但整体 push 可能较慢。如果遇到问题，可用 Git LFS。

### 🟡 第二优先级：部署到 GitHub Pages
- 启用 Pages：main 分支 /docs 路径
- 域名：可关联 `opcplatform.cn/game-theory` 或独立域名

### 🟢 第三优先级（建议迭代）
1. **课程 HTML 生成**：用 pandoc 将 51 门 MD 转为 HTML（参考 cosmic-lens 流水线）
2. **courses.html 补全**：目前课程列表只是占位，需生成 51 课卡片
3. **知识图谱优化**：knowledge-graph.html 包含力导向图，需校验数据加载
4. **用户系统后端**：目前 user.html 全 mock，可对接 SecondMe OAuth
5. **Web 交互系统**：web/ 目录空着，可放博弈矩阵计算器
6. **导航统一**：所有页面导航栏保持一致的链接结构

---

## 七、技术要点与已知坑

### 1. 圆桌辩论的 AI 回复机制
- **不是真 AI**，是纯前端关键词匹配 + 预设回复模板
- 关键词匹配在 `generateExpertResponse()` 函数中（第387行）
- 无匹配关键词时随机选专家 + 通用回复
- 消息持久化到 `localStorage`

### 2. 专家数量：代码有 9 位，UI 说 8 位
- EXPERTS 对象定义了 9 个专家（包括 evolutionary/史密斯）
- 但页面标题和面板标题写的是"8位"
- 需要统一

### 3. 音频文件
- 全部 51 个 MP3（单声道、48kbps、edge-tts 生成）
- `batch_tts.py` 是旧的批量生成脚本，依赖 edge-tts Python 库
- `audio/_chunks/` 是临时分片，可清理

### 4. 无外部依赖的纯静态站
- 所有页面是普通 HTML，无 React/Vue 框架
- roundtable-detail.html 引用了 CDN：Tailwind CSS + Font Awesome
- Font Awesome 用于专家列表图标（fa-users, fa-paper-plane）

### 5. 会员等级（已定义）
- Free（灰色）→ Starter（绿色 ¥99）→ Pro（蓝色 ¥999）→ Premium（紫色 ¥6999+）

### 6. 空目录
- `web/` 和 `scripts/` 为空，README 提到原计划在此放交互查询系统
- 实际所有页面都在 `docs/` 下

---

## 八、本地音频流水线（如需生成更多音频）

```bash
# TTS 生成（edge-tts）
edge_tts --voice zh-CN-YunyangNeural --rate=-8% --pitch=-2Hz \
  --text "$(cat lesson_text.txt)" --write-media /tmp/output.wav

# FFmpeg 后处理
ffmpeg -i /tmp/output.wav \
  -af "loudnorm=I=-16:TP=-1.5:LRA=9" \
  -ar 24000 -ac 1 -b:a 48k /tmp/output.mp3
```

---

## 九、快速启动

```bash
# 查看项目
cd ~/Desktop/OPC/game-theory-academy
open docs/index.html          # 在浏览器打开主页

# 创建 GitHub 仓库（需 gh CLI）
cd ~/Desktop/OPC/game-theory-academy
git init && git add -A && git commit -m "feat: 博弈研究院 v1.0.0"
gh repo create MoKangMedical/game-theory-academy --public --push

# 推送到已存在的仓库
git remote add origin https://github.com/MoKangMedical/game-theory-academy.git
git push -u origin main
```

---

**祝 Codex 顺利接管！** 🎲
