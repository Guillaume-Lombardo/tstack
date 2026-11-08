---
name: cleanup
description: Nettoie après un travail d'agent — worktrees, branches fusionnées, conteneurs de test, fichiers temporaires, processus de fond, tâches planifiées. À utiliser quand l'utilisateur dit « nettoie », « nettoie tout », « cleanup », « fais le ménage », et en fin de full-send, full-stop ou d'orchestration.
---

# Cleanup

Règle unique : **lister d'abord, ne supprimer que ce qui est prouvé**
fusionné, poussé, ou créé par cette session. Tout ce qui a des changements
non poussés est gardé et signalé.

Portée : le dépôt courant par défaut. « Nettoie tout » : tous les dépôts et
machines que la session (ou l'orchestration) a touchés.

La demande de l'utilisateur (ou full-send/full-stop) vaut permission pour
supprimer les éléments prouvés. Ne demande rien pour eux ; liste le reste.

## 1. Inventaire (lecture seule)

```bash
git fetch --prune origin
DEF=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
[ -n "$DEF" ] || DEF=$(git remote show origin | sed -n 's/.*HEAD branch: //p')
git worktree list --porcelain
git branch --format='%(refname:short)|%(upstream:short)|%(upstream:track)'
```

Pour chaque worktree (sauf le checkout principal) et chaque branche locale,
établir :

- **sale ?** `git -C <wt> status --porcelain` non vide → garder.
- **non poussée ?** pas d'upstream, ou `git rev-list --count @{u}..<b>` > 0
  → garder.
- **fusionnée ?** l'une de ces preuves :
  - `git merge-base --is-ancestor <b> origin/$DEF` ;
  - sa PR est fusionnée (squash ou rebase compris) et la tête locale est
    celle de la PR au moment du merge, ou un ancêtre :
    `gh pr list --head <b> --state merged --json number,headRefOid` /
    `glab mr list --source-branch <b> --merged` (voir `pr-forge`).
- **branche `t3/*`** : supprimable seulement si fusionnée selon ce qui
  précède, ou sans aucun commit hors de `origin/$DEF`, et si aucun thread T3
  non réglé ne l'utilise. Pour le savoir : `t3_thread_list` du projet
  (`settled: false`), puis `t3_worktree_list` avec le `threadId` de chacun
  pour lire sa branche. En cas de doute, garder.

Branches distantes : seulement celles des PR de l'utilisateur ou de ses
agents dont la PR est fusionnée et dont la branche source existe encore
(`git ls-remote --heads origin <b>`). Jamais la branche par défaut, une
branche protégée, ou la branche d'une PR ouverte ou d'un autre auteur.

Hors Git :

- **Conteneurs, volumes, images, réseaux de test** : ceux que la session a
  créés (projet compose de test, noms ou labels posés par la session, liste
  `.agent-tmp/session-resources.txt` si elle existe). Sur la machine que les
  instructions de l'utilisateur désignent pour Docker. Jamais un conteneur,
  volume ou réseau que l'inventaire de la machine marque comme prod, ni un
  conteneur qui tournait avant la session. `docker ps -a --format
  '{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Labels}}'`.
- **Fichiers temporaires** : `.agent-tmp/` des worktrees supprimés et du
  dépôt (sauf un état d'orchestration encore actif), fichiers et dossiers
  créés par la session dans `$TMPDIR` ou `/tmp` (clones temporaires, dumps,
  captures).
- **Processus de fond** lancés par la session : serveurs de dev, watchers
  (`pr-wait`, `mr-wait`, `gh pr checks --watch`), builds. `ps -o
  pid,etime,command -u "$USER"` ; ne tuer que ceux dont tu connais l'origine.
  En T3 : aperçus ouverts (`t3_preview_list`, `t3_preview_close`) et
  surveillances de PR finies (`unwatch_pull_request`).
- **Tâches planifiées** de la session (heartbeats d'orchestrateur, reprises
  différées) : `list_scheduled_tasks`, puis `delete_scheduled_task` si leur
  travail est fini.

## 2. Classer

Construire deux listes avant toute suppression :

| Élément | Preuve | Action |
|---|---|---|
| `../app-lot3` (worktree, `feat/lot-3`) | PR !41 fusionnée, tête identique | supprimer |
| `feat/essai` | 2 commits non poussés | garder |

## 3. Supprimer

Dans cet ordre, sans `--force` sauf preuve de fusion :

```bash
git worktree remove <chemin>           # échoue si sale : c'est voulu
git branch -d <b>                      # -D seulement si la PR est fusionnée (squash) et la tête identique
git push origin --delete <b>           # branches distantes prouvées seulement
git worktree prune
docker rm -f <conteneur>; docker volume rm <vol>; docker image rm <img>
rm -rf -- <chemins listés au point 2>  # jamais de motif large
kill <pid>
```

Si une commande refuse (worktree sale, branche non fusionnée), ne force pas :
passe l'élément dans « gardé ».

## 4. Rapport

Court : ce qui a été supprimé (nombre par type), ce qui est gardé avec la
raison (changements non poussés, PR ouverte, utilisé par un thread, origine
inconnue), et l'espace libéré si tu l'as mesuré.
