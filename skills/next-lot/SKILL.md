---
name: next-lot
description: Réalise le prochain lot non fait de la roadmap ou checklist du dépôt, de bout en bout. À utiliser quand l'utilisateur dit « réalise le lot suivant », « lot suivant », « fais le prochain lot », « next lot », souvent suivi de « sol-loop, full stop » ou « full send ».
---

# Lot suivant

Prendre le prochain lot de la roadmap, le cadrer, l'implémenter dans un
worktree isolé, le faire relire, et livrer une PR (ou MR, voir `pr-forge`).

Suite par défaut : `sol-loop` puis `full-stop`. Utiliser `full-send` à la
place seulement si l'utilisateur l'a dit (« full send »).

## 1. Vérifier que personne d'autre n'y travaille

- En T3 Code : `t3_thread_list` sur le projet (`statuses: ["running",
  "waiting", "idle"]`, `settled: false`). Si un thread dont le titre commence
  par `[orch]` pilote ce dépôt, ne lance rien : signale-le à l'utilisateur
  (lot, lien du thread) et arrête-toi, sauf si cet orchestrateur t'a lui-même
  délégué ce lot.
- PR ouvertes : `gh pr list --state open` / `glab mr list`. Si une PR couvre
  déjà le lot, reprends-la avec `takeover` au lieu d'en ouvrir une seconde.

## 2. Trouver la roadmap et le lot

Chercher dans cet ordre, le premier qui existe fait foi :

```bash
git fetch origin
git ls-files | grep -iE '(^|/)(roadmap|plan|todo|lots?|checklist)[^/]*\.md$'
```

Puis `AGENTS.md`, `CLAUDE.md`, `README.md` (section roadmap), et les issues
(`gh issue list --label roadmap`, `glab issue list --milestone <m>`) si la
roadmap y vit.

Le prochain lot est le premier, dans l'ordre du document, qui est non coché
(`- [ ]`, statut « à faire »), sans PR fusionnée, et dont les dépendances
sont faites. En cas de doute entre deux lots, prends le premier dans l'ordre
du document et dis-le. Si aucun lot n'est identifiable, demande à
l'utilisateur au lieu d'inventer.

## 3. Cadrer (court)

Écrire dans `.agent-tmp/lot-<id>.md` (non versionné) :

- objectif en une phrase, repris du texte du lot ;
- critères d'acceptation vérifiables (3 à 6) ;
- tests à ajouter et commandes de vérification (celles de la CI) ;
- hors périmètre ;
- fichiers probablement touchés.

Ce cadrage sert de brief pour l'implémentation, pour `sol-loop` et pour la
description de PR. Si le lot est trop gros pour une PR (plus de ~800 lignes
ou plusieurs sous-systèmes), découpe-le en sous-lots, note-les dans la
checklist et ne fais que le premier.

## 4. Implémenter dans un worktree isolé

Jamais sur le checkout principal.

```bash
git worktree add ../<dépôt>-<lot> -b feat/<lot-slug> origin/<branche-par-défaut>
```

En T3 Code, `delegate_task` avec `isolation: "worktree"` ou
`t3_thread_launch` avec `workspaceStrategy: {type: "worktree"}` crée le
worktree pour toi. Respecte les conventions de nommage de branche des
instructions de l'utilisateur.

Qui implémente :

- Si les instructions de l'utilisateur (AGENTS.md) disent de favoriser Codex,
  ou si l'utilisateur l'a dit (« favorise codex ») : délègue
  l'implémentation à Codex Sol, `delegate_task` avec `role:
  "implementation"`, `mode: "async"`, `isolation: "worktree"`,
  `target.options: {"reasoningEffort":"high"}` (toujours explicite : le
  défaut de Sol est `low`). Le brief contient le cadrage complet, les
  commandes de test, les règles machine des instructions, et : « Ne termine
  pas ton tour avant d'avoir livré un commit testé sur la branche, ou d'être
  bloqué avec un diagnostic. »
- Sinon, implémente toi-même dans le worktree.
- Jamais un modèle « lecture seule » (Terra, Luna, Haiku) pour écrire du code.

Pendant qu'un délégué travaille, termine ton tour : sa fin te réveille. Ne
dis jamais « j'attends le sous-agent » sans délégué async actif ou
`t3_background_wait` en cours.

À la fin, vérifie toi-même le résultat : diff, tests, critères
d'acceptation un par un.

## 5. Mettre à jour la checklist

Dans la même branche : coche le lot (ou passe son statut à « fait »), ajoute
le lien de la PR une fois créée, et note les sous-lots ou suites
découvertes. La fusion de la PR marque donc le lot comme fait.

## 6. Enchaîner

1. `sol-loop` sur le diff du lot (avec le cadrage comme intention).
2. `full-stop` (défaut) ou `full-send` (si demandé) : preuve, PR, suivi CI,
   parcours croisé, nettoyage.

## Rapport

En quelques lignes : lot traité, lien PR, critères d'acceptation et preuve,
tours de revue, ce qui reste dans la roadmap (prochain lot), décisions prises.
