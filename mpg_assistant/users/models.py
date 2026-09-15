from django.db import models  # noqa: F401

# Cette application ne définit pas de modèles propres pour le MVP.
# - ai/      : logique de service pure (voir services.py, prompts.py)
# - users/   : utilise le modèle User standard de Django pour les comptes
#              du back-office (Phase 13). Un modèle dédié pourra être ajouté
#              plus tard si des rôles/permissions spécifiques sont nécessaires.
