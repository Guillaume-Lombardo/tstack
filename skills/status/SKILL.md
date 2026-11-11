---
name: status
description: Fait le point sur un dépôt en une réponse courte, en lecture seule. À utiliser quand l'utilisateur demande « on en est où ? », « où en est ce projet ? », « état du projet », « status », « point d'avancement ».
---

# Status

Lecture seule : ne modifie rien, ne pousse rien, ne commente rien, ne relance
aucun thread. Si une action semble urgente, recommande-la à la fin.

## Collecter

Lance ce qui est indépendant en parallèle.

1. **Dépôt** : `git fetch --prune origin`, branche courante,
   `git status --short`, `git worktree list`, branches locales en avance sur
   leur upstream (`git branch -vv`), derniers commits de la branche par
   défaut (`git log --oneline -10 origin/<défaut>`).
2. **Roadmap** : le fichier trouvé comme dans `next-lot` (roadmap, plan,
   todo, checklist). Compter fait / en cours / reste ; nommer le prochain lot.
3. **PR/MR ouvertes** (voir `pr-forge`) :
   - GitHub : `gh pr list --state open --json number,title,headRefName,isDraft,reviewDecision,mergeStateStatus,statusCheckRollup,url`
   - GitLab : `glab mr list` puis, pour chacune,
     `detailed_merge_status` et `head_pipeline.status` via `glab api`.
   Pour chaque PR : CI, revue, conflits, ce qui la bloque.
4. **Threads T3 actifs** (en T3 Code) : `t3_thread_list` sur le projet,
   `settled: false`, avec `statuses: ["running","waiting","idle","failed",
   "interrupted"]`. Si `t3_environment_links` liste d'autres machines qui ont
   ce projet, interroge-les aussi (`environmentId`). Signale les threads
   `[orch]`, les threads en échec et ceux sans mise à jour depuis plus de
   45 minutes alors qu'ils sont `running`.
5. **Releases et déploiements** : `git describe --tags --abbrev=0`,
   `gh release list -L 3` / `glab release list`, et le dernier déploiement
   si le dépôt le documente (workflow de déploiement, `CHANGELOG.md`).

Si une source n'est pas accessible (pas de T3, forge injoignable), dis-le en
une ligne et continue.

## Répondre

En français, 20 lignes au plus, dans cet ordre :

```
**<dépôt>** — <branche par défaut> @ <sha court>, dernière release <tag> (<date>)

Roadmap : <n> faits / <n> en cours / <n> restants. Prochain : <lot>.
PR/MR :
| # | Titre | CI | Bloquant |
Threads actifs : <n> (<liens>, statut, dernière activité)
Local : <worktrees / branches non poussées / changements non commités>

**Prochaine action recommandée** : <une action, la plus utile>
```

Toutes les heures et dates sont en heure de Paris (`Europe/Paris`), jamais en
UTC : convertis les horodatages `…Z` ou epoch renvoyés par la forge, la CI et
T3 avant de les écrire (`HH:MM` aujourd'hui, `JJ/MM HH:MM` sinon). Une
dernière activité récente s'écrit plutôt en relatif (« il y a 12 min »).

Omets une section vide plutôt que d'écrire « aucun ». Ne raconte pas comment
tu as collecté.
