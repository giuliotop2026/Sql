import streamlit as st
import anthropic
import base64
from PIL import Image
import io
import streamlit.components.v1 as components

# --- 1. GRAFICA WESTERN CHIARO (SALOON MEZZOGIORNO DI FUOCO) ---
st.markdown("""
    <style>
    /* Sfondo chiaro: Pergamena / Sabbia del deserto */
    .stApp { 
        background-color: #f4e4bc; 
        background-image: url("https://www.transparenttextures.com/patterns/aged-paper.png"); /* Texture carta invecchiata opzionale */
        color: #3d2b1f; /* Testo marrone scuro/sepia per contrasto */
        font-family: 'Courier New', Courier, monospace; 
    }
    
    /* Titoli: Legno bruciato / Cuoio scuro */
    h1, h2, h3 { 
        color: #8b4513 !important; /* Saddle Brown */
        text-transform: uppercase; 
        font-weight: 900; 
        text-shadow: 1px 1px 2px #cda26e; /* Ombra chiara per profondità */
        border-bottom: 3px solid #5a3a22; /* Bordo scuro */
    }
    
    /* Testo all'interno degli Alert (es. il referto) */
    .stAlert p {
        color: #3d2b1f !important; /* Testo scuro per leggere bene su sfondo chiaro */
        font-size: 1.3rem !important;
        line-height: 1.6 !important;
        font-weight: bold;
    }
    
    /* Bottone: Stile Cuoio Sella */
    .stButton>button { 
        background-color: #a0522d !important; /* Sienna (Cuoio rossiccio) */
        color: #fff8dc !important; /* Testo Crema/Bianco sporco */
        border: 3px solid #5a3a22 !important; /* Bordo marrone scuro */
        font-weight: bold; font-size: 1.5em; text-transform: uppercase;
        border-radius: 8px; height: 3.5em;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    
    /* Hover Bottone: Diventa cuoio più scuro */
    .stButton>button:hover { 
        background-color: #8b4513 !important; /* Saddle Brown al passaggio */
        color: #ffd700 !important; /* Testo oro al passaggio */
        border-color: #ffd700 !important;
    }
    
    /* Personalizzazione Selectbox e File Uploader per coerenza */
    .stSelectbox label, .stFileUploader label {
        color: #8b4513 !important;
        font-weight: bold;
    }
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
    st.error("☠️ EHI PARTNER! MANCANO LE MUNIZIONI (CLAUDE_API_KEY)!")
    st.stop()

# --- TITOLI AGGIORNATI AL TEMA WESTERN ---
st.title("🤠 SALOON 'EL GRANITO' - CACCIA ALL'ORO")
st.markdown("### *'Sole alto, pistole cariche. Il protocollo dello Sceriffo Claude.'*")

# --- 4. FUNZIONE CODIFICA IMMAGINE ---
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# --- 5. INTERFACCIA DI CACCIA ---
nazione = st.selectbox("🗺️ TERRITORIO DI FRONTIERA:", [
    "UK", "IRLANDA", "USA", "ITALIA", "FRANCIA", "SUD AFRICA", "AUSTRALIA"
])

uploaded_files = st.file_uploader("📜 AFFIGGI I MANIFESTI DEI RICERCATI (SCREENSHOT):", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if st.button("🐎 SCATENA IL PISTOLERO (ESEGUI PROTOCOLLO)"):
    if not uploaded_files:
        st.warning("EHI STRANIERO, CARICA I MANIFESTI PRIMA DI SPARARE!")
    else:
        with st.spinner("LO SCERIFFO CLAUDE STA PRENDENDO LA MIRA... ⏳"):
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
                
                # Visualizzazione del referto (lo stile è gestito dal CSS sopra)
                st.info(sentenza)
                
                # REAZIONE ALLA GLORIA
                if "SACRO GRAAL" in sentenza.upper() and "NESSUN" not in sentenza.upper():
                    play_victory_sound()
                    st.balloons()
                    st.success("✅ TAGLIA RISCOSSA! OBIETTIVO IDENTIFICATO.")
                    
            except Exception as e:
                st.error(f"☠️ SERPENTE NELLO STIVALE (ERRORE): {e}")
                
