from django.contrib import admin

from .models import Chunk, Contact, Document, FAQ


@admin.action(description="Activer les éléments sélectionnés")
def activer(modeladmin, request, queryset):
    queryset.update(statut_activite='actif')


@admin.action(description="Repasser en 'en attente de validation' / obsolète")
def desactiver(modeladmin, request, queryset):
    if modeladmin.model is Chunk:
        queryset.update(statut_activite='en_attente_validation')
    else:
        queryset.update(statut_activite='obsolete')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'titre', 'type_document', 'langue', 'categorie_principale',
        'statut_officialite', 'niveau_confiance', 'statut_activite',
        'date_derniere_verification',
    )
    list_filter = ('statut_activite', 'statut_officialite', 'niveau_confiance', 'langue', 'categorie_principale')
    search_fields = ('titre', 'notes_internes')
    actions = [activer, desactiver]


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'document', 'categorie', 'langue', 'statut_activite', 'ordre_dans_document')
    list_filter = ('statut_activite', 'categorie', 'langue', 'document')
    search_fields = ('contenu_texte',)
    autocomplete_fields = ['document']
    actions = [activer, desactiver]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'categorie', 'langue', 'statut_activite')
    list_filter = ('statut_activite', 'categorie', 'langue')
    search_fields = ('question', 'reponse')
    actions = [activer, desactiver]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('service', 'role_associe', 'telephone', 'email', 'statut_activite')
    list_filter = ('statut_activite',)
