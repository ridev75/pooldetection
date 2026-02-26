import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

# Configuración de la interfaz
st.set_page_config(page_title="Detector de Piletas - Luján AI", layout="centered")

# 1. Cargar el modelo con cache para optimizar rendimiento
@st.cache_resource
def load_model():
    # El archivo debe estar en la misma carpeta que este script
    return tf.keras.models.load_model('modelo_piletas.h5')

with st.spinner('Cargando cerebro artificial...'):
    model = load_model()

st.title("🛰️ Clasificador de Piletas")
st.write("Subí una captura satelital para verificar si el modelo detecta una piscina.")

# 2. Función de Predicción (Aquí es donde agregamos la corrección de canales)
def import_and_predict(image_data, model):
    # Definimos el tamaño exacto usado en el entrenamiento
    size = (224, 224)    
    
    # --- LÍNEA CLAVE: Convertimos a RGB para pasar de 4 canales (RGBA) a 3 ---
    image_rgb = image_data.convert('RGB')
    
    # Redimensionamos la imagen
    image_resized = ImageOps.fit(image_rgb, size, Image.LANCZOS)
    img_array = np.asarray(image_resized)
    
    # Normalización: (img / 255.0) como en la celda 13 de tu notebook
    img_reshape = img_array.astype('float32') / 255.0
    img_reshape = np.expand_dims(img_reshape, axis=0) 
    
    prediction = model.predict(img_reshape)
    return prediction

# 3. Lógica de carga de archivos
file = st.file_uploader("Selecciona una imagen", type=["jpg", "png", "jpeg"])

if file is not None:
    image = Image.open(file)
    st.image(image, caption='Imagen cargada', use_container_width=True)
    
    if st.button("Analizar"):
        # Llamamos a la función corregida
        prediction = import_and_predict(image, model)
        probabilidad = prediction[0][0]
        
        st.subheader("Resultado:")
        if probabilidad > 0.5:
            st.success(f"✅ Piscina detectada (Confianza: {probabilidad:.2%})")
        else:
            st.error(f"❌ No se detectó piscina (Confianza: {(1-probabilidad):.2%})")
        
        st.progress(float(probabilidad))