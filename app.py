import streamlit as st

# Set page config - MUST be the first Streamlit command
st.set_page_config(
    page_title="Acil Durum Asistanı",
    page_icon="🚨",
    layout="centered"
)

import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# Custom CSS
st.markdown("""
    <style>
    .urgent-1 { color: #4CAF50; }  /* Yeşil */
    .urgent-2 { color: #8BC34A; }  /* Açık Yeşil */
    .urgent-3 { color: #FFC107; }  /* Sarı */
    .urgent-4 { color: #FF9800; }  /* Turuncu */
    .urgent-5 { color: #F44336; }  /* Kırmızı */
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error("API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

try:
    # Initialize model with Gemini 1.5 Pro
    model = genai.GenerativeModel("gemini-1.5-pro")
                
except Exception as e:
    st.error(f"API Bağlantı Hatası: {str(e)}")
    st.error("Lütfen API anahtarınızı kontrol edin ve Google Cloud Console'da gerekli ayarları yapın.")
    st.stop()

# Title
st.title("🚨 Acil Durum Asistanı")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            try:
                response = json.loads(message["content"])
                
                # Aciliyet seviyesi göstergesi
                urgency_level = response["urgency"]
                st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f'<h3 class="urgent-{urgency_level}">Aciliyet Seviyesi: {urgency_level}/5</h3>', unsafe_allow_html=True)
                
                # Gerekçe ve öneriler
                st.markdown(f"**Gerekçe:** {response['rationale']}")
                if response.get("suggestions"):
                    st.markdown(f"**Öneriler:** {response['suggestions']}")
                st.markdown('</div>', unsafe_allow_html=True)
            except json.JSONDecodeError:
                st.error("Yanıt format hatası")
        else:
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Acil durumu açıklayın..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Create Gemini prompt
    gemini_prompt = f"""
    Sen ileri düzey bir acil durum asistanısın. Aşağıdaki acil durum mesajını analiz et:

    Mesaj: {prompt}

    Lütfen şu kriterlere göre değerlendir:
    1. Mesajı dikkatlice analiz et; olayın ciddiyetini ve risk unsurlarını tespit et.
    2. Güncel acil durum müdahale protokollerine ve standartlarına uygun olarak 1'den 5'e kadar bir aciliyet puanı belirle.
    3. Belirlediğin puanın nedenini kısa ve öz bir şekilde gerekçelendir.
    4. Uygun gördüğün durumlarda ek müdahale önerileri veya acil aksiyon tavsiyelerini de sun.

    Yanıtını kesinlikle aşağıdaki JSON formatında ver:
    {{
        "urgency": <1-5 arası tam sayı>,
        "rationale": <Seçilen aciliyet puanının kısa gerekçesi>,
        "suggestions": <Ek aksiyon veya müdahale önerileri>
    }}
    """
    
    # Get response from Gemini
    with st.chat_message("assistant"):
        try:
            with st.spinner("Değerlendiriliyor..."):
                response = model.generate_content(gemini_prompt)
                response_text = response.text
                
                # Find JSON in response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                json_str = response_text[start_idx:end_idx]
                
                # Parse JSON response
                response_data = json.loads(json_str)
                
                # Display formatted response
                urgency_level = response_data["urgency"]
                st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f'<h3 class="urgent-{urgency_level}">Aciliyet Seviyesi: {urgency_level}/5</h3>', unsafe_allow_html=True)
                st.markdown(f"**Gerekçe:** {response_data['rationale']}")
                if response_data.get("suggestions"):
                    st.markdown(f"**Öneriler:** {response_data['suggestions']}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": json_str})
        except Exception as e:
            st.error(f"Yanıt alınırken bir hata oluştu: {str(e)}")

# Footer
st.markdown("---")
st.markdown("⚠️ **Not:** Bu bir yapay zeka asistanıdır. Acil durumlarda profesyonel yardım almayı ihmal etmeyin. Acil durumlarda 112'yi arayın.") 