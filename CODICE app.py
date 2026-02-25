import streamlit as st
import google.generativeai as genai

# --- CONFIGURAZIONE PAGINA (MOBILE-FRIENDLY) ---
st.set_page_config(page_title="GRANITO 3.0", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main-header { font-size: 2rem; font-weight: 900; color: #1E3A8A; margin-bottom: 0px;}
    .sub-header { font-size: 1rem; color: #64748B; margin-bottom: 20px;}
    .trace-box { background-color: #F8FAFC; border-left: 4px solid #3B82F6; padding: 15px; border-radius: 5px; font-size: 0.95rem; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# --- CONNESSIONE AI ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-pro')
except Exception as e:
    st.error("Inserisci la GEMINI_API_KEY nei Secrets.")
    st.stop()

# --- PROMPT DI SISTEMA ---
SYSTEM_PROMPT = """
Sei l'assistente del metodo Granito 3.0 per Basi di Dati (Prof. Maratea).
1. Mai dare la soluzione completa. Guida passo-passo.
2. SQL: SOLO IN UPPERCASE. Non usare MAI ORDER BY, ROWNUM o ROWID per i massimi/minimi. Usa >= ALL o EXISTS.
3. Algebra: Usa sintassi Navathe (<-) e spiega le doppie negazioni.
4. Trigger: Spiega la logica tra lo stato passato e :NEW.
"""

st.markdown('<p class="main-header">⚽ GRANITO 3.0</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Addestramento Basi di Dati</p>', unsafe_allow_html=True)

# --- TRACCE PRECARICATE DALLE FOTO ---
missioni = {
    "1. EER - Parcheggio MiniBrin": "Gestione parcheggio multipiano (3 piani). Aree moto/auto/furgoncino. Registrare targa, ingresso, uscita, ticket univoco. Tariffe dipendono dal mezzo e dal giorno (feriale/festivo). Tenere traccia dei pagamenti alla cassa automatica e calcolare posti disponibili in tempo reale per bloccare ingressi. Festivi max 4 ore sosta.",
    "2. EER - Ferramenta Online": "Vendita online a clienti registrati. Articoli divisi per categoria (codice a barre, prezzo, nome). Memorizzare pezzi disponibili a inizio anno e vendite, per calcolare con una query i pezzi residui. Tracciare cosa è venduto, a chi, quantità, quando, prezzo, pagamento e spedizione. No spedizioni nei fine settimana.",
    "3. ALGEBRA - Broker / Il 'SOLO'": "Visualizzare il nome e cognome di tutti gli utenti che hanno fatto SOLO offerte su aste di opere d'arte di tipo 'scultura'.",
    "4. SQL - Broker / Prima Offerta": "Visualizzare il nome e cognome dell'utente che ha fatto la più recente offerta superiore a 500 euro sulla più recente asta di opera d'arte. (Non usare ORDER BY, ROWID, ROWNUM).",
    "5. TRIGGER - Spa Chalet-v": "Un utente può rilanciare su max tre aste contemporaneamente mentre queste sono in corso. Il totale di tutti i rilanci sulle aste in corso a cui partecipa non può superare i 500 euro.",
    "6. TEORIA - Integrità e Transazioni": "Definire l'Integrità Referenziale e le sue conseguenze sul popolamento. Spiegare cosa sono le Transazioni, le proprietà ACID e quali problemi risolvono."
}

scelta = st.selectbox("Seleziona il Bersaglio:", list(missioni.keys()))

st.markdown(f'<div class="trace-box"><b>TESTO:</b><br>{missioni[scelta]}</div>', unsafe_allow_html=True)

# --- CHAT ENGINE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Scrivi qui il tuo ragionamento o chiedimi come iniziare..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Calcolo traiettoria..."):
            context = f"{SYSTEM_PROMPT}\n\nBERSAGLIO: {scelta}\nTRACCIA: {missioni[scelta]}\n\nUTENTE: {prompt}"
            response = model.generate_content(context)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
