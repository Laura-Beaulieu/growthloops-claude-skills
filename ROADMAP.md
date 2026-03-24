# GrowthLoops Claude Skills -- Build Roadmap

This is the working plan for new skills, integrations, and content drops. Updated each Thursday session.

---

## Live Skills (shipped)

| Skill | Status | Public Repo | Proof Point |
|-------|--------|-------------|-------------|
| `/competitive-ads` | Shipped 2026-03-23 | Yes | Augmentt scan: 7 competitors, 3 platforms, 20 screenshots |
| `/strategy-audit` | Shipped 2026-03-24 | Yes | -- |
| `/repurpose` | Shipped 2026-03-24 | Yes | -- |

---

## In Progress

### Creative Asset Generator (`/visual-kit`)
**Priority:** High -- next build (Thursday 3/27)
**Problem it solves:** Marketing teams without a designer need webinar thumbnails, YouTube thumbnails, LinkedIn ads, and email headers. Currently takes hours per asset. Should take seconds.
**How it works:** User provides a topic, event name, or campaign. Skill generates one visual concept and outputs it in multiple formats: webinar thumbnail (1200x628), YouTube thumbnail (1280x720), LinkedIn ad (1200x627), email header (600x200), Instagram story (1080x1920).
**Tools to explore:**
- Remotion (React-based image/video rendering)
- HTML/CSS-to-PNG pipeline (Claude Code generates markup, renders to image)
- AI image generation APIs
- Gamma, Canva API, or similar
**Content angle:** Film building a full webinar promo kit in real time. "One prompt. Five assets. Zero designer."

### Apify Content Scraper Skills
**Priority:** High -- second build
**Problem it solves:** Content optimization is guesswork without data. Apify scrapers pull real engagement data from TikTok, LinkedIn, websites, and competitors.
**Potential skills:**
- `/tiktok-scrape` -- Pull top-performing TikToks for a keyword/account. Feed into `/gl-tiktok` for data-driven script writing.
- `/site-crawl` -- Crawl a competitor's blog, landing pages, and messaging. Feed into `/competitive-ads` positioning analysis.
- `/social-scrape` -- Pull LinkedIn post engagement data for a company or thought leader. Feed into `/linkedin-intel`.
**Integration:** Apify has an API. Could build an MCP server so Claude Code talks to Apify directly.
**Content angle:** "How I scraped 10,000 TikToks to find the 3 patterns that actually work in B2B."

---

## Backlog -- Skills to Convert (private to public)

These exist in the private repo and need GrowthLoops-specific references replaced with [BRAND] framework. Ordered by public value and conversion effort.

| Skill | Effort | Public Value | Notes |
|-------|--------|-------------|-------|
| `/tiktok` | Medium | High | B2B TikTok script writer. Remove pillar/persona refs, replace with generic framework. |
| `/objection` | Medium | High | Objection handling coach. Replace 12-objection master list with generic B2B objections. Methodology is gold. |
| `/linkedin-intel` | Medium | High | Thought leader intelligence mining. Replace specific thought leader list with template. |
| `/qc` | Medium | Medium-High | 7-check quality control framework. Replace brand-specific checks with templates. |
| `/visual` | Medium | Medium-High | Creative brief generator. Replace GrowthLoops color palette/fonts with brand template. |
| `/ai-news` | Easy | Very High | Daily AI news brief for GTM operators. Nearly ready as-is. Just remove Laura references. |

---

## Backlog -- New Skills to Build

Ideas for net-new skills that don't exist yet.

| Skill Idea | Problem It Solves | Tools/Integrations |
|------------|-------------------|-------------------|
| `/webinar-kit` | Full webinar launch package: title, description, email sequence, social promo, slides outline, follow-up sequence | Could combine repurpose + email + visual-kit |
| `/ad-copy` | Generate platform-specific ad copy (LinkedIn, Meta, Google) from a positioning brief | Feed from competitive-ads insights |
| `/landing-page` | Generate landing page copy (headline, subhead, sections, CTA) from a campaign brief | Could output HTML or Webflow-ready copy |
| `/case-study` | Interview transcript or notes in, formatted case study out | Pairs with Fireflies MCP |
| `/seo-brief` | Keyword research + content brief for blog posts | Would need a keyword data source |
| `/email-sequence` | Full nurture or onboarding email sequence from a single brief | Could integrate with HubSpot when upgraded |
| `/social-calendar` | Weekly/monthly content calendar with topics mapped to personas and channels | Orchestrator skill |
| `/competitor-monitor` | Scheduled weekly scan of competitor changes (new pages, new ads, new messaging) | Apify + competitive-ads + cron |

---

## Integrations to Explore

| Tool | What It Enables | MCP Available? |
|------|----------------|---------------|
| **Apify** | TikTok scraping, website crawling, social data | API available, MCP could be built |
| **Remotion** | Programmatic image/video generation | npm package, runs locally |
| **HubSpot** | CRM data, email sequences, workflows | MCP available (read-only on free plan) |
| **Fireflies** | Meeting transcripts for case studies, objection mining | MCP available |
| **Playwright** | Browser automation for ad libraries, screenshots | MCP installed and working |
| **Facebook Ads Library** | Ad intelligence | MCP available (trypeggy) |
| **Canva** | Design asset generation | API available |
| **Webflow** | Landing page deployment | API available |

---

## Content Drop Schedule

Each skill release follows this pattern:
1. Build the skill
2. Run it on a real use case (client or self)
3. Film the demo / capture the output
4. Post: LinkedIn write-up + TikTok video + GitHub release
5. Link to public repo for downloads

| Drop | Skill | Content Angle | Target Date |
|------|-------|--------------|-------------|
| 1 | `/competitive-ads` | "I scanned 7 competitors across 3 ad platforms in 20 minutes" | Filmed 2026-03-24 |
| 2 | `/visual-kit` | "One prompt. Five assets. Zero designer." | 2026-03-27 |
| 3 | Apify integration | "I scraped 10,000 TikToks to find 3 patterns that work in B2B" | TBD |
| 4 | `/tiktok` (public) | "The Claude skill that writes my TikTok scripts" | TBD |
| 5 | `/ai-news` (public) | "How I stay ahead of AI news in 5 minutes a day" | TBD |
| 6 | `/objection` (public) | "Every sales objection has a fear underneath it. This skill finds it." | TBD |

---

## Principles

- **Build in public.** Every skill we ship is content.
- **Proof over theory.** Run it on a real use case before promoting it.
- **One visual moment, multiple formats.** Every build should produce assets for LinkedIn, TikTok, and GitHub.
- **Brand-agnostic by default.** Public skills use [BRAND] framework so anyone can use them.
- **GrowthLoops eats its own cooking.** We use these skills to run our own marketing. That's the proof.
