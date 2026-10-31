# AGENTS.md

本仓库是 **AI Workflow 母版仓**：维护/发布三包，不是业务执行现场；只复制单个包到项目，不整仓复制。

1. 开工先读 `README.md`（维护约定）和 `activeContext.md`（当前状态/下一步）。
2. 改包后跑三包自检：产品/开发 `规则/tools/Test-Template.ps1`，测试 `规则/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`，技能 `check_skills.py --strict`。
3. 协作/公开面按 `.public/allowlist.txt` + deploy `surfaces.txt` 的 `split` 规则；根 `AGENTS.md`、`activeContext.md`、`.public/`、`extras/` 不进公开面。
4. 提交用本目录 `commit.bat` / `scripts/commit.ps1` 或 deploy `commit.bat`；人工双击仍交互确认；split 禁止裸推 `github`。
5. **AI 代跑提交（硬）**：用户口令「提交 / 提交推送」时必须走参数面（禁止管道/`Read-Host`、禁止仓内临时 stdin 文件）：
   - 先 `git status` + diff，按**一类一提交**拆批；每批写出有内容的 `-Message`（主题/版本 + 简述），**禁止**默认 `update 时间戳`。
   - 每批：`git add <本批路径>` → `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/commit.ps1 -Message '…' -StagedOnly -PushTarget <skip|both>`（只提交 → `skip`；提交推送 → `both`；也可用 `collab`/`public`）。
   - 也可用 deploy：`tools/commit.ps1 -Only <项目名> -Message '…' -StagedOnly -PushTarget …`（AI 参数必须带 `-Only`）。
   - 默认不更新服务器；用户明确要求部署时再加 `-UpdateServer`。临时文件只放 `%TEMP%`；`.commit-input*` / `.tmp_*` / `_parse_check*` 已 ignore。
6. 当前任务/版本/未提交状态只看 `activeContext.md`，历史看 `CHANGELOG.md`。

文档必须保持当前有效状态:{
    1.只描述当前存在的功能、流程、规则和约束。
    2.删除内容后直接移除，不增加“禁止xxx”“不要xxx”“已废弃xxx”等说明。
    3.不记录历史修改过程、原因、旧方案和取消内容。
    4.不为了防止误解而引入不存在的概念。
    5.修改结果以最终状态为准，保持文档简洁准确。
    6.结果输出都为结论性输出，不输出用户需求和改变；用户明确要求变更说明/版本对比/复盘/交接/培训时，可按时间线说明差异，但该说明不回流正式资产。
    7.以当前最终状态为唯一事实来源，禁止在正式资产中记录历史修改过程、废弃内容和变更原因。
    8.不要把修改方案写入正式文档。
    };

执行任务前：{
    1.先检查有没有错误前提、逻辑跳跃或信息缺失。
    2.不要迎合我，要独立判断。
    3.涉及数字、人物和结论时，尽量核实来源。
    4.如果我说得不对，直接指出来，并说明依据和风险。
    5.主动提醒我忽略的变量、成本和偏差。
    6.若我的想法不适配项目、不合适或不好，或你有更好的方案，须输出依据与主推（可附备选）告诉我；禁止静默照做劣解。
    }。

澄清原则：{
    先查可查的事实/文档/代码/数据，再问真正影响范围、验收、风险或不可逆决策的未知；
    一次只问一个关键问题，问到“能做出可验证的最小方案”即可，不以100%为目标；
    低风险/可逆/只读任务可边做边记假设，不把提问当流程；
    高风险/不可逆/对外承诺/权限资金迁移必须先确认。
    }