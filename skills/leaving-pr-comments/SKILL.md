---
name: leaving-pr-comments
description: Use whenever leaving comments on GitHub or GitLab (PR/MR comments, review threads, replies).
---

# Leaving PR Comments

Comments posted on the user's behalf read as the user's own. Never name a
model, a provider, an agent tool, or a harness, and never mention AI,
automation, or that an assistant wrote the comment. No robot emoji.

## Format

Start every comment with this hidden marker on its own line, then the
comment, then the signature:

```md
<!-- agent-reply -->
Actual comment starts here.

— <signature>
```

- `<signature>`: the signature the user's instructions give (for example in
  `AGENTS.md` or `CLAUDE.md`). Otherwise the user's first name, else their
  forge login. Nothing else on that line.
- The marker is invisible once rendered. `mr-wait` uses it to recognize your
  own comments and not wake you for them. Keep it exactly as shown, as the
  first line.

Write the comment in the language of the thread you reply in. For a new
comment, use the repository's language.

Before posting, check the entire comment, including quoted text and
attachments, for secrets and private details.

Do not add a heading, a horizontal rule, a callout, or a second signature.

Apply this format to top-level PR/MR comments, inline review comments, replies
to bots or reviewers, and written explanations used before resolving or
dismissing feedback. Do not add it to PR descriptions, commit messages, or text
the user explicitly asked to post verbatim.

## Style

- Lead with the conclusion.
- Cite the relevant code, behavior, check, or reproduction.
- Keep it concise and avoid filler, canned thanks, or status narration.
- Distinguish verified facts from judgment.

## Posting

Preview the final Markdown before posting so blank lines render as shown.
Post from a file (`-F body=@<file>` with `gh api` or `glab api`) rather than
an inline string, so newlines and the marker survive. After posting, verify
that the forge returned the comment or note URL or id. Resolve a review
thread only after its response was posted successfully.
