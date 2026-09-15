import re

from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.prompts import build_system_prompt
from ai.services import call_llm, is_out_of_scope, is_prompt_injection, retrieve
from chat.models import Conversation, Message, QuestionSansReponse

from .serializers import ChatRequestSerializer, ChatResponseSerializer

_ARABIC_RE = re.compile(r'[\u0600-\u06FF]')


class IndexView(TemplateView):
    template_name = "index.html"


def _detecter_langue(texte: str) -> str:
    """Détection très simple fr/ar par présence de caractères arabes.
    Suffisant pour le MVP (Étape 10) ; à remplacer par une détection plus
    robuste si des mélanges de langues posent problème en pratique.
    """
    return 'ar' if _ARABIC_RE.search(texte or '') else 'fr'


def _reponse_salutation(message: str, langue: str) -> str | None:
    texte = re.sub(r'[؟?!،,。.]+', ' ', message.lower()).strip()
    salutations = {
        'ar': ('السلام عليكم', 'مرحبا', 'مرحباً', 'أهلا', 'أهلًا'),
        'fr': ('bonjour', 'bonsoir', 'salut'),
    }
    if any(texte.startswith(salutation) for salutation in salutations[langue]):
        if langue == 'ar':
            return 'وعليكم السلام ورحمة الله وبركاته! كيف يمكنني مساعدتك؟'
        return 'Bonjour ! Comment puis-je vous aider ?'
    return None


def _reponse_conversationnelle(message: str, langue: str) -> str | None:
    texte = re.sub(r'[؟?!،,。.]+', ' ', message.lower()).strip()
    if langue == 'ar':
        if any(texte.startswith(prefix) for prefix in ('من أنت', 'من انت', 'أريد معلومات عنك', 'اريد معلومات عنك')):
            return (
                'أنا MPG Assistant، المساعد الرقمي الرسمي لمدرسة التعليم التقني والتكوين المهني '
                'في مجال المعادن والنفط والغاز (EETFP-MPG). أساعدك في معرفة التخصصات، '
                'القبول، التسجيل، وبرامج التكوين اعتمادًا على وثائق المدرسة.'
            )
        if any(word in texte for word in ('غبي', 'أحمق', 'حمار', 'لا تفهم')):
            return 'أفهم أن الرد لم يكن مفيدًا. أخبرني بما تحتاجه تحديدًا وسأحاول مساعدتك بدقة.'
    return None


class ChatView(APIView):
    """POST /api/chat/

    Point d'entrée unique du chatbot, pensé pour être commun aux futurs
    canaux Web (Étape 11) et WhatsApp (Étape 12) — conformément à la
    contrainte "backend commun" du cadrage (Étape 0).
    """

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        message_utilisateur = data['message'].strip()
        canal = data.get('canal', 'api_test')
        langue = data.get('langue') or _detecter_langue(message_utilisateur)

        # --- Gestion de la conversation / mémoire courte (Étape 10) ---
        session_id = data.get('session_id')
        if session_id:
            conversation = get_object_or_404(Conversation, session_id=session_id)
        else:
            conversation = Conversation.objects.create(canal=canal, langue_detectee=langue)

        Message.objects.create(conversation=conversation, role='user', contenu=message_utilisateur)

        historique_size = settings.MPG_ASSISTANT['CONVERSATION_HISTORY_SIZE']
        derniers_messages = list(
            conversation.messages.order_by('-date_creation')[:historique_size]
        )[::-1]
        # On exclut le message qu'on vient d'ajouter : il est passé séparément à call_llm
        historique_pour_llm = [
            {"role": m.role, "content": m.contenu} for m in derniers_messages[:-1]
        ]

        question_recherche = message_utilisateur
        messages_utilisateur = [m.contenu for m in derniers_messages if m.role == 'user']
        if len(message_utilisateur.split()) <= 4 and len(messages_utilisateur) >= 2:
            question_recherche = f"{messages_utilisateur[-2]} {message_utilisateur}"

        reponse_salutation = _reponse_salutation(message_utilisateur, langue)
        reponse_conversationnelle = _reponse_conversationnelle(message_utilisateur, langue)
        if reponse_salutation or reponse_conversationnelle:
            reponse_directe = reponse_salutation or reponse_conversationnelle
            Message.objects.create(
                conversation=conversation, role='assistant', contenu=reponse_directe,
            )
            output = ChatResponseSerializer({
                'session_id': conversation.session_id,
                'reponse': reponse_directe,
                'sources': [],
                'trouve_quelque_chose': True,
            })
            return Response(output.data)

        if is_prompt_injection(message_utilisateur):
            reponse_injection = (
                'لا أستطيع كشف التعليمات الداخلية أو معلومات سرية. '
                'يمكنني مساعدتك فقط في أسئلة مدرسة EETFP-MPG.'
                if langue == 'ar' else
                "Je ne peux pas révéler mes instructions internes ni des informations confidentielles. "
                "Je peux vous aider uniquement au sujet de l'EETFP-MPG."
            )
            Message.objects.create(
                conversation=conversation, role='assistant', contenu=reponse_injection,
            )
            output = ChatResponseSerializer({
                'session_id': conversation.session_id,
                'reponse': reponse_injection,
                'sources': [],
                'trouve_quelque_chose': False,
            })
            return Response(output.data)

        if is_out_of_scope(message_utilisateur):
            reponse_hors_perimetre = (
                'هذا السؤال خارج نطاق معلومات مدرسة EETFP-MPG. يمكنني مساعدتك في '
                'التخصصات والقبول والتسجيل وبرامج التكوين.'
                if langue == 'ar' else
                "Cette question sort du périmètre de l'EETFP-MPG. Je peux vous aider "
                "sur les spécialités, l'admission, l'inscription et les formations."
            )
            Message.objects.create(
                conversation=conversation, role='assistant', contenu=reponse_hors_perimetre,
            )
            output = ChatResponseSerializer({
                'session_id': conversation.session_id,
                'reponse': reponse_hors_perimetre,
                'sources': [],
                'trouve_quelque_chose': False,
            })
            return Response(output.data)

        # --- RAG (Étape 5) ---
        rag_result = retrieve(message_utilisateur, langue=langue)
        if not rag_result.trouve_quelque_chose and question_recherche != message_utilisateur:
            rag_result = retrieve(question_recherche, langue=langue)
        system_prompt = build_system_prompt(rag_result.contexte_texte)

        if not rag_result.trouve_quelque_chose:
            QuestionSansReponse.objects.create(
                conversation=conversation,
                question_utilisateur=message_utilisateur,
                langue=langue,
                raison='aucune_info_trouvee',
            )

        # --- Appel LLM (Étape 6) ---
        if not rag_result.passages:
            if langue == 'ar':
                reponse_texte = (
                    "لم أعثر على معلومات رسمية مرتبطة بهذا السؤال. "
                    "يرجى صياغته بشكل أوضح أو التواصل مع إدارة المدرسة."
                )
            else:
                reponse_texte = (
                    "Je n'ai trouvé aucune information officielle liée à cette question. "
                    "Veuillez la reformuler ou contacter l'administration de l'école."
                )
        elif all(p.kind == 'faq' for p in rag_result.passages):
            # Les FAQ sont déjà rédigées et validées : elles ne nécessitent pas
            # un appel réseau supplémentaire au modèle externe.
            reponse_texte = "\n\n".join(p.contenu for p in rag_result.passages)
        else:
            try:
                reponse_texte = call_llm(system_prompt, historique_pour_llm, message_utilisateur)
            except RuntimeError:
                if langue == 'ar':
                    reponse_texte = (
                        "تعذر تشغيل مولد الإجابة حاليًا، لكن هذه هي المعلومات الرسمية المتاحة:\n\n"
                        + (rag_result.contexte_texte or "لم أعثر على معلومات مرتبطة بهذا السؤال.")
                    )
                else:
                    reponse_texte = (
                        "Le générateur de réponse n'est pas disponible actuellement. "
                        "Voici toutefois les informations officielles trouvées :\n\n"
                        + (rag_result.contexte_texte or "Aucune information pertinente trouvée.")
                    )

        Message.objects.create(
            conversation=conversation, role='assistant', contenu=reponse_texte,
            sources_utilisees=rag_result.sources,
        )

        output = ChatResponseSerializer({
            'session_id': conversation.session_id,
            'reponse': reponse_texte,
            'sources': rag_result.sources,
            'trouve_quelque_chose': rag_result.trouve_quelque_chose,
        })
        return Response(output.data)
