---
name: skills-help
description: Rappelle les skills disponibles, quand les utiliser et les combinaisons courantes. À utiliser quand l'utilisateur demande « quels skills ? », « skills-help », « aide-mémoire », « rappelle-moi les skills », « qu'est-ce que je peux te demander ? ».
---

# Aide-mémoire des skills

Réponse courte, en tableaux, sans préambule.

## 1. Liste dynamique

Exécuter le script du dossier de ce skill (chemin absolu) :

```bash
python3 <dossier-de-ce-skill>/list_skills.py --width 90
```

Il lit le frontmatter de `~/.claude/skills/*/SKILL.md` et
`~/.codex/skills/*/SKILL.md`, résout les liens symboliques et fusionne les
doublons. Afficher son tableau tel quel. Si l'utilisateur demande un seul
outil ou une seule source, filtrer.

Le script ne voit pas les skills intégrés au harnais (`/code-review`,
`/simplify`, `/loop`, etc.) : ne pas les inventer, les mentionner en une ligne
seulement si l'utilisateur les demande.

## 2. Mots-clés déclencheurs

| Tu dis | Skill | Effet |
|---|---|---|
| « full send » | `full-send` | jusqu'à la PR fusionnée, sans surveillance |
| « full stop » | `full-stop` | idem, s'arrête avec la PR prête à fusionner |
| « sol loop » | `sol-loop` | revue par GPT Sol, 3 tours max |
| « council » | `council` | revue par trois modèles de fournisseurs différents |
| « réalise le lot suivant » | `next-lot` | prochain lot de la roadmap, en worktree |
| « on en est où ? » | `status` | point d'avancement, lecture seule |
| « nettoie tout » | `cleanup` | worktrees, branches, conteneurs, temporaires |
| « babysit » | `babysit-pr` | suit une PR jusqu'au vert |
| « modernize » | `modernize` | rebase et réévalue une vieille PR |
| « take over » | `takeover` | reprend la PR ou le thread de quelqu'un d'autre |

## 3. Combos courants

| Demande | Enchaînement |
|---|---|
| « réalise le lot suivant. sol-loop, full stop » | `next-lot` → `sol-loop` → `full-stop` (PR prête, non fusionnée) |
| « réalise le lot suivant. sol-loop, full send » | `next-lot` → `sol-loop` → `full-send` → parcours croisé → `cleanup` |
| « gère la PR. sol-loop, full send » | `sol-loop` → `babysit-pr` → fusion → `cleanup` |
| « on en est où ? » | `status` |
| « avance le dépôt jusqu'à <objectif> » | `repo-orchestrator` si installé : un seul orchestrateur par dépôt, délègue les lots, gère le budget |
| « traite les MR Renovate » | `renovate-daily` si installé |
| « optimise T3 » / « qu'est-ce qui marche ou pas ? » | `optimise-t3` si installé (coûteux en tokens) |
| « favorise codex » | modifie le routage : implémentation déléguée à Codex Sol (`reasoningEffort: high`) |

Ne lister dans la réponse que les combos dont les skills apparaissent dans la
liste dynamique.
