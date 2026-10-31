# 绑定：browser-automation

> 仅当清单启用本槽且需要端口/server/profile 时保留本文件。  
> **SSOT**：本文件；`环境基线.md` §8 只索引到 `测试/能力/`。  
> 宿主 MCP/Skill **安装**在用户级配置；此处只记标识与指针（无密钥）。

| 项 | 值 |
| --- | --- |
| kind | `{mcp｜skill-cli｜builtin}` |
| impl | `{如 chrome-devtools-mcp@x｜playwright-mcp｜ego-browser｜…}` |
| serverIdentifier | `{MCP server 键；skill-cli 可写 skill 名}` |
| 宿主标识 | `{cursor｜opencode｜…}` |
| debugPort | `{CDP 端口；skill-cli/自管则可删}` |
| userDataDir | `{专用 profile；禁与日常浏览器共用}` |
| browserUrl | `http://127.0.0.1:{debugPort}`（有端口时） |
| 拉起命令 | `{仅 mcp+debugPort 时；只替换端口与 profile}` |
| 配置入口 | `{宿主用户级路径类型 + 键；禁项目内 mcp 作规范入口}` |
| 能力面核对 | navigate / snapshot / network：`{具备｜缺哪些→降级说明}` |

### 多套并行（按需）

| # | 宿主 | 实例键 | server/skill | profile | debugPort | 备注 |
| ---: | --- | --- | --- | --- | ---: | --- |
| 1 | | | | | | |
