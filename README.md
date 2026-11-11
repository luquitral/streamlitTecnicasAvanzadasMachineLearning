# Clasificación de Imágenes con CNN y Transfer Learning (Imagenette)

Aplicación de visión por computadora que clasifica imágenes mediante una red
convolucional basada en **MobileNetV2**, utilizando *Transfer Learning* sobre
el subconjunto **Imagenette** de ImageNet.

El proyecto incluye el modelo entrenado y una aplicación web interactiva en
**Streamlit**. El usuario puede subir una imagen JPG, JPEG o PNG y ver la
predicción principal, su nivel de confianza, las tres clases más probables y
la distribución completa de probabilidades.

## Características principales

- **Arquitectura:** MobileNetV2 preentrenada en ImageNet.
- **Entrenamiento:** dos fases:
  1. *Feature Extraction* con las capas base congeladas.
  2. *Fine-Tuning* de las últimas 30 capas convolucionales con un *learning
     rate* bajo.
- **Dataset:** Imagenette de 320 px, con 10 clases.
- **División de datos:** 70 % entrenamiento (9.372 imágenes), 15 %
  validación y 15 % prueba aislada.
- **Evaluación:** accuracy, precision, recall, F1-score, matriz de confusión y
  análisis de errores.
- **Inferencia:** procesamiento RGB a 224 x 224 px y normalización MobileNetV2
  al intervalo `[-1, 1]`.
- **Despliegue:** aplicación Streamlit lista para ejecutarse localmente.

## Clases reconocidas

1. Pez (Tenca)
2. Perro (Canino)
3. Casete de Audio
4. Motosierra
5. Iglesia / Catedral
6. Corno Francés
7. Camión de Basura
8. Surtidor de Bencina
9. Pelota de Golf
10. Paracaídas

## Requisitos

- Git.
- Python 3.9 o superior. Se recomienda Python 3.10, 3.11 o 3.12.
- Conexión a Internet para instalar las dependencias.
- Aproximadamente 2 GB de espacio libre para las dependencias.
- El archivo `modelo_imagenette_mobilenet.keras`, incluido en este repositorio,
  ocupa aproximadamente 21 MB.

> La ejecución utiliza CPU por defecto. TensorFlow puede tardar unos segundos
> en iniciar y en realizar la primera predicción.

## Instalación desde cero

### 1. Clonar el repositorio

```bash
git clone https://github.com/luquitral/streamlitTecnicasAvanzadasMachineLearning.git
cd streamlitTecnicasAvanzadasMachineLearning
```

### 2. Crear un entorno virtual

#### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecuta una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Después vuelve a ejecutar:

```powershell
.\.venv\Scripts\Activate.ps1
```

#### macOS o Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

Con el entorno virtual activado:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecutar la aplicación

Desde la carpeta raíz del proyecto y con el entorno virtual activado:

```bash
python -m streamlit run app.py
```

Luego abre en el navegador la dirección que indique Streamlit, normalmente:

```text
http://localhost:8501
```

### Atajo en Windows

También puedes hacer doble clic en `run.bat`. El lanzador busca
automáticamente un entorno virtual llamado `.venv` o `venv` y abre la
aplicación en el puerto `8501`; no es necesario activar el entorno previamente.

Si no existe ninguno de esos entornos, créalo e instala las dependencias con:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

El lanzador mantiene abierta la ventana si ocurre un error para que puedas
leer el mensaje mostrado.

## Uso

1. Inicia Streamlit.
2. Abre `http://localhost:8501`.
3. Selecciona una imagen JPG, JPEG o PNG.
4. Revisa la clase predicha y el porcentaje de confianza.
5. Consulta el Top-3 y el gráfico de probabilidades.

La aplicación carga el modelo solamente cuando se sube una imagen, por lo que
la pantalla inicial aparece más rápido. Después de la primera carga,
`st.cache_resource` reutiliza el modelo mientras la aplicación esté activa.

## Estructura del proyecto

```text
.
├── app.py                              # Interfaz Streamlit e inferencia
├── modelo_imagenette_mobilenet.keras   # Modelo entrenado
├── requirements.txt                    # Dependencias Python
├── run.bat                             # Atajo de ejecución para Windows
├── .gitignore                          # Archivos excluidos de Git
└── README.md                           # Documentación
```

## Solución de problemas

### No se encuentra el modelo

Comprueba que `modelo_imagenette_mobilenet.keras` exista en la misma carpeta
que `app.py`. La aplicación construye la ruta a partir de la ubicación del
script, por lo que no es necesario copiar el modelo a otra carpeta.

### `streamlit` no se reconoce

Activa el entorno virtual y ejecuta:

```bash
python -m streamlit run app.py
```

Usar `python -m streamlit` garantiza que se utilice el Streamlit instalado en
el entorno virtual correcto.

### `run.bat` no inicia la aplicación

Comprueba que estés ejecutando el archivo desde la carpeta raíz del proyecto y
que exista `.venv\Scripts\python.exe` o `venv\Scripts\python.exe`. Si no
existe, crea el entorno siguiendo las instrucciones de instalación. También
puedes iniciar la aplicación manualmente con:

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\app.py --server.port 8501
```

### Error al instalar TensorFlow en Windows

Verifica que estés usando Python de 64 bits y una versión compatible. Se
recomienda crear un entorno nuevo con Python 3.10, 3.11 o 3.12 y repetir la
instalación:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### La aplicación queda cargando

La primera carga de TensorFlow y del modelo puede tardar. Espera unos
segundos y revisa la ventana de `run.bat`. Si la página no aparece, detén el
proceso con `Ctrl+C` y vuelve a iniciar la aplicación desde la carpeta raíz
del repositorio.

## Nota sobre Git y el modelo

El modelo `.keras` está incluido para que el proyecto funcione inmediatamente
después de clonar. No se deben subir los entornos virtuales `.venv` ni `venv`
al repositorio; las dependencias se reconstruyen usando `requirements.txt`.

## Licencia

Este repositorio es un proyecto académico. Revisa las licencias de
TensorFlow, Keras, MobileNetV2 e Imagenette antes de redistribuirlo fuera de
un contexto académico.
