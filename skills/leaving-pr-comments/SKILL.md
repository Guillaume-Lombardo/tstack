---
name: leaving-pr-comments
description: Use whenever leaving comments on GitHub or GitLab (PR/MR comments, review threads, replies).
---

# Leaving PR Comments

Prefix every agent-authored comment left on the user's behalf with this note
callout. GitHub and GitLab both render it.

```md
> [!NOTE]
> 🤖 **<model> responding on behalf of <user>**

Actual comment starts here.
```

Write the callout in the comment's language. In French:

```md
> [!NOTE]
> 🤖 **<model> répond au nom de <user>**

Le commentaire commence ici.
```

Use the language of the thread you reply in. For a new comment, use the
repository's language.

Use the verified public name of the model that wrote the comment. If the
harness does not expose a model name, use the harness name. Do not guess.
For `<user>`, use the name the user's instructions give. Otherwise use their
name or login on the forge.

Keep the callout's first two lines exactly as shown. `mr-wait` recognizes
`> [!NOTE]` followed by `> 🤖` as the agent's own comments and does not wake
you for them.

Before posting, check the entire comment, including quoted text and
attachments, for secrets and private details.

Keep the attribution inside the note and the actual reply outside it. The
context line must start with the robot emoji. Do not add a horizontal rule,
Setext underline, heading, signature footer, or a second attribution.

Apply this format to top-level PR/MR comments, inline review comments, replies
to bots or reviewers, and written explanations used before resolving or
dismissing feedback. Do not add it to PR descriptions, commit messages, or text
the user explicitly asked to post verbatim without attribution.

Write the comment itself in a direct style:

- Lead with the conclusion.
- Cite the relevant code, behavior, check, or reproduction.
- Keep it concise and avoid filler, canned thanks, or status narration.
- Distinguish verified facts from judgment.

Preview the final Markdown before posting so quoting and blank lines render as
shown. Post from a file (`-F body=@<file>` with `gh api` or `glab api`) rather
than an inline string, so newlines survive. After posting, verify that the
forge returned the comment or note URL or id. Resolve a review thread only
after its response was posted successfully.
