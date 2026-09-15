from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    """Entrée de l'endpoint POST /api/chat/.

    session_id est optionnel : s'il est absent, une nouvelle conversation
    est créée (Étape 10). Le client (Web/WhatsApp) doit le renvoyer aux
    appels suivants pour bénéficier de la mémoire de conversation.
    """
    session_id = serializers.UUIDField(required=False, allow_null=True)
    message = serializers.CharField(allow_blank=False, max_length=2000)
    langue = serializers.ChoiceField(choices=['fr', 'ar'], required=False)
    canal = serializers.ChoiceField(
        choices=['web', 'whatsapp', 'api_test'], required=False, default='api_test',
    )


class ChatResponseSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    reponse = serializers.CharField()
    sources = serializers.ListField(child=serializers.CharField())
    trouve_quelque_chose = serializers.BooleanField()
