# 子状态机 · defect-fix/fix

> **嵌套闭环**：长链路中的一小段。进入本区读一次；区内仍 **一次只开一个** step packet。

## 定位

- **包轨**：wf-development
- **父流程**：`rules/packets/defect-fix/_chain.md`
- **本区**：`fix` — 修复与门禁
- **出口**：进入下一子机 `rules/packets/defect-fix/_region-close.md`（关闭与收尾）

## 区内步骤

| step | 名称 | when | 步骤包 |
| --- | --- | --- | --- |
| `clarify` | 澄清/非缺陷回写 | `need_clarification` | `rules/packets/defect-fix/clarify.md` |
| `fix` | 红证与修复 | `implementation_required` | `rules/packets/defect-fix/fix.md` |
| `gates` | 门禁 | `has_code_change` | `rules/packets/defect-fix/gates.md` |
| `menu` | 总结菜单 | `implementation_required` | `rules/packets/defect-fix/menu.md` |

## 区内纪律

1. 本区是闭环：按表推进；`when` 跳过则不打开该步包。
2. 当前 `packet=` 必须是区内某一步；离开本区前心跳刷新到下一步/下一区。
3. 技能只按**当前步骤包 §6** 打开→执行→回包；不在本区预读全部 skill。
4. 不要为「看全貌」打开其他区的全部步骤包。
