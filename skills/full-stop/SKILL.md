---
name: full-stop
description: Trigger this if the user says 'full stop'.
---

# Full Stop

Do the same work as `full-send`, but stop with the PR ready for the user to merge.
Never merge it.

Read [full-send](../full-send/SKILL.md) and follow its workflow, proof rules,
review, and babysitting steps. An explicit "full stop" request authorizes that
work without a separate "full send" request. That includes full-send's
testing permission. A "full stop" request is the permission for the test
methods Proof needs, even when a project file says to ask first, for
example before computer use. Use those methods directly. Its merge
permission does not apply. The overrides below take precedence.

## No merging

You may commit, push, rebase, fix conflicts, and use `--force-with-lease` on
this task's branch. Never merge, enable auto-merge, enter a merge queue, push
to the default branch, bypass branch protection, or delegate those actions.

Disable existing auto-merge and remove the PR from any merge queue before
work begins; check again before each push. Report these changes. If you
cannot prevent automatic merging, report the blocker before proceeding.

On GitLab, never run `glab mr merge`: it turns on auto-merge by default. If the
MR has `merge_when_pipeline_succeeds: true`, cancel it with the `pr-forge`
command. Do not pass `--auto-merge` to `glab mr create`.

## What still applies from full-send

- **Staying awake.** Never end a turn on "waiting" without an active wake
  mechanism, until the handoff.
- **Hosted CI out of budget.** Replay the CI jobs locally and use that as the
  CI part of the readiness check. Put the replay line in the PR description
  and say in the handoff that hosted CI did not run.
- **Cross-lot journey.** Run it on the PR branch, rebased on the latest
  default branch, before the handoff. There is no merge to wait for.
- **Clean up** with the `cleanup` skill before the handoff, but keep the PR
  branch and the worktree it lives in: the user still needs them.

## Stop at the gate

Use full-send's merge gate as the readiness check. Replace its merge and
final report steps with a handoff. Proof and review must cover the final diff;
recheck behavior changes and meaningful conflict fixes before handoff.

Fetch the target branch and check the live PR's head, base, checks, reviews,
and mergeability. Confirm it is open, not a draft, and not set to merge
without the user. If someone else merged it, report that instead.

- **Ready to merge:** the merge gate passes. Leave the PR open and unmerged.
- **Waiting for required approval:** only human approval remains. Confirm
  that this is the actual blocker.
- **Blocked:** explain what prevents readiness, what you tried, and what is
  needed. Follow full-send's rules for asking the user.

In T3 Code, call `unwatch_pull_request` before the handoff or a question.
Stop `mr-wait` or `pr-wait` if one is running.
Report the PR link, final head, verdict, proof, reviewer outcome, the journey
you replayed, what cleanup removed or kept, and remaining risks. State whether the PR is still open and unmerged.
