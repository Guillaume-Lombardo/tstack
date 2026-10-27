---
name: pr-forge
description: Command reference for pull requests on GitHub (gh) and merge requests on GitLab (glab). Read before running any PR/MR, CI, comment, or merge command, and whenever another skill says "PR" in a GitLab repo.
---

# PR forge

The other PR skills say "PR" and show `gh` commands. In a GitLab repo, read
"PR" as "merge request" (MR, `!123`), "checks" as "pipeline", and "review
threads" as "resolvable discussions", then use the GitLab column below.

## Detect the forge

Run `git remote get-url origin` (or the remote the PR lives on).

- `github.com` → GitHub, use `gh`.
- `gitlab.com`, a GitLab host named in the user's instructions, or any host
  listed by `glab auth status` → GitLab, use `glab`.
- Anything else → ask the user. Do not guess.

A PR/MR URL settles it too: `/pull/<n>` is GitHub, `/-/merge_requests/<n>`
is GitLab.

## Commands

`:id` is the current project in `glab api`. For another project, use
`projects/<url-encoded group%2Fname>` and `--hostname <host>`.

`glab` finds the project from the remote's host. If the remote uses an SSH
alias or an IP that differs from the host `glab` is logged in to, `:id` and
`glab mr create` fail to find the project. Do not rewrite the remote. Use
`projects/<encoded path>` with `--hostname`, `-R <url>`, or the MR URL.

Flags differ between glab versions (`glab --version`). Check
`glab <cmd> --help` before using a flag this table does not show.

| Task | GitHub | GitLab |
|---|---|---|
| PR for this branch | `gh pr list --head <branch> --state all` | `glab mr list --source-branch <branch> --all` |
| Read PR | `gh pr view <n> --json ...` | `glab api 'projects/:id/merge_requests/<iid>?include_diverged_commits_count=true'` |
| Create | `gh pr create --title ... --body-file <f> --base <b>` | `glab mr create --title ... --description "$(cat <f>)" --target-branch <b> --remove-source-branch --yes` |
| Use a template | `.github/PULL_REQUEST_TEMPLATE.md` | `.gitlab/merge_request_templates/<name>.md` |
| Edit description | `gh pr edit <n> --body-file <f>` | `glab mr update <iid> --description "$(cat <f>)"` |
| Attach a screenshot | drag into the web UI | `glab mr update <iid> --attach <png>` (glab 1.124+) |
| Checks | `gh pr checks <n>` | `glab ci status --branch <b>`; jobs: `glab api projects/:id/pipelines/<id>/jobs` |
| Failed job log | `gh run view <id> --log-failed` | `glab ci trace <job-id>` |
| Retry a flaky job | `gh run rerun <id> --failed` | `glab ci retry <job-id>` |
| Top-level comment | `gh pr comment <n> --body-file <f>` | `glab mr note <iid> -m "$(cat <f>)"` |
| Threads | GraphQL `reviewThreads` | `glab api 'projects/:id/merge_requests/<iid>/discussions?per_page=100'` |
| Reply in a thread | `gh api .../pulls/<n>/comments/<id>/replies -F body=@<f>` | `glab api -X POST projects/:id/merge_requests/<iid>/discussions/<did>/notes -F body=@<f>` |
| Resolve a thread | GraphQL `resolveReviewThread` | `glab api -X PUT projects/:id/merge_requests/<iid>/discussions/<did> -f resolved=true` |
| Disable auto-merge | `gh pr merge <n> --disable-auto` | `glab api -X POST projects/:id/merge_requests/<iid>/cancel_merge_when_pipeline_succeeds` |
| Merge | `gh pr merge <n> --squash --match-head-commit <sha>` | `glab mr merge <iid> --auto-merge=false --sha <sha> --yes` (see below) |
| Wait for events | `watch_pull_request` (T3) or `babysit-pr/scripts/pr-wait` | `watch_pull_request` (T3) or `babysit-pr/scripts/mr-wait` |

Unresolved threads on GitLab are discussions where a note has
`resolvable: true` and `resolved: false`.

## GitLab readiness

The MR's `detailed_merge_status` is the merge gate GitLab enforces. Only
`mergeable` means ready. The others tell you what to do:

- `ci_must_pass`, `ci_still_running`: wait for the pipeline.
- `discussions_not_resolved`: answer and resolve threads.
- `need_rebase`: rebase onto the target branch and force-push with lease.
- `conflict`: rebase and resolve conflicts.
- `not_approved`, `requested_changes`: a human must act. Ask the user.
- `draft_status`: mark ready only if the user asked you to file a real MR.
- `checking`, `unchecked`: read again in a moment.

Read the project's settings once: `glab api projects/:id` →
`merge_method`, `squash_option`,
`only_allow_merge_if_pipeline_succeeds`,
`only_allow_merge_if_all_discussions_are_resolved`. With `merge_method: ff`,
the branch must be rebased on the latest target before merging.

## Merging on GitLab

`glab mr merge` turns on auto-merge by default when a pipeline is running.
Always pass `--auto-merge=false` and `--sha <reviewed head>`. Let the
project's `squash_option` decide squashing. If it is `default_off` or
`default_on`, pass `--squash` to match the user's default (squash). Never skip
a pipeline, push to the target branch, or change project settings to get a
merge through.

## Rate limits

GitHub's GraphQL and REST limits are separate. See `babysit-pr`. A
self-hosted GitLab rarely has a rate limit to worry about, but poll it with
`mr-wait`, not with a loop of your own.
