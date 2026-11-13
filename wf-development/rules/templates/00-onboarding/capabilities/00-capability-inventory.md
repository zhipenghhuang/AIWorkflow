# 能力清单（开发实例 SSOT）

> 包契约：`wf-development/capabilities/00-contract.md`；候选：`wf-development/capabilities/reference.md`。  
> 简单槽仅一行；复杂槽按需 `槽位/` · `绑定/`。  
> `kind`：`mcp`｜`skill-cli`｜`builtin`｜`none`。`status`：`available`｜`missing`｜`degraded`｜`prompted`｜`undecided`。  
> 「接受降级」→`degraded` 且备注 `accepted=YYYY-MM-DD`。硬/软触达见契约 §2。

| 能力名 | 启用 | kind | impl | status | 详情 | 绑定 | verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `git` | 是 | builtin | 宿主 git | undecided | — | — | |
| `defect-platform` | 未定 | | | undecided | — | — | |
| `browser-automation` | 未定 | | | undecided | — | 可写复用指针 | |

> 其它槽按启用追加。浏览器优先写复用指针，避免双份绑定。别名 `browser-mcp` 与 `browser-automation` 同行。
