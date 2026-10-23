# Playbook · 页面原型（含 quick path）

> 只读本卡 + 当前步 YAML；技能按步读，**不要一次读两个技能全本**。
> 当前步：`prototype.context / ia / wireframe / visual / hi-fi / engineering / review / usability / handoff`。

## 1. 分级

| 级别 | 典型 | 路径 |
| --- | --- | --- |
| P0 单页/小改 | 1～2 页、已有设计系统/IA | context（简）→ wireframe/hi-fi 合并 → review |
| P1 功能流 | 3～7 页、需要 IA | context → ia → wireframe → hi-fi → review → handoff |
| P2 新产品/≥8 页 | 多角色/多流程/品牌级 | 全链 + 分页子代理 + 可用性走查 |

已有 IA/设计系统时允许从中间进入；无 IA 不直接高保真。P0 不强制 2～3 个视觉方向。

## 2. 读什么

| 步 | 必读 | 可选/按需 |
| --- | --- | --- |
| context | `prototype.yaml` + `技能/prototype-and-interaction/SKILL.md` §0 | PRD/计划/截图/品牌、设计简报/项目适配 |
| ia | 技能 §1 | 现有系统 IA |
| wireframe | 技能 §2 + 原型脚手架 | 设计评审模板 |
| visual | `技能/ui-visual-design-system/SKILL.md` + 门表 `confirm_design` | 设计系统策略/参考 |
| hi-fi | 两项技能相关节 + tokens | ui-generation（可选） |
| engineering | 工程化检查模板 | 脚本/链接检查 |
| review | 设计评审模板 + 评分卡 | 子代理（≥8 页） |
| usability | 可用性走查模板 | 真实用户（无则内部走查） |
| handoff | `开发交接模板.md` + 门表 `confirm_prototype` | PRD §14 |

## 3. 流程卡

1. **context**：读 PRD/计划/UAT/截图/品牌/约束；写清用户/任务/环境/设备/数据量/权限/术语/合规；设计策略/项目适配/交付等级；2～3 个参考（链接+日期）；设计原则 3～5 条。PRD 缺失 → 一句话说明，按用户输入继续，不阻塞。
2. **ia**：站点地图/导航/页面清单/关键流程/角色权限；每页目标/入口/主操作/出口；本期做/不做；覆盖矩阵初稿。
3. **wireframe**：先结构后视觉；每页覆盖空/加载/失败/成功/禁用/无权限；交互与文案就地标注。
4. **visual**：设计系统策略（复用/扩展/选一套）；2～3 个方向（P0 可 1 个），写清为什么适合本产品；推荐 1 个；design tokens；`confirm_design` 后才高保真。
5. **hi-fi**：静态 HTML/CSS（或项目现有栈），可点击；状态矩阵逐项落地；响应式/无障碍基础；≥8 页分页构建，禁并行写 `index.html`。
6. **engineering**：导航/路由/历史/返回/未保存提醒；数据/seed/重置；状态矩阵核对；WCAG 2.2 AA；缺项列阻断。
7. **review**：按清单 + 12 项评分卡；阻断项必须 2 分；需修回 hi-fi（同回合≤1）；≥8 页可按维度扇出。
8. **usability**：3～5 个关键任务走查；Nielsen 10；无真实用户标「内部走查」，不冒充用户测试。
9. **handoff**：按 `开发交接模板.md` 写设计意图/必须保留/可优化/未提供/需开发决策；组件/状态/交互/tokens/响应式/无障碍证据/验收对照；回填 PRD §14；`confirm_prototype` 后才交开发。

## 4. 红线

- 原型≠生产代码；不冒充品牌级视觉；不臆造品牌/用户数据。
- 未过设计评审不交开发；状态/响应式/无障碍不可省。
- 页面分片只写本页文件；共享 tokens/组件由编排定。

## 5. 输出

情境/IA/线框/高保真/tokens/工程化检查/评审/走查/交接。收尾按 `规则/模板/收尾骨架.md`。
