# 悦达智科｜商业方法论 × AI Skill / Agent / 本地应用样板库

> 这不是提示词合集，而是一套把商业方法论、企业经验和 AI 协作能力转译成 Skill、Agent、本地应用与 OA 协同系统的公开样板库。

官网入口：  
[https://yuedalee.github.io/](https://yuedalee.github.io/)

---

## 这个仓库是什么？

`yueda-ai-workflow-kit` 是悦达智科用于公开沉淀 AI 工作流、Agent Skill、方法论转译、内容自动化与人机协同方法的样板库。

它的目标不是炫技，也不是简单收集提示词，而是把中小企业经营中反复出现的任务、判断、沟通、复盘和经验沉淀，整理成可复制、可执行、可持续迭代的 AI 协作能力。

简单说：

> 把企业经验变成流程，把商业方法论变成 Skill，把 Skill 变成企业可用的 AI 生产力。

---

## 悦达智科关注什么？

悦达智科关注的是：如何把商业判断、企业教练、经营共创工具、营销管理理论，与企业自身经验和工作方式结合，沉淀为：

* Agent Skill
* AI 工作流
* 本地应用原型
* 企业知识库
* OA 协同模块
* 人机协同工作中枢

目标不是替代老板、管理者或员工，而是让科学管理工具变得更容易使用，让普通团队也能一边使用、一边学习、一边沉淀自己的组织能力。

---

## 适合谁使用？

这个仓库适合：

* 中小企业老板
* 企业高管和部门负责人
* 新媒体与内容团队
* 企业服务从业者
* AI 工具实践者
* 正在搭建个人或企业 AI 工作流的人
* 想把经验方法沉淀成 Agent Skill 的专业人士

---

## 当前公开样板

### 1. [内容资料包生成 Skill](skills/official-account-package/SKILL.md)

状态：已公开 v1.0

用于把一个选题整理成适合长文、图文、短视频、直播复盘和内容传播使用的资料包，包括：

* 标题候选
* 摘要
* 正文结构
* 配图清单
* 插图位置
* 发布检查清单
* 示例输入
* 示例输出骨架

相关文件：

* [Skill 说明文件](skills/official-account-package/SKILL.md)
* [示例输入 input.md](skills/official-account-package/examples/input.md)
* [示例输出骨架 output-outline.md](skills/official-account-package/examples/output-outline.md)

目标不是替代创作者，而是让内容生产过程更稳定、更可复用。

---

### 2. [企业问题诊断 Skill](skills/business-problem-diagnosis/SKILL.md)

状态：已公开 v1.0

用于帮助企业老板和管理者判断一个问题是否值得投入资源，识别真正的关键问题，并形成 72 小时行动建议。

它重点判断：

* 这个问题是不是关键问题
* 是否影响收入、现金流、客户信任和团队协同
* 哪些部分属于可行动范围
* 下一步 72 小时内最应该做什么
* 哪些事情不建议立刻做

相关文件：

* [Skill 说明文件](skills/business-problem-diagnosis/SKILL.md)
* [示例输入 input.md](skills/business-problem-diagnosis/examples/input.md)
* [示例输出骨架 output-outline.md](skills/business-problem-diagnosis/examples/output-outline.md)

目标不是替代专业咨询，而是帮助用户从“情绪化焦虑”进入“结构化判断”。

---

### 3. [Agent Skill 通用模板](templates/skill-template.md)

状态：已公开 v1.0

用于创建新的 Agent Skill / AI 工作流样板，保证不同 Skill 的结构、边界、质量标准和示例格式保持一致。

建议所有后续 Skill 都基于这个模板创建。

---

### 4. 短视频脚本策划 Skill

状态：规划中

用于把选题判断、口播稿、分镜、封面文案和平台发布版本，沉淀成可复用的内容工作流。

---

## 方法论转译方向

后续会逐步把更多商业、管理、营销、决策和教练模型转译成可使用的工具。公开表达时，我们优先使用普通人能理解的中文功能名，例如：

* 关键问题分级
* 行动边界判断
* 目标对齐
* 战略拆解
* 教练式提问
* 行动复盘
* 顾客动机分析
* 说服力检核
* 行为触发设计
* 关键体验设计

这些名称用于描述工具功能，不直接把第三方课程、书籍或模型缩写作为悦达智科自己的产品名。

---

## 推荐目录结构

```text
yueda-ai-workflow-kit/
├── README.md
├── LICENSE
├── skills/
│   ├── official-account-package/
│   │   ├── SKILL.md
│   │   └── examples/
│   │       ├── input.md
│   │       └── output-outline.md
│   ├── business-problem-diagnosis/
│   │   ├── SKILL.md
│   │   └── examples/
│   │       ├── input.md
│   │       └── output-outline.md
│   └── short-video-script/
│       └── SKILL.md
├── templates/
│   └── skill-template.md
├── docs/
│   ├── roadmap.md
│   └── faq.md
└── examples/
    └── use-cases.md
```

说明：GitHub 不支持真正的空文件夹，所以每个目录都需要至少放一个文件。

---

## 什么是 Agent Skill？

在本项目中，Agent Skill 指的是一套可以被 AI 使用的专业任务说明包。

它通常包括：

* 角色定位
* 任务目标
* 输入要求
* 输出格式
* 判断标准
* 执行步骤
* 示例输入
* 示例输出
* 风险提醒

它不是一句提示词，而是一套让 AI 稳定完成某类任务的工作说明书。

---

## 公开版与商业版的边界

本仓库只公开基础样板、学习示例和通用框架。

不会公开：

* 客户数据
* 私有项目资料
* 商业交付模板
* 企业内部知识库
* 完整商业版 Agent Skill 包

如果需要完整企业版工作流、私有化部署或定制化 Skill 设计，需要通过商业合作方式进行。

---

## 商业服务方向

悦达智科可围绕以下方向提供服务：

### 1. 企业经营诊断与方法论转译

把商业判断和管理工具变成可执行流程。

### 2. 内容、营销和客户增长工作流

把顾客洞察、说服力检核和行为触发设计用于实际获客。

### 3. Agent Skill 设计

把岗位经验、专家方法和内容规范封装成可调用能力。

### 4. 企业知识库与本地应用原型

把文档、会议、客户沟通和员工经验沉淀为可查询、可复盘、可协作的系统。

### 5. 人机协同工作中枢规划

围绕经营、会议、任务、客户、内容和复盘，设计真人掌舵、AI 协同的工作中枢。

---

## 使用建议

你可以把本仓库当作：

* 学习 AI 工作流设计的参考库
* 搭建企业内部 AI 助手的起点
* 设计 Agent Skill 的结构模板
* 评估企业 AI 转型路径的启发材料

但请注意：

> 真正有效的 AI 工作流，不是复制模板，而是从真实业务问题出发，结合企业自己的流程、数据、人员和目标进行设计。

---

## 许可证

本仓库采用 MIT License。

这意味着你可以学习、参考和改造公开样板，但使用时需要保留原始版权声明。

商业项目中直接使用或深度改造本项目内容时，建议注明来源：

```text
Based on Yueda AI Workflow Kit by 悦达智科
```

---

## 后续计划

* [x] 创建内容资料包生成 Skill
* [x] 添加内容资料包 Skill 示例输入
* [x] 添加内容资料包 Skill 示例输出骨架
* [x] 创建企业问题诊断 Skill
* [x] 添加企业问题诊断 Skill 示例输入
* [x] 添加企业问题诊断 Skill 示例输出骨架
* [x] 增加 Skill 设计模板
* [ ] 创建短视频脚本策划 Skill
* [ ] 增加方法论转译案例
* [ ] 增加企业 AI 工作流案例
* [ ] 增加 FAQ 文档
* [ ] 增加使用演示
* [ ] 增加中英文版本说明

---

## 关于悦达智科

悦达智科是悦达传媒围绕 AI 工具、商业方法论、企业工作流、内容自动化、Agent Skill 和人机协同系统展开的实践型项目。

我们相信：

> AI 的真正价值，不是让人追逐工具，而是帮助企业把经验变成系统，把系统变成生产力。

官网：  
[https://yuedalee.github.io/](https://yuedalee.github.io/)

---

© 2026 悦达传媒｜悦达智科. Released under the MIT License.
