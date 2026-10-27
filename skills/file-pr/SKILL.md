---
name: file-pr
description: File a pull request or GitLab merge request. Use when the user asks to file, open, or create a PR or MR.
---

# File PR

Works on GitHub and GitLab. Detect the forge and get the commands from the
`pr-forge` skill.

Before filing, check whether a PR for this branch already exists. Review the
diff locally against the base branch (usually `origin/main`) to make sure its
contents match the goal.

## Language

Write the title and description in the repository's language. Look at its
README, recent merged PRs, and the template. A French repository gets a French
description. Keep code identifiers, commands, and Conventional Commit types
as they are.

## Title

PR titles usually become commit messages, so follow the repository's title
conventions (often Conventional Commits). Look at recently merged PRs and Git
history for examples. Prefer a concise, human-readable title that explains why
the change matters:

BAD

> ❌ perf(server): negotiate permessage-deflate on the websocket

GOOD

> ✅ perf(server): cut websocket frame size by 70%+ with gzipping

## Description

Pick the format in this order. The first that applies wins.

1. **Repository template.** If the repo has
   `.gitlab/merge_request_templates/Default.md`,
   `.github/PULL_REQUEST_TEMPLATE.md`, or PR rules in `CONTRIBUTING.md`, fill
   that template. Keep its headings and checklist. Tick a box only when you
   checked it in this session. Drop nothing the template asks for: write "N/A"
   and a reason instead.
2. **Full format.** Use the 9-section structure from the `pr-description`
   skill when any of these is true:
   - the diff is over about 300 changed lines or 10 files,
   - it changes a public API, schema, database migration, auth, security,
     personal data handling, CI, deployment, or dependencies,
   - it is a breaking change,
   - the user asks for a detailed description.
3. **Short format.** Everything else.

Even with a template or the full format, lead with the problem in plain
words, like the short format does. Open with a simple explanation of the problem
based on the user's original prompt, then briefly explain the solution. Do not
lead with an implementation inventory:

BAD

> ❌ Removed implicit workspace carry-over from every "new thread" entry point (cmd+n / cmd+shift+o, sidebar v1/v2 buttons, command palette). New threads inherit only the project from context; branch, worktree, and env mode always come from the configured defaults. Deleted buildContextualThreadOptions, startNewThreadInProjectFromContext, and the v1 sidebar's seed-context machinery.

GOOD

> ✅ My "new worktree" default was ignored when starting new threads on existing worktrees. Super unintuitive. Now your preferences always apply.

The short format is that: problem, solution, one line on how you tested it.
Nothing else unless a reviewer needs it.

## Attribution

If the harness gives an attribution line for PR descriptions, end with that
line and nothing else. Otherwise end with the public model name and harness
that made the changes, for example `Created with <model> in <harness>.`
Include subagent models that wrote part of the change. Use the model name the
harness reports. If model identity is unavailable, name the harness without
guessing a model.

## Filing

Before submission, check the title, description, quotes, and attachments for
secrets and private details. Student data, emails, tokens, and internal
hostnames other than the forge itself count.

Open a real PR rather than a draft so review bots and pipelines run. Default to
squash merge (on GitLab: let the project's `squash_option` decide, or pass
`--squash-before-merge` when it is optional) and delete the source branch on
merge.

On GitHub, if `gh pr create` fails because the GraphQL rate limit is used up,
open it through REST with
`gh api repos/<owner>/<repo>/pulls -f title=... -f head=... -f base=... -F body=@<file>`.

In T3 Code, register the new PR or MR with `link_pull_request` right after it
is created. If the user also asked to babysit it, continue with the
`babysit-pr` skill.

Do not post a follow-up PR comment unless it serves the user's request. When a
comment is needed, use the `leaving-pr-comments` skill.
