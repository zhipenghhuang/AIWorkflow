# layout.yaml 模板（项目根）

> 复制到项目根为 `layout.yaml`；单包/多包二选一。`{workroot}` 由本文件解析，正文不再写死。
> 索引随工作区：单包 `docs/INDEX.md`；多包 `docs/development/INDEX.md` + 总览 `docs/INDEX.md`。

## 单包

```yaml
layout:
  mode: single
  version: 2
  inbound_root: inbound
  ssot_root: docs
  materials_root: docs/materials
  packages:
    wf-development:
      root: wf-development
      workroot: docs
      handoff_root: docs/handoff
      archive_root: docs/_archive
```

## 多包

```yaml
layout:
  mode: multi
  version: 2
  inbound_root: inbound
  ssot_root: docs
  materials_root: docs/materials
  packages:
    wf-product:
      root: wf/wf-product
      workroot: docs/product
      handoff_root: docs/product/handoff
      archive_root: docs/product/_archive
    wf-development:
      root: wf/wf-development
      workroot: docs/development
      handoff_root: docs/development/handoff
      archive_root: docs/development/_archive
    wf-testing:
      root: wf/wf-testing
      workroot: docs/testing
      handoff_root: docs/testing/handoff
      archive_root: docs/testing/_archive
```
