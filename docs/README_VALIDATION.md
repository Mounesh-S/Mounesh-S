# README validation · 9 September 2026

- Rendered the actual README through GitHub's Markdown API.
- Inspected local browser screenshots in dark/light themes at 1024, 390, and 320 px.
- No page overflow, failed image decoding, HTTP errors, or JavaScript errors.
- All navigation anchors resolve; native expandable sections open.
- Both animated SVGs change between frames and stop with reduced motion enabled.
- Expanded preview: no axe WCAG 2 A/AA or WCAG 2.1 AA violations.
- Contribution calendar: one SVG cell per returned day, matching API totals,
  validated drawing bounds, and error responses rejected before writing.
- Activity: duplicate filtering, profile-maintenance filtering, date distinction,
  and five-entry limit checked with deterministic fixtures.
- Gallery build checked in a temporary copy: main README unchanged byte for byte.
- `git diff --check` passes.

The preview uses GitHub-rendered Markdown with a local GitHub-style page shell.
It does not establish that this revision has been published. The updated Actions
workflow still needs its first run on GitHub after publication.
