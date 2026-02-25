import streamlit as st
import google.generativeai as genai

# --- CONFIGURAZIONE ESTETICA (UI ULTRA-CHIARA) ---
st.set_page_config(page_title="SQL BLUE LOCK ACADEMY", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .main-header { font-size: 2.8rem; font-weight: 800; color: #0F172A; text-align: center; margin-bottom: 0px; }
    .navathe-banner { background: linear-gradient(90deg, #1E40AF, #3B82F6); color: white; padding: 10px; border-radius: 10px; text-align: center; font-weight: 600; margin-bottom: 25px; }
    .traccia-box { background-color: #F1F5F9; border-radius: 12px; padding: 20px; border: 1px solid #E2E8F0; font-size: 1.1rem; line-height: 1.6; color: #1E293B; }
    .stChatMessage { border-radius: 15px; border: 1px solid #E2E8F0 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAZIONE MODELLO 2.5 FLASH ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Impostazione del modello richiesto dall'utente
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    st.error("⚠️ Chiave API mancante nei Secrets o modello 2.5 non disponibile.")
    st.stop()

# --- IL MENTORE (LOGICA NAVATHE & RAGIONAMENTO) ---
INSTRUCTIONS = """
Sei il Mentore Blue Lock, esperto in Basi di Dati (Libro Navathe). 
Il tuo obiettivo è il 30 e lode per lo studente.
REGOLE DI RISPOSTA:
1. Usa SEMPRE la scomposizione Navathe con l'operatore <- in Algebra.
2. In SQL usa solo UPPERCASE. Mai ORDER BY per trovare i massimi (usa >= ALL o NOT EXISTS).
3. Spiega il RAGIONAMENTO prima del codice.
4. Identifica le entità Forti e Deboli come richiesto nei compiti del prof.
"""

# --- INTERFACCIA PRINCIPALE ---
st.markdown('<p class="main-header">⚽ SQL BLUE LOCK ACADEMY</p>', unsafe_allow_html=True)
st.markdown('<div class="navathe-banner">MODALITÀ ADDESTRAMENTO: RIGORE NAVATHE ATTIVATO 🧬</div>', unsafe_allow_html=True)

# Sidebar: Percorso di Addestramento basato sulle FOTO
with st.sidebar:
    st.header("🏆 PIANO DI STUDI")
    fase = st.selectbox("Seleziona il modulo:", [
        "Fase 1: Modellazione EER",
        "Fase 2: Algebra Relazionale",
        "Fase 3: SQL Avanzato",
        "Fase 4: PL/SQL Trigger",
        "Fase 5: Teoria e Assiomi"
    ])
    
    st.divider()
    
    # Tracce reali estratte dalle tue foto
    tracce = {
        "Parcheggio MiniBrin": "Gestione multipiano (3 piani). Aree separate per tipo mezzo. Tariffa variabile feriale/festivo. Ticket univoco. Posti disponibili in tempo reale.",
        "Sartoria 'Cuci & Scuci'": "Abiti pre-confezionati vs su misura. Info antropometriche. Appuntamenti per aggiusti (max 5 al giorno per sarto).",
        "Broker Assicurativo": "Visualizzare utenti con SOLO offerte su sculture (Algebra). SQL: Offerta > 500€ sulla più recente asta.",
        "Ospedale & Infermieri": "Visualizzare CF infermieri con almeno un collega dello stesso sesso assunto nello stesso anno.",
        "Vincolo Spa Chalet-v": "Trigger: Max 3 aste contemporanee e budget totale rilanci < 500€."
    }
    
    scelta_traccia = st.selectbox("Scegli il bersaglio:", list(tracce.keys()))

st.markdown(f'<div class="traccia-box"><b>TRACCIA ATTIVA:</b><br>{tracce[scelta_traccia]}</div>', unsafe_allow_html=True)

# --- CHAT ENGINE ---
if "history" not in st.session_state:
    st.session_state.history = []

for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Inizia il tuo addestramento..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_context = f"{INSTRUCTIONS}\nTRACCIA: {tracce[scelta_traccia]}\nMODULO: {fase}\nUTENTE: {prompt}"
        response = model.generate_content(full_context)
        st.markdown(response.text)
        st.session_state.history.append({"role": "assistant", "content": response.text})
