# 绑定：browser-automation

> 仅当清单启用本槽且需要端口/server/profile 时保留本文件。  
> **SSOT**：本文件；`env-baseline.md` §8 只索引到 `{workroot}/capabilities/`。  
> MCP/Skill **安装**在各 agent 宿主本地/用户级配置；此处只记标识与指针（无密钥）。  
> **选用/退程**：`rules/capabilities/instance-discipline.md` §7 + `rules/special/multi-agent-output.md` §2.2。

| 项 | 值 |
| --- | --- |
| kind | `{mcp｜skill-cli｜builtin}` |
| impl | `{如 chrome-devtools-mcp@x｜playwright-mcp｜ego-browser｜…}` |
| 优先 server/skill | `{当前项目默认键；以 agent 已挂载为准}` |
| debugPort | `{CDP 端口；skill-cli/自管则可删}` |
| userDataDir | `{专用 profile；禁与日常浏览器共用}` |
| browserUrl | `http://127.0.0.1:{debugPort}`（有端口时） |
| 拉起命令（按需） | `{仅 mcp+debugPort 时；只替换端口与 profile}` |
| 退程命令（任务链结束） | `{结束本套调试进程；只替换端口与 profile；关 tab 不够}` |
| 配置入口 | `{各 agent 宿主用户级路径类型 + 键；禁项目内 mcp 作规范入口}` |
| 能力面核对 | navigate / snapshot / network：`{具备｜缺哪些→降级说明}` |

> **生命周期**：默认不预启动；按需「拉起命令」；任务链结束「退程命令」。并行只用下表已登记隔离套；优先套占用时用表内已挂载空闲套并记 `browser_mcp=`；未登记停问。只读+独立会话/路由或独占实例可并行；写需独立 profile/context、账号/数据/写域隔离，否则串行。

### 多套库存（按需）

| # | 套键 | server/skill | profile | debugPort | 备注 |
| ---: | --- | --- | --- | ---: | --- |
| 1 | | | | | 本项目优先 |
| 2 | | | | | 备用 |
