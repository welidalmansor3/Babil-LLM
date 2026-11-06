# 🌐 BABIL LLM - CHATGPT TARZI CANLI ARAYÜZ
import os
import time
import subprocess
import re

# 1. TOKEN AYARI
from google.colab import userdata
hf_token = userdata.get('hf_token')
os.environ["HF_TOKEN"] = hf_token

# 2. APP.PY DOSYASINI OLUŞTUR
print("📝 app.py oluşturuluyor...")
app_code = '''
import os
import streamlit as st
import requests
import fitz
from duckduckgo_search import DDGS

st.set_page_config(page_title="BABIL LLM", page_icon="🧠", layout="wide")

DILLER = {
    "🇹🇷 Türkçe": "tr", "🇬🇧 English": "en", "🇸🇦 العربية": "ar",
    "🇮🇳 हिन्दी": "hi", "🇬🇷 Ελληνικά": "el", "🇮🇷 فارسی": "fa",
    "🇺🇦 Українська": "uk", "🇷🇴 Română": "ro", "🇮🇩 Indonesia": "id",
    "🇨🇿 Čeština": "cs", "🇸🇰 Slovenčina": "sk", "🇭🇺 Magyar": "hu",
    "🇸🇮 Slovenščina": "sl", "🇯🇵 日本語": "ja", "🇰🇷 한국어": "ko",
    "🇩🇪 Deutsch": "de", "🇫🇷 Français": "fr", "🇷🇺 Русский": "ru",
    "🇪🇸 Español": "es", "🇮🇹 Italiano": "it", "🇵🇹 Português": "pt",
    "🇻🇳 Tiếng Việt": "vi", "🇹🇭 ไทย": "th", "🇲🇾 Melayu": "ms",
    "🇵🇭 Filipino": "fil", "🇧🇩 বাংলা": "bn", "🇵🇰 اردو": "ur",
    "🇳🇱 Nederlands": "nl", "🇨🇳 中文": "zh"
}

HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_USER = "wellid"
MODEL_ID = f"{HF_USER}/babilllm-all-in-one"

# Z.AI / ChatGPT Tarzı CSS (Karanlık Tema)
st.markdown("""
<style>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap");
* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0d0d0f; color: #e4e4e7; }
section[data-testid="stSidebar"] { background: #0a0a0c !important; border-right: 1px solid #1a1a1e !important; }
.main-header { background: linear-gradient(135deg, #18181b 0%, #09090b 100%); border: 1px solid #27272a; border-radius: 16px; padding: 24px 28px; margin-bottom: 20px; display: flex; align-items: center; gap: 16px; }
.main-header .logo { font-size: 3em; }
.main-header h1 { margin: 0; font-size: 1.8em; font-weight: 800; color: #f4f4f5; letter-spacing: -0.5px; }
.main-header p { margin: 4px 0 0 0; color: #71717a; font-size: 0.85em; }
.stChatMessage { border-radius: 12px; padding: 16px 20px; margin: 8px 0; border: 1px solid #27272a !important; background: #18181b !important; }
[data-testid="stChatMessage"]:has([data-testid="chat-avatar-user"]) { background: #1c1c21 !important; border-color: #2e2e35 !important; }
[data-testid="stChatMessage"]:has([data-testid="chat-avatar-assistant"]) { background: #131316 !important; border-color: #1f1f25 !important; }
.stChatInput textarea { background: #18181b !important; border: 1px solid #27272a !important; border-radius: 12px !important; color: #e4e4e7 !important; padding: 14px 18px !important; }
.stButton > button { background: #18181b !important; color: #e4e4e7 !important; border: 1px solid #27272a !important; border-radius: 10px !important; padding: 10px 20px !important; font-weight: 600 !important; }
.stButton > button:hover { background: #27272a !important; border-color: #3f3f46 !important; }
.stSelectbox > div > div { background: #18181b !important; color: #e4e4e7 !important; border: 1px solid #27272a !important; border-radius: 8px !important; }
.stCheckbox label { color: #a1a1aa !important; }
.stFileUploader { border: 2px dashed #27272a !important; border-radius: 12px !important; background: #0d0d0f !important; padding: 20px !important; }
.stExpander { background: #131316 !important; border: 1px solid #1f1f25 !important; border-radius: 10px !important; }
.stAlert { border-radius: 10px !important; background: #18181b !important; border: 1px solid #27272a !important; }
hr { border-color: #1a1a1e !important; }
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color: #e4e4e7 !important; font-weight: 700 !important; }
.stCaption { color: #71717a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div class="logo">🧠</div>
    <div>
        <h1>BABIL LLM</h1>
        <p>Yapay Zeka Asistanı · 29 Dil · Deep Search · PDF Analizi</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚙️ Ayarlar")
    st.markdown("---")
    st.markdown("### 🌍 Dil")
    secili_dil = st.selectbox("Yanıt dili", list(DILLER.keys()))
    st.markdown("---")
    st.markdown("### 🔍 Deep Search")
    deep_search_acik = st.checkbox("Web araması", value=False)
    st.markdown("---")
    st.markdown("### 📄 PDF Analizi")
    st.caption("Maksimum: 50MB · PDF formatı")
    uploaded_file = st.file_uploader("PDF yükle", type=["pdf"])
    st.markdown("---")
    st.markdown("### ℹ️ Durum")
    st.caption(f"Dil: {secili_dil}\\nArama: {'✅' if deep_search_acik else '❌'}\\nModel: Qwen 7B\\nLisans: Apache 2.0")
    st.markdown("---")
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

def generate_response(prompt, system_prompt):
    try:
        if not HF_TOKEN:
            return "⚠️ HF_TOKEN eksik!"
        headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
        full_prompt = f"System: {system_prompt}\\n\\nUser: {prompt}\\n\\nAssistant:"
        data = {"inputs": full_prompt, "parameters": {"max_new_tokens": 800, "temperature": 0.3, "top_p": 0.9, "repetition_penalty": 1.1, "return_full_text": False}}
        
        url = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
        response = requests.post(url, headers=headers, json=data, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0: return result[0].get("generated_text", "").strip()
            elif isinstance(result, dict) and "generated_text" in result: return result["generated_text"].strip()
            else: return str(result)
        elif response.status_code == 503:
            return "⏳ Model yükleniyor, 20 saniye sonra tekrar deneyin."
        else:
            return f"❌ Hata ({response.status_code})"
    except Exception as e:
        return f"❌ Hata: {str(e)}"

def deep_search(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if results: return "\\n\\n".join([f"Başlık: {r['title']}\\nİçerik: {r['body']}" for r in results])
    except: pass
    return None

def read_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc: text += page.get_text()
    return text

SISTEM_PROMPTU = f"""Sen BABIL LLM'sin. Her şeyi bilebilen tek bir süper asistansın.
Kullanıcı hangi dilde yazarsa ({secili_dil}) o dilde cevap ver.

Görevlerin:
1. SOHBET VE FELSEFE: Genel sorulara mantıklı, derin ve empatik cevaplar ver.
2. KOD YAZMA: Python, HTML, C++ vb. istendiğinde temiz, çalışan ve profesyonel kodlar yaz.
3. MATEMATİK: Matematik problemlerini adım adım çöz, doğru sonucu ver.
4. SİBER GÜVENLİK: Kod denetimi, açık tespiti yap. SADECE SAVUNMA amaçlı yardım et, asla saldırı/exploit kodu yazma.

Kullanıcının sorusuna bakıp hangi şapkayı giyeceğine (uzmanlığın hangisiyse) sen karar ver ve kusursuz bir cevap ver.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.session_state.messages.append({"role": "assistant", "content": "Merhaba! Ben **BABIL LLM** 🧠\\n\\nKod yazabilirim, matematik çözebilirim, felsefe yapabilirim ve siber güvenlikte danışmanlık verebilirim.\\n\\nSize nasıl yardımcı olabilirim?"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

pdf_context = ""
if uploaded_file is not None:
    file_size = len(uploaded_file.read())
    uploaded_file.seek(0)
    if file_size > 50 * 1024 * 1024:
        st.error(f"❌ 50MB'ı aştı! ({file_size/(1024*1024):.1f} MB)")
    else:
        with st.spinner("📖 PDF okunuyor..."):
            pdf_context = read_pdf(uploaded_file)
        st.success(f"✅ PDF yüklendi! ({file_size/(1024*1024):.1f} MB)")

user_input = st.chat_input(f"Mesajınızı {secili_dil} dilinde yazın...")

if user_input:
    final_prompt = user_input
    if pdf_context:
        final_prompt = f"Kullanıcının yüklediği PDF içeriği:\\n{pdf_context[:3000]}\\n\\nKullanıcının sorusu: {user_input}"
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("🧠 Düşünüyorum..."):
            if deep_search_acik:
                with st.spinner("🔍 Web'de aranıyor..."):
                    sonuc = deep_search(user_input)
                    if sonuc:
                        final_prompt = f"Web Arama Sonuçları:\\n{sonuc}\\n\\nSoru: {user_input}"
                        st.info("✅ Web araması tamamlandı")
            
            cevap = generate_response(final_prompt, SISTEM_PROMPTU)
            st.markdown(cevap)
    
    st.session_state.messages.append({"role": "assistant", "content": cevap})

st.markdown("---")
st.markdown('<div style="text-align: center; padding: 16px; color: #52525b;"><p style="font-size: 0.8em;">🧠 BABIL LLM · All-in-One · Apache 2.0 · 29 Dil</p></div>', unsafe_allow_html=True)
'''

with open("/content/app.py", "w") as f:
    f.write(app_code)

print("✅ app.py oluşturuldu!")

# 3. KÜTÜPHANELERİ KUR
print("📦 Kütüphaneler kuruluyor...")
os.system("pip install -q streamlit requests PyMuPDF duckduckgo_search")

# 4. STREAMLIT'İ BAŞLAT
print("🚀 Streamlit başlatılıyor (CORS/XSRF kapalı)...")
os.system("fuser -k 8501/tcp 2>/dev/null")
streamlit_cmd = (
    "streamlit run /content/app.py "
    "--server.port 8501 "
    "--server.address 0.0.0.0 "
    "--server.enableCORS false "
    "--server.enableXsrfProtection false "
    "--server.headless true "
    "--browser.gatherUsageStats false > /dev/null 2>&1 &"
)
os.system(streamlit_cmd)
time.sleep(5)

# 5. CLOUDFLARE TUNNEL'I BAŞLAT
print("🌐 Cloudflare Tunnel başlatılıyor...")
os.system("cloudflared tunnel --url http://localhost:8501 > /content/cf.log 2>&1 &")

print("⏳ Link bekleniyor (15 saniye)...")
time.sleep(15)

# 6. LİNKİ BUL VE GÖSTER
with open("/content/cf.log", "r") as f:
    cf_output = f.read()

urls = re.findall(r'https://[a-z0-9-]+\.trycloudflare\.com', cf_output)

if urls:
    print("\n" + "="*55)
    print("🎉 BABIL LLM CANLI!")
    print("="*55)
    print(f"\n🔗 {urls[0]}\n")
    print("✅ Şifre YOK!")
    print("✅ JS Hatası YOK!")
    print("✅ ChatGPT gibi akıcı!")
    print("\n💡 Bu linki tarayıcıda aç ve test et!")
    
    # Keep-Alive döngüsü
    print("\n🛡️ Sistem canlı tutuluyor...")
    print("❌ Bu hücreyi kapatma, bağlantı kopar!")
    while True:
        time.sleep(60)
        print("✅ Sistem çalışıyor... " + time.strftime("%H:%M:%S"))
else:
    print("❌ Link bulunamadı!")
    print("📋 Cloudflare Logları:")
    print(cf_output[-1000:])
