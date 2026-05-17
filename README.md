# 悦达智科｜商业方法论 × AI Skill / Agent / 本地应用样板库

> 本仓库是悦达智科网站背后的公开样板库。  
> 悦达智科网站负责对外主叙事；本仓库负责沉淀公开版 Skill、工作流样板、方法论转译示例和基础文档。

悦达智科网站：  
[https://yuedalee.github.io/](https://yuedalee.github.io/)

---

## 一、这个仓库是什么？

`yueda-ai-workflow-kit` 是悦达智科用于公开沉淀 AI 工作流、Agent Skill、方法论转译、内容自动化与人机协同方法的样板库。

它不是提示词合集，也不是单纯的技术演示仓库。

它服务于悦达智科当前对外定位：

> 商业方法论 × AI Skill / Agent / 本地应用 / OA 协同系统

本仓库的目标是把中小企业经营中反复出现的任务、判断、沟通、复盘和经验沉淀，整理成可复制、可执行、可持续迭代的 AI 协作能力。

简单说：

> 把企业经验变成流程，把商业方法论变成 Skill，把 Skill 变成企业可用的 AI 生产力。

---

## 二、与悦达智科网站的关系

本仓库与悦达智科网站的关系是：

```text
悦达智科网站
= 对外主口径 / 品牌门面 / 合作咨询入口

本仓库
= 公开证据库 / Skill 样板库 / 方法论转译样板 / 后续文档沉淀区
```

因此，后续维护时应遵守：

> 网站定方向，仓库做支撑。

也就是说，仓库里的 README、Skill、示例和目录说明，都应该和悦达智科网站的定位同频，而不是让网站被仓库当前文件数量限制。

---

## 三、悦达智科关注什么？

悦达智科关注的是：如何把商业判断、企业教练、经营共创工具、营销管理理论，与企业自身经验和工作方式结合，沉淀为：

- Agent Skill；
- AI 工作流；
- 本地应用原型；
- 企业知识库；
- OA 协同模块；
- 人机协同工作中枢。

目标不是替代老板、管理者或员工，而是让科学管理工具变得更容易使用，让普通团队也能一边使用、一边学习、一边沉淀自己的组织能力。

---

## 四、适合谁使用？

这个仓库适合：

- 中小企业老板；
- 企业高管和部门负责人；
- 新媒体与内容团队；
- 企业服务从业者；
- AI 工具实践者；
- 正在搭建个人或企业 AI 工作流的人；
- 想把经验方法沉淀成 Agent Skill 的专业人士。

---

## 五、当前公开样板

### 1. [公众号资料包生成 Skill](skills/official-account-package/SKILL.md)

状态：已公开 v1.0

用于把一个选题整理成适合微信公众号发布、排版、配图、审核、交付给自动化发布流程的完整资料包。

相关文件：

- [Skill 说明文件](skills/official-account-package/SKILL.md)
- [示例输入 input.md](skills/official-account-package/examples/input.md)
- [示例输出骨架 output-outline.md](skills/official-account-package/examples/output-outline.md)

目标不是替代创作者，而是让内容生产过程更稳定、更可复用。

---

### 2. [企业问题诊断 Skill](skills/business-problem-diagnosis/SKILL.md)

状态：已公开 v1.0

用于帮助企业老板和管理者判断一个问题是否值得投入资源，识别真正的关键问题，并形成 72 小时行动建议。

相关文件：

- [Skill 说明文件](skills/business-problem-diagnosis/SKILL.md)
- [示例输入 input.md](skills/business-problem-diagnosis/examples/input.md)
- [示例输出骨架 output-outline.md](skills/business-problem-diagnosis/examples/output-outline.md)

目标不是替代专业咨询，而是帮助用户从“情绪化焦虑”进入“结构化判断”。

---

### 3. [Agent Skill 通用模板](templates/skill-template.md)

状态：已公开 v1.0

用于创建新的 Agent Skill / AI 工作流样板，保证不同 Skill 的结构、边界、质量标准和示例格式保持一致。

建议所有后续 Skill 都基于这个模板创建。

---

## 六、规划中内容

以下内容属于规划中，不代表已经完成商业交付：

- 短视频脚本策划 Skill；
- 方法论转译案例；
- 企业 AI 工作流案例；
- 常见问题 FAQ；
- 公开使用案例；
- 中英文版本说明。

为避免 README 链接指向不存在的文件，本仓库会逐步创建最小占位文档，并在文档中标注当前状态。

---

## 七、目录结构

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
│   └── business-problem-diagnosis/
│       ├── SKILL.md
│       └── examples/
│           ├── input.md
│           └── output-outline.md
├── templates/
│   └── skill-template.md
├── docs/
│   ├── roadmap.md
│   └── faq.md
└── examples/
    └── use-cases.md
```

说明：`docs/roadmap.md`、`docs/faq.md`、`examples/use-cases.md` 当前为基础占位文档，用于后续逐步完善。

---

## 八、什么是 Agent Skill？

在本项目中，Agent Skill 指的是一套可以被 AI 使用的专业任务说明包。

它通常包括：

- 角色定位；
- 任务目标；
- 输入要求；
- 输出格式；
- 判断标准；
- 执行步骤；
- 示例输入；
- 示例输出；
- 风险提醒。

它不是一句提示词，而是一套让 AI 稳定完成某类任务的工作说明书。

---

## 九、公开版与商业版的边界

本仓库只公开基础样板、学习示例和通用框架。

不会公开：

- 客户数据；
- 私有项目资料；
- 商业交付模板；
- 企业内部知识库；
- 完整商业版 Agent Skill 包；
- 私有化部署脚本；
- 飞书、企业微信、公众号等平台的 Webhook、Token、API Key。

如果需要完整企业版工作流、私有化部署或定制化 Skill 设计，需要通过商业合作方式进行。

---

## 十、商业服务方向

悦达智科可围绕以下方向提供服务：

### 1. 企业经营诊断与方法论转译

把商业判断、管理工具和企业经验转译成可执行流程。

### 2. 内容、营销和客户增长工作流

把顾客洞察、说服力检核、内容生产和客户跟进变成可复用流程。

### 3. Agent Skill 设计

把岗位经验、专家方法和内容规范封装成可调用能力。

### 4. 企业知识库与本地应用原型

把文档、会议、客户沟通和员工经验沉淀为可查询、可复盘、可协作的系统。

### 5. 人机协同工作中枢规划

围绕经营、会议、任务、客户、内容和复盘，设计真人掌舵、AI 协同的工作中枢。

---

## 十一、许可证

本仓库采用 MIT License。

这意味着你可以学习、参考和改造公开样板，但使用时需要保留原始版权声明。

商业项目中直接使用或深度改造本项目内容时，建议注明来源：

```text
Based on Yueda AI Workflow Kit by 悦达智科
```

---

## 十二、后续计划

- [x] 创建公众号资料包生成 Skill
- [x] 添加公众号资料包 Skill 示例输入
- [x] 添加公众号资料包 Skill 示例输出骨架
- [x] 创建企业问题诊断 Skill
- [x] 添加企业问题诊断 Skill 示例输入
- [x] 添加企业问题诊断 Skill 示例输出骨架
- [x] 增加 Agent Skill 通用模板
- [ ] 创建短视频脚本策划 Skill
- [ ] 增加方法论转译案例
- [ ] 增加企业 AI 工作流案例
- [ ] 完善 FAQ 文档
- [ ] 完善公开使用案例
- [ ] 增加中英文版本说明

---

## 十三、关于悦达智科

悦达智科是悦达传媒围绕 AI 工具、商业方法论、企业工作流、内容自动化、Agent Skill 和人机协同系统展开的实践型项目。

我们相信：

> AI 的真正价值，不是让人追逐工具，而是帮助企业把经验变成系统，把系统变成生产力。

官网：  
[https://yuedalee.github.io/](https://yuedalee.github.io/)

---

© 2026 悦达传媒｜悦达智科. Released under the MIT License.
