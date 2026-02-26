import streamlit as st
import google.generativeai as genai

# --- CONFIGURAZIONE UI MOBILE-FIRST ---
st.set_page_config(page_title="MASTER SQL", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 1.8rem; font-weight: 800; color: #1E3A8A; text-align: center; }
    .phase-card { background-color: #F8FAFC; border-radius: 10px; padding: 15px; border-left: 5px solid #3B82F6; margin-bottom: 20px; font-size: 0.9rem; }
    .stChatInput { border-radius: 15px !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONNESSIONE AI ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Usiamo 1.5-flash che è il più veloce e stabile per evitare blocchi
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("ERRORE: API KEY MANCANTE!")
    st.stop()

# --- PROMPT DI SISTEMA ---
SYSTEM_PROMPT = """
Sei il Mentore Blue Lock per l'esame del Prof. Maratea (Parthenope).
1. Segui rigorosamente il libro NAVATHE.
2. SQL: SOLO UPPERCASE, NO ORDER BY per i massimi.
3. Algebra: Usa <- per ogni passaggio logico.
4. Sii breve e chiaro per la lettura su smartphone.
"""

st.markdown('<p class="main-title">⚽ MASTER 30 E LODE</p>', unsafe_allow_header=True)

# --- IL PERCORSO ---
st.subheader("🚀 Il tuo Percorso")
fase = st.select_slider("Seleziona Fase:", options=["EER", "ALGEBRA", "SQL", "TRIGGER", "TEORIA"])

# Tracce estratte dalle tue foto
testi = {
    "EER": "MODELLAZIONE: Parcheggio MiniBrin (Multipiano, tariffe feriali/festive, ticket univoco, posti in tempo reale).",
    "ALGEBRA": "ALGEBRA: Trova gli utenti che hanno fatto SOLO offerte su 'sculture' (Usa la differenza).",
    "SQL": "SQL: Provenienze oggetti con maggior numero di aste nel 2023. VIETATO ORDER BY.",
    "TRIGGER": "PL/SQL: Limite max 3 aste e budget totale 500 euro.",
    "TEORIA": "TEORIA: Spiegare Integrità Referenziale e Assiomi di Armstrong."
}

st.markdown(f'<div class="phase-card">{testi[fase]}</div>', unsafe_allow_html=True)

# --- CHAT ---
if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Scrivi qui il tuo ragionamento..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            full_p = f"{SYSTEM_PROMPT}\nSTIAMO LAVORANDO SULLA FASE: {fase}\nTRACCIA: {testi[fase]}\nSTUDENTE: {prompt}"
            response = model.generate_content(full_p)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("Quota esaurita! Aspetta 1 minuto e riprova.")
