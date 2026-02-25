import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAZIONE ESTETICA E DI PAGINA ---
st.set_page_config(page_title="SQL BLUE LOCK: MASTERCLASS", page_icon="⚽", layout="wide")

# Custom CSS per renderla "Bella" e professionale
st.markdown("""
    <style>
    .main-title { font-size: 3rem; color: #1E90FF; font-weight: 800; text-transform: uppercase; margin-bottom: 0;}
    .sub-title { font-size: 1.2rem; color: #A9A9A9; margin-bottom: 2rem;}
    .navathe-box { background-color: #1E1E1E; padding: 15px; border-left: 5px solid #1E90FF; border-radius: 5px; margin-bottom: 20px;}
    .stTextInput>div>div>input { border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">⚽ BLUE LOCK ACADEMY</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">PERCORSO INTENSIVO: OBIETTIVO 30 E LODE</p>', unsafe_allow_html=True)

# --- 2. CONNESSIONE AL MOTORE AI ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ ATTENZIONE: Inserisci la tua GEMINI_API_KEY nei Secrets di Streamlit per scendere in campo!")
    st.stop()

# --- 3. IL CERVELLO DEL MENTORE (PROMPT DI SISTEMA) ---
SYSTEM_PROMPT = """
SEI IL MENTORE SUPREMO DI BASI DI DATI. IL TUO SCOPO È FORGIARE UN ESPERTO DA 30 E LODE.
REGOLE INVIOLABILI:
1. NESSUNA SOLUZIONE PRONTA. Insegna a ragionare a "mattoni" (Quali tabelle? Quali chiavi?).
2. SINTASSI SQL: SEMPRE E SOLO IN UPPERCASE. Usa costrutti avanzati (ALL, ANY, EXISTS), niente ORDER BY per cercare i massimi.
3. ALGEBRA RELAZIONALE: Usa ESCLUSIVAMENTE la sintassi rigorosa ELMASRI-NAVATHE con l'operatore di assegnazione (<-). Scomponi in passaggi. Esempio: R1 <- \sigma_{cond}(Tabella).
4. PL/SQL TRIGGER: Spiega sempre la differenza logica tra lo stato passato (tabelle) e il nuovo evento (:NEW).
5. Tono: Esigente, motivante, tecnico.
"""

# --- 4. IL PERCORSO DI ADDESTRAMENTO (SIDEBAR) ---
with st.sidebar:
    st.header("🗺️ ROADMAP ESAME")
    fase = st.radio(
        "Seleziona il Modulo di Addestramento:",
        [
            "1️⃣ MODELLAZIONE (ER/EER)",
            "2️⃣ ALGEBRA (NAVATHE)",
            "3️⃣ SQL AVANZATO",
            "4️⃣ PL/SQL TRIGGER",
            "5️⃣ TEORIA E ASSIOMI"
        ]
    )
    
    st.markdown("---")
    st.subheader("📚 ARCHIVIO TRACCE PROF")
    traccia_selezionata = st.selectbox(
        "Carica una traccia in memoria:",
        [
            "Traccia 1000271189: Parcheggio MiniBrin / Rilanci Uffizi",
            "Traccia 1000271184: Pasticceria Sweets / Prezzo Base 5000",
            "Traccia 1000271188: Spa Chalet-v / Trigger Budget 500€",
            "Traccia 1000271186: PC Assemblati / Utenti 2010"
        ]
    )

# --- 5. CONTENUTO DINAMICO BASATO SULLA FASE ---
st.markdown(f'<div class="navathe-box"><b>MODULO ATTIVO:</b> {fase}<br><b>BERSAGLIO:</b> {traccia_selezionata}</div>', unsafe_allow_html=True)

if "MODELLAZIONE" in fase:
    st.info("💡 FOCUS: Identifica le Entità forti, le Entità deboli e le cardinalità (1:N, N:N). Attenzione alle generalizzazioni totali/parziali.")
elif "ALGEBRA" in fase:
    st.warning("📐 REGOLA NAVATHE: Scomponi sempre. Prima Seleziona, poi Fai il Join, infine Proietta.")
    st.latex(r"R_1 \leftarrow \sigma_{condizione}(Tabella)")
    st.latex(r"R_2 \leftarrow R_1 \bowtie_{chiave} Tabella_2")
    st.latex(r"Risultato \leftarrow \pi_{attributi}(R_2)")
elif "SQL" in fase:
    st.success("🛡️ BLINDA LA QUERY: Ricorda il divieto di usare ORDER BY, ROWID o ROWNUM. Usa HAVING COUNT(*) >= ALL (...).")
elif "TRIGGER" in fase:
    st.error("⚡ DIFESA ATTIVA: Usa BEFORE INSERT/UPDATE. Gestisci i NULL con NVL() e solleva sempre RAISE_APPLICATION_ERROR.")
elif "TEORIA" in fase:
    st.info("🧠 DOMINIO CONCETTUALE: Preparati su Dipendenze Funzionali, Assiomi di Armstrong, Tipi UNIONE e Proprietà ACID.")

# --- 6. MOTORE CHAT E RAGIONAMENTO ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostra la cronologia
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Utente
user_input = st.chat_input("Incolla un pezzo della traccia, scrivi il tuo codice o chiedi come iniziare...")

if user_input:
    # Aggiungi e mostra messaggio utente
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Elaborazione AI
    with st.chat_message("assistant"):
        with st.spinner("Calcolo densità tecnica in corso..."):
            prompt_completo = f"""
            {SYSTEM_PROMPT}
            MODULO ATTIVO: {fase}
            TRACCIA DI RIFERIMENTO: {traccia_selezionata}
            INPUT STUDENTE: {user_input}
            """
            response = model.generate_content(prompt_completo)
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})

# Pulsante per pulire la lavagna
if st.sidebar.button("🧹 Pulisci Lavagna (Reset)"):
    st.session_state.chat_history = []
    st.rerun()
