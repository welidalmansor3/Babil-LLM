# 🌐 BABIL LLM - CHATGPT KLONU (Inference API ile)
import os
import streamlit as st
import requests
import io
import fitz  # PyMuPDF
from duckduckgo_search import DDGS
from huggingface_hub import InferenceClient

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="BABIL LLM", page_icon="🧠", layout="wide")

# --- 2. DİL DESTEĞİ (29 DİL) ---
DILLER = {
    "Türkçe": "tr", "English": "en", "العربية": "ar", "हिन्दी": "hi",
    "Ελληνικά": "el", "فارسی": "fa", "Українська": "uk", "Română": "ro",
    "Indonesia": "id", "Čeština": "cs", "Slovenčina": "sk", "Magyar": "hu",
    "Slovenščina": "sl", "日本語": "ja", "한국어": "ko", "Deutsch": "de",
    "Français": "fr", "Русский": "ru", "Español": "es", "Italiano": "it",
    "Português": "pt", "Tiếng Việt": "vi", "ไทย": "th", "Melayu": "ms",
    "Filipino": "fil", "বাংলা": "bn", "اردو": "ur", "Nederlands": "nl"
}

# --- 3. TOKEN KONTROLÜ ---
HF_TOKEN = os.environ.get("HF_TOKEN", "")
if not HF_TOKEN:
    st.error("⚠️ HF_TOKEN eksik! Render Environment'a HF_TOKEN ekleyin!")
    st.stop()

client = InferenceClient(token=HF_TOKEN)
HF_USER = "wellid"

# --- 4. MODEL YÖNLENDİRME ---
MODELLER = {
    "💬 Sohbet": f"{HF_USER}/babilllm-sohbet",
    "💻 Codex": f"{HF_USER}/babilllm-codex",
    "🧮 Matematik": f"{HF_USER}/babilllm-matematik-7b",
    "🛡️ Güvenlik": f"{HF_USER}/babilllm-guvenlik"
}

# --- 5. CSS STİLLERİ ---
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 25px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.main-header h1 {
    margin: 0;
    font-size: 2.8em;
    font-weight: 800;
}
.main-header p {
    margin: 8px 0 0 0;
    opacity: 0.9;
    font-size: 1.1em;
}
.stButton > button {
    width: 100%;
    border-radius: 25px;
    border: none;
    padding: 12px 24px;
    font-weight: bold;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    transition: all 0.3s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}
</style>
""", unsafe_allow_html=True)

# --- 6. HEADER ---
st.markdown("""
<div class="main-header">
    <h1>🧠 BABIL LLM</h1>
    <p>Türkiye'nin Yapay Zeka Asistanı | 29 Dil | Apache 2.0</p>
</div>
""", unsafe_allow_html=True)

# --- 7. SIDEBAR (AYARLAR) ---
with st.sidebar:
    st.markdown("### ⚙️ Ayarlar")
    
    # Dil Seçimi
    secili_dil = st.selectbox("🌍 Yanıt Dili", list(DILLER.keys()))
    
    # Deep Search Aç/Kapa
    deep_search_acik = st.checkbox("🔍 Deep Search (Web Arama)", value=False)
    
    # PDF Ayarı
    st.markdown("### 📄 PDF Analizi")
    st.caption("⚠️ Maksimum 50MB")
    
    st.markdown("---")
    
    # Mod Seçimi
    mod = st.radio("📋 Modül Seçin:", list(MODELLER.keys()))
    
    st.markdown("---")
    
    # Bilgi
    st.markdown("### ℹ️ Hakkında")
    st.info(f"""
    **BABIL LLM Pro**
    
    • Model: Qwen 2.5 (7B)
    • Lisans: Apache 2.0
    • Dil: {secili_dil}
    • Deep Search: {'✅ Açık' if deep_search_acik else '❌ Kapalı'}
    """)

# --- 8. FONKSİYONLAR ---

# Deep Search
def deep_search(query, lang_code):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if results:
            context = "\n".join([f"Başlık: {r['title']}\nİçerik: {r['body']}" for r in results])
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

# LLM Cevap Üretme (Inference API)
def generate_response(prompt, model_name, system_prompt=""):
    try:
        full_prompt = f"{system_prompt}\n\nKullanıcı: {prompt}\nAsistan:" if system_prompt else f"Kullanıcı: {prompt}\nAsistan:"
        
        response = client.text_generation(
            model=model_name,
            prompt=full_prompt,
            max_new_tokens=500,
            temperature=0.3,
            top_p=0.9,
            repetition_penalty=1.1
        )
        return response.strip()
    except Exception as e:
        return f"Hata: {str(e)}"

# --- 9. ANA EKRAN ---

# DeepSeek benzeri özel karşılama mesajı
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Merhaba! Ben **BABIL LLM** 🧠\n\nTürkiye'nin yapay zeka asistanıyım. {secili_dil} dilinde hizmet veriyorum.\n\nSize nasıl yardımcı olabilirim?"
    })

# Sohbet geçmişini göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girdisi
user_input = st.chat_input("Mesajınızı yazın...")

if user_input:
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Asistan cevabı
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            # Sistem promptu
            sistem = f"Sen {secili_dil} dilinde cevap veren yardımcı bir asistansın."
            
            if mod == "💻 Codex":
                sistem += " Sen uzman bir yazılımcısın."
            elif mod == "🧮 Matematik":
                sistem += " Sen matematik uzmanısın."
            elif mod == "🛡️ Güvenlik":
                sistem += " Sen siber güvenlik uzmanısın."
            
            # Deep Search
            if deep_search_acik:
                search_results = deep_search(user_input, DILLER[secili_dil])
                if search_results:
                    user_input = f"Web Arama Sonuçları:\n{search_results}\n\nSoru: {user_input}"
            
            # Cevap üret
            cevap = generate_response(user_input, MODELLER[mod], sistem)
            st.markdown(cevap)
    
    st.session_state.messages.append({"role": "assistant", "content": cevap})

# --- 10. PDF YÜKLEME ---
st.markdown("---")
st.markdown("### 📄 PDF Analizi (Maksimum 50MB)")

uploaded_file = st.file_uploader(
    "PDF dosyası yükleyin",
    type=["pdf"],
    help="Maksimum dosya boyutu: 50MB"
)

if uploaded_file is not None:
    # Dosya boyutu kontrolü
    file_size = len(uploaded_file.read())
    uploaded_file.seek(0)  # Pointer'ı başa al
    
    if file_size > 50 * 1024 * 1024:  # 50MB
        st.error("❌ Dosya boyutu 50MB'ı aşıyor!")
    else:
        st.success(f"✅ PDF yüklendi! ({file_size/(1024*1024):.1f} MB)")
        
        # PDF oku
        pdf_text = read_pdf(uploaded_file)
        
        # PDF içeriğini göster
        with st.expander("PDF İçeriği (İlk 1000 karakter)"):
            st.text(pdf_text[:1000])
        
        # PDF ile ilgili soru
        pdf_question = st.text_input("PDF ile ilgili sorunuz:")
        
        if st.button("PDF'yi Analiz Et"):
            if pdf_question:
                with st.spinner("PDF analiz ediliyor..."):
                    prompt = f"PDF İÇERİĞİ:\n{pdf_text[:3000]}\n\nSORU: {pdf_question}"
                    cevap = generate_response(prompt, MODELLER[mod], sistem)
                    
                    st.markdown("### 📋 Analiz Sonucu:")
                    st.write(cevap)
            else:
                st.warning("Lütfen bir soru girin.")
