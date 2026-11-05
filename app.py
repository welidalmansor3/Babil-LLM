# 🌐 BABIL LLM - CHATGPT KLONU (app.py)
# GitHub -> HuggingFace -> Render mimarisi

import os
import streamlit as st
import torch
import time
import requests
import io
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
import fitz  # PyMuPDF for PDF reading
from duckduckgo_search import DDGS

# --- 1. GİRİŞ YETKİLENDİRME ---
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    st.error("HuggingFace Token bulunamadı! Render'a HF_TOKEN ekleyin.")
    st.stop()

login(token=HF_TOKEN)
HF_USER = "wellid"

# --- 2. MODELLERİ CACHE'LEME (RAM Dostu) ---
@st.cache_resource
def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(f"{HF_USER}/{model_name}")
    model = AutoModelForCausalLM.from_pretrained(
        f"{HF_USER}/{model_name}",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    model.eval()
    return model, tokenizer

# --- 3. ARAÇLAR (TOOLS) ---

# PDF Okuma
def read_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Deep Search (Web Arama)
def deep_search(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
    return results

# --- 4. ARAYÜZ TASARIMI ---
st.set_page_config(page_title="BABIL LLM", page_icon="🧠", layout="wide")

st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🧠 BABIL LLM</h1>
    <p>Türkçe Yapay Zeka | Apache 2.0 | 29 Dil | Deep Search & PDF</p>
</div>
""", unsafe_allow_html=True)

# Sol Menü (Mod Seçimi)
mod = st.sidebar.radio(
    "Modül Seçin:",
    ["💬 Sohbet", "💻 Codex (Kod)", "🧮 Matematik", "🛡️ Siber Güvenlik", "📄 PDF Analiz", "🔍 Deep Search"]
)

# Model Yükleme (Sadece gerektiğinde)
if mod == "💬 Sohbet" or mod == "📄 PDF Analiz" or mod == "🔍 Deep Search":
    model, tokenizer = load_model("babilllm-sohbet")
elif mod == "💻 Codex (Kod)":
    model, tokenizer = load_model("babilllm-codex")
elif mod == "🧮 Matematik":
    model, tokenizer = load_model("babilllm-matematik-7b")
elif mod == "🛡️ Siber Güvenlik":
    model, tokenizer = load_model("babilllm-guvenlik")

# --- 5. MODÜLLERİN ÇALIŞMASI ---
def generate_response(prompt, system_prompt="Sen yardımcı bir Türkçe asistanısın."):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=500,
            temperature=0.3,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1
        )
    return tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)

# --- 6. ARAYÜZ İÇERİĞİ ---
if mod == "💬 Sohbet":
    st.header("💬 Sohbet")
    user_input = st.text_area("Mesajınız:")
    if st.button("Gönder"):
        if user_input:
            with st.spinner("Düşünüyorum..."):
                st.write(generate_response(user_input))

elif mod == "💻 Codex (Kod)":
    st.header("💻 Codex")
    user_input = st.text_area("Kod İsteği:")
    if st.button("Kod Yaz"):
        if user_input:
            with st.spinner("Kod yazılıyor..."):
                st.code(generate_response(user_input, "Sen uzman bir yazılımcısın. Sadece kod yaz ve Türkçe yorumla."))

elif mod == "🧮 Matematik":
    st.header("🧮 Matematik")
    user_input = st.text_area("Matematik Sorusu:")
    if st.button("Çöz"):
        if user_input:
            with st.spinner("Hesaplanıyor..."):
                st.write(generate_response(user_input, "Sen matematik uzmanısın. Adım adım çöz."))

elif mod == "🛡️ Siber Güvenlik":
    st.header("🛡️ Siber Güvenlik")
    user_input = st.text_area("Güvenlik Sorusu:")
    if st.button("Analiz Et"):
        if user_input:
            with st.spinner("Analiz ediliyor..."):
                st.write(generate_response(user_input, "Sen siber güvenlik uzmanısın. Sadece savunma odaklı yardım et."))

elif mod == "📄 PDF Analiz":
    st.header("📄 PDF Analiz")
    uploaded_file = st.file_uploader("PDF yükle", type="pdf")
    if uploaded_file:
        pdf_text = read_pdf(uploaded_file)
        st.text_area("PDF İçeriği", pdf_text[:2000], height=200)
        question = st.text_input("PDF ile ilgili sorunuz:")
        if st.button("Soru Sor"):
            if question:
                prompt = f"PDF İÇERİĞİ:\n{pdf_text[:3000]}\n\nSORU: {question}"
                with st.spinner("PDF okunuyor..."):
                    st.write(generate_response(prompt))

elif mod == "🔍 Deep Search":
    st.header("🔍 Deep Search (Web Araması)")
    query = st.text_input("Web'de ara:")
    if st.button("Ara ve Cevapla"):
        if query:
            with st.spinner("Web'de aranılyor..."):
                results = deep_search(query)
                if results:
                    context = "\n".join([f"Başlık: {r['title']}\nİçerik: {r['body']}" for r in results])
                    prompt = f"WEB ARAMA SONUÇLARI:\n{context}\n\nSORU: {query}\n\nBu bilgilere dayanarak cevap ver."
                    st.write(generate_response(prompt))
