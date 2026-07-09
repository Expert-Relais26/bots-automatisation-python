# Agent post-call N8N

Workflow N8N qui se déclenche automatiquement après chaque appel client, inspiré de la démonstration décrite par Henri :

1. Récupère le transcript de l'appel via **Fireflies**
2. Génère un email de suivi personnalisé (via **OpenRouter**) et le dépose en **brouillon dans Gmail**
3. Envoie un récap de coaching (note + axes d'amélioration) dans **Slack**

Le fichier `post-call-agent.json` est un export N8N standard, prêt à importer.

## Import dans N8N

1. Dans ton instance N8N (`https://automation-lead.app.n8n.cloud`), va dans **Workflows → Import from File**
2. Sélectionne `n8n/post-call-agent.json`
3. Le workflow apparaît avec 7 nœuds mais **sans credentials** (ils ne sont jamais exportés) : N8N va te demander de les associer avant de pouvoir activer le workflow

## Credentials à créer dans N8N (section Credentials)

| Nœud | Type de credential | Ce qu'il faut |
|---|---|---|
| Fireflies - Récupérer le transcript | Header Auth (`httpHeaderAuth`) | Header `Authorization: Bearer <clé API Fireflies>` |
| OpenRouter - Générer email + coaching | Header Auth (`httpHeaderAuth`) | Header `Authorization: Bearer <clé API OpenRouter>` |
| Gmail - Créer le brouillon | Gmail OAuth2 | Connexion OAuth de ta boîte Gmail |
| Slack - Récap coaching | Slack API | Bot token Slack + accès au channel cible |

Une fois les credentials créés, réaffecte-les sur chaque nœud correspondant (clic sur le nœud → champ Credential).

## Configurer le déclencheur côté Fireflies

1. Active le workflow dans N8N pour obtenir l'URL du webhook (nœud "Webhook - Fin d'appel")
2. Dans Fireflies, section **Integrations → Webhooks**, colle cette URL pour l'événement "Transcription completed"
3. Fireflies enverra `{ meetingId, eventType, ... }` ; le workflow récupère ensuite le transcript complet via l'API GraphQL Fireflies

## À vérifier / ajuster

- Le champ `sendTo` du brouillon Gmail utilise `organizer_email` renvoyé par Fireflies — vérifie qu'il correspond bien à l'adresse du client (pas à l'organisateur interne) selon ta configuration Fireflies, sinon adapte le mapping dans le nœud "Formater le transcript".
- Le nom exact des champs de la query GraphQL Fireflies (`sentences`, `summary`, `organizer_email`, ...) peut évoluer — vérifie contre la [doc API Fireflies](https://docs.fireflies.ai/) si le nœud renvoie une erreur.
- Le modèle OpenRouter est réglé sur `anthropic/claude-3.5-sonnet` ; change la valeur `model` dans le nœud "OpenRouter - Générer email + coaching" selon tes préférences/coûts.
- Le channel Slack cible n'est pas pré-rempli (`channelId.value` vide) — sélectionne-le dans le nœud après import.

## Sécurité

Aucune clé API n'est stockée dans ce fichier ni dans ce dépôt. Toutes les clés (Fireflies, OpenRouter, Gmail, Slack) doivent être saisies directement dans la section **Credentials** de N8N après import.
