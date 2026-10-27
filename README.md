# tstack (Guillaume's fork)

Fork of [t3dotgg/tstack](https://github.com/t3dotgg/tstack). Branch `guillaume`
holds the changes. `upstream` is Theo's repo:
`git fetch upstream && git rebase upstream/main` to take his updates.

What this fork changes:

- GitHub **and** GitLab, self-hosted included. New `pr-forge` skill maps every
  `gh` command to `glab`, and `babysit-pr/scripts/mr-wait` is the GitLab twin of
  `pr-wait`.
- `file-pr` writes in the repo's language and picks the description format:
  repo template, else the 9-section `pr-description` format for large or risky
  changes, else the short tstack format.
- `council` seats Claude Opus, GPT Sol, and GLM (OpenCode), with explicit
  effort. `sol-loop` runs Sol at `high` (its default is `low`).
- `leaving-pr-comments` signs in French or English, with the name from your
  instructions.
- `full-send` runs containers on the host your instructions name.

Personal settings (forge hosts, logins, signature name, container host) live
in `~/.codex/AGENTS.md`, not in this repo.

The agent skills I use every day, cleaned up so anyone can use them. They work
in Claude Code and Codex. Some use [T3 Code](https://github.com/pingdotgg/t3code)
features when they are available and fall back to native tools when they are
not.

## Skills

| Skill | Say | What it does |
|---|---|---|
| `full-send` | "full send" | Takes a change to a merged PR with nobody watching: proves it, reviews it, files it, babysits it, merges it. |
| `full-stop` | "full stop" | Same as `full-send`, but stops when the PR is ready for you to merge. |
| `council` | "council" | Gets review from three models from different providers, and loops until they agree. |
| `sol-loop` | "sol loop" | Reviews a change with GPT Sol in a loop until both agents agree. |
| `file-pr` | "file a PR" | Files a short PR that leads with the problem, not an inventory of changes. |
| `takeover` | "take over" | Finishes someone else's PR, branch, or agent thread, and keeps their credit. |
| `babysit-pr` | "babysit" | Watches a PR through CI and review bots, and fixes the real findings. |
| `modernize` | "modernize" | Rebases an old PR and decides if it should still exist. |
| `leaving-pr-comments` | (automatic) | Formats comments that an agent posts on your behalf. |
| `pr-forge` | (automatic) | GitHub/GitLab command map and GitLab merge rules. |

Some skills call others. Install the ones they need too:

- `full-send` uses `sol-loop`, `file-pr`, and `babysit-pr`.
- `full-stop` uses `full-send`.
- `takeover` uses `modernize`, `file-pr`, `babysit-pr`, and `leaving-pr-comments`.
- `file-pr`, `babysit-pr`, and `modernize` use `leaving-pr-comments`.
- `file-pr` uses `pr-description` (in `~/.claude/skills`, not in this repo).
- Every PR skill uses `pr-forge`.

## Install

Symlinks, so edits here apply at once:

```bash
for d in ~/Documents/tstack/skills/*/; do
  n=$(basename "$d")
  ln -sfn "$d" ~/.claude/skills/"$n"   # Claude Code
  ln -sfn "$d" ~/.codex/skills/"$n"    # Codex
done
```

## Requirements

- An authenticated [GitHub CLI](https://cli.github.com) (`gh`).
- An authenticated `glab` for GitLab repos.
- `python3` for `babysit-pr`'s `pr-wait` and `mr-wait` scripts.
- `council` and `sol-loop` need subagents on other providers' models. T3 Code
  does this with `delegate_task`. Otherwise you need a harness that can run
  those models.

## Make them yours

These are starting points. Edit them. Put personal settings, like which models
sit on your council, in your `CLAUDE.md` or `AGENTS.md`, so you can update the
skills without losing them.

## License

[MIT](LICENSE)
