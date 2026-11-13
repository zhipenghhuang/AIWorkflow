# 实例能力纪律（产品）

> **读取级别：参考**。装配 / 体检 / 首次触达外部工具 / 收尾拟提能力·技能建议时读；业务顺跑只读 `{workroot}/capabilities/00-能力清单.md` 相关行 + 契约 §2（硬触达时）。

## 1. 单一出处

- **真源**：`{workroot}/capabilities/`（清单必有；`槽位/` · `绑定/` · `装配/` 按需）。
- **禁双写**：`product-profile.md` 等只索引清单；不抄绑定正文。
- **包侧**：`capabilities/00-contract.md` + `capabilities/reference.md`。实例选型不写回包内。

## 2. 渐进读

| 文件 | 何时读 |
| --- | --- |
| `{workroot}/capabilities/00-能力清单.md` | 需要外部工具时（Tier1） |
| `{workroot}/capabilities/槽位/{slot}.md` | 清单 `详情=` 指向或复杂选型（Tier2） |
| `{workroot}/capabilities/绑定/{slot}.md` | 清单 `绑定=` 指向或执行需端口/server（Tier3） |
| `{workroot}/capabilities/装配/*` | 装配留痕 / 排障 |

无清单 → 接入不强制填满；**命中槽需落状态**或「装配能力」→ 确认后写入（缺失提示见契约 §2）。

## 3. 字段与 kind

清单行：`能力名` · `启用` · `kind`（`mcp`｜`skill-cli`｜`builtin`｜`none`）· `impl` · `status`（available｜missing｜degraded｜prompted｜undecided）· `详情` · `绑定` · `verified`。

- `kind=mcp`：按 MCP 稳态；禁静默换 server。  
- `kind=skill-cli` / `builtin`：按该实现；`none`=未装。  
- **禁**未确认改启用集或换 `impl`。
- **status**：
  - `available`：可用，不提示。
  - `missing` / `undecided`：硬触达按契约 §2 出【能力缺失】；软触达见「业务建议」。
  - `prompted`：仅审计曾出过全块 → **不**单独当作已接受。
  - `degraded`：备注含 `accepted=日期` 才算接受 → 同会话免全块；跨会话/新战役短提醒；无 `accepted` 视同未接受。

他轨能力实例可复用：清单写 `复用=` 指针，不复制绑定正文；生命周期按该绑定执行。

## 4. 口令

| 口令 | 行为 |
| --- | --- |
| 装配能力 | 对照契约+参考目录+现清单 → 安装宿主侧 → **写 `{workroot}/capabilities/`** |
| 接受降级 / 暂不装 | 该槽 → `degraded` + `accepted=日期`；档案索引同步；不假装已装 |
| 体检能力 | **能力**只改 `{workroot}/capabilities/`；**技能**可改包内 `skills/`（HITL） |

## 5. 业务建议（收尾 · 至多 1 条）

**可提**（满足 ≥1）：本步因缺槽走了契约降级且影响定稿/评审/交付证据；同会话或近 2 战役同槽反复降级；清单状态与实机明显不符；步骤必开技能不够用且有返工/门失败证据。

**禁提**：无上列证据；同会话同类已提过；把建议写成缺陷或完成阻碍冒充。

文案：`{对象}：{现象} → 说装配能力|体检能力`。写入收尾「能力/技能建议」；无则写「无」。

## 6. 安全

无密钥入库；宿主配置仅指针。高风险槽（缺陷写回等）装配须显式确认。

## 7. 外部工具/浏览器生命周期

- 默认不预启动；仅竞品/页面取证或原型实走时按需拉起；结束后按绑定退程。
- 复用他轨实例时按该绑定生命周期执行。
- 共享可写状态只一个写会话；写需隔离，否则串行。
