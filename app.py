import streamlit as st
import tensorflow as tf
from keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Clasificador ImageNet (Imagenette)",
    page_icon="🖼️",
    layout="centered"
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

# Interfaz gráfica
st.title("🖼️ Clasificador de Imágenes CNN")
st.caption("Transfer Learning con MobileNetV2 entrenado en el subconjunto Imagenette (ImageNet)")

st.write("Sube una imagen para realizar la inferencia y visualizar las probabilidades predichas.")

# Componente para subir archivo
archivo_subido = st.file_uploader("Selecciona una imagen (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])

if archivo_subido is not None:
    # Cargar y mostrar la imagen original
    imagen_pil = Image.open(archivo_subido).convert('RGB')
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Imagen subida")
        st.image(imagen_pil, use_container_width=True)
    
    # 2. Preprocesamiento de la imagen nueva
    # Redimensionar a 224x224
    img_resized = imagen_pil.resize((224, 224))
    img_array = np.array(img_resized, dtype=np.float32)
    
    # Normalización oficial MobileNetV2 [-1, 1]
    img_preprocessed = preprocess_input(img_array)
    
    # Expandir dimensión para simular el batch: (224, 224, 3) -> (1, 224, 224, 3)
    img_batch = np.expand_dims(img_preprocessed, axis=0)
    
    # 3. Inferencia con el modelo
    with st.spinner("Clasificando imagen..."):
        predicciones = model.predict(img_batch)[0]
    
    idx_pred = np.argmax(predicciones)
    clase_detectada = NOMBRES_CLASES[idx_pred]
    confianza = predicciones[idx_pred] * 100
    
    with col2:
        st.subheader("Resultado de Inferencia")
        st.success(f"**Predicción:** {clase_detectada}")
        st.metric(label="Nivel de Confianza", value=f"{confianza:.2f}%")
    
    st.divider()
    
    # 4. Visualización de probabilidades por clase
    st.subheader("📊 Distribución de Confianza entre Clases")
    
    # Preparar datos para st.bar_chart
    datos_probabilidades = {
        clase: float(prob * 100)
        for clase, prob in zip(NOMBRES_CLASES, predicciones)
    }
    
    st.bar_chart(datos_probabilidades)