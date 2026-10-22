import streamlit as st
import os
import time
import glob
import base64
from gtts import gTTS

st.title("Conversión de Texto a Audio")
st.image(
    "https://media.elcomercio.com/wp-content/uploads/2026/05/db96b4aa3439c3329f869932a22672e1-1024x683.jpg",
    width=350
)

with st.sidebar:
    st.subheader("Escribe y/o selecciona texto para ser escuchado.")

try:
    os.mkdir("temp")
except FileExistsError:
    pass

st.subheader("Una pequeña Fábula.")
st.write('¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. '
         'Corría y corría y por cierto que me alegraba ver esos muros, a diestra y siniestra, en la distancia. '
         'Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está '
         'la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo dijo el gato...y se lo comió. '
         ' '
         'Franz Kafka.'
         )

st.markdown("¿Quieres escucharlo? Copia el texto")
text = st.text_area("Ingrese el texto a escuchar.")

option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English"))
if option_lang == "Español":
    lg = 'es'
if option_lang == "English":
    lg = 'en'


def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]
    except Exception:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text


def get_binary_file_downloader_html(data, file_name, file_label='File'):
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_name}">Descargar {file_label}</a>'
    return href


if st.button("Convertir a Audio"):
    if not text.strip():
        st.warning("Primero escribe o pega un texto.")
    else:
        result, output_text = text_to_speech(text, 'com', lg)
        with open(f"temp/{result}.mp3", "rb") as f:
            audio_bytes = f.read()

        st.markdown("## Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        st.markdown(
            get_binary_file_downloader_html(audio_bytes, "audio.mp3", file_label="Audio"),
            unsafe_allow_html=True
        )


def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)
