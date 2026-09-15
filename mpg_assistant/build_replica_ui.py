import base64
import os

b64_header_path = r'api\static\header_banner.b64'
html_path = r'api\templates\index.html'

with open(b64_header_path, 'r', encoding='utf-8') as f:
    header_b64 = f.read().strip()

html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MPG Assistant — مدرسة التعليم التقني والتكوين المهني</title>
    <meta name="description" content="المساعد الرقمي التفاعلي لمدرسة التعليم التقني والتكوين المهني في مجال المعادن والنفط والغاز.">
    
    <!-- Google Fonts: Cairo, Amiri, Outfit -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
    
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Marked.js for Markdown Rendering -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <style>
        :root {
            --sidebar-bg: #07172e;
            --sidebar-active: rgba(255, 255, 255, 0.12);
            --sidebar-text: #e2e8f0;
            --sidebar-text-muted: #94a3b8;
            --main-bg: #f4f8fc;
            --card-bg: #ffffff;
            --text-dark: #0f294a;
            --text-gray: #64748b;
            --primary-blue: #1d4ed8;
            --accent-gold: #f59e0b;
            --border-light: #e2e8f0;
            --shadow-sm: 0 4px 12px rgba(15, 41, 74, 0.04);
            --shadow-md: 0 8px 24px rgba(15, 41, 74, 0.08);
            --radius-pill: 30px;
            --radius-card: 16px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Cairo', -apple-system, sans-serif;
        }

        body {
            background-color: var(--main-bg);
            color: var(--text-dark);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* -------------------------------------------------------------
           1. TOP HEADER BANNER (100% Official Match)
        ------------------------------------------------------------- */
        .top-header {
            background: #ffffff;
            border-bottom: 3px solid #eab308;
            padding: 8px 24px;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
            z-index: 100;
            height: 85px;
            flex-shrink: 0;
        }

        .top-header img {
            max-height: 72px;
            width: auto;
            max-width: 100%;
            object-fit: contain;
        }

        /* -------------------------------------------------------------
           2. MAIN WORKSPACE LAYOUT (SIDEBAR + MAIN AREA)
        ------------------------------------------------------------- */
        .app-body {
            flex: 1;
            display: flex;
            overflow: hidden;
            position: relative;
        }

        /* LEFT SIDEBAR (RTL Position: Right side of screen for Arabic layout) */
        .sidebar {
            width: 260px;
            background: linear-gradient(180deg, #07172e 0%, #0a1e3f 100%);
            color: var(--sidebar-text);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 24px 16px;
            flex-shrink: 0;
            border-left: 1px solid rgba(255, 255, 255, 0.05);
            position: relative;
            z-index: 20;
        }

        .sidebar-top {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .brand-box {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding-bottom: 12px;
        }

        .sparkle-icon {
            color: var(--accent-gold);
            font-size: 1.2rem;
            margin-top: 2px;
        }

        .brand-titles h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
            line-height: 1.2;
        }

        .brand-titles p {
            font-size: 0.76rem;
            color: var(--sidebar-text-muted);
            margin-top: 3px;
        }

        /* Menu List */
        .menu-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            list-style: none;
        }

        .menu-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 0.92rem;
            font-weight: 600;
            color: var(--sidebar-text-muted);
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .menu-item i {
            font-size: 1.1rem;
            width: 22px;
            text-align: center;
        }

        .menu-item:hover {
            background: rgba(255, 255, 255, 0.06);
            color: #ffffff;
        }

        .menu-item.active {
            background: var(--sidebar-active);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        /* Sidebar Footer */
        .sidebar-footer {
            padding-top: 16px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .footer-motto {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.78rem;
            color: #cbd5e1;
            line-height: 1.4;
        }

        .cap-badge {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.08);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--accent-gold);
            font-size: 0.95rem;
            flex-shrink: 0;
        }

        .gold-line {
            height: 3px;
            width: 60px;
            background: var(--accent-gold);
            border-radius: 2px;
            margin-top: 4px;
        }

        /* -------------------------------------------------------------
           3. CENTER MAIN CHAT WORKSPACE
        ------------------------------------------------------------- */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
            overflow-y: auto;
            position: relative;
        }

        .content-scroll-container {
            width: 100%;
            max-width: 900px;
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
        }

        /* Welcome Hero Card */
        .welcome-hero {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            margin-top: 15px;
            margin-bottom: 25px;
            animation: fadeIn 0.4s ease;
        }

        .logo-sunburst {
            position: relative;
            width: 100px;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16px;
        }

        .logo-sunburst::before {
            content: '';
            position: absolute;
            width: 110px;
            height: 110px;
            border-radius: 50%;
            border: 2px dashed rgba(245, 158, 11, 0.4);
            animation: rotateBg 20s linear infinite;
        }

        .logo-sunburst img {
            width: 82px;
            height: 82px;
            border-radius: 50%;
            object-fit: contain;
            background: #ffffff;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
            border: 2px solid #ffffff;
        }

        @keyframes rotateBg {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .welcome-hero h2 {
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--text-dark);
            margin-bottom: 8px;
        }

        .welcome-hero h2 span {
            color: var(--primary-blue);
            font-family: 'Outfit', sans-serif;
        }

        .welcome-hero p {
            font-size: 0.92rem;
            color: var(--text-gray);
            max-width: 580px;
            line-height: 1.6;
        }

        /* Action Cards Grid (6 items: 2 rows of 3 columns) */
        .cards-grid {
            width: 100%;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-bottom: 24px;
        }

        .action-card {
            background: var(--card-bg);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-card);
            padding: 16px 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: var(--shadow-sm);
        }

        .action-card:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-md);
            border-color: rgba(29, 78, 216, 0.3);
        }

        .card-main {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .card-icon-box {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            flex-shrink: 0;
        }

        .card-title {
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--text-dark);
        }

        .card-arrow {
            color: #94a3b8;
            font-size: 0.8rem;
            transition: transform 0.2s ease;
        }

        .action-card:hover .card-arrow {
            color: var(--primary-blue);
            transform: translateX(-3px);
        }

        /* Card Icon Theme Colors */
        .icon-purple { background: #f3e8ff; color: #9333ea; }
        .icon-green { background: #dcfce7; color: #16a34a; }
        .icon-blue { background: #dbeafe; color: #2563eb; }
        .icon-cyan { background: #e0f2fe; color: #0284c7; }
        .icon-red { background: #fee2e2; color: #dc2626; }
        .icon-gold { background: #fef3c7; color: #d97706; }

        /* Active Chat Message Log Container */
        .chat-log {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 16px;
            padding-bottom: 20px;
        }

        .msg-row {
            display: flex;
            gap: 12px;
            animation: slideUp 0.3s ease;
        }

        .msg-row.user {
            flex-direction: row-reverse;
        }

        .msg-avatar {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            flex-shrink: 0;
        }

        .msg-row.user .msg-avatar {
            background: var(--primary-blue);
            color: #ffffff;
        }

        .msg-row.assistant .msg-avatar {
            background: var(--sidebar-bg);
            color: var(--accent-gold);
            border: 1px solid rgba(255,255,255,0.1);
        }

        .msg-bubble-wrap {
            max-width: 80%;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .msg-bubble {
            padding: 14px 18px;
            border-radius: 18px;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        .msg-row.user .msg-bubble {
            background: var(--primary-blue);
            color: #ffffff;
            border-bottom-right-radius: 4px;
            box-shadow: 0 4px 14px rgba(29, 78, 216, 0.2);
        }

        .msg-row.assistant .msg-bubble {
            background: #ffffff;
            border: 1px solid var(--border-light);
            color: var(--text-dark);
            border-bottom-left-radius: 4px;
            box-shadow: var(--shadow-sm);
        }

        .msg-bubble table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 0.85rem;
        }

        .msg-bubble th, .msg-bubble td {
            padding: 8px 12px;
            border: 1px solid var(--border-light);
            text-align: right;
        }

        .msg-bubble th {
            background: #f8fafc;
            color: var(--primary-blue);
        }

        .msg-sources {
            font-size: 0.76rem;
            color: #0284c7;
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            padding: 4px 10px;
            border-radius: 20px;
            align-self: flex-start;
        }

        /* Floating Bottom Input Bar */
        .bottom-section {
            width: 100%;
            max-width: 900px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            margin-top: auto;
        }

        .input-bar {
            width: 100%;
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-radius: var(--radius-pill);
            padding: 6px 10px 6px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: var(--shadow-md);
            transition: all 0.2s ease;
        }

        .input-bar:focus-within {
            border-color: var(--primary-blue);
            box-shadow: 0 0 20px rgba(29, 78, 216, 0.15);
        }

        .icon-attach {
            color: #94a3b8;
            font-size: 1.1rem;
            cursor: pointer;
            transition: color 0.2s ease;
        }

        .icon-attach:hover {
            color: var(--primary-blue);
        }

        .input-bar input {
            flex: 1;
            border: none;
            outline: none;
            font-size: 0.95rem;
            color: var(--text-dark);
            background: transparent;
        }

        .input-bar input::placeholder {
            color: #94a3b8;
        }

        .btn-submit {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: var(--primary-blue);
            border: none;
            color: #ffffff;
            font-size: 1rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3);
        }

        .btn-submit:hover {
            background: #1e40af;
            transform: scale(1.05);
        }

        .footer-notice {
            font-size: 0.75rem;
            color: var(--text-gray);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(14px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Responsive Breakpoints */
        @media (max-width: 900px) {
            .cards-grid { grid-template-columns: repeat(2, 1fr); }
            .sidebar { width: 220px; }
        }

        @media (max-width: 680px) {
            .sidebar { display: none; }
            .cards-grid { grid-template-columns: 1fr; }
            .main-content { padding: 14px; }
            .top-header { height: 70px; padding: 6px 12px; }
        }
    </style>
</head>
<body>

    <!-- 1. TOP HEADER BANNER (100% Matching Official Branding) -->
    <header class="top-header">
        <img src="HEADER_BANNER_B64_PLACEHOLDER" alt="الترويسة الرسمية لمدرسة التعليم التقني والتكوين المهني في مجال المعادن والنفط والغاز">
    </header>

    <!-- 2. APPLICATION BODY (SIDEBAR + MAIN AREA) -->
    <div class="app-body">
        
        <!-- RIGHT SIDEBAR (RTL Arabic Navigation) -->
        <aside class="sidebar">
            <div class="sidebar-top">
                <div class="brand-box">
                    <span class="sparkle-icon"><i class="fa-solid fa-sparkles"></i></span>
                    <div class="brand-titles">
                        <h1>MPG Assistant</h1>
                        <p>مساعدك الذكي للإجابة على أسئلتك</p>
                    </div>
                </div>

                <ul class="menu-list">
                    <li class="menu-item active" id="btn-new-chat">
                        <i class="fa-regular fa-comment-dots"></i>
                        <span>محادثة جديدة</span>
                    </li>
                    <li class="menu-item">
                        <i class="fa-regular fa-folder-open"></i>
                        <span>المحادثات السابقة</span>
                    </li>
                    <li class="menu-item">
                        <i class="fa-regular fa-user"></i>
                        <span>حول المدرسة</span>
                    </li>
                    <li class="menu-item">
                        <i class="fa-regular fa-circle-question"></i>
                        <span>المساعدة</span>
                    </li>
                </ul>
            </div>

            <div class="sidebar-footer">
                <div class="footer-motto">
                    <div class="cap-badge"><i class="fa-solid fa-graduation-cap"></i></div>
                    <span>معاً نحو تكوين مهني أفضل ومستقبل واعد</span>
                </div>
                <div class="gold-line"></div>
            </div>
        </aside>

        <!-- MAIN WORKSPACE -->
        <main class="main-content">
            <div class="content-scroll-container">
                
                <!-- Welcome Card Section -->
                <div class="welcome-hero" id="welcome-section">
                    <div class="logo-sunburst">
                        <img src="HEADER_BANNER_B64_PLACEHOLDER" alt="شعار المدرسة">
                    </div>
                    <h2>مرحبا بك في <span>MPG Assistant</span></h2>
                    <p>أنا هنا لمساعدتك في العثور على المعلومات المتعلقة بالمدرسة والتكوينات، وشروط الالتحاق، وكل ما يخص التكوين التقني والمهني.</p>
                </div>

                <!-- 6 Quick Action Grid Cards -->
                <div class="cards-grid" id="cards-section">
                    
                    <!-- Card 1 -->
                    <div class="action-card" data-query="متى تبدأ التسجيلات في المدرسة؟">
                        <div class="card-main">
                            <div class="card-icon-box icon-purple"><i class="fa-regular fa-calendar-days"></i></div>
                            <span class="card-title">متى تبدأ التسجيلات؟</span>
                        </div>
                        <i class="fa-solid fa-chevron-left card-arrow"></i>
                    </div>

                    <!-- Card 2 -->
                    <div class="action-card" data-query="ما هي شروط الالتحاق والمستندات المطلوبة؟">
                        <div class="card-main">
                            <div class="card-icon-box icon-green"><i class="fa-regular fa-file-lines"></i></div>
                            <span class="card-title">ما هي شروط الالتحاق؟</span>
                        </div>
                        <i class="fa-solid fa-chevron-left card-arrow"></i>
                    </div>

                    <!-- Card 3 -->
                    <div class="action-card" data-query="ما هي التخصصات المتوفرة في المدرسة؟">
                        <div class="card-main">
                            <div class="card-icon-box icon-blue"><i class="fa-solid fa-graduation-cap"></i></div>
                            <span class="card-title">ما هي التخصصات المتوفرة؟</span>
                        </div>
                        <i class="fa-solid fa-chevron-left card-arrow"></i>
                    </div>

                    <!-- Card 4 -->
                    <div class="action-card" data-query="كيف يمكنني التواصل مع إدارة المدرسة؟">
                        <div class="card-main">
                            <div class="card-icon-box icon-cyan"><i class="fa-solid fa-headset"></i></div>
                            <span class="card-title">أريد التحدث مع الإدارة</span>
                        </div>
                        <i class="fa-solid fa-chevron-left card-arrow"></i>
                    </div>

                    <!-- Card 5 -->
                    <div class="action-card" data-query="أين تقع المدرسة وكيف أصل إليها؟">
                        <div class="card-main">
                            <div class="card-icon-box icon-red"><i class="fa-solid fa-location-dot"></i></div>
                            <span class="card-title">أين تقع المدرسة؟</span>
                        </div>
                        <i class="fa-solid fa-chevron-left card-arrow"></i>
                    </div>

                    <!-- Card 6 -->
                    <div class="action-card" data-query="ما هي الوثائق المطلوبة للتسجيل؟">
                        <div class="card-main">
                            <div class="card-icon-box icon-gold"><i class="fa-regular fa-folder-open"></i></div>
                            <span class="card-title">ما هي الوثائق المطلوبة؟</span>
                        </div>
                        <i class="fa-solid fa-chevron-left card-arrow"></i>
                    </div>

                </div>

                <!-- Active Chat Messages Log Container -->
                <div class="chat-log" id="chat-log" style="display: none;"></div>

            </div>

            <!-- Floating Bottom Input Section -->
            <div class="bottom-section">
                <div class="input-bar">
                    <i class="fa-solid fa-paperclip icon-attach" title="إرفاق ملف"></i>
                    <input type="text" id="user-input" placeholder="اكتب رسالتك هنا..." autocomplete="off">
                    <button class="btn-submit" id="btn-send" title="إرسال">
                        <i class="fa-solid fa-paper-plane"></i>
                    </button>
                </div>
                <div class="footer-notice">
                    <i class="fa-solid fa-shield-halved"></i>
                    <span>جميع المعلومات مستمدة من المصادر الرسمية للمدرسة</span>
                </div>
            </div>

        </main>
    </div>

    <!-- Client Script -->
    <script>
        let currentSessionId = localStorage.getItem('mpg_session_id') || null;

        const welcomeSection = document.getElementById('welcome-section');
        const cardsSection = document.getElementById('cards-section');
        const chatLog = document.getElementById('chat-log');
        const userInput = document.getElementById('user-input');
        const btnSend = document.getElementById('btn-send');
        const btnNewChat = document.getElementById('btn-new-chat');
        const actionCards = document.querySelectorAll('.action-card');

        marked.setOptions({ breaks: true, gfm: true });

        function showChatView() {
            welcomeSection.style.display = 'none';
            cardsSection.style.display = 'none';
            chatLog.style.display = 'flex';
        }

        function resetToWelcomeView() {
            currentSessionId = null;
            localStorage.removeItem('mpg_session_id');
            chatLog.innerHTML = '';
            chatLog.style.display = 'none';
            welcomeSection.style.display = 'flex';
            cardsSection.style.display = 'grid';
        }

        function appendUserMessage(text) {
            showChatView();
            const row = document.createElement('div');
            row.className = 'msg-row user';
            row.innerHTML = `
                <div class="msg-avatar"><i class="fa-solid fa-user"></i></div>
                <div class="msg-bubble-wrap">
                    <div class="msg-bubble">${escapeHtml(text)}</div>
                </div>
            `;
            chatLog.appendChild(row);
            scrollToBottom();
        }

        function appendAssistantMessage(text, sources = []) {
            const row = document.createElement('div');
            row.className = 'msg-row assistant';
            
            const formattedContent = marked.parse(text);

            let sourcesHtml = '';
            if (sources && sources.length > 0) {
                sourcesHtml = `
                    <div class="msg-sources">
                        <i class="fa-solid fa-book-bookmark"></i> المصدر: ${sources.join(', ')}
                    </div>
                `;
            }

            row.innerHTML = `
                <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
                <div class="msg-bubble-wrap">
                    <div class="msg-bubble">${formattedContent}</div>
                    ${sourcesHtml}
                </div>
            `;
            chatLog.appendChild(row);
            scrollToBottom();
        }

        function showTypingIndicator() {
            const row = document.createElement('div');
            row.id = 'typing-indicator';
            row.className = 'msg-row assistant';
            row.innerHTML = `
                <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
                <div class="msg-bubble-wrap">
                    <div class="msg-bubble" style="color: #64748b;">
                        <i class="fa-solid fa-circle-notch fa-spin"></i> جاري البحث في المستندات الرسمية...
                    </div>
                </div>
            `;
            chatLog.appendChild(row);
            scrollToBottom();
        }

        function hideTypingIndicator() {
            const indicator = document.getElementById('typing-indicator');
            if (indicator) indicator.remove();
        }

        function scrollToBottom() {
            chatLog.scrollTop = chatLog.scrollHeight;
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

                appendAssistantMessage(data.reponse || "لم يتم استلام إجابة.", data.sources || []);
            } catch (error) {
                hideTypingIndicator();
                appendAssistantMessage("⚠️ **خطأ في الاتصال**: تعذر الاتصال بالخادم حالياً. يرجى المحاولة لاحقاً.", []);
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

        btnNewChat.addEventListener('click', resetToWelcomeView);

        actionCards.forEach(card => {
            card.addEventListener('click', () => {
                const query = card.getAttribute('data-query');
                if (query) sendMessage(query);
            });
        });
    </script>
</body>
</html>
"""

html_final = html_content.replace('HEADER_BANNER_B64_PLACEHOLDER', header_b64)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_final)

print("SUCCESSFULLY BUILT 100% EXACT MATCH REPLICA INDEX.HTML!")
