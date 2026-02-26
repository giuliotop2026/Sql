import streamlit as st
import google.generativeai as genai

# --- CONFIGURAZIONE UI ANTI-BLOCCO ---
st.set_page_config(page_title="GRANITO 3.0", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 1.8rem; font-weight: 900; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 1rem; color: #64748B; text-align: center; margin-bottom: 20px; }
    .phase-card { background-color: #F8FAFC; border-radius: 12px; padding: 15px; border-left: 6px solid #3B82F6; margin-bottom: 20px; font-size: 0.95rem; color: #1E293B; line-height: 1.5; }
    </style>
""", unsafe_allow_html=True)

# --- CONNESSIONE AI ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Impostato esattamente sul modello richiesto
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    st.error("ERRORE: Inserisci la tua API KEY nei Secrets di Streamlit.")
    st.stop()

# --- PROMPT DI SISTEMA ---
SYSTEM_PROMPT = """
Sei il Mentore Blue Lock per l'esame del Prof. Maratea.
1. Non dare la soluzione completa, ma guida l'utente a ragionare sulle entità e sulle chiavi.
2. SQL: Scrivi SEMPRE in UPPERCASE. NON usare ORDER BY per i massimi/minimi, usa HAVING COUNT >= ALL o EXISTS.
3. Algebra: Usa la sintassi Navathe con l'assegnazione (<-) e spiega le doppie negazioni.
4. Usa formattazione chiara e liste puntate.
"""

st.markdown('<p class="main-title">⚽ GRANITO 3.0</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Addestramento 2.5 Flash - Streaming Attivo</p>', unsafe_allow_html=True)

# --- IL PERCORSO (Estratto dalle tue foto) ---
missioni = {
    "1. EER: Parcheggio MiniBrin": "MODELLAZIONE: Gestione parcheggio 3 piani, aree separate moto/auto/furgone. Tariffe feriali/festive, ticket univoco. Calcolare posti disponibili in tempo reale per bloccare ingressi.",
    "2. EER: Pasticceria Sweets": "MODELLAZIONE: Dolci preconfezionati a pezzo vs sfusi a peso. Calcolare quanti dolci venduti e ordinare materie prime (zucchero, farina) ai fornitori.",
    "3. ALGEBRA: Il 'SOLO' (Broker)": "ALGEBRA NAVATHE: Visualizzare nome e cognome di chi ha fatto SOLO offerte su 'sculture'. (Richiede doppia differenza).",
    "4. SQL: Massimi (No Order By)": "SQL: Provenienze antiquariato andate all'asta il maggior numero di volte nel 2023. Divieto assoluto di usare ORDER BY.",
    "5. TRIGGER: Budget 500€": "PL/SQL: Un utente può rilanciare su max 3 aste contemporaneamente e il totale dei rilanci non può superare i 500 euro.",
    "6. TEORIA: Assiomi": "TEORIA: Spiegare l'Integrità Referenziale e le sue conseguenze sul popolamento. Enunciare gli Assiomi di Armstrong."
}

scelta = st.selectbox("Seleziona il Bersaglio:", list(missioni.keys()))

st.markdown(f'<div class="phase-card"><b>TRACCIA:</b><br>{missioni[scelta]}</div>', unsafe_allow_html=True)

# --- MOTORE CHAT CON STREAMING ---
if "messages" not in st.session_state: 
    st.session_state.messages = []

# Mostra lo storico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): 
        st.markdown(msg["content"])

# Input utente
if prompt := st.chat_input("Scrivi qui il tuo ragionamento..."):
    # 1. Salva e mostra il messaggio dell'utente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): 
        st.markdown(prompt)

    # 2. Mostra la risposta dell'AI in streaming
    with st.chat_message("assistant"):
        full_prompt = f"{SYSTEM_PROMPT}\nSTIAMO LAVORANDO SU: {scelta}\nTESTO TRACCIA: {missioni[scelta]}\nUTENTE: {prompt}"
        
        try:
            # Qui avviene la magia: stream=True impedisce il blocco del telefono
            response_stream = model.generate_content(full_prompt, stream=True)
            testo_completo = st.write_stream(response_stream)
            
            # Salva la risposta completa nello storico
            st.session_state.messages.append({"role": "assistant", "content": testo_completo})
            
        except Exception as e:
            st.error("Errore di connessione o Quota Esaurita. Riprova tra un istante.")
