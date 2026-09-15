"""
Commande de seed pour le MVP.

Charge dans la base de connaissances UNIQUEMENT les passages de
'Presentation_MPG_actualisée.pptx' classés en section "🟢 publique" lors de
la revue conjointe (conversation du 2026-09-14) — c'est-à-dire : création de
l'école, description du nouveau local, spécialités programmées/ouvertes,
ambition institutionnelle.

Sont volontairement EXCLUS (gardés hors de cette commande, donc jamais
insérés comme chunks actifs) : effectifs RH détaillés, coûts d'équipement,
budget précis, statistiques d'inscription incomplètes, taux d'insertion
professionnelle, plan d'action interne, tentative de jumelage, contraintes.
Si ce contenu interne doit un jour être exploitable par l'administration
(pas par le chatbot public), il devra être ajouté séparément avec
`statut_officialite='interne'` (voir Chunk.actifs_pour_rag()).

Usage :
    python manage.py seed_knowledge
"""

from datetime import date

from django.core.management.base import BaseCommand

from knowledge.models import Chunk, Document

DATE_CREATION_DOCUMENT = date(2024, 10, 6)      # dcterms:created du .pptx
DATE_DERNIERE_VERIFICATION = date(2025, 10, 20)  # dcterms:modified du .pptx


GREEN_CONTENT = [
    {
        "categorie": "ecole",
        "texte": (
            "L'École d'Enseignement Technique et de Formation Professionnelle dans le "
            "domaine des Mines, du Pétrole et du Gaz (EETFP-MPG) a été créée en 2022 par "
            "le décret N° 154-2022, conformément aux engagements du Président de la "
            "République, Monsieur Mohamed Cheikh El Ghazouani. Elle a pour objectif "
            "d'offrir aux jeunes mauritaniens des opportunités d'insertion dans des "
            "emplois de qualité et de fournir la main d'œuvre hautement qualifiée "
            "qu'exige l'exploitation des ressources gazières, pétrolières et la "
            "diversification des activités minières."
        ),
    },
    {
        "categorie": "ecole",
        "texte": (
            "L'école dispose de 8 plateformes spécialisées regroupant l'ensemble des "
            "laboratoires et des ateliers par spécialités, en plus des bureaux "
            "administratifs et des espaces pédagogiques communs. Un nouveau local est "
            "en construction à Nouakchott Nord grâce à un investissement de l'État "
            "mauritanien."
        ),
    },
    {
        "categorie": "ecole",
        "texte": (
            "Le nouveau local de l'EETFP-MPG (en cours de construction) comprend un "
            "bloc administratif avec 14 bureaux, une bibliothèque, une infirmerie, un "
            "restaurant, ainsi que des loges pour le personnel de gardiennage. Il "
            "comprendra également 15 salles de cours, 2 salles de bureautique, 2 salles "
            "de logiciels, un amphithéâtre, une salle de conférence, une salle de "
            "réunion, une salle des professeurs, 10 ateliers et 3 laboratoires."
        ),
    },
    {
        "categorie": "specialites",
        "texte": (
            "L'EETFP-MPG propose dix (10) spécialités de formation programmées : "
            "Maintenance Réseau de Transport et Equipement de Traitement du Gaz (MRTG), "
            "Instrumentation, Travaux Carrières et Mines (TCM), Production Pétrolière "
            "et Gazière (PPG), Electromécanique (EM), Soudure Industrielle (SI), "
            "Maintenance des Engins de Chantiers (MEC), QHSE (Qualité Hygiène Sécurité "
            "Environnement), Raffinage et Pétrochimie (RP), et Technique de Forage."
        ),
    },
    {
        "categorie": "specialites",
        "texte": (
            "Secteurs d'activité liés aux spécialités de l'EETFP-MPG : MRTG cible "
            "l'industrie de production de pétrole et gaz ; Instrumentation couvre "
            "l'électrique, l'automobile, l'énergie et le pétrole ; TCM et Technique de "
            "Forage couvrent le pétrole, le gaz, l'eau et les chantiers de génie civil "
            "(BTP) ; PPG couvre l'industrie des hydrocarbures ; Electromécanique couvre "
            "les usines, transports, exploitations agricoles et chantiers de "
            "construction ; Soudure Industrielle couvre la chaudronnerie, la "
            "serrurerie métallière et la soudure industrielle (y compris scaphandrier) ; "
            "QHSE couvre la qualité, l'hygiène, la sécurité et l'environnement au "
            "travail ; Raffinage et Pétrochimie couvre l'industrie de production "
            "d'énergie et la pétrochimie."
        ),
    },
    {
        "categorie": "specialites",
        "texte": (
            "Parmi les dix spécialités programmées à l'EETFP-MPG, neuf (9) sont déjà "
            "ouvertes : Maintenance Réseau de Transport et Equipement de Traitement du "
            "Gaz (MRTG), Travaux Carrières et Mines (TCM), Production Pétrolière et "
            "Gazière (PPG), Electromécanique (EM), Soudure Industrielle (SI), "
            "Maintenance des Engins de Chantiers (MEC), Technique de Forage, QHSE, et "
            "Raffinage et Pétrochimie (RP)."
        ),
    },
    {
        "categorie": "ecole",
        "texte": (
            "L'ambition de l'EETFP-MPG, dans la continuité de la vision du Président de "
            "la République, est d'être un pôle d'excellence dans la région, d'avoir un "
            "partenariat efficace et gagnant-gagnant avec les partenaires nationaux et "
            "internationaux actifs dans le domaine des Mines, du Pétrole et du Gaz en "
            "Mauritanie, et de répondre efficacement aux besoins en formation initiale "
            "et continue de ses partenaires avec une très haute qualité."
        ),
    },
]


class Command(BaseCommand):
    help = "Charge le contenu public validé de la présentation MPG dans la base de connaissances."

    def handle(self, *args, **options):
        document, created = Document.objects.update_or_create(
            titre="Présentation MPG actualisée — extraits publics",
            defaults=dict(
                type_document='powerpoint',
                fichier_original='Presentation_MPG_actualisée.pptx',
                langue='fr',
                categorie_principale='ecole',
                date_creation_document=DATE_CREATION_DOCUMENT,
                date_derniere_verification=DATE_DERNIERE_VERIFICATION,
                statut_officialite='officiel_valide',
                niveau_confiance='haute',
                statut_activite='actif',
                version='v1',
                notes_internes=(
                    "Seuls les passages validés comme 'publics' lors de la revue du "
                    "2026-09-14 sont inclus ici. Le reste du PPTX (RH, budget, "
                    "statistiques incomplètes, taux d'insertion, contraintes, "
                    "jumelage) est volontairement exclu de cette base de connaissances "
                    "publique — voir la conversation de cadrage pour le détail."
                ),
            ),
        )

        # On repart d'une base propre pour ce document à chaque exécution du seed,
        # pour que la commande reste idempotente pendant la phase de calibration.
        document.chunks.all().delete()

        for i, item in enumerate(GREEN_CONTENT):
            Chunk.objects.create(
                document=document,
                contenu_texte=item["texte"],
                langue='fr',
                categorie=item["categorie"],
                ordre_dans_document=i,
                statut_activite='actif',  # déjà revu manuellement dans cette conversation
            )

        self.stdout.write(self.style.SUCCESS(
            f"Document '{document.titre}' {'créé' if created else 'mis à jour'} "
            f"avec {len(GREEN_CONTENT)} chunks actifs."
        ))
