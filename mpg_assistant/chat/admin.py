from django.contrib import admin

from .models import Conversation, Message, QuestionSansReponse


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('role', 'contenu', 'sources_utilisees', 'date_creation')
    can_delete = False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'canal', 'langue_detectee', 'date_creation', 'date_derniere_activite')
    list_filter = ('canal', 'langue_detectee')
    inlines = [MessageInline]


@admin.register(QuestionSansReponse)
class QuestionSansReponseAdmin(admin.ModelAdmin):
    list_display = ('question_utilisateur', 'raison', 'langue', 'date', 'traitee')
    list_filter = ('raison', 'traitee', 'langue')
    search_fields = ('question_utilisateur',)
