import streamlit as st
import anthropic
import base64
from PIL import Image
import io
import streamlit.components.v1 as components

# --- 1. GRAFICA 'SALOON EL GRANITO' (MASSIMO CONTRASTO) ---
st.markdown("""
    <style>
    .stApp { 
        background-color: #2b1d0e; 
        background-image: url("https://www.transparenttextures.com/patterns/wood-pattern.png");
        color: #d4c4a9; 
        font-family: 'Courier New', Courier, monospace; 
    }
    h1, h2, h3 { 
        color: #ffcc00 !important; 
        text-transform: uppercase; 
        font-weight: 900; 
        text-shadow: 2px 2px 4px #000;
        border-bottom: 3px solid #8b4513;
    }
    .stAlert p { 
        color: #ffffff !important; 
        font-size: 1.6rem !important; 
        font-weight: bold; 
        text-shadow: 1px 1px 2px #000;
    }
    .stButton>button { 
        background-color: #8b4513 !important; 
        color: #ffcc00 !important; 
        border: 3px solid #ffcc00 !important; 
        font-weight: bold; font-size: 1.6em; text-transform: uppercase;
        width: 100%; border-radius: 12px; height: 4em;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.6);
    }
    .stButton>button:hover { background-color: #ffcc00 !important; color: #2b1d0e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. RADAR ACUSTICO (IL GONG DEL DUELLO) ---
def play_victory_sound():
    audio_url = "https://www.myinstants.com/media/sounds/boxing-bell.mp3"
    components.html(f'<audio autoplay><source src="{audio_url}" type="audio/mpeg"></audio>', height=0, width=0)

# --- 3. CONNESSIONE AL CERVELLO CLAUDE ---
try:
    client_claude = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
except KeyError:
    st.error("☠️ EHI PARTNER! MANCANO LE MUNIZIONI NEL FILE SECRETS (CLAUDE_API_KEY)!")
    st.stop()

st.title("🌵 SALOON 'EL GRANITO' 🌵")
st.markdown("### *'Legge dello Sceriffo 3.0. Niente chiacchiere, solo piombo.'*")

# --- 4. FUNZIONE CODIFICA ---
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# --- 5. BACHECA DEI RICERCATI ---
nazione = st.selectbox("🗺️ TERRITORIO DI CACCIA:", ["UK", "IRLANDA", "USA", "ITALIA", "FRANCIA", "SUD AFRICA", "AUSTRALIA"])
uploaded_files = st.file_uploader("📜 AFFIGGI I MANIFESTI (SCREENSHOT STATISTICHE):", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.markdown("### 🧐 SOSPETTATI IN BACHECA:")
    cols = st.columns(len(uploaded_files))
    for i, file in enumerate(uploaded_files):
        with cols[i]:
            st.image(file, caption=f"Manifesto #{i+1}", use_column_width=True)

# --- 6. IL GRILLETTO (PROTOCOLLO BLUE LOCK) ---
if st.button("🤠 SCATENA IL PISTOLERO (ANALIZZA)"):
    if not uploaded_files:
        st.warning("EHI STRANIERO, CARICA I MANIFESTI PRIMA DI SPARARE!")
    else:
        with st.spinner("CLAUDE STA PRENDENDO LA MIRA... ⏳"):
            try:
                # Carichiamo tutti i manifesti nel caricatore di Claude
                content_list = []
                for file in uploaded_files:
                    b64_img = encode_image(file)
                    m_type = f"image/{file.type.split('/')[-1]}"
                    content_list.append({"type": "image", "source": {"type": "base64", "media_type": m_type, "data": b64_img}})
                
                # ISTRUZIONI SPIETATE [cite: 2026-02-25]
                prompt_claude = f"""
                SEI IL PISTOLERO DEL 'PROGETTO BLUE LOCK'. SINTASSI: RIGOROSAMENTE IN MAIUSCOLO. [cite: 2026-01-20]
                NAZIONE: {nazione}

                REGOLE DEL GRANITO (FILTRI INVIOLABILI):
                1. MURO FORMA: SEQ deve iniziare con 1 o 2. [cite: 2026-02-25]
                2. FILTRO RUGGINE: GG < 45. [cite: 2026-02-25]
                3. SE MAIDEN: Accetta solo SEQ 1 e GG < 15. [cite: 2026-02-25]
                4. DENSITÀ TECNICA: Identifica i 'Polmoni d'Acciaio' (RT/REC). [cite: 2026-02-18, 2026-02-20]

                ORDINE DELLO SCERIFFO:
                NON FARE DISCORSI. NON SPIEGARE I FILTRI. DAI SOLO IL NOME E IL NUMERO.
                
                SE TROVI IL SACRO GRAAL:
                '💰 TAGLIA RISCOSSA: PISTOLERO [NUMERO #] - [NOME]'
                'BULLONE SERRATO: [Motivazione di una riga].'
                
                SE NON C'È NULLA:
                '🌵 NESSUNA PEPITA D'ORO IN QUESTO FIUME.'
                """
                content_list.append({"type": "text", "text": prompt_claude})

                response = client_claude.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=500,
                    messages=[{"role": "user", "content": content_list}]
                )
                
                sentenza = response.content[0].text
                st.info(sentenza)
                
                if "TAGLIA" in sentenza.upper() and "NESSUNA" not in sentenza.upper():
                    play_victory_sound(); st.balloons()
            except Exception as e:
                st.error(f"☠️ SERPENTE NELLO STIVALE (ERRORE): {e}")
                
