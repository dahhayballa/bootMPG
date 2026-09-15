import uuid

from django.db import models


# --- Listes contrôlées (Étape 3) -------------------------------------------------

CATEGORIE_CHOICES = [
    ('ecole', 'École'),
    ('specialites', 'Spécialités'),
    ('admission', 'Admission'),
    ('inscription', 'Inscription'),
    ('etudes', 'Études'),
    ('examens', 'Examens'),
    ('reglement', 'Règlement'),
    ('stages', 'Stages'),
    ('services_etudiants', 'Services étudiants'),
    ('actualites', 'Actualités'),
    ('faq', 'FAQ'),
    ('contacts', 'Contacts'),
]

LANGUE_CHOICES = [
    ('fr', 'Français'),
    ('ar', 'Arabe'),
    ('mixte', 'Mixte'),
]

TYPE_DOCUMENT_CHOICES = [
    ('site_web', 'Site web'),
    ('powerpoint', 'PowerPoint'),
    ('pdf', 'PDF'),
    ('reglement_interieur', 'Règlement intérieur'),
    ('guide_etudiant', 'Guide étudiant'),
    ('programme_filiere', 'Programme de filière'),
    ('procedure', 'Procédure'),
    ('calendrier', 'Calendrier'),
    ('faq', 'FAQ'),
    ('annonce', 'Annonce'),
    ('autre', 'Autre'),
]

STATUT_OFFICIALITE_CHOICES = [
    ('officiel_valide', 'Officiel validé'),
    ('officiel_non_valide', 'Officiel non validé'),
    ('interne', 'Interne'),
    ('public_informel', 'Public informel'),
]

NIVEAU_CONFIANCE_CHOICES = [
    ('haute', 'Haute'),
    ('moyenne', 'Moyenne'),
    ('faible', 'Faible'),
]

STATUT_ACTIVITE_DOCUMENT_CHOICES = [
    ('actif', 'Actif'),
    ('obsolete', 'Obsolète'),
    ('brouillon', 'Brouillon'),
    ('archive', 'Archivé'),
]

STATUT_ACTIVITE_CHUNK_CHOICES = [
    ('en_attente_validation', 'En attente de validation'),
    ('actif', 'Actif'),
    ('obsolete', 'Obsolète'),
    ('desactive_manuellement', 'Désactivé manuellement'),
]


class Document(models.Model):
    """Document source original (Étape 3, Entité 1).

    IMPORTANT (règle anti-hallucination) : un document `statut_officialite=interne`
    ou `statut_activite != actif` ne doit JAMAIS alimenter le chatbot public,
    même si certains de ses chunks existent en base — voir Chunk.actifs_pour_rag().
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=255)
    type_document = models.CharField(max_length=30, choices=TYPE_DOCUMENT_CHOICES)
    fichier_original = models.CharField(
        max_length=500, blank=True,
        help_text="Chemin du fichier ou URL de la source",
    )
    langue = models.CharField(max_length=10, choices=LANGUE_CHOICES, default='fr')
    categorie_principale = models.CharField(max_length=30, choices=CATEGORIE_CHOICES)

    date_creation_document = models.DateField(
        null=True, blank=True,
        help_text="Date du document lui-même (pas de l'import)",
    )
    date_import = models.DateTimeField(auto_now_add=True)
    date_derniere_verification = models.DateField(
        null=True, blank=True,
        help_text="Dernière fois qu'un humain a confirmé la validité de ce document",
    )

    statut_officialite = models.CharField(max_length=30, choices=STATUT_OFFICIALITE_CHOICES)
    niveau_confiance = models.CharField(max_length=10, choices=NIVEAU_CONFIANCE_CHOICES)
    statut_activite = models.CharField(
        max_length=15, choices=STATUT_ACTIVITE_DOCUMENT_CHOICES, default='brouillon',
    )

    version = models.CharField(max_length=30, blank=True)
    remplace_document = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='remplace_par',
    )
    notes_internes = models.TextField(
        blank=True,
        help_text="Commentaires internes — jamais exposés au chatbot",
    )

    def __str__(self):
        return f"{self.titre} ({self.get_statut_activite_display()})"

    class Meta:
        ordering = ['-date_import']


class Chunk(models.Model):
    """Passage exploitable par le RAG (Étape 3, Entité 2)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    contenu_texte = models.TextField()
    langue = models.CharField(max_length=5, choices=[('fr', 'Français'), ('ar', 'Arabe')])
    categorie = models.CharField(max_length=30, choices=CATEGORIE_CHOICES)

    # Embedding vectoriel : réservé pour une future recherche sémantique (pgvector,
    # Étape 6). Pour le MVP, le service de recherche (ai/services.py) utilise une
    # recherche par mots-clés simple sur `contenu_texte`, volontairement, pour
    # rester "simple + maintenable" (règle de priorité du projet) tant que le
    # volume de contenu réel est faible.
    embedding = models.JSONField(null=True, blank=True)

    ordre_dans_document = models.PositiveIntegerField(default=0)
    statut_activite = models.CharField(
        max_length=25, choices=STATUT_ACTIVITE_CHUNK_CHOICES, default='en_attente_validation',
    )
    date_derniere_maj = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chunk {str(self.id)[:8]} ({self.categorie}, {self.langue})"

    class Meta:
        ordering = ['document_id', 'ordre_dans_document']

    @classmethod
    def actifs_pour_rag(cls):
        """Seuls les chunks actifs, dont le document parent est actif ET
        n'est PAS interne, doivent être utilisés par le moteur RAG public.
        C'est ici, en un seul endroit, qu'on applique la règle Phase 2
        (anti-hallucination) + la règle de confidentialité validée avec
        l'utilisateur (contenu 'interne' jamais exposé au chatbot public).
        """
        return cls.objects.filter(
            statut_activite='actif',
            document__statut_activite='actif',
        ).exclude(document__statut_officialite='interne')


class FAQ(models.Model):
    """Paire question/réponse validée manuellement (Étape 3, Entité 3).

    Interrogée en priorité par le moteur RAG (Étape 5) car elle est
    considérée comme plus fiable qu'une réponse générée à partir de chunks bruts.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    reponse = models.TextField()
    langue = models.CharField(max_length=5, choices=[('fr', 'Français'), ('ar', 'Arabe')])
    categorie = models.CharField(max_length=30, choices=CATEGORIE_CHOICES)
    source_document = models.ForeignKey(
        Document, null=True, blank=True, on_delete=models.SET_NULL, related_name='faqs',
    )
    statut_activite = models.CharField(
        max_length=15,
        choices=[('actif', 'Actif'), ('obsolete', 'Obsolète')],
        default='actif',
    )
    date_derniere_maj = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[:80]

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"


class Contact(models.Model):
    """Contact structuré (Étape 3, Entité 4) — jamais improvisé par le LLM."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.CharField(max_length=150)
    role_associe = models.CharField(max_length=150, blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    horaires = models.CharField(max_length=150, blank=True)
    statut_activite = models.CharField(
        max_length=15,
        choices=[('actif', 'Actif'), ('obsolete', 'Obsolète')],
        default='actif',
    )

    def __str__(self):
        return self.service

    class Meta:
        verbose_name_plural = "Contacts"
