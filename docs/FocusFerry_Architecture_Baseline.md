# FocusFerry Architecture Baseline v0.1

> 本文件是 FocusFerry「专注渡」当前阶段的工程基线。  
> 核心目标：**把混乱的想法，渡成清楚的下一步。**

---

## 0. 产品红线

### 0.1 前台极简

前台禁止展示任何方法论名称。用户不需要知道马斯洛、邓宁-克鲁格、乔哈里视窗、U 型理论、SECI、私董会七步法、冰山模型、KT 法、麦肯锡七步法、BSC、PERMA 等概念。

前台唯一主入口：

```text
输入你当下的混乱、焦虑、拖延或任务。
我会帮你渡成一个清楚的下一步。
```

### 0.2 技术控盘

LLM 不负责流程控制。  
LLM 只负责结构化理解与自然语言生成。  
流程控制必须由 Conversation State Machine 强制执行。

### 0.3 商业分层

- 公开基础版：个人注意力清场与行动摆渡。
- 私有化交付版：将脱敏后的岗位踩坑、任务模板、流程经验转译为企业私有资产。

---

## 1. 核心闭环

```text
Raw_User_Input
  ↓
CleanInputParser
  ↓
Conversation State Machine
  ↓
Control Split
  ↓
Min_Action Generator
  ↓
Min_Action Validator
  ↓
Focus / Execute
  ↓
Review
  ↓
Personal Experience Card
  ↓
Privacy Guard
  ↓
Enterprise Asset Candidate
```

---

## 2. ConversationState 刚性状态机

### 2.1 状态定义

```python
from typing import Literal, Optional, List
from pydantic import BaseModel, Field

Stage = Literal[
    "S0_START",
    "S1_SAFETY_GATE",
    "S2_CLEARING_INPUT",
    "S3_FACT_CAPTURE",
    "S4_CONTROL_SPLIT",
    "S5_MIN_ACTION_DRAFT",
    "S6_ACTION_COMMIT",
    "S7_FOCUS_RUN",
    "S8_REVIEW",
    "S9_EXPERIENCE_CARD",
    "S10_ENTERPRISE_ASSET_CANDIDATE",
    "S_BLOCKED_NEED_FACTS",
    "S_HOLD_EMOTION",
    "S_DEEP_DIAGNOSE",
]

EntryChannel = Literal[
    "web",
    "feishu",
    "wecom",
    "wechat",
    "unknown",
]

RiskLevel = Literal[
    "normal",
    "elevated",
    "unsafe",
]

class EvidenceLedger(BaseModel):
    confirmed_facts: List[str] = Field(default_factory=list)
    inferred_possibilities: List[str] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)
    verification_next_step: Optional[str] = None

class MinimalAction(BaseModel):
    action_text: str = Field(..., min_length=4, max_length=120)
    first_physical_step: str = Field(..., min_length=2, max_length=100)
    estimated_minutes: int = Field(..., ge=1, le=15)
    completion_signal: str = Field(..., min_length=2, max_length=120)
    target_object: str = Field(..., min_length=1, max_length=100)
    within_user_control: bool
    depends_on_immediate_reply: bool = False
    risk: Literal["low", "medium", "high"] = "low"
    source_controllable_part: str = Field(..., min_length=2, max_length=200)
    not_doing: Optional[str] = Field(default=None, max_length=160)

class ExperienceCard(BaseModel):
    card_id: str
    user_id: str
    session_id: str
    created_at: str
    chaos_input_summary: str
    confirmed_facts: List[str] = Field(default_factory=list)
    core_blocker: str
    expectation: Optional[str] = None
    controllable_part: str
    uncontrollable_part: Optional[str] = None
    minimal_action: MinimalAction
    result: Optional[str] = None
    lesson: Optional[str] = None
    next_action: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    privacy_level: Literal["personal", "work_safe", "enterprise_candidate", "blocked_sensitive"] = "personal"
    enterprise_asset_candidate: bool = False

class ConversationState(BaseModel):
    user_id: str
    session_id: str
    entry_channel: EntryChannel = "unknown"
    stage: Stage = "S0_START"
    raw_user_input: str = ""

    risk_level: RiskLevel = "normal"
    emotion_label: Optional[str] = None
    chaos_summary: Optional[str] = None
    task_candidate: Optional[str] = None

    confirmed_facts: List[str] = Field(default_factory=list)
    inferred_possibilities: List[str] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)

    core_blocker: Optional[str] = None
    expectation: Optional[str] = None

    controllable_part: Optional[str] = None
    uncontrollable_part: Optional[str] = None
    minimal_action: Optional[MinimalAction] = None
    evidence_ledger: EvidenceLedger = Field(default_factory=EvidenceLedger)
    experience_card: Optional[ExperienceCard] = None

    turn_count: int = 0
    clarification_count: int = 0

    allow_advice: bool = False
    allow_action_generation: bool = False
    allow_deep_diagnosis: bool = False
    allow_enterprise_export: bool = False
```

---

### 2.2 状态转移表

| 当前状态 | 触发条件 | 下一状态 | 允许动作 | 禁止动作 |
|---|---|---|---|---|
| `S0_START` | 用户输入 | `S1_SAFETY_GATE` | 接收输入 | 分析、建议 |
| `S1_SAFETY_GATE` | 无危机 | `S2_CLEARING_INPUT` | 风险识别 | 效率建议 |
| `S1_SAFETY_GATE` | 危机/危险 | `S_HOLD_EMOTION` | 安全承接 | 行动推动 |
| `S2_CLEARING_INPUT` | 可解析 | `S3_FACT_CAPTURE` | 抽取事实/情绪/任务 | 输出方案 |
| `S3_FACT_CAPTURE` | 事实足够 | `S4_CONTROL_SPLIT` | 确认事实 | 推测根因 |
| `S3_FACT_CAPTURE` | 事实不足 | `S_BLOCKED_NEED_FACTS` | 只问一个问题 | 连问、诊断 |
| `S4_CONTROL_SPLIT` | 可控部分明确 | `S5_MIN_ACTION_DRAFT` | 切分可控/不可控 | 战略扩展 |
| `S5_MIN_ACTION_DRAFT` | 生成最小动作 | `S6_ACTION_COMMIT` | 只给一个动作 | 给多个建议 |
| `S6_ACTION_COMMIT` | 用户接受 | `S7_FOCUS_RUN` | 启动执行 | 继续分析 |
| `S6_ACTION_COMMIT` | 用户拒绝/抗拒 | `S_DEEP_DIAGNOSE` | 轻量下潜 | 责备用户 |
| `S7_FOCUS_RUN` | 用户结束 | `S8_REVIEW` | 收集结果 | 评价人格 |
| `S8_REVIEW` | 复盘完成 | `S9_EXPERIENCE_CARD` | 生成经验卡 | 扩成咨询报告 |
| `S9_EXPERIENCE_CARD` | 有企业复用价值 | `S10_ENTERPRISE_ASSET_CANDIDATE` | 标记候选 | 自动同步 |

---

### 2.3 状态路由伪代码

```python
def route_after_safety(state: ConversationState) -> str:
    if state.risk_level == "unsafe":
        return "S_HOLD_EMOTION"
    return "S2_CLEARING_INPUT"


def route_after_fact_capture(state: ConversationState) -> str:
    has_min_facts = len(state.confirmed_facts) >= 1
    has_blocker = bool(state.core_blocker)
    has_expectation_or_question = bool(state.expectation) or len(state.unknowns) > 0

    if has_min_facts and has_blocker and has_expectation_or_question:
        return "S4_CONTROL_SPLIT"
    return "S_BLOCKED_NEED_FACTS"


def route_after_control_split(state: ConversationState) -> str:
    if state.controllable_part:
        state.allow_action_generation = True
        return "S5_MIN_ACTION_DRAFT"
    return "S_BLOCKED_NEED_FACTS"


def route_after_action_commit(state: ConversationState, user_reply: str) -> str:
    if user_reply.strip() in ["开始", "开始做", "好", "可以"]:
        return "S7_FOCUS_RUN"
    state.allow_deep_diagnosis = True
    return "S_DEEP_DIAGNOSE"


def route_after_experience_card(state: ConversationState) -> str:
    if state.allow_enterprise_export and state.experience_card and state.experience_card.enterprise_asset_candidate:
        return "S10_ENTERPRISE_ASSET_CANDIDATE"
    return "END"
```

---

## 3. advice_markers 拦截网关

### 3.1 禁止提前建议

```python
ADVICE_MARKERS = [
    "建议你",
    "你应该",
    "你需要",
    "最好",
    "方案是",
    "计划是",
    "下一步是",
    "可以先",
    "你要做的是",
]

ACTION_MARKERS = [
    "只做这一步",
    "第一步",
    "完成标志",
    "用时",
    "开始做",
]

FORBIDDEN_FRONTEND_TERMS = [
    "马斯洛",
    "邓宁",
    "乔哈里",
    "U型理论",
    "U 型理论",
    "SECI",
    "私董会",
    "冰山模型",
    "KT法",
    "KT 法",
    "麦肯锡",
    "BSC",
    "PERMA",
    "方法论",
    "模型",
    "理论",
]

FACT_COLLECTION_STAGES = [
    "S2_CLEARING_INPUT",
    "S3_FACT_CAPTURE",
    "S_BLOCKED_NEED_FACTS",
]
```

### 3.2 阶段权限校验

```python
def contains_any(text: str, markers: list[str]) -> bool:
    return any(marker in text for marker in markers)


def validate_stage_permission(state: ConversationState, output: str) -> tuple[bool, list[str]]:
    violations: list[str] = []

    if contains_any(output, FORBIDDEN_FRONTEND_TERMS):
        violations.append("forbidden_methodology_term_leaked")

    if state.stage in FACT_COLLECTION_STAGES:
        if contains_any(output, ADVICE_MARKERS):
            violations.append("advice_before_fact_capture")
        if contains_any(output, ACTION_MARKERS):
            violations.append("action_before_control_split")

    if state.stage != "S5_MIN_ACTION_DRAFT":
        if "只做这一步" in output and not state.allow_action_generation:
            violations.append("min_action_generated_in_wrong_stage")

    if state.stage == "S5_MIN_ACTION_DRAFT" and not state.allow_action_generation:
        violations.append("min_action_without_permission")

    return len(violations) == 0, violations


def reject_output_and_retry(stage: str, output: str, violations: list[str]) -> str:
    return f"""
上一轮输出被 FocusFerry 状态机拒绝。

当前状态：{stage}
违规项：{violations}

被拒绝内容：
{output}

请重新生成。
硬性要求：
1. 遵守当前状态允许动作。
2. 不泄露后台方法论名称。
3. 如果当前状态还在事实收集阶段，不许给建议。
4. 如果还没有切出可控部分，不许生成下一步行动。
5. 每次最多问一个问题。
"""
```

---

## 4. CleanInputParser：事实、卡点、预期

### 4.1 目标

CleanInputParser 是 FocusFerry 的前置强阻尼解析器。它必须把用户混乱输入压缩为三个核心元数据：

```json
{
  "Fact": [],
  "Core_Blocker": {},
  "Expectation": {}
}
```

它不输出建议，不进行深层诊断，不讲理论。

---

### 4.2 CleanInputParser System Prompt

```text
你是 FocusFerry 的 CleanInputParser「强阻尼清场解析器」。

你的任务不是安慰用户，也不是给建议。
你的唯一任务是：从用户混乱输入中抽取结构化元数据。

你必须从输入中抽离出：

1. Fact
可观察、可复述、来自用户原文的事实。
事实必须是用户明确说过的内容。
不能加入你的解释。

2. Core_Blocker
当前最阻碍用户进入行动的一个核心卡点。
只能选择一个。
必须用大白话表达。
不能使用心理诊断语言。

3. Expectation
用户希望这次对话或这次专注得到什么结果。
如果用户没有明确说，标记为 inferred，并降低 confidence。

4. Emotion_Label
只做轻量情绪命名，例如：焦虑、烦躁、混乱、疲惫、委屈、抗拒。
不能展开情绪分析。

5. Noise
不适合现在处理的背景噪音、泛化担忧、不可控抱怨。

硬性禁止：
- 不许给建议
- 不许输出行动计划
- 不许讲方法论
- 不许使用任何模型名称
- 不许说“你应该”
- 不许推断用户人格
- 不许把情绪扩写成心理诊断

输出必须是严格 JSON。
不要输出 Markdown。
不要输出解释。
```

---

### 4.3 CleanInput JSON Schema

```python
from enum import Enum
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class RiskLevel(str, Enum):
    normal = "normal"
    elevated = "elevated"
    unsafe = "unsafe"

class CoreBlocker(BaseModel):
    text: str = Field(..., min_length=2, max_length=120)
    source_span: Optional[str] = None
    confidence: float = Field(..., ge=0.0, le=1.0)

class Expectation(BaseModel):
    text: str = Field(..., min_length=2, max_length=160)
    is_explicit: bool = False
    confidence: float = Field(..., ge=0.0, le=1.0)

class CleanInputResult(BaseModel):
    parser_version: Literal["clean_input_v0.1"] = "clean_input_v0.1"
    risk_level: RiskLevel = RiskLevel.normal
    emotion_label: Optional[str] = None

    fact: List[str] = Field(default_factory=list, max_length=5)
    core_blocker: Optional[CoreBlocker] = None
    expectation: Optional[Expectation] = None

    noise: List[str] = Field(default_factory=list, max_length=5)
    missing_info: List[str] = Field(default_factory=list, max_length=3)
    one_question: Optional[str] = None

    allow_next_state: bool = False
    next_state: str = "S3_FACT_CAPTURE"
```

### 4.4 CleanInput 输出示例

```json
{
  "parser_version": "clean_input_v0.1",
  "risk_level": "normal",
  "emotion_label": "混乱、烦躁",
  "fact": [
    "用户认为当前产品越做越复杂",
    "用户认为 Codex 经常跑偏",
    "用户不知道下一步该做什么"
  ],
  "core_blocker": {
    "text": "想法和任务太多，导致下一步失焦",
    "source_span": "我不知道下一步该干啥",
    "confidence": 0.86
  },
  "expectation": {
    "text": "希望把当前混乱压缩成一个清楚的下一步",
    "is_explicit": false,
    "confidence": 0.74
  },
  "noise": [
    "感觉自己一直在瞎折腾",
    "时间也浪费了"
  ],
  "missing_info": [
    "用户现在最想先推进哪一个任务"
  ],
  "one_question": "现在只选一个方向：你更想先推进产品重构，还是先处理官网未完成的任务？",
  "allow_next_state": false,
  "next_state": "S_BLOCKED_NEED_FACTS"
}
```

---

## 5. Min_Action 收敛算法

### 5.1 合格标准

Min_Action 必须满足：

1. 单一动作。
2. 3 分钟内可启动。
3. 15 分钟内可完成或看到阶段性完成标志。
4. 用户自己可控。
5. 不依赖他人立刻回复。
6. 动词具体。
7. 对象明确。
8. 风险低。
9. 有完成标志。

### 5.2 不合格动词

```python
VAGUE_VERBS = [
    "思考", "研究", "优化", "规划", "推进", "解决", "梳理清楚",
    "提升", "完善", "加强", "复盘一下", "沟通一下", "联系客户",
    "做方案", "做规划", "重新定义", "深入分析",
]

CONCRETE_VERBS = [
    "打开", "写下", "列出", "圈出", "删除", "复制", "粘贴",
    "发送", "截图", "标注", "命名", "保存", "新建",
    "选择", "改掉", "读完", "录下", "整理出",
]

MULTI_ACTION_MARKERS = [
    "并且", "然后", "同时", "再", "接着", "以及", "顺便",
    "一方面", "另一方面", "第一", "第二", "第三",
]

DEPENDENCY_MARKERS = [
    "等客户回复", "等老板确认", "等同事", "让别人", "叫他们",
    "对方同意", "客户确认后",
]
```

### 5.3 MinAction 校验器

```python
class ValidationResult:
    def __init__(self, ok: bool, violations: list[str]):
        self.ok = ok
        self.violations = violations


def contains_any(text: str, words: list[str]) -> bool:
    return any(w in text for w in words)


def validate_min_action(action: MinimalAction) -> ValidationResult:
    violations: list[str] = []

    if action.estimated_minutes > 15:
        violations.append("estimated_minutes_over_15")

    if action.estimated_minutes < 1:
        violations.append("estimated_minutes_too_short")

    if not action.within_user_control:
        violations.append("not_within_user_control")

    if action.depends_on_immediate_reply:
        violations.append("depends_on_immediate_reply")

    if action.risk != "low":
        violations.append("risk_not_low")

    if contains_any(action.action_text, VAGUE_VERBS):
        violations.append("vague_action_verb")

    if not contains_any(action.action_text + action.first_physical_step, CONCRETE_VERBS):
        violations.append("missing_concrete_verb")

    if contains_any(action.action_text, MULTI_ACTION_MARKERS):
        violations.append("multi_action_detected")

    if contains_any(action.action_text, DEPENDENCY_MARKERS):
        violations.append("external_dependency_detected")

    if not action.completion_signal.strip():
        violations.append("missing_completion_signal")

    if not action.target_object.strip():
        violations.append("missing_target_object")

    return ValidationResult(ok=len(violations) == 0, violations=violations)
```

### 5.4 失败重试机制

```python
MAX_RETRY = 2

def build_rewrite_prompt(action: MinimalAction, violations: list[str]) -> str:
    return f"""
你刚才生成的最小行动不合格。

不合格原因：{violations}
原动作：{action.action_text}

请重新生成一个更小、更具体、更可立即开始的动作。

硬性要求：
1. 只能一个动作
2. 3 分钟内可以启动
3. 15 分钟内可以完成
4. 必须有具体动词
5. 必须有明确对象
6. 必须有完成标志
7. 不依赖别人立刻回复
8. 不使用“优化、研究、规划、推进、思考、做方案”等抽象词

只输出 MinimalAction JSON。
"""


def fallback_min_action(controllable_part: str) -> MinimalAction:
    return MinimalAction(
        action_text="写下这件事接下来最小的 3 个动作，并圈出第 1 个",
        first_physical_step="打开一个空白文档，写下“接下来能做的 3 个小动作”",
        estimated_minutes=8,
        completion_signal="写出 3 个动作，并圈出第 1 个",
        within_user_control=True,
        depends_on_immediate_reply=False,
        target_object="当前卡住的事情",
        risk="low",
        source_controllable_part=controllable_part,
        not_doing="不解决全部问题，不做完整方案",
    )


def generate_min_action_with_guard(llm, state: ConversationState) -> MinimalAction:
    retry_count = 0
    prompt = build_min_action_prompt(state)

    while retry_count <= MAX_RETRY:
        raw = llm.invoke(prompt)
        action = MinimalAction.model_validate_json(raw)
        result = validate_min_action(action)

        if result.ok:
            return action

        prompt = build_rewrite_prompt(action, result.violations)
        retry_count += 1

    return fallback_min_action(state.controllable_part or "当前可控部分不清")
```

---

## 6. 个人专注经验卡片

### 6.1 JSON Data Schema

```python
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class PrivacyLevel(str, Enum):
    personal = "personal"
    work_safe = "work_safe"
    enterprise_candidate = "enterprise_candidate"
    blocked_sensitive = "blocked_sensitive"

class CardSource(str, Enum):
    web_chat = "web_chat"
    feishu_bot = "feishu_bot"
    wecom_bot = "wecom_bot"
    focus_session = "focus_session"

class RootPatternType(str, Enum):
    task_too_large = "task_too_large"
    unclear_first_step = "unclear_first_step"
    external_dependency = "external_dependency"
    fear_of_quality = "fear_of_quality"
    low_energy = "low_energy"
    priority_conflict = "priority_conflict"
    unclear_standard = "unclear_standard"
    tool_or_workflow_friction = "tool_or_workflow_friction"
    unknown = "unknown"

class SurfaceEvent(BaseModel):
    raw_summary: str = Field(..., max_length=240)
    task_context: Optional[str] = Field(default=None, max_length=160)
    emotion_label: Optional[str] = Field(default=None, max_length=60)
    source_channel: CardSource

class DeepPattern(BaseModel):
    root_pattern_type: RootPatternType = RootPatternType.unknown
    root_pattern_hypothesis: Optional[str] = Field(default=None, max_length=200)
    repeated_count: int = Field(default=1, ge=1)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

class ActionRecord(BaseModel):
    controllable_part: str = Field(..., max_length=180)
    min_action: str = Field(..., max_length=160)
    first_physical_step: str = Field(..., max_length=120)
    estimated_minutes: int = Field(..., ge=1, le=15)
    completion_signal: str = Field(..., max_length=120)

class ReviewRecord(BaseModel):
    result: Optional[str] = Field(default=None, max_length=200)
    blocker_during_action: Optional[str] = Field(default=None, max_length=200)
    lesson: Optional[str] = Field(default=None, max_length=240)
    next_action: Optional[str] = Field(default=None, max_length=160)

class EnterpriseCandidateMeta(BaseModel):
    is_candidate: bool = False
    asset_type: Optional[str] = None
    suggested_role: Optional[str] = None
    suggested_scenario: Optional[str] = None
    reason: Optional[str] = None
    requires_human_review: bool = True

class PersonalExperienceCard(BaseModel):
    schema_version: str = "personal_experience_card_v0.1"
    card_id: str
    user_id: str
    session_id: str
    created_at: str

    privacy_level: PrivacyLevel = PrivacyLevel.personal
    consent_for_enterprise_transform: bool = False

    surface_event: SurfaceEvent
    evidence_ledger: EvidenceLedger
    deep_pattern: DeepPattern
    action_record: ActionRecord
    review_record: Optional[ReviewRecord] = None
    tags: List[str] = Field(default_factory=list, max_length=10)
    enterprise_candidate: EnterpriseCandidateMeta = Field(default_factory=EnterpriseCandidateMeta)
```

---

## 7. 企业私有资产接口

### 7.1 企业资产 Schema

```python
class EnterpriseAssetType(str, Enum):
    role_pitfall = "role_pitfall"
    workflow_template = "workflow_template"
    sop_candidate = "sop_candidate"
    faq_candidate = "faq_candidate"
    onboarding_case = "onboarding_case"

class ReviewStatus(str, Enum):
    draft = "draft"
    pending_review = "pending_review"
    approved = "approved"
    rejected = "rejected"

class EnterpriseSkillAsset(BaseModel):
    schema_version: str = "enterprise_skill_asset_v0.1"

    asset_id: str
    source_card_id: str

    asset_type: EnterpriseAssetType
    review_status: ReviewStatus = ReviewStatus.pending_review

    title: str = Field(..., max_length=100)
    applicable_role: str = Field(..., max_length=80)
    applicable_scenario: str = Field(..., max_length=160)

    generalized_problem: str = Field(..., max_length=200)
    common_blocker_pattern: str = Field(..., max_length=200)
    recommended_min_action_template: str = Field(..., max_length=200)

    checklist: List[str] = Field(default_factory=list, max_length=8)
    pitfall_warning: Optional[str] = Field(default=None, max_length=200)
    reusable_prompt: Optional[str] = Field(default=None, max_length=500)

    privacy_status: Literal["redacted", "blocked", "pending"] = "pending"
    human_review_required: bool = True

    created_at: str
    created_by: str = "focusferry_system"
```

---

### 7.2 隐私脱敏规则

禁止进入企业知识库的内容：

```text
个人姓名
手机号
身份证号
邮箱
微信号
家庭住址
客户真实名称
合同金额
API Key
Token
Webhook
服务器 IP
数据库连接串
私密聊天原文
家庭关系细节
医疗/心理敏感内容
```

```python
import re

PII_PATTERNS = {
    "phone": r"1[3-9]\d{9}",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "id_card": r"\b\d{17}[\dXx]\b",
    "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "url": r"https?://[^\s]+",
    "api_key": r"(?i)(api[_-]?key|token|secret|webhook)[=:：]\s*[A-Za-z0-9_\-\.\/]+",
}

SENSITIVE_WORDS = [
    "密码", "token", "Token", "API Key", "apikey", "secret", "Webhook",
    "身份证", "银行卡", "家庭住址", "服务器地址", "数据库", "连接串",
]


def detect_sensitive_text(text: str) -> list[str]:
    hits = []
    for label, pattern in PII_PATTERNS.items():
        if re.search(pattern, text):
            hits.append(label)
    for word in SENSITIVE_WORDS:
        if word in text:
            hits.append(f"sensitive_word:{word}")
    return hits


def redact_text(text: str) -> str:
    redacted = text
    replacements = {
        "phone": "[手机号已脱敏]",
        "email": "[邮箱已脱敏]",
        "id_card": "[身份证号已脱敏]",
        "ip_address": "[IP地址已脱敏]",
        "url": "[链接已脱敏]",
        "api_key": "[密钥已脱敏]",
    }
    for label, pattern in PII_PATTERNS.items():
        redacted = re.sub(pattern, replacements[label], redacted)
    return redacted


def has_blocking_sensitive_info(card_dict: dict) -> bool:
    text = str(card_dict)
    hits = detect_sensitive_text(text)
    return any(
        h in ["api_key", "id_card"] or h.startswith("sensitive_word")
        for h in hits
    )
```

---

### 7.3 个人卡片 → 企业资产转译

```python
def is_enterprise_candidate(card: PersonalExperienceCard) -> bool:
    if not card.consent_for_enterprise_transform:
        return False
    if card.privacy_level == PrivacyLevel.blocked_sensitive:
        return False
    if has_blocking_sensitive_info(card.model_dump()):
        return False
    if not card.enterprise_candidate.is_candidate:
        return False
    return True


def generalize_problem(card: PersonalExperienceCard) -> str:
    pattern = card.deep_pattern.root_pattern_type

    if pattern == RootPatternType.task_too_large:
        return "任务范围过大，导致执行者不知道从哪里开始"
    if pattern == RootPatternType.unclear_first_step:
        return "目标存在，但第一步动作不清楚"
    if pattern == RootPatternType.tool_or_workflow_friction:
        return "工具或流程不清，导致任务推进被卡住"
    if pattern == RootPatternType.unclear_standard:
        return "完成标准不清，导致反复修改或无法启动"
    return "任务推进中出现行动入口不清的问题"


def build_min_action_template(card: PersonalExperienceCard) -> str:
    action = card.action_record
    return (
        f"遇到类似任务时，先不要处理全部问题。"
        f"先执行一个 {action.estimated_minutes} 分钟内可完成的小动作："
        f"{redact_text(action.min_action)}。"
        f"完成标志：{redact_text(action.completion_signal)}。"
    )


def transform_to_enterprise_asset(
    card: PersonalExperienceCard,
    asset_id: str,
    created_at: str,
) -> EnterpriseSkillAsset:
    if not is_enterprise_candidate(card):
        raise ValueError("card_not_allowed_for_enterprise_transform")

    scenario = card.enterprise_candidate.suggested_scenario or "任务推进卡住"
    role = card.enterprise_candidate.suggested_role or "通用岗位"

    return EnterpriseSkillAsset(
        asset_id=asset_id,
        source_card_id=card.card_id,
        asset_type=EnterpriseAssetType.workflow_template,
        review_status=ReviewStatus.pending_review,
        title=f"{role}：{scenario}的最小行动模板",
        applicable_role=role,
        applicable_scenario=scenario,
        generalized_problem=generalize_problem(card),
        common_blocker_pattern=card.deep_pattern.root_pattern_hypothesis or "行动入口不清",
        recommended_min_action_template=build_min_action_template(card),
        checklist=[
            "先确认当前任务是否过大",
            "只保留一个可控部分",
            "把动作压缩到 15 分钟内",
            "写清楚完成标志",
            "完成后记录一次复盘",
        ],
        pitfall_warning="不要一开始就做完整方案，先用一个低风险动作打开局面。",
        reusable_prompt=(
            "我现在有一个任务推进不下去。"
            "请帮我把它压缩成一个 15 分钟内可以完成的最小动作，"
            "并告诉我第一步和完成标志。"
        ),
        privacy_status="redacted",
        human_review_required=True,
        created_at=created_at,
    )


def can_sync_to_enterprise_kb(asset: EnterpriseSkillAsset) -> bool:
    return (
        asset.privacy_status == "redacted"
        and asset.human_review_required is True
        and asset.review_status == ReviewStatus.approved
    )
```

---

## 8. 企业资产数据流

```text
PersonalExperienceCard
  ↓
PrivacyGuard.detect_sensitive_text
  ↓
如果存在阻断级敏感信息：blocked_sensitive，停止
  ↓
用户授权 consent_for_enterprise_transform
  ↓
redact_text 脱敏
  ↓
generalize_problem 场景泛化
  ↓
build_min_action_template 模板化
  ↓
EnterpriseSkillAsset
  ↓
pending_review
  ↓
企业管理员审核
  ↓
approved
  ↓
企业私有知识库
```

硬规则：

```text
个人经验卡不得自动同步企业知识库。
必须经过：用户授权、隐私脱敏、人工审核。
```

---

## 9. MVP 技术验收标准

1. 所有对话必须经过 ConversationState。
2. 所有 LLM 输出必须经过 `validate_stage_permission`。
3. 事实未收齐，不得建议。
4. 可控部分未明确，不得生成行动。
5. `S5_MIN_ACTION_DRAFT` 输出必须通过 `validate_min_action`。
6. 不合格动作必须触发 `reject_output_and_retry`。
7. 连续两次失败后必须走 `fallback_min_action`。
8. 前台不得泄露后台方法论名称。
9. 经验卡片必须包含 EvidenceLedger。
10. 企业资产候选必须通过 PrivacyGuard。
11. 企业资产默认 `pending_review`，不得自动 approved。

---

## 10. 核心工程口号

```text
CleanInputParser 负责降噪。
StateMachine 负责控盘。
Min_Action 负责收敛。
ExperienceCard 负责资产化。
PrivacyGuard 负责商业安全边界。
```

FocusFerry 不做模型堆砌。  
FocusFerry 只做一件事：

> **把混乱的想法，渡成清楚的下一步。**
