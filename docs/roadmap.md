# Roadmap｜悦达智科公开样板库路线图

> 状态：占位文档 v0.3  
> 用途：记录 `yueda-ai-workflow-kit` 后续公开样板、文档和 Skill 的建设方向。

---

## 一、当前已完成

- [x] 创建公众号资料包生成 Skill
- [x] 添加公众号资料包 Skill 示例输入
- [x] 添加公众号资料包 Skill 示例输出骨架
- [x] 创建企业问题诊断 Skill
- [x] 添加企业问题诊断 Skill 示例输入
- [x] 添加企业问题诊断 Skill 示例输出骨架
- [x] 创建 Agent Skill 通用模板
- [x] 更新 README，使仓库口径与悦达智科网站同频
- [x] 创建本地商品内容与发货工作台顶层设计
- [x] 创建本地商品内容与发货工作台落地路线
- [x] 创建本地商品内容与发货工作台验收标准
- [x] 创建本地商品内容与发货工作台 Codex 构建任务书
- [x] 创建本地商品内容与发货工作台设计 Skill
- [x] 创建本地商品内容与发货工作台 V0.1 工程骨架
- [x] 增加 demo 商品、CLI、测试和 GitHub Actions CI

---

## 二、下一阶段规划

### 1. 本地商品内容与发货工作台 V1

状态：V0.1 工程骨架已建立，等待继续补强视频处理、模板化商品包和模块拆分。

目标：帮助一人公司、软件/插件卖家、虚拟商品卖家，把商品资料、主图、轮播图、详情页、教程视频、发货话术和发货日志整理成一套低成本、本地运行、可验收的半自动工作台。

核心文档与代码入口：

- [顶层设计](local-commerce-content-delivery-workbench.md)
- [落地路线](local-commerce-content-delivery-implementation-plan.md)
- [验收标准](local-commerce-content-delivery-acceptance-criteria.md)
- [Codex 构建任务书](codex-tasks/local-workbench-v1.md)
- [实现状态](local-workbench-v1-implementation-status.md)
- [Skill 说明](../skills/local-commerce-content-delivery-workbench/SKILL.md)
- [Python CLI 入口](../local_commerce_workbench/cli.py)
- [Demo 商品资料](../products/demo-plugin-001/product.yaml)

当前 V0.1 能力：商品资料校验、基础商品图生成、详情页 HTML 与长图生成、发货文案生成、订单文本解析、卡密消耗、发货日志、重复订单检测、基础测试。

原则：先做本地确定性生产线，再做平台自动化；先做半自动可控，再做全自动；先做可直接交付文件，再谈 Agent 和工作流。

---

### 2. 短视频脚本策划 Skill

状态：规划中

目标：把选题判断、口播稿、分镜、封面文案和平台发布版本，整理成可复用的内容生产工作流。

---

### 3. 方法论转译案例

状态：规划中

目标：展示如何把商业判断、企业教练、营销管理、行为设计等方法，转译为 AI 可调用的任务说明与执行流程。

---

### 4. 企业 AI 工作流案例

状态：规划中

目标：围绕内容生产、客户跟进、会议复盘、经营诊断等真实业务场景，沉淀公开版案例说明。

---

### 5. FAQ 文档

状态：基础占位中

目标：解释 Agent Skill、AI 工作流、公开版与商业版边界、如何使用本仓库等常见问题。

---

### 6. 使用案例文档

状态：基础占位中

目标：通过公开、脱敏、可复用的方式，展示这些 Skill 和工作流可以如何被使用。

---

## 三、维护原则

后续所有公开内容应遵守：

```text
悦达智科网站定方向
GitHub 仓库做支撑
Skill / 示例 / 文档提供证据
```

仓库内容要与悦达智科网站定位保持一致，不暴露客户数据、私有配置、Webhook、API Key 或商业交付细节。

---

© 2026 悦达传媒｜悦达智科. Released under the MIT License.
