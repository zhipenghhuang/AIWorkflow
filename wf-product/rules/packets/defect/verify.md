# 步骤包 · defect/verify

> **运行时正文**：执行本步只读本文（+ §6 模板）。skills / 长文规则 / playbook / read-index 为维护素材，默认不打开。

## 1. 元信息

- **包轨**：产品轨
- **workflow**：`defect`
- **step**：`verify`（验证与关闭）
- **packet**：`rules/packets/defect/verify.md`
- **条件步** `when=needs_linked_update`：条件不满足则跳过本步（不打开本包）。
- 低风险档（L0/P0/T0）按 AGENTS 分级表可跳过未命中步骤；本包仅在执行本步时适用。

## 2. 本步目标

- **目标**：验证与关闭
- **产出**：验证结果 + 批末总结

## 3. 本步硬约束

- **继承开局卡**：本会话已读 `cold-start` 的八条硬约束仍全部生效（此处不复述，避免冲淡本步）。
- **本步只读**：本文 +（若 §6 列出）**一个模板**；禁止通读 rules / read-index / playbook / 未嵌入 skill。
- **完成声称**：本步有完成类 gate 时，无 `CLAIM: ALLOWED` 不得写完成/通过/可提测。
- **回执**：`reads=` 必须含本 packet 路径。

### 本步专有

- **单一出处**：通用联动/关闭规则以 `workflows/change.yaml` verify 为准；本步只保留缺陷平台差异。 运行 `verify/Invoke-Gate.ps1 -Mode change`（读 `.gate/wf-product/change.json`）；受理单联动清单未闭合、验证结果缺失 → 不得关闭。 未 READY → **保持受理单打开，不得进入 wrap/commit 冒充完成**；先补联动/证据或报阻塞。 按 `rules/defects/platform-collaboration.md` + `rules/templates/30-review-change/defect-writeup-template.md` ： 产品缺陷 → 受影响 AC/UAT 重验；开发完成新文档实施后验证；未验证不关单。 实现缺陷 → 产品侧回执后由开发/测试流程跟踪；产品侧不写「已修复」。 非问题/重复/信息不足 → 产品给依据；测试接受后关闭或转需求；未接受转产品复核。 下版 → 回池/路线图；不修 → 理由/接受人；退回开发 → 回执，缺陷状态由开发/测试跟踪。 验证通过后需再次回写平台（入口 writeback）更新状态/关闭；批末输出【产品缺陷协作总结】。

## 4. 本步门

- **GATE `change-closure`**：运行 `verify/Invoke-Gate.ps1 -Mode change`；§6 每项“已更新/不适用/待补”，待补有责任人/截止；未闭合不得关闭

## 5. 做法

### 本步动作清单

- **单一出处**：通用联动/关闭规则以 `workflows/change.yaml` verify 为准。
- 本步只保留缺陷平台差异。 运行 `verify/Invoke-Gate.ps1 -Mode change`（读 `.gate/wf-product/change.json`）。
- 受理单联动清单未闭合、验证结果缺失 → 不得关闭。 未 READY → **保持受理单打开，不得进入 wrap/commit 冒充完成**。
- 先补联动/证据或报阻塞。 按 `rules/defects/platform-collaboration.md` + `rules/templates/30-review-change/defect-writeup-template.md` ： 产品缺陷 → 受影响 AC/UAT 重验。
- 开发完成新文档实施后验证。
- 未验证不关单。 实现缺陷 → 产品侧回执后由开发/测试流程跟踪。
- 产品侧不写「已修复」。 非问题/重复/信息不足 → 产品给依据。
- 测试接受后关闭或转需求。
- 未接受转产品复核。 下版 → 回池/路线图。
- 不修 → 理由/接受人。
- 退回开发 → 回执，缺陷状态由开发/测试跟踪。 验证通过后需再次回写平台（入口 writeback）更新状态/关闭。
- 批末输出【产品缺陷协作总结】。

## 6. 打开/填写

- 运行时正文：仅本文件（开局卡已在会话开头读过）。
- 验证：`verify/Invoke-Gate.ps1`（完成声称加 `-Claim`）；有 UI 另按包内前端条。

## 7. 完成信号

- §2 产出已落盘。
- 本步 hitl 已确认，或 when 条件跳过。
- 若本步含完成类 gate：须 `CLAIM: ALLOWED` 后才可写完成态。
- wrap：收尾骨架字段齐全；commit：拟提交块经 `confirm_commit`。

## 8. 回执字段

```text
route=workflow:defect | step=verify | reads=rules/packets/defect/verify.md | skills=embedded | claim=ALLOWED|DENIED|na | next=…
```

`reads=` 必须包含 `rules/packets/defect/verify.md`；对不上 = 未遵守读链。
