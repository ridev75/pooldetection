# 🛰️ Detector de Piscinas en Imágenes Satelitales

Este proyecto utiliza **Deep Learning** para identificar la presencia de piscinas en capturas satelitales. Fue desarrollado como parte de la **Diplomatura en Desarrollo de Soluciones de IA en la Nube**.

## 🧠 El Modelo
Se empleó **Transfer Learning** con la arquitectura **MobileNetV2** preentrenada en ImageNet. 
- **Entrada:** Imágenes RGB de 224x224 píxeles.
- **Exactitud (Accuracy):** 81% en el set de validación.
- **Frameworks:** TensorFlow / Keras.

## 💻 Tecnologías utilizadas
- **Python 3.12**
- **Streamlit** (Interfaz de usuario)
- **Docker / Podman** (Contenedorización)
- **Fedora Linux** (Entorno de desarrollo)

## 🚀 Cómo ejecutarlo

### Localmente (con venv)
1. Clonar el repositorio.
2. Crear un venv y activar: `python3.12 -m venv venv && source venv/bin/activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Correr: `streamlit run app.py`

### Con Docker/Podman
1. Construir la imagen: `docker build -t detector-piletas:v1 .`
2. Ejecutar: `docker-compose up`

---
Desarrollado por **Ricardo Castiñeira** - Luján, Argentina. 🇦🇷