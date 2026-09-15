# MPG Assistant — Backend MVP (Django)

MVP du backend décrit dans le projet MPG Assistant (Étape 8 : Backend Django).
Implémente le flux RAG complet (Étape 5) sur un premier contenu réel et validé
(extraits publics de `Presentation_MPG_actualisée.pptx`).

## ⚠️ Ce que ce MVP est — et n'est pas

**Est** : une API REST fonctionnelle de bout en bout — question → recherche
dans une base de connaissances réelle → construction de contexte → (appel LLM
si clé API fournie) → réponse avec sources citées → mémoire de conversation →
journal des questions sans réponse.

**N'est pas** :
- Un système de recherche sémantique par embeddings (Étape 6/18) — la
  recherche actuelle est un matching par mots-clés simple, volontairement,
  car le volume de contenu réel est encore faible (une seule source). Voir
  `ai/services.py::_score` — **des faux positifs sont possibles** dès qu'un
  mot générique (ex. un nom de ville) apparaît dans plusieurs chunks. Ce
  point doit être calibré/amélioré avant tout usage réel avec les étudiants.
- Connecté à un vrai fournisseur LLM par défaut : sans `ANTHROPIC_API_KEY`
  dans `.env`, l'API répond quand même (mode dégradé) en affichant les
  passages qui auraient servi de contexte, pour permettre de tester le RAG
  sans dépendre d'une clé API.
- Une interface Web ou WhatsApp (Étapes 11 et 12, non commencées).
- Sécurisé pour la production (Phase 14 non traitée : pas de rate limiting
  avancé, pas de HTTPS, secret de dev par défaut, etc.)

## Installation

```bash
python -m venv venv
source venv/bin/activate       # Windows : venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# éditez .env : au minimum ANTHROPIC_API_KEY si vous voulez de vraies réponses générées

python manage.py migrate
python manage.py seed_knowledge     # charge le contenu public validé (Étape 4)
python manage.py createsuperuser    # pour accéder à /admin/ (mini back-office, Phase 13)
python manage.py runserver
```

## Utiliser l'API

```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Quelles sont les spécialités ouvertes à l'\''école ?"}'
```

Réponse (extrait) :
```json
{
  "session_id": "....",
  "reponse": "...",
  "sources": ["Présentation MPG actualisée — extraits publics"],
  "trouve_quelque_chose": true
}
```

Pour continuer la même conversation (mémoire courte, Étape 10), renvoyez le
`session_id` reçu dans l'appel suivant.

## Back-office (Phase 13, version minimale)

`http://127.0.0.1:8000/admin/` permet dès maintenant de :
- activer/désactiver des `Document` et `Chunk` ;
- consulter les `Conversation` et leurs `Message` ;
- consulter les `QuestionSansReponse` non traitées (utile pour la Phase 16 - pilote) ;
- gérer `FAQ` et `Contact` (vides pour l'instant — à peupler).

## Structure du projet (conforme à l'architecture validée, Étape 8)

```
mpg_assistant/
├── config/     # settings, urls racine
├── knowledge/  # Document, Chunk, FAQ, Contact + commande seed_knowledge
├── chat/       # Conversation, Message, QuestionSansReponse
├── ai/         # prompts.py (system prompt Étape 2) + services.py (RAG + appel LLM)
├── users/      # réservé aux comptes back-office (Phase 13) — utilise le User Django standard pour l'instant
└── api/        # ChatView (point d'entrée unique, commun Web/WhatsApp)
```

## Points ouverts / prochaines étapes recommandées

1. **Tester avec une vraie clé API Anthropic** pour valider la qualité réelle
   des réponses générées (actuellement seul le retrieval a été testé).
2. **Calibrer le seuil de pertinence et le scoring** (`ai/services.py`) — le
   matching par mots-clés produit des faux positifs sur des mots génériques
   (ex. "Nouakchott" fait remonter un chunk non pertinent pour une question
   hors périmètre). C'est le rôle de l'Étape 7 (prototype/calibration).
3. **Enrichir la base de connaissances** avec d'autres documents réels
   (règlement intérieur, procédures d'inscription, contacts) — le MVP ne
   contient volontairement qu'une seule source pour l'instant.
4. **Ajouter des tests Postman** (Étape 9) sur cette API, notamment les cas
   adversariaux (prompt injection, données personnelles) qui n'ont pas
   encore été testés ici.
5. Revenir sur les points encore ouverts du projet : contact d'escalade réel,
   politique arabe standard/dialectal, hébergement de production.
