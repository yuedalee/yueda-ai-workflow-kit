# 仓库更新片段｜本地商品内容与发货工作台

> 用途：如果要把本方案加入 `yueda-ai-workflow-kit`，可以把以下片段复制到 README 和 Roadmap 中。  
> 注意：该文件只提供 README 与 Roadmap 更新建议，避免直接破坏现有 README 主体结构。

---

## 1. README「当前公开样板」建议新增

建议放在 README 的「五、当前公开样板」中，作为新的公开样板条目：

```markdown
### 4. [本地商品内容与发货工作台设计 Skill](skills/local-commerce-content-delivery-workbench/SKILL.md)

状态：设计草案 v0.1

用于帮助一人公司、软件/插件卖家、虚拟商品卖家，把商品资料、商品图、详情页、教程视频和半自动发货整理成一套低成本、可验收、可本地运行的工作台设计。

相关文件：

- [顶层设计](docs/local-commerce-content-delivery-workbench.md)
- [落地路线](docs/local-commerce-content-delivery-implementation-plan.md)
- [验收标准](docs/local-commerce-content-delivery-acceptance-criteria.md)
- [Codex 构建任务书](docs/codex-tasks/local-workbench-v1.md)
- [Skill 说明文件](skills/local-commerce-content-delivery-workbench/SKILL.md)
- [示例输入](skills/local-commerce-content-delivery-workbench/examples/input.md)
- [示例输出骨架](skills/local-commerce-content-delivery-workbench/examples/output-outline.md)

目标不是承诺全自动电商机器人，而是先把“能直接交付文件、能重复运行、能人工确认、能记录日志”的本地确定性生产线设计清楚。
```

---

## 2. README「规划中内容」建议新增/替换

可在「六、规划中内容」加入：

```markdown
- 本地商品内容与发货工作台 V1：商品资料、商品图/详情页、教程视频处理、半自动发货与日志；
- Codex 构建任务书：把 AI 代码生成任务拆成可运行、可验收、可回滚的小步任务；
```

---

## 3. README「后续计划」建议新增

可在「十二、后续计划」加入：

```markdown
- [x] 创建本地商品内容与发货工作台顶层设计
- [x] 创建本地商品内容与发货工作台落地路线
- [x] 创建本地商品内容与发货工作台验收标准
- [x] 创建 Codex 构建任务书
- [x] 创建本地商品内容与发货工作台设计 Skill
- [ ] 基于 Codex 任务书实现本地工作台 V1 代码原型
```

---

## 4. Roadmap 建议新增

建议在 `docs/roadmap.md` 的「下一阶段规划」加入：

```markdown
### 本地商品内容与发货工作台 V1

状态：设计草案完成，代码原型规划中

目标：围绕软件/插件/虚拟商品的一人公司场景，沉淀一套本地运行、低成本、半自动、可验收的商品内容与发货工作台。

V1 聚焦：

- 商品资料标准化；
- 商品主图、轮播图、详情页模板化生成；
- 教程视频录屏处理；
- 发货话术、卡密、下载链接半自动管理；
- 发货日志和重复订单检测。

边界：不做绕过验证码、平台风控、刷单刷评、全自动买家消息发送。
```

---

## 5. 建议提交信息

```bash
git add docs/local-commerce-content-delivery-workbench.md \
  docs/local-commerce-content-delivery-implementation-plan.md \
  docs/local-commerce-content-delivery-acceptance-criteria.md \
  docs/codex-tasks/local-workbench-v1.md \
  docs/repo-update-snippets.md \
  skills/local-commerce-content-delivery-workbench/SKILL.md \
  skills/local-commerce-content-delivery-workbench/examples/input.md \
  skills/local-commerce-content-delivery-workbench/examples/output-outline.md

git commit -m "docs: add local commerce content and delivery workbench design"
```
