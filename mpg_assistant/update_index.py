import base64
import os

b64_path = r'api\static\header_banner.b64'
html_path = r'api\templates\index.html'

with open(b64_path, 'r', encoding='utf-8') as f:
    b64_img = f.read().strip()

html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MPG Assistant — EETFP-MPG Mauritanie</title>
    <meta name="description" content="Assistant virtuel officiel de l'École d'Enseignement Technique et de Formation Professionnelle dans le domaine des Mines, du Pétrole et du Gaz (EETFP-MPG).">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Marked.js -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <style>
        :root {
            --bg-dark: #090d16;
            --bg-card: rgba(18, 25, 41, 0.85);
            --bg-card-border: rgba(255, 255, 255, 0.1);
            --primary-emerald: #10b981;
            --primary-cyan: #06b6d4;
            --primary-gold: #d97706;
            --accent-gradient: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
            --accent-gradient-hover: linear-gradient(135deg, #059669 0%, #0891b2 100%);
            --user-bubble: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            --bot-bubble: rgba(30, 41, 59, 0.9);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --radius-xl: 20px;
            --radius-lg: 14px;
            --radius-md: 10px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', 'Amiri', -apple-system, sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(16, 185, 129, 0.07) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(6, 182, 212, 0.07) 0%, transparent 40%);
            color: var(--text-main);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Official Header Banner Container */
        .official-header-banner {
            background: #ffffff;
            border-bottom: 3px solid var(--primary-emerald);
            padding: 10px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            z-index: 20;
        }

        .official-header-banner img {
            max-height: 85px;
            width: auto;
            max-width: 100%;
            object-fit: contain;
        }

        /* Sub-Header Bar */
        .sub-header {
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--bg-card-border);
            padding: 10px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            z-index: 10;
        }

        .sub-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .sub-brand .title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            color: #ffffff;
        }

        .sub-brand .subtitle {
            font-family: 'Amiri', serif;
            font-size: 0.95rem;
            color: #fbbf24;
            font-weight: 600;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.8rem;
            color: var(--primary-emerald);
            font-weight: 600;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--primary-emerald);
            box-shadow: 0 0 10px var(--primary-emerald);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(1.2); }
            100% { opacity: 1; transform: scale(1); }
        }

        .btn-clear {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid var(--bg-card-border);
            color: var(--text-muted);
            padding: 7px 14px;
            border-radius: var(--radius-lg);
            font-size: 0.82rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .btn-clear:hover {
            background: rgba(239, 68, 68, 0.15);
            color: #ef4444;
            border-color: rgba(239, 68, 68, 0.3);
        }

        /* Main Chat Layout */
        main {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 1050px;
            width: 100%;
            margin: 0 auto;
            padding: 16px 20px;
            overflow: hidden;
            position: relative;
        }

        #chat-container {
            flex: 1;
            overflow-y: auto;
            padding-right: 8px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            scroll-behavior: smooth;
        }

        #chat-container::-webkit-scrollbar {
            width: 6px;
        }
        #chat-container::-webkit-scrollbar-track {
            background: transparent;
        }
        #chat-container::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.12);
            border-radius: 10px;
        }

        /* Welcome Card */
        .welcome-card {
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            backdrop-filter: blur(12px);
            border-radius: var(--radius-xl);
            padding: 24px;
            text-align: center;
            margin-bottom: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            animation: fadeIn 0.4s ease;
        }

        .welcome-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(251, 191, 36, 0.12);
            border: 1px solid rgba(251, 191, 36, 0.3);
            color: #fbbf24;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
            margin-bottom: 12px;
        }

        .welcome-card h2 {
            font-family: 'Amiri', 'Outfit', serif;
            font-size: 1.5rem;
            margin-bottom: 10px;
            color: #ffffff;
        }

        .welcome-card p {
            color: var(--text-muted);
            font-size: 0.92rem;
            line-height: 1.6;
            max-width: 650px;
            margin: 0 auto;
        }

        .welcome-ar {
            font-family: 'Amiri', serif;
            font-size: 1.1rem;
            color: #e2e8f0;
            margin-top: 6px;
            direction: rtl;
        }

        /* Message Rows */
        .message-row {
            display: flex;
            gap: 12px;
            animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .message-row.user {
            flex-direction: row-reverse;
        }

        .avatar {
            width: 38px;
            height: 38px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 15px;
            flex-shrink: 0;
            margin-top: 2px;
        }

        .message-row.user .avatar {
            background: #2563eb;
            color: #ffffff;
        }

        .message-row.assistant .avatar {
            background: var(--accent-gradient);
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }

        .bubble-content {
            max-width: 84%;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .bubble {
            padding: 14px 18px;
            border-radius: var(--radius-xl);
            font-size: 0.95rem;
            line-height: 1.6;
        }

        .message-row.user .bubble {
            background: var(--user-bubble);
            color: #ffffff;
            border-bottom-right-radius: 4px;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.25);
        }

        .message-row.assistant .bubble {
            background: var(--bot-bubble);
            border: 1px solid var(--bg-card-border);
            color: var(--text-main);
            border-bottom-left-radius: 4px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }

        .bubble p { margin-bottom: 10px; }
        .bubble p:last-child { margin-bottom: 0; }
        .bubble h1, .bubble h2, .bubble h3 {
            font-family: 'Outfit', 'Amiri', sans-serif;
            margin: 12px 0 6px 0;
            color: #ffffff;
        }
        .bubble ul, .bubble ol { padding-left: 20px; margin-bottom: 10px; }
        .bubble li { margin-bottom: 4px; }
        .bubble table {
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 0.88rem;
            overflow-x: auto;
            display: block;
        }
        .bubble th, .bubble td {
            padding: 9px 13px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            text-align: left;
        }
        .bubble th {
            background: rgba(255, 255, 255, 0.08);
            color: var(--primary-cyan);
        }

        .sources-tag {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.25);
            color: var(--primary-cyan);
            font-size: 0.76rem;
            padding: 4px 12px;
            border-radius: 20px;
            margin-top: 4px;
            align-self: flex-start;
        }

        .typing-bubble {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 14px 20px;
            background: var(--bot-bubble);
            border: 1px solid var(--bg-card-border);
            border-radius: var(--radius-xl);
            border-bottom-left-radius: 4px;
            width: fit-content;
        }

        .dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--text-muted);
            animation: bounce 1.4s infinite ease-in-out both;
        }
        .dot:nth-child(1) { animation-delay: -0.32s; }
        .dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }

        /* Suggestions Bar */
        .suggestions-bar {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding: 8px 0;
            margin-top: 8px;
        }
        .suggestions-bar::-webkit-scrollbar { display: none; }

        .chip {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--bg-card-border);
            color: var(--text-muted);
            padding: 8px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .chip:hover {
            background: rgba(16, 185, 129, 0.15);
            border-color: rgba(16, 185, 129, 0.35);
            color: #ffffff;
            transform: translateY(-2px);
        }

        /* Input Bar */
        .input-area {
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            backdrop-filter: blur(16px);
            border-radius: var(--radius-xl);
            padding: 8px 10px 8px 18px;
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            transition: border-color 0.2s ease;
        }

        .input-area:focus-within {
            border-color: var(--primary-emerald);
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
        }

        .input-area input {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: var(--text-main);
            font-size: 0.95rem;
            padding: 8px 0;
        }

        .input-area input::placeholder {
            color: var(--text-dim);
        }

        .btn-send {
            width: 44px;
            height: 44px;
            border-radius: 14px;
            background: var(--accent-gradient);
            border: none;
            color: #ffffff;
            font-size: 16px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
        }

        .btn-send:hover {
            background: var(--accent-gradient-hover);
            transform: scale(1.05);
        }

        .btn-send:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        footer {
            text-align: center;
            padding: 8px;
            font-size: 0.74rem;
            color: var(--text-dim);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 768px) {
            .official-header-banner { padding: 6px 10px; }
            .official-header-banner img { max-height: 60px; }
            .sub-header { padding: 8px 14px; }
            .sub-brand .subtitle { display: none; }
            main { padding: 10px 12px; }
            .bubble-content { max-width: 92%; }
        }
    </style>
</head>
<body>

    <!-- Official Header Banner -->
    <div class="official-header-banner">
        <img src="HEADER_BANNER_B64_PLACEHOLDER" alt="Logo et En-tête Officiel EETFP-MPG Mauritanie">
    </div>

    <!-- Sub-Header Bar -->
    <div class="sub-header">
        <div class="sub-brand">
            <span class="title">MPG Assistant</span>
            <span class="subtitle">• المساعد الرقمي الرسمي</span>
        </div>
        <div class="header-actions">
            <div class="status-badge">
                <span class="status-dot"></span>
                <span>RAG Officiel</span>
            </div>
            <button class="btn-clear" id="btn-reset" title="Nouvelle conversation">
                <i class="fa-solid fa-rotate-right"></i>
                <span>Effacer</span>
            </button>
        </div>
    </div>

    <!-- Main Chat Container -->
    <main>
        <div id="chat-container">
            <div class="welcome-card">
                <div class="welcome-badge">
                    <i class="fa-solid fa-building-columns"></i> الجمهورية الإسلامية الموريتانية • Mauritanie
                </div>
                <h2>مرحباً بكم في المساعد الرقمي لـ EETFP-MPG</h2>
                <p class="welcome-ar">أنا المساعد التفاعلي الرسمي لمدرسة التعليم التقني والتكوين المهني في مجال المعادن والنفط والغاز. كيف يمكنني مساعدتك اليوم؟</p>
                <p style="margin-top: 8px; font-size: 0.85rem;">Posez vos questions sur les spécialités, admissions ou la vie de l'école. Les réponses sont basées sur les documents officiels.</p>
            </div>
        </div>

        <!-- Suggestion Chips -->
        <div class="suggestions-bar">
            <button class="chip" data-question="Quelles sont les spécialités ouvertes à l'école ?">
                <i class="fa-solid fa-layer-group"></i> Quelles sont les spécialités ?
            </button>
            <button class="chip" data-question="ما هي التخصصات المتاحة في المدرسة؟">
                <i class="fa-solid fa-list-check"></i> ما هي التخصصات المتاحة؟
            </button>
            <button class="chip" data-question="Quelles sont les formations Pétrole et Gaz ?">
                <i class="fa-solid fa-fire"></i> Formations Pétrole et Gaz
            </button>
            <button class="chip" data-question="Comment contacter l'administration ?">
                <i class="fa-solid fa-headset"></i> Contacts Administration
            </button>
        </div>

        <!-- Input Box -->
        <div class="input-area">
            <input type="text" id="user-input" dir="auto" placeholder="Posez votre question en français ou en arabe... / اكتب سؤالك هنا..." autocomplete="off">
            <button class="btn-send" id="btn-send" title="Envoyer">
                <i class="fa-solid fa-paper-plane"></i>
            </button>
        </div>

        <footer>
            École d'Enseignement Technique et de Formation Professionnelle dans le Domaine des Mines, Pétrole et Gaz
        </footer>
    </main>

    <script>
        let currentSessionId = localStorage.getItem('mpg_session_id') || null;

        const chatContainer = document.getElementById('chat-container');
        const userInput = document.getElementById('user-input');
        const btnSend = document.getElementById('btn-send');
        const btnReset = document.getElementById('btn-reset');
        const chips = document.querySelectorAll('.chip');

        marked.setOptions({ breaks: true, gfm: true });

        function scrollToBottom() {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function isArabic(text) {
            return /[\u0600-\u06FF]/.test(text);
        }

        function appendUserMessage(text) {
            const row = document.createElement('div');
            row.className = 'message-row user';
            const dirAttr = isArabic(text) ? 'style="direction: rtl; text-align: right;"' : '';
            row.innerHTML = `
                <div class="avatar"><i class="fa-solid fa-user"></i></div>
                <div class="bubble-content">
                    <div class="bubble" ${dirAttr}>${escapeHtml(text)}</div>
                </div>
            `;
            chatContainer.appendChild(row);
            scrollToBottom();
        }

        function appendAssistantMessage(text, sources = []) {
            const row = document.createElement('div');
            row.className = 'message-row assistant';
            
            const formattedContent = marked.parse(text);
            const dirAttr = isArabic(text) ? 'style="direction: rtl; text-align: right;"' : '';

            let sourcesHtml = '';
            if (sources && sources.length > 0) {
                sourcesHtml = `
                    <div class="sources-tag">
                        <i class="fa-solid fa-book-bookmark"></i>
                        <span>Source : ${sources.join(', ')}</span>
                    </div>
                `;
            }

            row.innerHTML = `
                <div class="avatar"><i class="fa-solid fa-robot"></i></div>
                <div class="bubble-content">
                    <div class="bubble" ${dirAttr}>${formattedContent}</div>
                    ${sourcesHtml}
                </div>
            `;
            chatContainer.appendChild(row);
            scrollToBottom();
        }

        function showTypingIndicator() {
            const row = document.createElement('div');
            row.id = 'typing-indicator';
            row.className = 'message-row assistant';
            row.innerHTML = `
                <div class="avatar"><i class="fa-solid fa-robot"></i></div>
                <div class="bubble-content">
                    <div class="typing-bubble">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                </div>
            `;
            chatContainer.appendChild(row);
            scrollToBottom();
        }

        function hideTypingIndicator() {
            const indicator = document.getElementById('typing-indicator');
            if (indicator) indicator.remove();
        }

        async function sendMessage(text) {
            const message = text || userInput.value.trim();
            if (!message) return;

            userInput.value = '';
            btnSend.disabled = true;

            appendUserMessage(message);
            showTypingIndicator();

            try {
                const payload = { message: message };
                if (currentSessionId) payload.session_id = currentSessionId;

                const response = await fetch('/api/chat/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();
                hideTypingIndicator();

                if (data.session_id) {
                    currentSessionId = data.session_id;
                    localStorage.setItem('mpg_session_id', currentSessionId);
                }

                appendAssistantMessage(data.reponse || "Aucune réponse reçue.", data.sources || []);
            } catch (error) {
                hideTypingIndicator();
                appendAssistantMessage("⚠️ **Erreur de connexion** : Impossible de contacter l'assistant pour le moment.", []);
                console.error('Chat error:', error);
            } finally {
                btnSend.disabled = false;
                userInput.focus();
            }
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.innerText = text;
            return div.innerHTML;
        }

        btnSend.addEventListener('click', () => sendMessage());

        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });

        btnReset.addEventListener('click', () => {
            currentSessionId = null;
            localStorage.removeItem('mpg_session_id');
            chatContainer.innerHTML = `
                <div class="welcome-card">
                    <div class="welcome-badge">
                        <i class="fa-solid fa-rotate-right"></i> المحادثة الجديدة
                    </div>
                    <h2>تم البدء بمحادثة جديدة</h2>
                    <p class="welcome-ar">تفضل بطرح سؤالك حول تخصصات وإجراءات المدرسة.</p>
                </div>
            `;
        });

        chips.forEach(chip => {
            chip.addEventListener('click', () => {
                const question = chip.getAttribute('data-question');
                if (question) sendMessage(question);
            });
        });
    </script>
</body>
</html>
"""

html_final = html_content.replace('HEADER_BANNER_B64_PLACEHOLDER', b64_img)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_final)

print("SUCCESSFULLY WRITTEN INDEX.HTML WITH OFFICIAL LOGO BANNER!")
