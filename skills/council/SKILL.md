---
name: council
description: Trigger this if the user says 'council'.
---

# Council

Bring in three delegates to help with the user's request, usually for review
or feedback. Use one strong model from each of three different providers, at
high reasoning effort. If the user names other council members for this
request, use those. Otherwise the council is:

| Seat | T3 provider instance | Model family | `target.options` |
| --- | --- | --- | --- |
| Claude Opus | `claudeAgent` | latest `claude-opus-*` | `{"effort":"high"}` |
| GPT Sol | `codex` | latest `gpt-*-sol` | `{"reasoningEffort":"high"}` |
| GLM | `opencode` | latest `glm-*` (via LiteLLM) | `{"variant":"high"}` |

In T3 Code, call `orchestrator_capabilities` and resolve each family to the
newest model ID it lists. Do not hardcode IDs. Pass the options explicitly:
Sol's default reasoning effort is `low`. Start one `delegate_task` per seat in
parallel (`role: "review"`, `mode: "async"`), and give each round a new
`clientRequestId`. Elsewhere, use the harness's subagent tools.

If a seat's provider instance is disabled or its family is missing, report it
instead of substituting. Ask the user whether to continue with two seats.

Give each delegate the request and relevant context. For review or feedback,
keep their work read-only. Collect their responses and summarize the useful
findings, disagreements, and recommended next steps.

For review or feedback, keep delegates read-only. Tell them: do not edit,
commit, push, comment on PRs/MRs, or start subagents.

For a code review, ask each delegate for a score out of 10.
Count each full review pass as one round.
A fresh review after fixes starts a new round.

If the work ends in a PR or MR, put the results in its description. Put this
section before the attribution line at the end. Translate the heading to the
description's language (`## Revue du conseil`, `Tours : 2`):

```markdown
## Council review

Rounds: 2

| Delegate | Round 1 | Round 2 |
| --- | --- | --- |
| Claude Opus | 7/10 | 9/10 |
| GPT Sol | 8/10 | 10/10 |
| GLM | 7/10 | 9/10 |
```

If a delegate gives no score, write `no score`. Do not invent one.
If the PR is open, edit the description (`pr-forge` has the command). Do not
post a comment for this.
If there is no PR, put the same results in the final reply only.

If you agree with their recommendations, make the changes and request a fresh
review after. Continue this process until all delegates are satisfied with the
outcome, for at most 3 rounds. After that, show the open disagreements and let
the user decide.

Do not let repeated reviews result in scope creep. It is your job to fight to
keep scope limited.
