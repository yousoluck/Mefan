cd /mnt/d/pycharmprojects/Mefan/

安装的框架
1. agent-skill: ~/.claude/plugins/cache/addy-agent-skills/agent-skills/2e0dfbfb436e/skills
2. superpowers: ~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills
   1.  15 个 superpowers skill 中对二次开发真正高频的只有 7 个
      1. 高频（每次都该用）：
         - test-driven-development                                                                
         - verification-before-completion
         - systematic-debugging（出 bug 时）
         - requesting-code-review
         - finishing-a-development-branch
      2. 低频（大改动时）：
         - brainstorming（澄清时）
         - writing-plans                                                                          
      3. 几乎用不到（单 dev 串行场景）：
         - dispatching-parallel-agents
         - subagent-driven-development
         - executing-plans
         - using-git-worktrees
         - using-superpowers（bootstrap）
         - writing-skills（meta）  
3. openspec安装在项目下
   1. cd your-project
   2. openspec init
   3. D:\PycharmProjects\Mefan\.claude
4. gstack: ~/.claude//skills/gstack

其它安装
1. openwolf: npm install -g openwolf
   1. 用于.claude的记忆
   2. cd /project-directory
   3. openwolf init
   4. 所有的记录会保存在/project-directory/.wolf目录下
2. agent memory
   1. url： https://github.com/rohitg00/agentmemory#quick-start
   2. 安装
      1. NPX
         1. Terminal 1: start the server： 
            1. npx @agentmemory/agentmemory
         2. Terminal 2: seed sample data and see recall in action
            1. npx @agentmemory/agentmemory demo
               - demo seeds 3 realistic sessions (JWT auth, N+1 query fix, rate limiting) and runs semantic searches against them. You'll see it find "N+1 query fix" when you search "database performance optimization" — keyword matching can't do that.
               - http://localhost:3113 to watch the memory build live.
      2. NPM
         1. npm install -g @agentmemory/agentmemory
            1. # If you hit EACCES on macOS/Linux system Node installs, retry with:
            2. # sudo npm install -g @agentmemory/agentmemory
         2. agentmemory                    # start the server (same as the npx form)
            1. REST API     http://localhost:3111
            2. Viewer       http://localhost:3113
            3. Streams      ws://localhost:3112
            4. Engine       ws://localhost:49134
            5. iii console  (install: curl -fsSL https://install.iii.dev/iii/main/install.sh | VERSION=0.11.2 sh)
         3. agentmemory stop               # tear it down
         4. agentmemory remove             # uninstall everything we created
         5. agentmemory connect claude-code   # wire one agent
         6. agentmemory doctor             # interactive diagnostics + fix prompts
         7. npx skills add rohitg00/agentmemory -y   # install 15 native skills (8 you can invoke, 7 reference) so your agent knows when to use the tools
      3. claude code
         1. Install agentmemory: run `npx @agentmemory/agentmemory` in a separate terminal to start the memory server. Then run `/plugin marketplace add rohitg00/agentmemory` and `/plugin install agentmemory` — the plugin registers all 12 hooks, 15 skills, AND auto-wires the `@agentmemory/mcp` stdio server via its `.mcp.json`, so you get 53 MCP tools (memory_smart_search, memory_save, memory_sessions, memory_governance_delete, etc.) without any extra config step. Verify with `curl http://localhost:3111/agentmemory/health`. The real-time viewer is at http://localhost:3113.
      4. 安装路径在：
         1. ~/.npm/_npx
         2. 配置：~/.agentmemory/.env
         3. bin: ~/.nvm/versions/node/v22.22.2/bin/agentmemory
      5. UI
         1. http://localhost:3113
         2. 但CLAUDE会连接：http://localhost:3111
   3. 使用

需要复制mefan文档
1. .claude/agents
2. commands
3. hooks
4. skills
5. templates
6. project.conf
7. me-fan的测试脚本
   1. 测试plan（包含了每个阶段的产出物及对应的测试用例：自动脚本与人工需要做的测试）: .claude/iterations/mf-testplan.md
   2. 测试脚本：tests/test_stage0_*.py