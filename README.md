# GrowthLoops Claude Skills

Open-source Claude Code skills for B2B SaaS growth marketing teams. Built by [Laura Beaulieu](https://www.linkedin.com/in/laurabeaulieu/), Founder of [GrowthLoops.io](https://growthloops.io).

These are the same skills I use to run marketing for B2B SaaS companies. Each one is designed to work with [Claude Code](https://claude.ai/code) as a slash command.

## What's Inside

| Skill | Command | What It Does |
|-------|---------|-------------|
| **Competitive Ads Extractor** | `/competitive-ads` | Scans Meta Ad Library, LinkedIn Ad Library, and Google Ads Transparency Center. Screenshots competitor ads, extracts messaging patterns, surfaces positioning gaps. |
| **Marketing Strategy Audit** | `/strategy-audit` | 18-exercise marketing strategy builder. ICP prioritization, positioning, revenue levers, big bet campaigns, KPOs, channel strategy, voice guide, tech stack audit, AI readiness assessment. |
| **Content Repurposer** | `/repurpose` | Takes one piece of content and restructures it for a different format. LinkedIn post to TikTok script. Blog to email. Maintains voice and persona targeting. |

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/Laura-Beaulieu/growthloops-claude-skills.git
cd growthloops-claude-skills
```

### 2. Configure your brand

Open `CLAUDE.md` and fill in your company details, personas, and voice rules. The skills reference this file to produce on-brand output.

If you skip this step, the skills will prompt you to fill in the required sections before running.

### 3. Run a skill

```bash
claude
```

Then use any skill as a slash command:

```
/competitive-ads full-scan "Competitor1, Competitor2, Competitor3"
/strategy-audit "Acme acme.com $10M ARR"
/repurpose "linkedin post" "60-sec tiktok script"
```

## How It Works

Each skill is a markdown file in `.claude/commands/`. When you run Claude Code in this directory, they become available as slash commands.

Every skill follows the same pattern:
1. **Setup** -- asks for your brand name, checks for voice rules and personas
2. **Research** -- uses web search and browser automation to gather data
3. **Analysis** -- structures findings into actionable frameworks
4. **Output** -- delivers formatted results with adaptation notes

The skills are brand-agnostic. Replace `[BRAND]` references by filling in your `CLAUDE.md`. They work for any B2B SaaS company.

## Requirements

- [Claude Code](https://claude.ai/code) (Anthropic's CLI)
- For competitive-ads: [Playwright MCP](https://github.com/anthropics/anthropic-tools/tree/main/computer-use/playwright-mcp) (for browser-based ad library scanning)

## About GrowthLoops

[GrowthLoops.io](https://growthloops.io) builds Human + AI GTM teams for B2B SaaS companies ($5M-$100M ARR). These skills are part of a larger agent system that runs content, competitive intel, outbound, and campaign planning.

If you want the full system deployed for your company: [Schedule a call](https://calendly.com/laura-beaulieu04)

## License

MIT. Use these however you want. If you build something cool with them, tag me on [LinkedIn](https://www.linkedin.com/in/laurabeaulieu/).
