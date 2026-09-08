# How this profile works

## The magic repo name

GitHub has one special rule: a **public** repo whose name is *exactly* your username
gets its `README.md` rendered on your profile page.

    github.com/Mounesh-S/Mounesh-S  ──▶  github.com/Mounesh-S

Nothing else is special. It's a normal repo.

## Three layers (this is the design)

| Layer | What | Can it break? |
|---|---|---|
| **1 · Static** | Markdown, tables, the `yaml` whoami block | Never |
| **2 · Live CDN** | `skillicons.dev`, `shields.io`, `komarev.com`, `streak-stats.demolab.com`, `summary-cards` | If the host goes down |
| **3 · Self-hosted** | `assets/*.svg` — built by Actions, served from *this repo* | Never (GitHub serves them) |
| **3b · Self-written text** | the *World Economic Journal* activity feed — written as real markdown by `activity.yml`, no image at all | Never — it's just text |

**Why this matters.** The popular tutorials tell you to use
`github-readme-stats.vercel.app`, `github-profile-trophy.vercel.app` and
`github-readme-activity-graph.vercel.app`. All three are currently returning
`402 Payment required` / `503 DEPLOYMENT_PAUSED` — their free Vercel quota ran out.
Profiles built from those guides today show broken-image icons.

Layer 3 solves that: a GitHub Action renders the same information into SVG files
**inside your repo**, so the images are served by GitHub itself.

## Setup — 4 steps

### 1. Create the repo
```bash
gh auth switch --user Mounesh-S
gh repo create Mounesh-S --public --description "My GitHub profile" \
  --source . --remote origin --push
```
> Must be **public**, and it must be created under the `Mounesh-S` account.

### 2. Add the metrics token
`lowlighter/metrics` needs a token to read your stats.

1. https://github.com/settings/tokens → **Generate new token (classic)**
2. Scope: `public_repo` only. Expiry: 1 year.
3. Copy it → repo → **Settings ▸ Secrets and variables ▸ Actions ▸ New secret**
4. Name it exactly `METRICS_TOKEN`

### 3. Allow Actions to write
Repo → **Settings ▸ Actions ▸ General ▸ Workflow permissions**
→ select **Read and write permissions** → Save.
(`activity.yml` commits straight to `main`; without this it fails.)

### 4. Run them once
Repo → **Actions** tab → run **Metrics** and **Recent activity** via *Run workflow*.
They also run on every push and on a schedule after that.

After ~2 minutes the placeholder SVGs in `assets/` are replaced with real cards,
and the *World Economic Journal* section in `README.md` fills in with your last
5 GitHub events. `activity.yml` needs no secret — it only reads public events
and commits with the default `GITHUB_TOKEN`.

## Schedule

| Workflow | Runs |
|---|---|
| `metrics.yml` | daily 02:00 UTC (07:30 IST) + on push + manual |
| `activity.yml` | every 30 min + manual |

> GitHub disables scheduled workflows on repos with no activity for 60 days.
> One commit re-enables them.

## Things to personalise

- `README.md` — the `whoami` yaml block, the *current voyage* table, LinkedIn URL
- The typing animation `lines=` (use `%20` for space, `;` between lines)
- Theme colours: `9E2A2B` (crimson), `D4AF37` (gold), `38BDF8` (azure)
- `skillicons` set → full icon list at https://skillicons.dev

## Also worth doing (outside this repo)

- **Bio, location, company** — https://github.com/settings/profile (currently empty)
- **Pin 6 repos** — profile page ▸ *Customize your pins*. Pin originals, not forks.
- **Give every pinned repo** a one-line description and a real README.
- **Profile picture** — the default identicon reads as an abandoned account.
- **Achievements** — Settings ▸ Profile ▸ show Achievements.

## Migrating repos from `mounesh0711`

```bash
gh auth switch --user mounesh0711
gh api -X POST repos/mounesh0711/<repo>/transfer -f new_owner=Mounesh-S
```
Transfers keep stars, issues, and history, and leave a redirect behind.
Forks aren't worth transferring — just re-fork them.

## About the other files in this folder

A separate, more elaborate profile system (Node.js build pipeline, Playwright
tests, GitHub Pages deploy — `site/`, `scripts/`, `themes/`, `index.html`,
`package.json`, `node_modules/`, `docs/`, `test-results/`) appeared in this
folder from a different session. It was not deleted, since it may be real
work worth keeping — but it is **not** part of this system and nothing here
depends on it. If you want it gone, say so explicitly; deleting it isn't done
automatically.
