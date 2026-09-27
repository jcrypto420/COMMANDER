# Claude Execution Packet: Hermes Money-Making Command Center

**Prepared for:** Claude Desktop / Claude Code  
**Owner:** Josh Stokesberry  
**Primary mission:** Set up Hermes Agent as a practical autonomous execution layer that helps Josh make money as passively and automatically as possible, while keeping costs low and avoiding context drift.

---

## 0. Read This First

You are helping Josh set up a real, executable AI command center.

Do not treat this as a vague home-lab project. The goal is not “cool infrastructure.” The goal is:

> Build a low-cost, private, increasingly autonomous agent system that moves Josh’s highest-value money-making projects forward every day.

The system should start simple, work immediately, and become more powerful over time.

Use this file as the source of truth until the repo has its own `CLAUDE.md`, `AGENTS.md`, `HERMES_SETUP.md`, and `TASK_QUEUE.md`.

---

## 1. Current Known Stack

Assume this unless Josh says otherwise:

- Raspberry Pi 4 Model B
- Hostname/device name: `commandcenter`
- Linux
- CasaOS installed
- Docker/Dockge likely installed
- Tailscale working
- SSH working
- 64 GB SanDisk Ultra microSD
- External 2 TB storage available
- Current/home-lab modules may include Immich, Vikunja, Uptime Kuma, and dashboard-style command center tools
- The Pi is the always-on lightweight runtime, not the final heavy AI machine

Important hardware constraint:

- The Raspberry Pi 4 should not be expected to run large local LLMs well.
- It can run tiny/local models for cheap, low-stakes tasks.
- Heavy local inference should eventually move to a Mac mini, custom PC, or GPU machine.
- Hermes can still run on the Pi as the operator/orchestrator.

---

## 2. Tool Roles

Use the tools this way:

```text
ChatGPT = architect / strategist / project manager
Claude Code = primary builder / file editor / terminal helper
Codex = second builder / reviewer / debugging assistant
GitHub = source of truth and task history
Raspberry Pi 4 = always-on runtime
Hermes Agent = autonomous execution operator
Ollama = local model runtime, first tiny models on Pi, stronger models later on better hardware
OpenRouter / Nous Portal / Venice / other APIs = cheap or fallback hosted inference
```

Do not overbuild. The first goal is a working Hermes `commander` profile with a safe task loop.

---

## 3. Hermes Capabilities to Exploit

Verify current docs before final implementation, but design around these capabilities:

- Hermes Agent can be installed and configured with provider/model settings.
- Hermes supports profiles. Each profile can have its own config, `.env`, `SOUL.md`, memories, sessions, skills, cron jobs, and state database.
- Hermes supports MCP for external tools such as GitHub, file systems, databases, browser stacks, and internal APIs.
- Hermes has built-in tools and can load MCP tools dynamically.
- Hermes supports provider routing, including cloud providers and self-hosted endpoints such as Ollama/vLLM.
- Hermes can be used with a portal/provider setup, OpenRouter-style model access, and potentially OpenAI-compatible APIs.
- Hermes should be given a limited tool surface first.
- Hermes must not be given broad destructive power until the repo, backups, and approval rules are working.

Reference links to verify:
- https://hermes-agent.nousresearch.com/docs/
- https://hermes-agent.nousresearch.com/docs/integrations/providers
- https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://github.com/NousResearch/hermes-agent
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/profiles.md

---

## 4. Core Objective

Build a repo named:

```text
command-center
```

This repo should let Claude Code, Codex, GitHub, terminal, and Hermes Agent all operate from the same compact project truth.

The repo must prioritize:

1. Hermes setup and safe execution
2. Money-making project execution
3. Low-cost model routing
4. Token efficiency
5. Project separation
6. Daily automated progress

---

## 5. Money-Making Priority Ladder

Hermes should optimize for cash flow, asset creation, business execution, and future optionality.

Priority order:

### Priority 1 — Command Center / Hermes Setup

Goal: get the operator working.

Outputs:
- Hermes installed
- `commander` profile created
- provider fallback strategy configured
- safe file/project access
- GitHub task loop
- daily execution loop
- cost logging
- approval rules

### Priority 2 — Fastest Practical Income / Career Defense

Goal: protect and increase income.

Outputs:
- resume/portfolio updates
- job leads
- targeted outreach drafts
- application tracking
- DeFi/data/Chainlink portfolio positioning
- consulting/freelance offer drafts
- follow-up reminders

### Priority 3 — Primoscapes

Goal: turn regenerative landscaping/native installations into actual revenue.

Outputs:
- service pages
- local lead lists
- bid response templates
- quote templates
- grant searches
- OKC municipal opportunity monitoring
- native plant/pricing database
- customer/project tracker
- strict separation between distinct Primoscapes sub-projects

Critical rule:
Do not mix separate Primoscapes sub-projects unless Josh explicitly says they are connected.

### Priority 4 — Weather Oracle MVP

Goal: finish a useful demo that can become a grant, Chainlink/public-good project, portfolio asset, or product.

Outputs:
- repo cleanup
- forecast source ingestion
- local news/weather scraping or API alternatives
- actuals comparison
- accuracy scoring
- frontend improvements
- README/demo documentation
- GitHub issues

### Priority 5 — DeFi / Chainlink / Research Dashboards

Goal: produce research, dashboards, and intelligence that can support jobs, consulting, investing, governance, or S&P-style portfolio value.

Outputs:
- Dune SQL drafts
- Chainlink service usage dashboards
- Aave/Chainlink overlap analysis
- Botto governance monitoring
- DeFi protocol notes
- yield/risk dashboards
- research memos with citations

### Priority 6 — Bad Boys / Joycat Creative Business

Goal: turn creative IP into products, Roblox items, memes, merch, comics, and campaigns.

Outputs:
- product backlog
- Roblox tasks
- merch concepts
- comic prompts
- brand consistency docs
- social calendar
- launch checklists

### Priority 7 — Sovereignty Stack Improvements

Goal: improve the private infrastructure only when it helps the money-making system.

Outputs:
- backup improvements
- monitoring
- knowledge vault
- local AI
- storage
- dashboards
- automation plumbing

---

## 6. Low-Cost Model Strategy

Josh wants to eventually use:

- Ollama
- Qwen
- GLM
- other local/open models
- OpenRouter
- Nous Portal
- Venice AI
- “Surplus” or other cheap/experimental model access sources
- any provider that reduces cost while keeping useful output quality

Design the system around a model router, not one fixed provider.

### Model Tiers

Create a file:

```text
MODEL_ROUTER.md
```

It should define these tiers:

```text
Tier 0 — Local / Nearly Free
Use for:
- summarization
- classification
- cleaning text
- extracting tasks
- drafting low-stakes first passes
- simple research organization
- repetitive formatting

Likely providers:
- Ollama on Pi for tiny models
- Ollama on future Mac mini/custom PC for stronger models

Candidate model families:
- Qwen small/medium
- GLM if available and supported
- Gemma
- Phi
- Llama small variants
- Hermes open models if feasible

Rule:
Never rely on Pi-hosted local models for high-stakes legal, financial, coding, or final strategic decisions.
```

```text
Tier 1 — Cheap Hosted
Use for:
- general agent work
- routine coding
- business drafts
- research synthesis
- brainstorming
- task planning

Candidate providers:
- OpenRouter cheap/free models
- Nous Portal
- Venice AI
- Hugging Face Inference Providers
- GitHub Models if available
- Together / Fireworks / Groq / DeepInfra / similar providers if cost-effective

Rule:
Prefer OpenAI-compatible APIs where possible to reduce integration lock-in.
```

```text
Tier 2 — Premium / Expensive
Use for:
- complex coding
- architecture decisions
- legal/financial-adjacent drafting
- final review before sending important materials
- debugging stuck issues
- strategic plans

Candidate providers:
- Claude
- GPT-class models
- premium OpenRouter models
- premium Nous Portal models

Rule:
Require cost awareness and avoid using premium models for bulk repetitive tasks.
```

---

## 7. Cost Control Rules

Create:

```text
COST_CONTROL.md
```

Include:

1. Default to the cheapest model capable of the task.
2. Use local/Ollama for bulk low-stakes work.
3. Use cheap hosted models for normal work.
4. Use premium models only for hard or high-value tasks.
5. Log model/provider usage where possible.
6. Track estimated daily spend.
7. Use small prompts and compact context.
8. Do not load unrelated project files.
9. Cache recurring summaries.
10. Create “briefing files” so agents read 1–3 compact files instead of entire chat histories.
11. Use human approval for purchases, subscriptions, deployments, credentials, and irreversible actions.

Suggested files:

```text
logs/model_usage.csv
logs/daily_progress.md
```

Suggested model usage CSV columns:

```text
date,task_id,project,provider,model,input_tokens,output_tokens,estimated_cost,outcome,next_action
```

---

## 8. Project Context Efficiency

The repo should prevent token waste.

Agents should follow:

```text
1. Read README.md first.
2. Read GOALS.md second.
3. Read NOW.md third.
4. Read only the active project file.
5. Read TASK_QUEUE.md only for the current task.
6. Do not summarize the whole repo unless asked.
7. Do not load unrelated project context.
8. Make small diffs.
9. Run verification after edits.
10. Ask Josh only when blocked by credentials, business judgment, money, legal/financial advice, or irreversible actions.
```

---

## 9. Safe Execution Rules

Hermes and Claude Code must obey:

```text
Allowed without asking:
- inspect files
- create project docs
- create scripts
- run read-only system inventory commands
- propose tasks
- draft issues
- create local files inside command-center
- run non-destructive verification commands

Ask before:
- sudo commands
- package installs
- deleting files
- modifying system services
- exposing ports publicly
- adding secrets
- creating paid accounts
- spending API credits
- pushing to GitHub
- deploying anything
- sending messages/emails
- making financial/legal claims as final advice
```

Never commit `.env`, API keys, tokens, private keys, wallet seeds, passwords, or personal documents.

---

## 10. Desired Repo Structure

Create this repo structure:

```text
command-center/
  README.md
  CLAUDE.md
  AGENTS.md
  GOALS.md
  NOW.md
  PROJECTS.md
  TASK_QUEUE.md
  HERMES_SETUP.md
  MODEL_ROUTER.md
  COST_CONTROL.md
  SECURITY.md
  MONEY_OPS.md
  LOCAL_MODELS.md
  PROVIDERS.md
  MCP_PLAN.md
  GITHUB_WORKFLOW.md
  .gitignore

  projects/
    career-income.md
    primoscapes.md
    weather-oracle.md
    defi-chainlink-research.md
    badboys-joycat.md
    sovereignty-stack.md

  configs/
    hermes_config_template.yaml
    hermes_env_template.env
    mcp_config_examples.yaml
    model_router_template.yaml

  scripts/
    pi_inventory.sh
    install_hermes.sh
    verify_hermes.sh
    install_ollama_optional.sh
    verify_ollama.sh
    backup_command_center.sh

  logs/
    .gitkeep
```

---

## 11. Initial Files: What They Should Say

### README.md

Purpose:
- explain what the repo is
- explain how Claude/Codex/Hermes should use it
- show first commands

### CLAUDE.md

Purpose:
- instructions specifically for Claude Code
- token efficiency rules
- command approval rules
- how to work with Josh

### AGENTS.md

Purpose:
- roles for Hermes, Claude, Codex, ChatGPT
- future sub-agent structure

### GOALS.md

Purpose:
- mission: make money with automation while preserving privacy and low cost
- short-term and long-term goals

### NOW.md

Purpose:
- current active focus
- next 3 tasks only
- current blockers
- today’s desired outcome

### TASK_QUEUE.md

Purpose:
- simple task board
- each task has project, priority, status, next action, approval required yes/no

### HERMES_SETUP.md

Purpose:
- exact install procedure
- current docs verification
- profile creation
- provider setup
- safe execution test

### MODEL_ROUTER.md

Purpose:
- model tiering
- local vs hosted
- cheap vs premium
- fallback logic

### MONEY_OPS.md

Purpose:
- define how Hermes finds, drafts, tracks, and advances money-making opportunities
- include daily “make money” loop

### LOCAL_MODELS.md

Purpose:
- Ollama plan
- Raspberry Pi limitations
- future Mac mini/custom PC migration
- model testing matrix

### PROVIDERS.md

Purpose:
- OpenRouter
- Nous Portal
- Venice AI
- Ollama
- Hugging Face Inference Providers
- GitHub Models
- other candidates such as Surplus
- base URLs/env var patterns where safe

### MCP_PLAN.md

Purpose:
- start with minimal MCP surface
- future GitHub/files/browser/database integrations
- never expose too much at once

---

## 12. Initial Daily Hermes Loop

Hermes should eventually run a daily command-center review.

Daily loop:

```text
1. Read NOW.md.
2. Review TASK_QUEUE.md.
3. Identify the highest-leverage money-making task.
4. Execute only if safe.
5. If not safe, draft the next action for Josh.
6. Update daily_progress.md.
7. Suggest one improvement to reduce cost or increase automation.
```

Daily question:

```text
What can I do today that most increases Josh’s income, assets, leverage, or optionality?
```

---

## 13. First Safe Hermes Task

After install, the first Hermes task should be:

```text
Read README.md, GOALS.md, NOW.md, PROJECTS.md, TASK_QUEUE.md, MODEL_ROUTER.md, and SECURITY.md.

Summarize:
1. The current mission.
2. The top three tasks.
3. The cheapest model/provider strategy.
4. Any blockers.

Do not edit files yet.
Do not run shell commands.
```

Second Hermes task:

```text
Inspect only the command-center repo. Propose the smallest safe change that improves Hermes setup reliability. Do not edit files until approved.
```

Third Hermes task:

```text
Create or update TASK_QUEUE.md with the first five implementation tasks for Command Center setup. Do not touch unrelated project files.
```

---

## 14. Claude Code Master Prompt

Paste this into Claude Code from inside the empty `command-center` repo.

```text
You are Claude Code helping Josh build his AI Command Center.

Your immediate job is to create a simple executable repo that lets Claude Code, Codex, GitHub, terminal, and Hermes Agent work together efficiently.

Primary mission:
Set up Hermes Agent as a safe autonomous operator that helps Josh make money as passively/automatically as possible while minimizing token/API costs.

Current hardware/context:
- Raspberry Pi 4 Model B named commandcenter
- Linux
- CasaOS
- Docker/Dockge likely present
- SSH and Tailscale working
- 64 GB microSD
- External 2 TB storage
- The Pi should be a lightweight always-on orchestrator, not the final heavy local LLM box

Important strategy:
- Start with one Hermes profile: commander
- Do not create multiple sub-agents yet
- Use GitHub/repo files as source of truth
- Add local/Ollama model support as a planned tier, but do not force heavy local inference on the Pi
- Design for cheap model routing across Ollama, OpenRouter, Nous Portal, Venice AI, Hugging Face Inference Providers, GitHub Models, and other low-cost OpenAI-compatible providers
- Keep premium models for hard/high-value tasks only
- Use cost logging and daily spend awareness
- Use minimal context loading to reduce token spend

Money-making priorities:
1. Command Center / Hermes setup
2. Career/income defense and portfolio leverage
3. Primoscapes revenue, bids, grants, leads
4. Weather Oracle MVP
5. DeFi / Chainlink / research dashboards
6. Bad Boys / Joycat creative business
7. Sovereignty Stack improvements that support the above

Critical Primoscapes rule:
Keep distinct Primoscapes sub-projects strictly separated. Do not merge recommendations or context between them unless Josh explicitly says they are connected.

Create the following repo structure:
- README.md
- CLAUDE.md
- AGENTS.md
- GOALS.md
- NOW.md
- PROJECTS.md
- TASK_QUEUE.md
- HERMES_SETUP.md
- MODEL_ROUTER.md
- COST_CONTROL.md
- SECURITY.md
- MONEY_OPS.md
- LOCAL_MODELS.md
- PROVIDERS.md
- MCP_PLAN.md
- GITHUB_WORKFLOW.md
- .gitignore
- projects/career-income.md
- projects/primoscapes.md
- projects/weather-oracle.md
- projects/defi-chainlink-research.md
- projects/badboys-joycat.md
- projects/sovereignty-stack.md
- configs/hermes_config_template.yaml
- configs/hermes_env_template.env
- configs/mcp_config_examples.yaml
- configs/model_router_template.yaml
- scripts/pi_inventory.sh
- scripts/install_hermes.sh
- scripts/verify_hermes.sh
- scripts/install_ollama_optional.sh
- scripts/verify_ollama.sh
- scripts/backup_command_center.sh
- logs/.gitkeep

Rules:
- Keep files compact and useful.
- Do not write giant essays.
- Do not invent API keys.
- Do not commit secrets.
- Do not run destructive commands.
- Do not install packages or use sudo without explicit approval.
- Scripts should be cautious, readable, and beginner-friendly.
- Any install script must verify docs/commands before running or clearly tell Josh to verify.
- Prefer OpenAI-compatible provider patterns where possible.
- Use .env templates for secrets.
- Include comments in scripts explaining what each step does.
- Add safety prompts before system-changing commands.

After creating the files, show:
1. The repo tree.
2. The exact first command Josh should run on the Raspberry Pi.
3. The exact first Hermes command or setup step.
4. Any assumptions that need confirmation.
5. The smallest next task to complete.
```

---

## 15. First Raspberry Pi Inventory Script Requirements

`scripts/pi_inventory.sh` should gather:

```text
hostname
OS version
architecture
RAM
disk space
external storage mounts
Docker version
CasaOS/Dockge presence if detectable
Tailscale status if installed
Git version
Python version
Node/npm version if present
current user
current directory
```

It should not change anything.

---

## 16. Install Strategy

Do not hardcode stale install instructions.

Claude should:

1. Open the current Hermes docs.
2. Verify the current install command.
3. Put the verified command in `HERMES_SETUP.md`.
4. Create `install_hermes.sh` as a cautious helper script.
5. Keep secrets in `configs/hermes_env_template.env`.
6. Create `commander` profile only after Josh approves the install path.

---

## 17. Provider Setup Strategy

Desired provider order for early testing:

```text
1. Nous Portal or OpenRouter for quickest working Hermes setup
2. Venice AI as OpenAI-compatible alternative
3. Ollama local for tiny low-cost tasks
4. Additional cheap providers after model router exists
```

Do not spend time perfecting every provider on day one.

Day one success means:
- Hermes runs
- `commander` profile exists
- one provider works
- one safe task completes
- token/cost strategy is documented

---

## 18. Ollama Strategy

Ollama should be included, but not allowed to derail setup.

On Pi:
- install only if Josh approves
- test tiny models first
- use only for low-stakes tasks
- record performance honestly

Future:
- move Ollama to Mac mini/custom PC
- run stronger Qwen/GLM/Gemma/Llama/Hermes models
- Hermes on Pi routes local inference to stronger machine

Create `LOCAL_MODELS.md` with:

```text
Phase A: Pi tiny-model test
Phase B: Mac mini/custom PC local AI server
Phase C: Hermes model router chooses local/cheap/premium based on task
```

---

## 19. Definition of Done for This Setup Phase

This phase is complete when:

```text
- command-center repo exists
- files above exist
- pi_inventory.sh has been run
- Hermes install path is verified
- Hermes is installed
- commander profile exists
- one model provider works
- model router strategy exists
- first safe Hermes task completes
- TASK_QUEUE.md has next tasks
- no secrets are committed
```

---

## 20. Do Not Do Yet

Do not do these until the base system is stable:

```text
- Kubernetes
- public web exposure
- broad Gmail access
- broad calendar access
- financial account integrations
- wallet/private key integrations
- autonomous spending
- autonomous job applications
- autonomous emails/messages
- multiple Hermes agents
- large local models on the Pi
- complicated Docker stack
- VPS migration
```

---

## 21. Final Instruction to Claude

Your job is not to impress Josh with complexity.

Your job is to create the smallest durable system that can:

```text
1. Run Hermes.
2. Execute safe bounded tasks.
3. Advance money-making projects.
4. Reduce token/model costs over time.
5. Keep context organized.
6. Avoid breaking the Pi.
```

Start by creating the repo files. Then stop and show Josh the repo tree and next command.
