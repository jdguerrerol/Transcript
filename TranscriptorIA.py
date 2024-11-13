# Se descarga e instala Git y se configura Git dentro de la ruta

#import os

# Ruta de Git a agregar
#git_path1 = r'C:\Program Files\Git\mingw64\bin'
#git_path2 = r'C:\Program Files\Git\cmd'

# Agregar las rutas al PATH actual
#os.environ['PATH'] = git_path1 + os.pathsep + git_path2 + os.pathsep + os.environ['PATH']

# Verificar que se agregó correctamente
#print(os.environ['PATH'])

#!git --version


# abrir anaconda prompt
# cd C:\Users\LENOVO\Documents\Automatizacion BANCO
# streamlit run TranscriptorIA.py

'''
import streamlit as st
import whisper

st.title("Transcriptor de Audio")

audio_file=st.file_uploader("Cargar el audio",type=["wav","mp3","m4a"])
 
model=whisper.load_model("base")
st.text("Modelo Cargado")  

if st.sidebar.button("Transcribir audio"):
    if audio_file is not None:
        st.sidebar.success("Transcribiendo audio")
        transcription = model.transcribe(audio_file.name)
        st.sidebar.success("Transcripción completada")
        st.markdown(transcription["text"])
    else:
        st.sidebar.error("Cargue un archivo de audio")
        
st.sidebar.header("Reproducir audio")
st.sidebar.audio(audio_file)        

'''

import streamlit as st
import whisper
import tempfile
import os
from moviepy.editor import VideoFileClip
from io import StringIO

# Cargar el logo desde la ruta del archivo que has subido
st.sidebar.image("logo_BP.png", use_column_width=True)

st.title("Transcriptor de Audio y Video")

uploaded_file = st.file_uploader("Cargar archivo (audio o video)", type=["wav", "mp3", "m4a", "mp4"])

model = whisper.load_model("base")

st.text("Modelo Cargado")

if st.sidebar.button("Transcribir archivo"):
    if uploaded_file is not None:
        st.sidebar.success("Transcribiendo archivo")
        
        # Guardar el archivo en un archivo temporal para que Whisper pueda acceder a él
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
        
        # Extraer audio si el archivo es un video
        if uploaded_file.type == "video/mp4":
            with VideoFileClip(temp_file_path) as video:
                audio_path = tempfile.mktemp(suffix=".wav")
                video.audio.write_audiofile(audio_path)
            transcription = model.transcribe(audio_path)
            os.remove(audio_path)
        else:
            transcription = model.transcribe(temp_file_path)
        
        st.sidebar.success("Transcripción completada")
        st.markdown(transcription["text"])
        
        # Crear un enlace para descargar el archivo de texto
        txt_file = StringIO(transcription["text"])
        st.download_button(
            label="Descargar Transcripción",
            data=txt_file.getvalue(),
            file_name="transcription.txt",
            mime="text/plain"
        )
    else:
        st.sidebar.error("Cargue un archivo de audio o video")

st.sidebar.header("Reproducir archivo")
if uploaded_file is not None:
    st.sidebar.audio(uploaded_file)
