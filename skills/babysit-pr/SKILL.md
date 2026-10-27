---
name: babysit-pr
description: Monitor a pull request or GitLab merge request through review and CI. Use when the user asks to monitor, watch, or babysit a PR or MR.
---

# Babysit PR

Works on GitHub PRs and GitLab MRs. Detect the forge and translate commands
with the `pr-forge` skill first.

Many repos have AI review bots. They're helpful, even if they are not always
right.

## Waiting

Never write your own watcher, polling loop, or `sleep` loop. Use one watcher
per PR: `watch_pull_request` in T3 Code, `pr-wait` (GitHub) or `mr-wait`
(GitLab) everywhere else. Never run both on the same PR. Every watcher on a
GitHub account shares one rate limit.

On GitLab, try `watch_pull_request` with the MR URL first. If T3 Code refuses
the host, or the watch stops because it cannot read the MR, use `mr-wait`.

### In T3 Code: `watch_pull_request`

Handle the existing checks and comments first. Then call
`watch_pull_request` and end your turn. T3 Code wakes you with a message when
a check fails, the required checks pass, someone comments or reviews, or the
branch conflicts.

- **Only the thread that owns the PR watches it.** If you are a delegated
  child task (a reviewer, a Sol round, any `delegate_task` child), never call
  `watch_pull_request`. The parent owns the PR. Do not watch PRs you are not
  working on.
- **A wake is news, not a merge decision.** Check the merge gate yourself.
- **Unwatch when you hand off.** A watched thread stays in Working and out of
  the user's inbox. When you stop (ready, blocked, or asking the user a question),
  call `unwatch_pull_request` first. A merge or close ends the watch on its
  own.
- **"Stopped watching, could not read it"** usually means GitHub's rate limit
  is used up. Run `gh api rate_limit --jq .resources.graphql` before you
  watch again. If `remaining` is near 0, wait for `reset` with one background
  command, then watch again. Never watch again in a tight loop.

### Everywhere else, GitHub: `pr-wait`

Wait with `scripts/pr-wait` from this skill's directory (use its absolute
path).

```bash
pr-wait <pr> [--repo owner/name] [--until ready|green|any-change]
```

It prints one line per real event. It exits 0 when the `--until` condition is
met or the PR merges, 1 when it needs you (a required check failed, conflicts,
unresolved threads, PR closed), and 2 on bad input.

- `ready` (default): required checks green, Greptile or Macroscope reviewed the
  head, and no unresolved threads. Use this to babysit.
- `green`: required checks only. Use it when the repo has no Greptile or
  Macroscope.
- `any-change`: exit on the first event.

### Everywhere else, GitLab: `mr-wait`

Wait with `scripts/mr-wait` from this skill's directory (use its absolute
path). It uses `glab api`, so glab's login is reused.

```bash
mr-wait <iid|url> [--repo group/name] [--hostname host] [--until ready|green|any-change]
```

Same exit codes as `pr-wait`. `ready` (default) means the head pipeline
succeeded, no discussion is unresolved, and `detailed_merge_status` is
`mergeable`. `green` means the head pipeline only. Notes that start with the
`leaving-pr-comments` callout are yours and are not reported. The user's own
comments are reported, marked `(you)`: treat them as review from the user.

### Running a watcher

In Claude Code, run `pr-wait` or `mr-wait` with the Monitor tool
(`timeout_ms: 3600000`), so each line wakes you. Without a monitor, run it as
one long command. It ends on its own.

Start it again after you push, after you handle an exit 1, and after a resume.
It remembers what it already reported, so nothing that arrived in between is
lost. If it says another pid already watches the PR, do not start a second one.
Kill the old one only if its events do not reach you.

With either watcher: when an event needs no action, end your turn without a
message. Never post or say "still waiting".

## GitHub rate limits

GitLab has no comparable limit on the self-hosted instance. This section is
GitHub only.

`gh pr create`, `gh pr view`, and `gh pr checks` use GraphQL. When GraphQL is
used up, the REST limit is separate and usually still has room. Use
`gh api repos/<owner>/<repo>/pulls/<n>` to read a PR, and
`gh api repos/<owner>/<repo>/commits/<sha>/check-runs` for checks.

## Reviews

Only act on checks and comments newer than the latest push. Verify every bot
finding against the source before changing code. Fix real findings and CI
failures, distinguish repository failures from infrastructure flakes, and reply
with a written reason when dismissing false positives.

If the repo has `.macroscope/check-run-agents/*.md`, read those rules before you
reply to a Macroscope finding. Its findings cite them.

On GitLab there is often no review bot. Findings come from the pipeline
(lint, types, tests, security jobs, CLA checks) and from people. Read failed
job logs with `glab ci trace <job-id>`. Retry a job only when its log shows an
infrastructure failure (runner lost, registry timeout), and say so. Renovate
MRs are not yours to babysit unless the user asks.

CodeRabbit is advisory. Treat its findings like any other finding, but never
wait for it and never hold a merge for it.

If a review bot leaves feedback you believe is not worth addressing, reply with
a written reason and resolve the comment. Use the `leaving-pr-comments` skill
for every comment posted on the user's behalf.

Screenshots and videos help as well, when you have a way to upload them. On
GitLab, `glab mr update <iid> --attach <file>` uploads them.

Keep the PR at the size the user's goal needs. Review loops tend to grow a
PR one cheap-looking fix at a time. Fix real bugs in the intended case.
Decline the rest with a written reason, and list them as follow-ups:
unneeded tests, guards for edge cases that do not matter, extra integration
or compatibility, and small performance costs. Prefer the fix that deletes or
narrows code.

## Base branch and merging

Keep an eye on changes to `main` and rebase when needed. `pr-wait` reports when
new base commits touch this PR's files, and when the PR becomes BEHIND or DIRTY.
`mr-wait` reports the same as `need_rebase` and `conflict`. With a fast-forward
merge method (`merge_method: ff`), GitLab refuses to merge until you rebase.
`watch_pull_request` reports conflicts only, so check for BEHIND or
`need_rebase` yourself before you call the PR ready.
If an overlapping PR makes this one obsolete, stop monitoring, report it to the
user, and ask before closing the PR unless closure was explicitly authorized.

If nothing has changed, stay quiet rather than posting filler comments. Stop
when `pr-wait` or `mr-wait` exits 0, or in T3 Code when the merge gate passes on
the latest head. Merge only when the user explicitly requested it;
otherwise report that the PR is ready. Right before a merge, run `git fetch` and
check the PR again. Never merge when it is BEHIND or DIRTY, or when base commits
that landed after the last green run touch this PR's files. Rebase, push, and
wait for green again.
