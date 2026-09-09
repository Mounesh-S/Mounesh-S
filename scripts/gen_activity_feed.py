"""Writes up to 5 distinct public GitHub events into README.md between the
START_SECTION/END_SECTION markers, replacing jamesgeorge007/github-activity-readme
(which only ever recognizes PR/Issue/IssueComment/Release events -- a hardcoded
check in its own source -- and this account's real activity is mostly forks,
discussions, and similar event types it can't see at all).

Uses only the public Events API with the default GITHUB_TOKEN; no extra scope.
Run from the repo root: python3 scripts/gen_activity_feed.py
"""
import json
import os
import pathlib
import urllib.request

USER = "Mounesh-S"
README = pathlib.Path(__file__).resolve().parent.parent / "README.md"
START = "<!--START_SECTION:activity-->"
END = "<!--END_SECTION:activity-->"


def fetch_events():
    req = urllib.request.Request(f"https://api.github.com/users/{USER}/events/public?per_page=30")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fmt(e):
    t = e["type"]
    repo = e["repo"]["name"]
    link = f"[{repo}](https://github.com/{repo})"
    payload = e.get("payload", {})

    if t == "PushEvent":
        n = payload.get("distinct_size") or payload.get("size") or len(payload.get("commits", []))
        if n:
            return f"🔀 Pushed {n} commit{'s' if n != 1 else ''} to {link}"
        return f"🔀 Pushed to {link}"
    if t == "ForkEvent":
        return f"🍴 Forked {link}"
    if t == "WatchEvent":
        return f"⭐ Starred {link}"
    if t == "CreateEvent":
        ref_type = payload.get("ref_type", "repository")
        return f"🎉 Created {ref_type} in {link}" if ref_type != "repository" else f"🎉 Created {link}"
    if t == "PublicEvent":
        return f"📢 Made {link} public"
    if t == "MemberEvent":
        return f"👥 Added as a collaborator on {link}"
    if t == "DiscussionEvent":
        title = payload.get("discussion", {}).get("title", "")
        return f"💬 Started a discussion “{title}” in {link}" if title else f"💬 Started a discussion in {link}"
    if t == "IssuesEvent":
        action = payload.get("action", "opened")
        return f"📌 {action.capitalize()} an issue in {link}"
    if t == "IssueCommentEvent":
        return f"💭 Commented on an issue in {link}"
    if t == "PullRequestEvent":
        action = payload.get("action", "opened")
        return f"🔧 {action.capitalize()} a pull request in {link}"
    if t == "ReleaseEvent":
        return f"🚀 Published a release on {link}"
    return f"⛵ {t.replace('Event', '')} on {link}"


def activity_lines(events, limit=5):
    """Show distinct dated events, excluding this profile's automated push noise."""
    lines, seen = [], set()
    for event in events:
        if event["type"] == "PushEvent" and event["repo"]["name"] == f"{USER}/{USER}":
            continue
        message = fmt(event)
        date = event.get("created_at", "")[:10]
        key = (date, message)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"- {date} · {message}" if date else f"- {message}")
        if len(lines) >= limit:
            break
    return lines


def main():
    events = fetch_events()
    lines = activity_lines(events)
    if not lines:
        lines = ["- ⛵ *No recent public events beyond profile maintenance. More of my work is described in the dockyard above.*"]

    body = README.read_text()
    start_i = body.index(START) + len(START)
    end_i = body.index(END)
    new_body = body[:start_i] + "\n" + "\n".join(lines) + "\n" + body[end_i:]
    README.write_text(new_body)
    print(f"wrote {len(lines)} activity lines")


if __name__ == "__main__":
    main()
