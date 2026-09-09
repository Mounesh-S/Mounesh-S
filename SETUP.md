# How this profile works

## The magic repo name

GitHub has one special rule: a **public** repo whose name is *exactly* your username
gets its `README.md` rendered on your profile page.

    github.com/Mounesh-S/Mounesh-S  ──▶  github.com/Mounesh-S

Nothing else is special. It's a normal repo.

## Layers (this is the design)

| Layer | What | Can it break? |
|---|---|---|
| **1 · Static** | Markdown, tables, the `yaml` whoami block | Never |
| **2 · Live CDN** | `skillicons.dev`, `shields.io`, `komarev.com`, `streak-stats.demolab.com`, `summary-cards` | If the host goes down |
| **3 · Self-hosted (SVG)** | `assets/op_*.svg`, `assets/metrics*.svg` — built by Actions, served from *this repo* | Never (GitHub serves them) |
| **3b · Self-written text** | the *World Economic Journal* activity feed — written as real markdown by `activity.yml` via `scripts/gen_activity_feed.py`, no image at all | Never — it's just text |
| **4 · AI-generated art** | `assets/emperors-log.png` (banner) — see `docs/ARTWORK.md` | Never (committed here), but see the copyright note below |

**Why the SVG layer matters.** The popular tutorials tell you to use
`github-readme-stats.vercel.app`, `github-profile-trophy.vercel.app` and
`github-readme-activity-graph.vercel.app`. All three have a history of returning
`402 Payment required` / `503 DEPLOYMENT_PAUSED` when their free Vercel quota runs
out. Layer 3 avoids that: a GitHub Action renders the same information into SVG
files **inside your repo**, so the images are served by GitHub itself.

**A note on the banner image.** `emperors-log.png` is an AI-generated
depiction of Luffy and the Thousand Sunny — recognizable copyrighted
character designs, even though AI-generated and disclosed as fan art
(`docs/ARTWORK.md`). It's included here at the profile owner's explicit
request; everything else in `assets/` is original vector art that doesn't
reproduce any copyrighted character design. A second such image
(`new-world.png`) was removed and replaced with a plain-text Luffy quote
near "The Voyage So Far".

## Token & permissions (already configured on this repo)

- `METRICS_TOKEN` — classic PAT, `public_repo` scope only, stored as a repo secret.
  Needed by `lowlighter/metrics` in `.github/workflows/metrics.yml`.
- **Settings → Actions → General → Workflow permissions** is set to
  **Read and write** so `activity.yml` and the `metrics.yml` `dynamic` job
  can commit straight to `main`.

## Schedule

| Workflow | Runs |
|---|---|
| `metrics.yml` | daily 02:00 UTC (07:30 IST) + on every push + manual |
| `activity.yml` | every 30 min + manual |

> GitHub disables scheduled workflows on repos with no activity for 60 days.
> One commit re-enables them.

## Things to personalise

- `README.md` — the `whoami` yaml block, the *current voyage* table, LinkedIn URL
- The typing animation `lines=` (use `%20` for space, `;` between lines)
- Theme colours: `9E2A2B` (crimson), `D4AF37` (gold), `38BDF8` (azure)
- `skillicons` set → full icon list at https://skillicons.dev
- Regenerate the Log Pose gauges / Ship's Log manually with
  `python3 scripts/gen_dynamic_logpose.py` (normally runs automatically as
  part of `metrics.yml`)
- Regenerate the activity feed manually with
  `python3 scripts/gen_activity_feed.py`

## Also worth doing (outside this repo)

- **Bio, location, company** — https://github.com/settings/profile
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

## Provenance docs

- `docs/ARTWORK.md` — where the AI-generated art came from and what was
  removed when a parallel redesign was merged back into this build.
- `docs/CONTENT_SOURCES.md` — where every résumé claim traces back to.
  Note: specific company-scale numbers documented there (tenant counts,
  invoice values, latency benchmarks) are **deliberately not published**
  in `README.md` itself, per an explicit earlier decision to keep
  employer-specific business metrics off the public profile.

## About the other files in this folder

Two separate, unrelated systems have appeared in this folder from other
sessions and were not deleted, since they may be real work worth keeping:

1. A Node.js build pipeline with Playwright tests and a GitHub Pages deploy
   (`site/`, `scripts/build_profile.cjs`, `scripts/verify_browser.cjs`,
   `themes/`, `index.html`, `package.json`, `node_modules/`, `test-results/`).
2. A standalone README preview tool (`readme-preview.html`,
   `scripts/preview_readme.py`, `assets/readme-preview.css`,
   `assets/github-markdown-css-LICENSE`, `docs/README_BRIEF.md`,
   `docs/README_VALIDATION.md`).

Neither is part of this system and nothing here depends on them. If you want
either gone, say so explicitly; deleting them isn't done automatically.
