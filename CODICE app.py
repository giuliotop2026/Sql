import streamlit as st
import anthropic
import base64
from PIL import Image
import io
import streamlit.components.v1 as components

# --- 1. GRAFICA GOLDEN EYE (MASSIMO CONTRASTO) ---
st.markdown("""
    <style>
    .stApp { 
        background-color: #05140b; 
        background-image: radial-gradient(circle, #0e2a1d 0%, #05140b 100%);
        color: #ffffff; 
        font-family: 'Courier New', Courier, monospace; 
    }
    h1, h2, h3 { 
        color: #ffd700 !important; 
        text-transform: uppercase; 
        font-weight: 900; 
        text-shadow: 3px 3px 6px #000;
        border-bottom: 2px solid #ffd700;
    }
    .stAlert p {
        color: #ffffff !important;
        font-size: 1.3rem !important;
        line-height: 1.6 !important;
        text-shadow: 1px 1px 2px #000;
    }
    .stButton>button { 
        background-color: #8b0000 !important; 
        color: #ffffff !important; 
        border: 2px solid #ffd700 !important; 
        font-weight: bold; font-size: 1.5em; text-transform: uppercase;
        border-radius: 8px; height: 3.5em;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.7);
    }
    .stButton>button:hover { background-color: #ffd700 !important; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. RADAR ACUSTICO (GONG DELLA VITTORIA) ---
def play_victory_sound():
    audio_url = "https://www.myinstants.com/media/sounds/boxing-bell.mp3"
    sound_html = f'<audio autoplay><source src="{audio_url}" type="audio/mpeg"></audio>'
    components.html(sound_html, height=0, width=0)

# --- 3. CONNESSIONE AL CERVELLO CLAUDE ---
try:
    client_claude = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
except KeyError:
    st.error("☠️ MUNIZIONE CLAUDE MANCANTE!")
    st.stop()

st.title("🏇 SNIPER 42.0: THE CLAUDE SHIELD")
st.markdown("### *'Logica Sonnet 3.5. Granito 3.0 Attivo. Zero Errori.'*")

# --- 4. FUNZIONE CODIFICA IMMAGINE ---
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# --- 5. INTERFACCIA DI CACCIA ---
nazione = st.selectbox("🌍 TERRITORIO DI CACCIA:", [
    "UK", "IRLANDA", "USA", "ITALIA", "FRANCIA", "SUD AFRICA", "AUSTRALIA"
])

uploaded_files = st.file_uploader("📸 CARICA GLI SCREENSHOT DEL CAVEAU:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if st.button("🏁 ESEGUI PROTOCOLO GRANITO 3.0"):
    if not uploaded_files:
        st.warning("CARICA I POSTER, COMANDANTE!")
    else:
        with st.spinner("CLAUDE STA ANALIZZANDO L'ABISSO... ⏳"):
            try:
                # Codifica del primo file per la visione di Claude
                base64_img = encode_image(uploaded_files[0])
                media_type = f"image/{uploaded_files[0].type.split('/')[-1]}"

                # IL PROMPT DEFINITIVO (LOGICA BLINDATA) [cite: 2026-02-25]
                prompt_claude = f"""
                SISTEMA: PROTOCOLO GRANITO 3.0 - ANALISI MOLECOLARE.
                RUOLO: ANALISTA IPPICO SENIOR (BLUE LOCK PHILOSOPHY). [cite: 2026-01-19]
                SINTASSI: RIGOROSAMENTE IN MAIUSCOLO. [cite: 2026-01-20]
                NAZIONE: {nazione}

                FASE 1: SCANSIONE CINETICA
                Identifica ogni particella (#) e i relativi dati: RT (REC), GG, SEQ (ULTIMI ARRIVI).
                REGOLE SEQ: IL PRIMO NUMERO A SINISTRA È IL RISULTATO PIÙ RECENTE. [cite: 2026-02-20]

                FASE 2: FILTRI INVIOLABILI (PROCESSO DI ELIMINAZIONE) [cite: 2026-02-25]
                1. MURO FORMA: SCARTA CHI NON HA 1 O 2 COME PRIMO NUMERO A SINISTRA.
                2. FILTRO RUGGINE: GG DEVE ESSERE < 45. SE MANCANTE O > 45, ELIMINA.
                3. SE MAIDEN: ACCETTA SOLO SEQ '1', GG < 15 E GAP RT >= 5 RISPETTO AL SECONDO.

                FASE 3: DENSITÀ TECNICA (POLMONI D'ACCIAIO) [cite: 2026-02-18]
                IGNORA LE QUOTE. IDENTIFICA IL SECONDO MIGLIORE PER DENSITÀ TECNICA CHE SCHIACCIA IL FAVORITO DI CARTA. [cite: 2026-02-20]

                REFERTO FINALE:
                '🏆 SACRO GRAAL INDIVIDUATO: PARTICELLA [NUMERO #]' (O 'NESSUN SACRO GRAAL')
                'PIANO DI CORSA: [ANALISI DETTAGLIATA DELLA SUPERIORITÀ TECNICA].'
                'BULLONE SERRATO: [CONFERMA REQUISITI SUPERATI].'
                """

                # Chiamata API Anthropic
                response = client_claude.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": base64_img}},
                            {"type": "text", "text": prompt_claude}
                        ]
                    }]
                )
                
                sentenza = response.content[0].text
                st.info(sentenza)
                
                # REAZIONE ALLA GLORIA
                if "SACRO GRAAL" in sentenza.upper() and "NESSUN" not in sentenza.upper():
                    play_victory_sound()
                    st.balloons()
                    st.success("✅ OBIETTIVO IDENTIFICATO. PROCEDERE AL MERCATO.")
                    
            except Exception as e:
                st.error(f"☠️ ERRORE DI INFILTRAZIONE: {e}")
