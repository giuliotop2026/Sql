import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAZIONE UI AVANZATA ---
st.set_page_config(page_title="SQL Academy: 30 e Lode", layout="wide", initial_sidebar_state="expanded")

# Stile CSS per rendere l'app ultra-leggibile e professionale
st.markdown("""
    <style>
    /* Tipografia e Colori */
    body { font-family: 'Inter', sans-serif; }
    .main-header { font-size: 2.5rem; font-weight: 900; color: #1E3A8A; margin-bottom: 0px; padding-bottom: 0px;}
    .sub-header { font-size: 1.1rem; color: #64748B; margin-bottom: 30px;}
    .trace-box { background-color: #F8FAFC; border-left: 5px solid #3B82F6; padding: 20px; border-radius: 8px; font-size: 1.05rem; color: #334155; line-height: 1.6;}
    .stChatInput { border-radius: 12px; }
    /* Nascondi elementi superflui Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. CONFIGURAZIONE GEMINI 2.5 FLASH ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Aggiornato all'ultimo modello performante richiesto
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("⚠️ Chiave API mancante! Aggiungi GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# --- 3. PROMPT DI SISTEMA (IL PROFESSORE NAVATHE) ---
SYSTEM_PROMPT = """
Sei il Mentore di Basi di Dati (metodo Elmasri-Navathe). 
L'utente sta seguendo un piano rigoroso per prendere 30 e lode.
REGOLE:
1. Sii chiaro, formatta il testo con elenchi puntati e grassetti per facilitare la lettura.
2. Niente soluzioni pronte: guida l'utente a capire quali tabelle usare.
3. SQL: Usa UPPERCASE. Non usare MAI 'ORDER BY' o 'ROWNUM' per trovare massimi/minimi, usa '>= ALL'.
4. Algebra: Usa la sintassi Navathe con assegnazione (<-) e LaTeX.
5. Trigger: Spiega sempre la differenza tra i dati già presenti nel DB e il record in entrata (:NEW).
"""

# --- 4. INTERFACCIA ---
st.markdown('<p class="main-header">⚽ SQL BLUE LOCK ACADEMY</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Il tuo piano d\'addestramento pre-impostato per dominare l\'esame.</p>', unsafe_allow_html=True)

# Layout a colonne per separare il piano di studi dalla chat
col_plan, col_chat = st.columns([1, 2])

with col_plan:
    st.subheader("📋 Seleziona la Missione")
    
    # Le tracce sono state hardcodate direttamente dalle tue foto
    missioni = {
        "Fase 1: ER - Parcheggio MiniBrin": "Gestione parcheggio multipiano. 3 piani, aree per moto/auto/furgoncino. Registrazione targa, ingresso, uscita, ticket univoco. Tariffe base a mezzo e giorno (feriale/festivo). Tenere traccia dei pagamenti e posti disponibili in tempo reale. Limite 4 ore nei festivi.",
        "Fase 2: Algebra - Il 'TUTTI' (Es. 2010)": "Visualizzare il nome e cognome degli utenti che nel 2010 si sono aggiudicati TUTTE le aste a cui hanno partecipato.",
        "Fase 3: SQL - Massimi senza ORDER BY": "Visualizzare senza ripetizioni le provenienze degli oggetti di antiquariato che sono andati all'asta il maggior numero di volte nel 2023. NON usare ORDER BY, ROWID e ROWNUM.",
        "Fase 4: Trigger - Vincoli di Tempo e Budget": "Un utente può rilanciare su max 3 aste contemporaneamente in corso. Il totale dei rilanci sulle aste in corso non può superare i 500 euro."
    }
    
    missione_scelta = st.radio("Seleziona la traccia su cui vuoi ragionare:", list(missioni.keys()))
    
    st.markdown("### 📄 Testo della Traccia")
    st.markdown(f'<div class="trace-box">{missioni[missione_scelta]}</div>', unsafe_allow_html=True)

with col_chat:
    st.subheader("💬 Dialogo con il Mentore")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostra i messaggi precedenti
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input dell'utente
    if prompt := st.chat_input("Scrivi il tuo ragionamento, la tua query, o chiedimi da dove iniziare..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analisi Navathe in corso..."):
                # Costruiamo il contesto completo da mandare a Gemini
                context = f"{SYSTEM_PROMPT}\n\nMISSIONE ATTUALE:\n{missione_scelta}\nTESTO: {missioni[missione_scelta]}\n\nSTUDENTE: {prompt}"
                try:
                    response = model.generate_content(context)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    # Fallback nel caso gemini-2.5-flash non sia ancora distribuito in tutte le region
                    st.warning("Esecuzione fallita con Gemini 2.5 Flash. Tentativo di recupero con Gemini 1.5 Pro...")
                    model_fallback = genai.GenerativeModel('gemini-1.5-pro')
                    response = model_fallback.generate_content(context)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
