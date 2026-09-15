"""
Services IA de MPG Assistant.

Implémente le flux défini en Étape 5 :

    Question -> recherche FAQ + recherche Chunks -> construction contexte
    -> appel LLM (avec system prompt Étape 2) -> réponse + sources

MVP volontairement simple (règle de priorité : simplicité avant tout) :
- Recherche par mots-clés (pas d'embeddings/pgvector pour l'instant — le
  volume de contenu réel est encore trop faible pour que ça change quoi que
  ce soit ; c'est prévu comme évolution en Étape 6/18, pas ré-écrit ici).
- Un seul appel LLM par tour de conversation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from django.conf import settings

from knowledge.models import FAQ, Chunk

_WORD_RE = re.compile(r"[\w']+", re.UNICODE)
_STOP_WORDS = {
    'ما', 'ماذا', 'هل', 'هي', 'هو', 'هذه', 'هذا', 'في', 'من', 'على', 'عن',
    'الى', 'إلى', 'المدرسة', 'المدرسه', 'the', 'what', 'are', 'how', 'the',
}

PROMPT_INJECTION_TERMS = {
    'ignore instructions', 'ignore all instructions', 'ignore toutes les instructions',
    'reveal your system prompt',
    'reveal the system prompt', 'prompt système', 'instructions précédentes',
    'تجاهل التعليمات', 'التعليمات السابقة', 'النص الداخلي للنظام', 'كلمة المرور',
}
OUT_OF_SCOPE_TERMS = {'bitcoin', 'crypto', 'cryptomonnaie', 'cryptocurrency', 'بيتكوين', 'عملات مشفرة'}


# Dictionnaire d'expansion sémantique et de synonymes (Français & Arabe)
SYNONYMS_MAP = {
    # Spécialités / Filières
    "spécialité": {"spécialités", "filière", "filières", "branche", "branches", "formation", "formations", "option", "options", "تخصص", "تخصصات", "شعبة", "شعب"},
    "filière": {"spécialité", "spécialités", "filières", "branche", "branches", "formation", "formations", "تخصص", "تخصصات"},
    # Inscription / Admission
    "inscription": {"inscriptions", "candidature", "candidatures", "admission", "admissions", "postuler", "inscrire", "dossier", "تسجيل", "التسجيل", "قبول", "القبول", "الالتحاق", "الترشح", "الترشيح"},
    "admission": {"inscription", "inscriptions", "candidature", "candidatures", "admissions", "dossier", "تسجيل", "التسجيل", "قبول", "القبول", "الالتحاق", "الترشح", "الترشيح"},
    # Frais / Tarifs / Prix
    "frais": {"tarif", "tarifs", "prix", "coût", "cout", "scolarité", "payer", "payant", "رسوم", "تكاليف", "سعر"},
    "tarif": {"frais", "prix", "coût", "cout", "scolarité", "payer", "رسوم"},
    # Durée / Temps
    "durée": {"duree", "durées", "année", "années", "ans", "semestre", "semestres", "temps", "مدة", "سنوات"},
    # Contacts / Horaires
    "contact": {"contacts", "téléphone", "telephone", "phone", "email", "mail", "joindre", "adresse", "localisation", "هاتف", "تواصل", "عنوان"},
    # Diplôme / Niveau
    "diplôme": {"diplome", "diplômes", "bts", "bt", "cap", "licence", "master", "شهادة", "الشهادة", "مستند", "مستندات", "المستندات", "وثيقة", "وثائق", "الوثائق", "ملف"},
}

# Reverse lookup dictionary generated automatically
_EXPANDED_SYNONYMS = {}
for canonical, syns in SYNONYMS_MAP.items():
    all_words = {canonical} | syns
    for w in all_words:
        _EXPANDED_SYNONYMS[w.lower()] = {s.lower() for s in all_words}


def _tokenize(text: str) -> set[str]:
    tokens = set()
    for word in _WORD_RE.findall(text or ""):
        token = word.lower()
        if len(token) <= 2 or token in _STOP_WORDS:
            continue
        # توحيد اللواصق العربية الشائعة: "التخصصات" و"والمستندات"
        # يجب أن تتطابق مع "تخصصات" و"مستندات" في قاعدة المعرفة.
        if re.match(r'[\u0600-\u06FF]', token):
            token = token.removeprefix('و')
            token = token.removeprefix('ال')
        if len(token) > 2:
            if token not in _STOP_WORDS:
                tokens.add(token)
    return tokens


def _expand_tokens(tokens: set[str]) -> set[str]:
    expanded = set(tokens)
    for token in tokens:
        if token in _EXPANDED_SYNONYMS:
            expanded.update(_EXPANDED_SYNONYMS[token])
    return expanded


def is_prompt_injection(text: str) -> bool:
    normalized = ' '.join((text or '').lower().split())
    return any(term in normalized for term in PROMPT_INJECTION_TERMS)


def is_out_of_scope(text: str) -> bool:
    normalized = ' '.join((text or '').lower().split())
    return any(term in normalized for term in OUT_OF_SCOPE_TERMS)


@dataclass
class RetrievedPassage:
    source_titre: str
    contenu: str
    categorie: str
    score: float
    kind: str  # "faq" ou "chunk"


@dataclass
class RagResult:
    passages: list[RetrievedPassage] = field(default_factory=list)
    contexte_texte: str = ""
    sources: list[str] = field(default_factory=list)
    trouve_quelque_chose: bool = False


def _score(question_tokens: set[str], candidate_text: str) -> float:
    cand_tokens = _tokenize(candidate_text)
    if not cand_tokens or not question_tokens:
        return 0.0

    # Match direct des mots exacts (poids 1.0)
    direct_overlap = question_tokens & cand_tokens
    
    # Match étendu par synonymes/concepts (poids 0.75 pour éviter le sur-score)
    expanded_q_tokens = _expand_tokens(question_tokens)
    expanded_cand_tokens = _expand_tokens(cand_tokens)
    synonym_overlap = expanded_q_tokens & expanded_cand_tokens

    direct_score = len(direct_overlap) / len(question_tokens)
    synonym_score = len(synonym_overlap) / len(expanded_q_tokens) if expanded_q_tokens else 0.0

    # Combinaison pondérée (70% direct + 30% sémantique)
    return (0.7 * direct_score) + (0.3 * synonym_score)



def retrieve(question: str, langue: str | None = None, top_k: int | None = None) -> RagResult:
    """Recherche hybride simplifiée : FAQ en priorité, puis Chunks actifs.

    Applique strictement la règle Étape 3 / Étape 4 : seuls les Chunks et FAQ
    `actif`, dont le document parent est `actif` et non `interne`, sont
    éligibles (voir Chunk.actifs_pour_rag()).
    """
    top_k = top_k or settings.MPG_ASSISTANT['RAG_TOP_K']
    question_tokens = _tokenize(question)

    result = RagResult()

    # 1) FAQ (priorité haute — Étape 5)
    faq_qs = FAQ.objects.filter(statut_activite='actif')
    if langue:
        faq_qs = faq_qs.filter(langue=langue)

    scored_faqs = []
    for faq in faq_qs:
        # Le libellé de la FAQ décrit mieux l'intention que sa réponse,
        # qui contient souvent des mots génériques réutilisés ailleurs.
        s = _score(question_tokens, faq.question)
        if s > 0:
            scored_faqs.append((s, faq))
    scored_faqs.sort(key=lambda t: t[0], reverse=True)

    expanded_question = _expand_tokens(question_tokens)
    category_terms = {
        'admission': {'inscription', 'admission', 'dossier', 'قبول', 'القبول', 'التحاق', 'الترشح', 'مستندات', 'وثائق', 'شهادة'},
        'specialites': {'spécialité', 'spécialités', 'filière', 'filières', 'formation', 'تخصص', 'تخصصات', 'شعبة', 'شعب'},
    }
    preferred_categories = {
        category for category, terms in category_terms.items()
        if expanded_question & terms
    }
    if preferred_categories:
        preferred = [item for item in scored_faqs if item[1].categorie in preferred_categories]
        if preferred:
            scored_faqs = preferred

    # Les questions composées (ex. conditions + pièces) peuvent nécessiter
    # plusieurs FAQ validées. On conserve seulement les meilleurs résultats.
    admission_intent = expanded_question & {
        'inscription', 'admission', 'conditions', 'قبول', 'التحاق', 'الترشح', 'شهادة', 'شروط',
    }
    document_intent = expanded_question & {'dossier', 'مستندات', 'وثائق', 'ملف'}
    faq_limit = 2 if admission_intent and document_intent else 1
    contenus_faq_vus = set()
    for s, faq in scored_faqs[:faq_limit]:
        minimum_score = 0.20 if preferred_categories else 0.30
        if s < minimum_score:
            continue
        if faq.reponse in contenus_faq_vus:
            continue
        contenus_faq_vus.add(faq.reponse)
        titre = f"FAQ: {faq.question[:60]}"
        result.passages.append(RetrievedPassage(titre, faq.reponse, faq.categorie, s, "faq"))
        result.sources.append(titre)
        result.trouve_quelque_chose = True

    # 2) Chunks actifs (recherche générale)
    chunk_qs = Chunk.actifs_pour_rag()
    if langue:
        chunk_qs = chunk_qs.filter(langue=langue)

    scored_chunks = []
    for chunk in chunk_qs.select_related('document'):
        s = _score(question_tokens, chunk.contenu_texte)
        if s > 0:
            scored_chunks.append((s, chunk))
    scored_chunks.sort(key=lambda t: t[0], reverse=True)

    seuil_pertinence = 0.15  # À calibrer empiriquement (Étape 5 / Étape 7)
    for s, chunk in scored_chunks[:top_k]:
        if s < seuil_pertinence:
            continue
        titre_doc = chunk.document.titre
        result.passages.append(RetrievedPassage(titre_doc, chunk.contenu_texte, chunk.categorie, s, "chunk"))
        if titre_doc not in result.sources:
            result.sources.append(titre_doc)
        result.trouve_quelque_chose = True

    # Construction du texte de contexte injecté au LLM
    blocs = []
    for p in result.passages:
        blocs.append(f"[Source : {p.source_titre} — catégorie : {p.categorie}]\n{p.contenu}")
    result.contexte_texte = "\n\n".join(blocs)

    return result


def call_llm(system_prompt: str, historique: list[dict], question: str) -> str:
    """Appelle l'API Anthropic. Lève une exception claire si la clé API
    n'est pas configurée, plutôt que d'échouer silencieusement ou d'inventer
    une réponse (cohérent avec la règle anti-hallucination du projet).

    Les erreurs authentification/fournisseur sont converties en RuntimeError
    explicite pour que l'API puisse afficher un fallback lisible au lieu de
    générer une 500 technique brute.
    """
    api_key = settings.MPG_ASSISTANT['ANTHROPIC_API_KEY']
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY n'est pas configurée. Ajoutez-la dans le fichier "
            ".env (voir .env.example) avant d'utiliser le endpoint /api/chat/."
        )

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        messages = list(historique) + [{"role": "user", "content": question}]

        response = client.messages.create(
            model=settings.MPG_ASSISTANT['LLM_MODEL'],
            max_tokens=1000,
            system=system_prompt,
            messages=messages,
        )

        text_parts = [block.text for block in response.content if getattr(block, "type", None) == "text"]
        return "\n".join(text_parts).strip()
    except Exception as exc:
        # Le contrôleur API sait attraper RuntimeError uniquement. On normalise
        # les erreurs d'authentification / réseau / fournisseur ici pour éviter
        # l'Internal Server Error non géré par la vue.
        raise RuntimeError(
            "Échec de l'appel Anthropic. Vérifiez la clé API ANTHROPIC_API_KEY "
            "et la validité du fournisseur LLM. Détail: " + str(exc)
        ) from exc
