import streamlit as st
import google.generativeai as genai

# --- CONFIGURAZIONE UI ---
st.set_page_config(page_title="GRANITO 3.0", layout="centered")

st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 900; color: #1E3A8A; text-align: center; }
    .trace-box { background-color: #F8FAFC; border-left: 5px solid #3B82F6; padding: 15px; border-radius: 8px; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# --- CONNESSIONE AI ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # USIAMO IL MODELLO CORRETTO: GEMINI 3 FLASH
    model = genai.GenerativeModel('gemini-3-flash')
except Exception:
    st.error("⚠️ Chiave API o Modello non trovato. Verifica i Secrets.")
    st.stop()

# --- PROMPT DI SISTEMA (MENTORE NAVATHE) ---
SYSTEM_PROMPT = """
Sei l'assistente Granito 3.0. Insegna SQL e Algebra (Navathe) per il 30 e lode.
1. SQL: SOLO UPPERCASE. No ORDER BY per i massimi.
2. Algebra: Usa <- per le assegnazioni.
3. Trigger: Spiega :NEW e :OLD.
"""

st.markdown('<p class="main-header">⚽ BLUE LOCK ACADEMY</p>', unsafe_allow_html=True)

# --- TRACCE (DALLE TUE FOTO) ---
missioni = {
    "Fase 1: EER - Parcheggio": "Gestione MiniBrin. Piani, aree mezzi, ticket univoco. Calcolo posti disponibili e tariffe feriali/festive.",
    "Fase 2: Algebra - Il 'TUTTI'": "Trova chi nel 2010 ha vinto TUTTE le aste (Divisione/Doppia Differenza).",
    "Fase 3: SQL - Massimi": "Provenienze con più aste nel 2023. NO ORDER BY.",
    "Fase 4: Trigger - Budget": "Max 3 aste e budget totale 500 euro sulle aste in corso."
}

scelta = st.selectbox("🎯 Seleziona Missione:", list(missioni.keys()))
st.markdown(f'<div class="trace-box">{missioni[scelta]}</div>', unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []

for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Analizziamo la traccia..."):
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_p = f"{SYSTEM_PROMPT}\nTRACCIA: {missioni[scelta]}\nUTENTE: {prompt}"
        try:
            res = model.generate_content(full_p)
            st.markdown(res.text)
            st.session_state.chat.append({"role": "assistant", "content": res.text})
        except:
            st.error("Errore di connessione al modello. Riprova tra un istante.")
