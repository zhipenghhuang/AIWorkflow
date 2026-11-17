# Materials Version README 模板

> 落盘：`docs/materials/{{ver}}/README.md`。给收件人的版本说明；不是交接清单。

# {{项目}} {{版本}} 文档集

- 版本 / 状态 / 更新时间
- 发布模式：默认覆盖最新（overwrite-latest）；仅显式保留历史时升 rev / `{ver}-r2`
- 本版范围（现行状态；完整包或仅补域）
- 阅读顺序（从 `00-overview` 起）
- 包含域：00-overview / 01-requirements / ...
- 不包含：草稿、过程、证据、密钥、PII；以及故意不收录项
- 来源：`IN-xxxx` / 工作区路径 / `generated`（溯源；正文须包内自洽）
- 缺失（三类分列，有「本包未完成」不得标完整）：
  - 产品缺口：
  - 故意不收录：
  - 本包未完成：
- 自包含：只发本 `{ver}/` 即可阅读；正文无未改写的工作区/`inbound` 路径
- 换迭代关账：关闭版须先覆盖刷新再标 superseded
