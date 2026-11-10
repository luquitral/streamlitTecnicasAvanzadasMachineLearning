import streamlit as st
import tensorflow as tf
from keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import numpy as np
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Clasificador ImageNet (Imagenette)",
    page_icon="🖼️",
    layout="wide"
)

# 1. Cargar el modelo en memoria (usando cache para evitar recargarlo en cada interacción)
@st.cache_resource
def cargar_modelo():
    return tf.keras.models.load_model("modelo_imagenette_mobilenet.keras")

with st.spinner("Cargando red neuronal convolucional MobileNetV2..."):
    model = cargar_modelo()

# Nombres de las 10 clases en el orden exacto del entrenamiento
NOMBRES_CLASES = [
    'Pez (Tenca)',
    'Perro (Canino)',
    'Casete de Audio',
    'Motosierra',
    'Iglesia / Catedral',
    'Corno Francés',
    'Camión de Basura',
    'Surtidor de Bencina',
    'Pelota de Golf',
    'Paracaídas'
]

# Panel lateral con información técnica del modelo
with st.sidebar:
    st.header("ℹ️ Ficha Técnica del Modelo")
    st.markdown("""
    - **Arquitectura Base:** MobileNetV2
    - **Técnica:** *Transfer Learning* (Fine-tuning)
    - **Resolución de entrada:** 224 × 224 px (RGB)
    - **Normalización:** Intervalo $[-1, 1]$
    - **Dataset:** Imagenette (Subconjunto de 10 clases de ImageNet)
    """)
    st.divider()
    st.subheader("📋 Clases Reconocidas (10)")
    for i, clase in enumerate(NOMBRES_CLASES, start=1):
        st.caption(f"**{i}.** {clase}")

# Interfaz gráfica principal
st.title("🖼️ Clasificador de Imágenes CNN")
st.caption("Transfer Learning con MobileNetV2 entrenado en el subconjunto Imagenette (ImageNet)")

st.write("Sube una imagen en formato JPG, JPEG o PNG para realizar la inferencia y visualizar las probabilidades predichas.")

# Componente para subir archivo
archivo_subido = st.file_uploader("Selecciona una imagen...", type=["jpg", "jpeg", "png"])

if archivo_subido is not None:
    # Cargar imagen original
    imagen_pil = Image.open(archivo_subido).convert('RGB')
    
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.subheader("📷 Imagen de Entrada")
        st.image(imagen_pil, width="stretch")
    
    # 2. Preprocesamiento de la imagen
    # Redimensionar a 224x224 requerido por MobileNetV2
    img_resized = imagen_pil.resize((224, 224))
    img_array = np.array(img_resized, dtype=np.float32)
    
    # Normalización oficial MobileNetV2 [-1, 1]
    img_preprocessed = preprocess_input(img_array)
    
    # Expandir dimensión para simular el batch: (224, 224, 3) -> (1, 224, 224, 3)
    img_batch = np.expand_dims(img_preprocessed, axis=0)
    
    # 3. Inferencia con el modelo
    with st.spinner("Clasificando imagen con MobileNetV2..."):
        predicciones = model.predict(img_batch)[0]
    
    # Índices ordenados de mayor a menor probabilidad
    indices_ordenados = np.argsort(predicciones)[::-1]
    idx_top1 = indices_ordenados[0]
    clase_top1 = NOMBRES_CLASES[idx_top1]
    confianza_top1 = predicciones[idx_top1] * 100
    
    with col2:
        st.subheader("🎯 Resultado de Inferencia")
        st.success(f"**Predicción Principal:** {clase_top1}")
        st.metric(label="Nivel de Confianza (Top-1)", value=f"{confianza_top1:.2f}%")
        
        st.markdown("#### 🏆 Top-3 Clases Más Probables")
        for rank, idx in enumerate(indices_ordenados[:3], start=1):
            prob = float(predicciones[idx])
            col_txt, col_bar = st.columns([2, 3])
            with col_txt:
                st.write(f"**#{rank}** {NOMBRES_CLASES[idx]}")
            with col_bar:
                st.progress(prob, text=f"{prob * 100:.2f}%")
    
    st.divider()
    
    # 4. Visualización de probabilidades ordenada
    st.subheader("📊 Distribución Completa de Confianza")
    
    df_probabilidades = pd.DataFrame({
        "Clase": [NOMBRES_CLASES[i] for i in indices_ordenados],
        "Confianza (%)": [float(predicciones[i] * 100) for i in indices_ordenados]
    }).set_index("Clase")
    
    st.bar_chart(df_probabilidades)
    
    with st.expander("🔍 Ver tabla detallada de probabilidades"):
        st.dataframe(df_probabilidades.style.format({"Confianza (%)": "{:.2f}%"}), width="stretch")
