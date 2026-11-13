# 步骤卡 · prototype/hi-fi

> 状态 = 本 step；全局规则见 `rules/core/global-rules.md`（遵守全文；重读按 §7）；方法在 §6 指定节（打开→执行→回包）。不读他步 packet / 大手册。

## 1. 元信息

- **workflow / step**：`prototype` / `hi-fi`（高保真可点击原型）
- **packet**：`rules/packets/prototype/hi-fi.md`
- **角色**：`ux-designer`（产品设计（信息架构/线框/视觉/高保真原型/评审/handoff/展示材料））。没有专职设计师时，由产品经理戴“设计帽子”，产出可用、可评审、可交付开发的高保真原型；本步只做该角色职责；越界交回或升级。
- **上游**：`visual`（取其产出为本步输入；该步被 `when` 跳过则记 `skip=`，不因缺上游阻塞，除非本步硬依赖其产出）
- **后续**：`engineering`
- **失败去向**：停在本步，按 §4 门与 §5 规则补齐或升级；不得静默跳过。

## 2. 本步目标

- **目标**：高保真可点击原型
- **产出**：{workroot}/{ver}/20-design/prototype/index.html + design-tokens.css

## 3. 本步硬约束（全局规则 + 本步边界）

> **全局规则**：遵守 `rules/core/global-rules.md`（重读按 §7）；本步未按 §7 复核不得写 `global=ok`。首行锚带 `global=ok`（偏离写 `global=dev:<原因>`）。

### 本步边界

- **主从**：本包=本步目的/门槛/门/推进；§6 技能=做法；§7 模板=壳；global-rules=跨步场规则。本步专属门槛以本包为准，不把技能当第二套流程。
- 只读本包 + §6 技能 + §7 模板；不通读他步/大手册。core/defects/collaboration 等具名索引按需打开当前节。
- 必开技能打开→执行→回包；未过 §4 门不得宣称完成。

## 4. 本步门

- 本步无额外 hitl/gate；仍遵守开局意图确认与完成口径。
- **推进**：默认本步完成后即停（仍输出收尾骨架），不打开下一步。仅当本会话是按链、继续、按计划执行或全链入口时，才进入阶段表的下一未跳过步。

## 5. 本步动作

> **本节 = 本步编排与门槛**（顺序、产出、门、禁做）。
> **方法质量在技能**：§6 列为必开/条件开的 skill 必须按闭环执行，**禁止**把技能正文粘进本包替代实读；**禁止**为省事跳过必开技能。

- **本步必开技能（质量不降）**：`ui-visual-design-system`、`prototype-and-interaction` → 见 §6 闭环。

### 本步动作清单

- 静态 HTML/CSS（可少量 JS），浏览器直接打开。
- 覆盖核心流程、状态、响应式、无障碍基础。
- 数据模型/seed/重置。
- 导航/历史/返回/未保存提醒。
- 每页状态矩阵逐项落地。
- 单据类 A4 打印/导出。
- 原型/PRD 版本元数据（页面 title/meta 或说明文件）。
- 不做生产级后端。
- 无设计师时以“清晰、一致、可用”为准，不冒充品牌级视觉。
- **分页构建**（子代理编排 ）：≥8 页 → 中心先定 IA/tokens/组件/页面契约。
- 一页或一小批一子代理，只写 `原型/pages/{page}.html`。
- pages 不相交可并行≤3。
- **禁止并行写 `prototype/index.html`**。
- 超时降级直做。
- 编排组装 index。
- verifier 一致性/无障碍。
- <8 页单 agent。
- 声明 `mode=`。
- 技能见 §6 `prototype-and-interaction`、§6 `ui-visual-design-system`。
- 能力 ui-generation 可选增强，未装不影响。

## 6. 技能指向（打开 → 执行 → 回包）

> **技能闭环（硬）**：打开 → **整卡读取**（必做 → 方法/判定 → 反模式/DoD）→ **回到本步骤包**继续门/产出/完成信号。  
> 多个必开技能**按表格顺序逐个**闭环（一次只打开 1 个，做完即回包）；不得并行打开，也不得用摘要代替实读。
> `references/` 仅在技能正文点名时再打开；不预读其它技能/手册。

| 技能 | 级别 | 何时 | 路径 | 打开后 |
| --- | --- | --- | --- | --- |
| `ui-visual-design-system` | **必开** | 进入本步即开（质量不降） | `skills/ui-visual-design-system/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |
| `prototype-and-interaction` | **必开** | 进入本步即开（质量不降） | `skills/prototype-and-interaction/SKILL.md` | 整卡读取（必做 → 方法/判定 → 反模式/DoD）→ 回本包 |

- 必开未整卡实读 / 未按方法执行 = **未遵守**（不得用「包内已有摘要」代替）。
- 条件未命中 → 该行 `na` + 一句理由。
- 禁止把 SKILL 全文粘贴进步骤包或对话冒充已执行。

## 7. 模板与证据

- **无强制模板**：§5 编排已给出动作/顺序；直接落 §2 产出。

## 8. 完成与退出

- §2 产出已落盘；§6 必开技能已实读执行（或条件 `na`）。
- 本步 hitl 已确认，或 when 条件跳过。
- 本步无完成 Claim 门：产出落盘且本步门已过（或 `na`）即可退出；`claim=na`。
- 失败：停在本步补齐或升级；不得静默跳过。

## 9. 回执

```text
route=workflow:prototype | step=hi-fi | agent=ux-designer | packet=rules/packets/prototype/hi-fi.md | global=ok | skills=ui-visual-design-system,prototype-and-interaction|done|na | claim=ALLOWED|DENIED|na | next=…
```
