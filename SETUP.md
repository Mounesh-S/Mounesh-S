# Maintaining the profile

Edit `README.md` directly. This public repository has the same name as the
account, so GitHub renders its README at https://github.com/Mounesh-S.
No GitHub Pages deployment is needed.

## Artwork and motion

All README images live in `assets/`, including the Luffy banner and Gear 5
illustration. The ship/current animation and Haki accent use CSS inside
standalone SVG images, with a still state for reduced-motion preferences.
No JavaScript, external image service, or external game is required.

Regenerate the five decorative SVGs with:

```bash
python3 scripts/build_readme_assets.py
```

Artwork provenance is recorded in `docs/ARTWORK.md`; professional content and
metric scope are recorded in `docs/CONTENT_SOURCES.md`.

## Automatic updates

| Workflow | Schedule | Output |
| --- | --- | --- |
| Recent activity | Every 30 minutes or manual run | Distinct dated public events and `assets/contributions.svg` |
| Metrics | Daily at 02:00 UTC, pushes to main, or manual run | Overview and language cards, plus legacy metrics assets |

Recent activity uses the default `GITHUB_TOKEN`; Metrics uses the existing
`METRICS_TOKEN` secret. Keep the README activity markers intact. Public activity
excludes repetitive pushes to this profile repository. Contribution counts come
from GitHub's contribution calendar; they are distinct from commit-only counts.

The calendar can also be refreshed locally with an authenticated `gh` CLI:

```bash
python3 scripts/gen_contributions.py
python3 scripts/gen_activity_feed.py
```

If an update fails, inspect its Actions log. Previously committed assets stay
available, though their data will be stale. Publish the README and its referenced
assets together. Internal company work and private projects should remain
accurately labelled; single-run ingestion totals should retain that scope.
