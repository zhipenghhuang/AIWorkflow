# AGENTS.md

本仓库是 **AI Workflow 母版仓**：维护/发布三包，不是业务执行现场；只复制单个包到项目，不整仓复制。

1. 开工先读 `README.md`（维护约定）和 `activeContext.md`（当前状态/下一步）。
2. 改包后跑三包自检：产品/开发 `规则/tools/Test-Template.ps1`，测试 `规则/tools/Invoke-TestWorkflow.ps1 -Action ValidateTemplateRefs`，技能 `check_skills.py --strict`。
3. 协作/公开面按 `.public/allowlist.txt` + deploy `surfaces.txt` 的 `split` 规则；根 `AGENTS.md`、`activeContext.md`、`.public/`、`extras/` 不进公开面。
4. 提交用本目录 `commit.bat` / `scripts/commit.ps1` 或 deploy `commit.bat`；默认只提交，推送/公开导出单独确认。
5. **AI 代跑提交（硬）**：用户口令「提交 / 提交推送」时，必须先根据 `activeContext` / diff 写出有内容的提交信息（主题或版本 + 简述，可一行），再喂给 `commit.ps1` 的「提交信息」提示；**禁止**回车接受默认 `update yyyy-MM-dd HH:mm`。人工双击 bat 仍可用默认时间戳。
6. 当前任务/版本/未提交状态只看 `activeContext.md`，历史看 `CHANGELOG.md`。

文档必须保持当前有效状态:{
    1.只描述当前存在的功能、流程、规则和约束。
    2.删除内容后直接移除，不增加“禁止xxx”“不要xxx”“已废弃xxx”等说明。
    3.不记录历史修改过程、原因、旧方案和取消内容。
    4.不为了防止误解而引入不存在的概念。
    5.修改结果以最终状态为准，保持文档简洁准确。
    6.结果输出都为结论性输出，不输出用户需求和改变；
    7.以当前最终状态为唯一事实来源，禁止记录历史修改过程、废弃内容和变更原因。
    8.不要把修改方案写入正式文档。
    };

执行任务前：{
    1.先检查有没有错误前提、逻辑跳跃或信息缺失。
    2.不要迎合我，要独立判断。
    3.涉及数字、人物和结论时，尽量核实来源。
    4.如果我说得不对，直接指出来，并说明依据和风险。
    5.主动提醒我忽略的变量、成本和偏差。
    }。

澄清追问环：{
    请你在回答和执行任务前先向我提问：
    要求一次只问一个问题，请根据我的回答继续追问，
    直到你有95%的信心，
    完全理解我的真实需求和目标时，
    再给出最终方案。
    }