# 🌐 BABIL LLM - CHATGPT KLONU (API ile)
import os
import streamlit as st
import requests
import fitz  # PyMuPDF
from duckduckgo_search import DDGS

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="BABIL LLM",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DİL DESTEĞİ (29 DİL) ---
DILLER = {
    "🇹🇷 Türkçe": "tr",
    "🇬🇧 English": "en",
    "🇸🇦 العربية": "ar",
    "🇮🇳 हिन्दी": "hi",
    "🇬🇷 Ελληνικά": "el",
    "🇮🇷 فارسی": "fa",
    "🇺🇦 Українська": "uk",
    "🇷🇴 Română": "ro",
    "🇮🇩 Indonesia": "id",
    "🇨🇿 Čeština": "cs",
    "🇸🇰 Slovenčina": "sk",
    "🇭🇺 Magyar": "hu",
    "🇸🇮 Slovenščina": "sl",
    "🇯🇵 日本語": "ja",
    "🇰🇷 한국어": "ko",
    "🇩🇪 Deutsch": "de",
    "🇫🇷 Français": "fr",
    "🇷🇺 Русский": "ru",
    "🇪🇸 Español": "es",
    "🇮🇹 Italiano": "it",
    "🇵🇹 Português": "pt",
    "🇻🇳 Tiếng Việt": "vi",
    "🇹🇭 ไทย": "th",
    "🇲🇾 Melayu": "ms",
    "🇵🇭 Filipino": "fil",
    "🇧🇩 বাংলা": "bn",
    "🇵🇰 اردو": "ur",
    "🇳🇱 Nederlands": "nl",
    "🇨🇳 中文": "zh"
}

# --- 3. TOKEN KONTROLÜ ---
HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_USER = "wellid"

MODELLER = {
    "💬 Sohbet": f"{HF_USER}/babilllm-sohbet",
    "💻 Codex": f"{HF_USER}/babilllm-codex",
    "🧮 Matematik": f"{HF_USER}/babilllm-matematik-7b",
    "🛡️ Güvenlik": f"{HF_USER}/babilllm-guvenlik"
}

# --- 4. CSS (DeepSeek Tarzı Kara Tema) ---
st.markdown("""
<style>
/* Ana arka plan */
.stApp {
    background: #0f0f1a;
    color: #e0e0e0;
}

/* Başlık */
.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
    border: 1px solid #1a1a3e;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.main-header h1 {
    margin: 0;
    font-size: 2.5em;
    background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}
.main-header p {
    margin: 10px 0 0 0;
    color: #888;
    font-size: 1em;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0a0a14;
    border-right: 1px solid #1a1a2e;
}

/* Chat input */
.stChatInput textarea {
    background: #1a1a2e !important;
    border: 1px solid #2a2a4e !important;
    color: #e0e0e0 !important;
    border-radius: 15px !important;
}

/* Chat messages */
.stChatMessage {
    border-radius: 15px;
    margin: 10px 0;
}

/* User mesajı */
[data-testid="stChatMessage"]:has([data-testid="chat-avatar-user"]) {
    background: #1a1a3e;
    border: 1px solid #2a2a5e;
}

/* Asistan mesajı */
[data-testid="stChatMessage"]:has([data-testid="chat-avatar-assistant"]) {
    background: #0f1a2e;
    border: 1px solid #1a2a4e;
}

/* Butonlar */
.stButton > button {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 10px 24px !important;
    font-weight: bold !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4) !important;
}

/* File uploader */
.stFileUploader {
    border: 2px dashed #2a2a4e !important;
    border-radius: 15px !important;
    background: #0a0a14 !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #1a1a2e !important;
    color: #e0e0e0 !important;
    border: 1px solid #2a2a4e !important;
    border-radius: 10px !important;
}

/* Checkbox */
.stCheckbox label {
    color: #e0e0e0 !important;
}

/* Text input */
.stTextInput > div > div {
    background: #1a1a2e !important;
    color: #e0e0e0 !important;
    border: 1px solid #2a2a4e !important;
    border-radius: 10px !important;
}

/* Expander */
.stExpander {
    background: #0a0a14 !important;
    border: 1px solid #1a1a2e !important;
    border-radius: 10px !important;
}

/* Spinner */
.stSpinner > div {
    border-color: #667eea !important;
}

/* Divider */
hr {
    border-color: #1a1a2e !important;
}

/* Warning/Info */
.stAlert {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# --- 5. HEADER ---
st.markdown("""
<div class="main-header">
    <h1>🧠 BABIL LLM</h1>
    <p>29 Dil Desteği | Deep Search | PDF Analizi | Apache 2.0</p>
</div>
""", unsafe_allow_html=True)

# --- 6. SIDEBAR (AYARLAR - SAĞ TARAFTA GÖRÜNÜR) ---
with st.sidebar:
    st.markdown("## ⚙️ AYARLAR")
    st.markdown("---")
    
    # Dil Seçimi (29 Dil)
    st.markdown("### 🌍 Yanıt Dili")
    secili_dil_adi = st.selectbox(
        "Dil seçin",
        list(DILLER.keys()),
        index=0
    )
    secili_dil_kodu = DILLER[secili_dil_adi]
    
    st.markdown("---")
    
    # Mod Seçimi
    st.markdown("### 📋 Modül")
    mod = st.selectbox(
        "Modül seçin",
        list(MODELLER.keys())
    )
    
    st.markdown("---")
    
    # Deep Search Aç/Kapa
    st.markdown("### 🔍 Deep Search")
    deep_search_acik = st.checkbox(
        "Web araması yap",
        value=False,
        help="Açık olduğunda, model web'de arama yaparak güncel bilgiler kullanır"
    )
    
    st.markdown("---")
    
    # PDF Bilgilendirme
    st.markdown("### 📄 PDF Analizi")
    st.info("📄 Maksimum: 50MB\n\n⬇️ PDF'i aşağıdan yükleyin")
    
    st.markdown("---")
    
    # Sistem Bilgisi
    st.markdown("### ℹ️ Sistem")
    st.caption(f"""
    • Model: Qwen 2.5 (7B)
    • Lisans: Apache 2.0
    • Dil: {secili_dil_adi}
    • Deep Search: {'✅ Açık' if deep_search_acik else '❌ Kapalı'}
    • Modül: {mod}
    """)

# --- 7. FONKSİYONLAR ---

# HuggingFace API ile ceap üret
def generate_response(prompt, model_id, system_prompt=""):
    try:
        if not HF_TOKEN:
            return "⚠️ HF_TOKEN eksik! Render Environment'a HF_TOKEN ekleyin."
        
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Full prompt
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        else:
            full_prompt = f"User: {prompt}\n\nAssistant:"
        
        data = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.3,
                "top_p": 0.9,
                "repetition_penalty": 1.1,
                "return_full_text": False
            }
        }
        
        url = f"https://api-inference.huggingface.co/models/{model_id}"
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()
            elif isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"].strip()
            else:
                return str(result)
        elif response.status_code == 503:
            return "⏳ Model şu anda yükleniyor. Lütfen 20 saniye sonra tekrar deneyin."
        else:
            return f"❌ Hata ({response.status_code}): {response.text[:200]}"
            
    except Exception as e:
        return f"❌ Hata: {str(e)}"

# Deep Search
def deep_search(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if results:
            context = "\n\n".join([
                f"Başlık: {r['title']}\nİçerik: {r['body']}"
                for r in results
            ])
            return context
    except:
        pass
    return None

# PDF Okuma
def read_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# --- 8. SOHBET EKRANI (DeepSeek Tarzı) ---

# Sohbet geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Karşılama mesajı (ilk açılışta)
if len(st.session_state.messages) == 0:
    hosgeldin_mesaji = f"""Merhaba! Ben **BABIL LLM** 🧠

Türkiye'nin yapay zeka asistanıyım. Size nasıl yardımcı olabilirim?

**Özellikler:**
- 💬 Sohbet ve felsefe
- 💻 Kod yazma (Codex)
- 🧮 Matematik çözme
- 🛡️ Siber güvenlik
- 📄 PDF analizi
- 🔍 Deep Search (Web arama)

**Aktif Dil:** {secili_dil_adi}
**Aktif Modül:** {mod}

Bir şey yazın, size yardımcı olayım! 😊"""
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": hosgeldin_mesaji
    })

# Eski mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girdisi (chat input)
user_input = st.chat_input(f"Mesajınızı {secili_dil_adi} dilinde yazın...")

if user_input:
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Asistan cevabı
    with st.chat_message("assistant"):
        with st.spinner("🧠 Düşünüyorum..."):
            # Sistem promptu
            sistem = f"Sen {secili_dil_adi.split(' ', 1)[-1]} dilinde cevap veren yardımcı bir asistansın."
            
            if mod == "💻 Codex":
                sistem += " Sen uzman bir yazılımcısın. Sadece kod yaz ve Türkçe açıklama ekle."
            elif mod == "🧮 Matematik":
                sistem += " Sen matematik uzmanısın. Adım adım çöz."
            elif mod == "🛡️ Güvenlik":
                sistem += " Sen siber güvenlik uzmanısın. Sadece savunma amaçlı yardım et."
            
            # Deep Search
            arama_sonucu = ""
            if deep_search_acik:
                with st.spinner("🔍 Web'de aranıyor..."):
                    sonuc = deep_search(user_input)
                    if sonuc:
                        arama_sonucu = f"\n\nWeb Arama Sonuçları:\n{sonuc}\n\nSoru: {user_input}"
                        st.info("✅ Web araması tamamlandı, cevap hazırlanıyor...")
                    else:
                        st.warning("Web araması başarısız, model kendi bilgisini kullanacak.")
            
            # Cevap üret
            final_prompt = arama_sonucu + user_input if arama_sonucu else user_input
            cevap = generate_response(final_prompt, MODELLER[mod], sistem)
            
            st.markdown(cevap)
    
    # Cevabı kaydet
    st.session_state.messages.append({"role": "assistant", "content": cevap})

# --- 9. PDF YÜKLEME BÖLÜMÜ ---
st.markdown("---")
st.markdown("## 📄 PDF Analizi")
st.markdown("**⚠️ Maksimum dosya boyutu: 50MB**")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "PDF dosyası yükleyin",
        type=["pdf"],
        help="Maksimum 50MB"
    )

with col2:
    st.info("""
    📋 **PDF Bilgileri**
    
    • Maksimum: 50MB
    • Format: PDF
    • İşleme: Otomatik
    """)

if uploaded_file is not None:
    # Dosya boyutu kontrolü
    file_size = len(uploaded_file.read())
    uploaded_file.seek(0)  # Pointer'ı başa al
    
    if file_size > 50 * 1024 * 1024:  # 50MB
        st.error(f"❌ Dosya boyutu 50MB'ı aşıyor! (Mevcut: {file_size/(1024*1024):.1f} MB)")
    else:
        st.success(f"✅ PDF yüklendi! Boyut: {file_size/(1024*1024):.1f} MB")
        
        # PDF oku
        with st.spinner("📖 PDF okunuyor..."):
            pdf_text = read_pdf(uploaded_file)
        
        if pdf_text:
            # PDF içeriğini göster
            with st.expander("📄 PDF İçeriği (İlk 1000 karakter)"):
                st.text(pdf_text[:1000])
            
            # PDF sorusu
            st.markdown("### ❓ PDF ile ilgili sorunuz:")
            pdf_question = st.text_input(
                "Sorunuzu yazın:",
                placeholder="Örn: Bu PDF'nin özeti nedir?"
            )
            
            if st.button("🔍 PDF'yi Analiz Et"):
                if pdf_question:
                    with st.spinner("🧠 PDF analiz ediliyor..."):
                        # Prompt
                        prompt = f"PDF İÇERİĞİ:\n{pdf_text[:3000]}\n\nSORU: {pdf_question}"
                        
                        # Sistem promptu
                        sistem = f"Sen {secili_dil_adi.split(' ', 1)[-1]} dilinde cevap veren yardımcı bir asistansın."
                        
                        # Cevap üret
                        cevap = generate_response(prompt, MODELLER[mod], sistem)
                        
                        # Sonucu göster
                        st.markdown("### 📋 Analiz Sonucu:")
                        st.write(cevap)
                else:
                    st.warning("⚠️ Lütfen bir soru girin.")

# --- 10. ALT BİLGİ ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p>🧠 BABIL LLM | Apache 2.0 | 29 Dil Desteği | HuggingFace + Render</p>
    <p style="font-size: 0.8em;">© 2025 BABIL LLM. Tüm hakları saklıdır.</p>
</div>
""", unsafe_allow_html=True)
