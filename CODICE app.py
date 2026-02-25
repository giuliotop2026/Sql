import streamlit as st
import google.generativeai as genai

# 1. RECUPERO API KEY DAI SECRETS
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("ERRORE: CHIAVE API NON TROVATA NEI SECRETS!")

# 2. DEFINIZIONE DEL MENTORE (SYSTEM PROMPT)
SYSTEM_PROMPT = """
SEI IL MENTORE DEL PROGETTO BLUE LOCK. IL TUO OBIETTIVO È RENDERE L'UTENTE UN FUORICLASSE DI SQL.
REGOLE DI INSEGNAMENTO:
1. MAI DARE LA SOLUZIONE SUBITO. CHIEDI SEMPRE: 'QUALI TABELLE TI SERVONO?'.
2. SCRIVI SEMPRE IN UPPERCASE PER MASSIMA CLARITY.
3. SE L'UTENTE SBAGLIA UN JOIN, SPIEGA IL 'PONTE' LOGICO MANCANTE.
4. PER I TRIGGER, SEPARA SEMPRE 'PASSATO' (SELECT) E 'FUTURO' (:NEW).
5. MOSTRA SEMPRE L'EQUIVALENTE IN ALGEBRA RELAZIONALE USANDO LATEX (ES: $$\\pi_{A}(\\sigma_{C}(R))$$).
"""

# 3. INTERFACCIA UTENTE
st.set_page_config(page_title="BLUE LOCK: SQL ACADEMY", page_icon="⚽")
st.title("⚽ BLUE LOCK: DIVENTA UN FUORICLASSE SQL")

if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR PER LE TRACCE DEL PROF
st.sidebar.header("📚 TRACCE DEL PROF")
traccia_scelta = st.sidebar.selectbox("Scegli l'esercizio:", [
    "QUERY: OPERA CON PIÙ RILANCI (SENZA ORDER BY)",
    "TRIGGER: LIMITE 500 EURO E 3 ASTE",
    "ALGEBRA: TROVA TUTTI GLI UTENTI CHE HANNO RILANCIATO",
    "CUSTOM: INCOLLA LA TUA TRACCIA"
])

# VISUALIZZAZIONE CHAT
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# INPUT UTENTE
if prompt := st.chat_input("Scrivi qui il tuo ragionamento o codice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # GENERAZIONE RISPOSTA AI
    with st.chat_message("assistant"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_input = f"{SYSTEM_PROMPT}\nTRACCIA CORRENTE: {traccia_scelta}\nSTORIA CHAT: {st.session_state.messages}\nUTENTE DICE: {prompt}"
        response = model.generate_content(full_input)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
      
