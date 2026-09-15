import uuid

from django.db import models


class Conversation(models.Model):
    """Une session de conversation anonyme (Étape 10 : pas de compte utilisateur en V1)."""

    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    canal = models.CharField(
        max_length=20,
        choices=[('web', 'Web'), ('whatsapp', 'WhatsApp'), ('api_test', 'Test API')],
        default='api_test',
    )
    langue_detectee = models.CharField(max_length=5, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_derniere_activite = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {str(self.session_id)[:8]} ({self.canal})"

    class Meta:
        ordering = ['-date_derniere_activite']


class Message(models.Model):
    """Un message dans une conversation (utilisateur ou assistant)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=[('user', 'Utilisateur'), ('assistant', 'Assistant')])
    contenu = models.TextField()
    # Sources citées (liste de titres/IDs de documents) — pour audit/traçabilité (Étape 5)
    sources_utilisees = models.JSONField(default=list, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_creation']

    def __str__(self):
        return f"[{self.role}] {self.contenu[:60]}"


class QuestionSansReponse(models.Model):
    """Log des questions non résolues, pour amélioration continue (Étape 3, Phase 16)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, null=True, blank=True, on_delete=models.SET_NULL, related_name='questions_sans_reponse',
    )
    question_utilisateur = models.TextField()
    langue = models.CharField(max_length=5, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    raison = models.CharField(
        max_length=30,
        choices=[
            ('aucune_info_trouvee', 'Aucune information trouvée'),
            ('contradiction_detectee', 'Contradiction détectée'),
            ('hors_perimetre', 'Hors périmètre'),
            ('erreur_technique', 'Erreur technique'),
        ],
    )
    traitee = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.question_utilisateur[:80]
