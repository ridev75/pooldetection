import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from PIL import Image
import numpy as np
import tensorflow as tf
import io
import math
# --- CAMBIO 1: Importar el preprocesamiento específico de EfficientNetV2 ---
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input

# Configuración de la página al estilo "IA de Luján"
st.set_page_config(page_title="Geo-Detector de Piletas MASTER", layout="wide")

# 1. CARGA DEL MODELO (Actualizado al modelo Master)
@st.cache_resource
def load_model():
    # --- CAMBIO 2: Asegurate de que el nombre coincida con tu archivo descargado ---
    return tf.keras.models.load_model('modelo_piletas_master_v4.h5') 

model = load_model()

# 2. FUNCIONES MATEMÁTICAS (Sin cambios)
def get_tile_url(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{ytile}/{xtile}"

# 3. INTERFAZ DE USUARIO
st.title("🛰️ Escáner de Piletas - Versión MASTER 90%")
st.subheader("Detección de alta fidelidad para el Partido de Luján")

col1, col2 = st.columns([2, 1])

with col1:
    if 'center' not in st.session_state:
        st.session_state.center = [-34.5640, -59.1248]
    
    m = folium.Map(location=st.session_state.center, zoom_start=18, max_zoom=19)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satelital (Esri)',
        overlay=False,
        control=True
    ).add_to(m)

    map_data = st_folium(m, height=500, width=800, key="mapa_principal")

with col2:
    st.write("### Panel de Control")
    st.info("El modelo EfficientNetV2B0 está activo. Precisión esperada: 99% en positivos.")
    
    if st.button("🔍 Escanear Centro del Mapa", use_container_width=True):
        if map_data and map_data['center']:
            lat = map_data['center']['lat']
            lon = map_data['center']['lng']
            zoom = map_data['zoom']
            
            url = get_tile_url(lat, lon, zoom)
            response = requests.get(url)
            
            if response.status_code == 200:
                img = Image.open(io.BytesIO(response.content))
                st.image(img, caption="Vista Satelital", use_container_width=True)
                
                # --- CAMBIO 3: Preprocesamiento MASTER ---
                # Redimensionamos a 224x224
                img_resized = img.resize((224, 224))
                img_array = np.array(img_resized)
                
                # ¡IMPORTANTE! Quitamos el "/ 255.0" manual y usamos la función oficial
                # Esta función escala los datos exactamente como EfficientNet lo requiere
                img_array = preprocess_input(img_array) 
                img_array = np.expand_dims(img_array, axis=0)
                
                # 7. PREDICCIÓN
                prediction = model.predict(img_array)
                probabilidad = prediction[0][0]
                
                # --- CAMBIO 4: Umbral Optimizado ---
                # Usamos 0.52 que fue tu punto de mayor precisión (99%)
                umbral_master = 0.52 
                
                st.write("---")
                if probabilidad > umbral_master:
                    st.error(f"⚠️ ¡PILETA DETECTADA! (Confianza: {probabilidad:.2%})")
                    st.balloons()
                else:
                    st.success(f"✅ Zona despejada (Confianza: {1-probabilidad:.2%})")
            else:
                st.error("Error de conexión satelital.")