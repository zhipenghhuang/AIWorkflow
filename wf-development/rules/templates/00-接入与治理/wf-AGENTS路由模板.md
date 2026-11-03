# 多包路由（`wf/AGENTS.md`）

> 多包项目根 `wf/AGENTS.md`；由 onboard 生成，已有则只补已装包行。
> 只列已装包；未装不列、不预置行。

## 已启用包

<!-- 按实际已装包保留；示例三行，未装删除 -->
- wf-product → wf/wf-product/AGENTS.md
- wf-development → wf/wf-development/AGENTS.md
- wf-testing → wf/wf-testing/AGENTS.md

## 意图→包

| 信号 | 包 |
| --- | --- |
| 产品缺陷评估 / 平台产品单 | wf-product |
| 修代码 / 开发缺陷流 | wf-development |
| 交平台 / 测试回归 | wf-testing |
| 发布=业务上线/UAT | wf-product |
| 发布=部署/回滚 | wf-development |
| 发布=准出报告 | wf-testing |
| 下一步/继续 | activeContext 当前包分节；无焦点则一问 |
| 提交/推送/交接 | 当前会话已绑定包；未开跑则一问 |

## 纪律

一次会话只跑一个包；各守写域。
