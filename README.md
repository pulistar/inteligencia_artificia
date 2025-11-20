# 🍎 Sistema Completo de Clasificación de Alimentos 

## 📖 Documentación Técnica Completa

Un sistema integral de inteligencia artificial que combina **Machine Learning**, **Computer Vision**, **APIs REST** y **Asistentes Conversacionales** para la clasificación automática de alimentos y consulta nutricional inteligente.


### 🎯 ¿Qué hace este sistema?

Este proyecto implementa una solución completa que permite:

1. **📸 Subir una foto de alimento** → El sistema la analiza con IA
2. **🤖 Obtener clasificación automática** → Identifica qué alimento es con % de confianza  
3. **📊 Consultar información nutricional** → Calorías, proteínas, carbohidratos, etc.
4. **💬 Chatear con asistente IA** → Preguntas sobre nutrición respondidas por Gemini AI

### 🏗️ Arquitectura del Sistema Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    SISTEMA COMPLETO DE IA                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
        │   FRONTEND   │ │   BACKEND   │ │ ASISTENTE  │
        │   (React)    │ │  (FastAPI)  │ │  GEMINI    │
        │ Puerto: 3000 │ │Puerto: 8000 │ │Puerto: 5001│
        └──────────────┘ └─────────────┘ └────────────┘
                │               │               │
        ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
        │ Interfaz Web │ │ Modelo ML   │ │ Google AI  │
        │   Moderna    │ │TensorFlow   │ │  Gemini    │
        │   (Vite)     │ │   (.h5)     │ │    API     │
        └──────────────┘ └─────────────┘ └────────────┘
```

## 🔬 Proceso Completo de Desarrollo - Paso a Paso

### **PASO 1: Entrenamiento del Modelo de Machine Learning** 🧠

#### 1.1 Preparación del Dataset
- **Ubicación**: `entrenamineto/clasificador_alimentos.py`
- **20 clases de alimentos**: Apple, Banana, Orange, Tomato, Carrot, Cucumber, Onion, Peach, Pear, Cherry, Grape, Pepper, Potato, Avocado, Mango, Strawberry, Lemon, Watermelon, Corn, Eggplant

**Estructura esperada del dataset: https://www.kaggle.com/datasets/moltean/fruits**:
```
dataset/
├── Training/
│   ├── Apple 10/
│   ├── Banana 1/
│   ├── Orange 1/
│   └── ... (17 clases más)
└── Test/
    ├── Apple 10/
    ├── Banana 1/
    └── ... (17 clases más)
```

#### 1.2 Arquitectura del Modelo
```python
# Transfer Learning con MobileNetV2
Base Model: MobileNetV2 (preentrenado en ImageNet)
├── GlobalAveragePooling2D()
├── Dropout(0.2)
├── Dense(256, activation='relu')
├── Dropout(0.2)
└── Dense(20, activation='softmax')  # 20 clases de salida
```

#### 1.3 Técnicas de Optimización Implementadas
- **Data Augmentation**: Rotación, zoom, flip horizontal, desplazamientos
- **Transfer Learning**: MobileNetV2 como base congelada
- **Callbacks inteligentes**:
  - `EarlyStopping`: Para evitar overfitting
  - `ReduceLROnPlateau`: Reduce learning rate automáticamente
  - `ModelCheckpoint`: Guarda el mejor modelo automáticamente
- **Generadores de datos**: No carga todo en memoria (eficiente)

#### 1.4 Proceso de Entrenamiento
```bash
# Ejecutar entrenamiento
python entrenamineto/clasificador_alimentos.py

# Archivos generados:
# - best_model_20_clases.h5 (modelo entrenado)
# - classes.txt (lista de clases)
# - modelo.h5 (backup del modelo)
```

### **PASO 2: Desarrollo del Backend API** ⚙️

#### 2.1 API Principal (FastAPI)
- **Ubicación**: `backend/main.py`
- **Puerto**: 8000

**Endpoint de Predicción**:
```python
POST /predict
# Recibe: imagen (multipart/form-data)
# Devuelve: {"clase": "Apple 10", "probabilidad": 95.67}
```

**Endpoint de Chat Nutricional**:
```python
POST /chat  
# Recibe: {"message": "¿Cuántas calorías tiene una manzana?"}
# Devuelve: {"response": "Información nutricional detallada..."}
```

#### 2.2 Procesamiento de Imágenes
```python
def preprocess_image(image_bytes):
    # 1. Convertir bytes a imagen PIL
    # 2. Convertir a RGB
    # 3. Redimensionar a 224x224
    # 4. Normalizar (0-1)
    # 5. Expandir dimensiones para batch
    return processed_image
```

### **PASO 3: Asistente Conversacional con Gemini AI** 🤖

#### 3.1 Servidor Flask Especializado
- **Ubicación**: `asistente-gemini/app.py`
- **Puerto**: 5001
- **Modelo**: Google Gemini 2.5 Flash

#### 3.2 Funcionalidades del Asistente
```python
# Endpoints disponibles:
GET  /test     # Prueba de conectividad
GET  /models   # Lista modelos disponibles  
POST /chat     # Chat inteligente
```

### **PASO 4: Frontend Moderno en React** 🎨

#### 4.1 Arquitectura del Frontend
- **Framework**: React 18.2.0 con Hooks
- **Build Tool**: Vite 5.0.8 (Hot Module Replacement)
- **Puerto**: 3000
- **Estructura**: Componentes modulares y reutilizables

#### 4.2 Componentes Principales

**App.jsx** - Componente Principal:
```jsx
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Clasificación de Alimentos para Asistentes de Nutrición</h1>
      </header>
      <main className="App-main">
        <div className="sections-container">
          <ImageClassifier />      // Clasificador de imágenes
          <NutritionChatbot />     // Chat nutricional básico
        </div>
      </main>
      <GeminiChat />             // Chat flotante con Gemini AI
    </div>
  )
}
```

**ImageClassifier.jsx** - Clasificador de Imágenes:
```jsx
// Estados del componente
const [selectedFile, setSelectedFile] = useState(null)
const [previewUrl, setPreviewUrl] = useState(null)
const [result, setResult] = useState(null)
const [loading, setLoading] = useState(false)

// Funcionalidades:
// - Selección de archivos de imagen
// - Preview de imagen antes de clasificar
// - Llamada a API de predicción
// - Mostrar resultados con clase y probabilidad
```

**GeminiChat.jsx** - Chat Inteligente:
```jsx
// Estados del componente
const [isOpen, setIsOpen] = useState(false)
const [messages, setMessages] = useState([...])
const [inputMessage, setInputMessage] = useState('')
const [isLoading, setIsLoading] = useState(false)

// Funcionalidades:
// - Chat modal flotante
// - Historial de mensajes
// - Indicador de escritura
// - Conexión directa con Gemini API
```

**api.js** - Servicios de API:
```javascript
// Predicción de imágenes
export const predictImage = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  // POST a http://localhost:8000/predict
}

// Chat nutricional
export const sendChatMessage = async (message) => {
  // POST a http://localhost:8000/chat
}
```

#### 4.3 Funcionalidades de la Interfaz
- **Subida de imágenes**: Input file con preview automático
- **Clasificación en tiempo real**: Botón de clasificar con loading state
- **Resultados visuales**: Clase predicha + porcentaje de confianza
- **Chat flotante**: Modal con Gemini AI integrado
- **Historial de chat**: Mensajes persistentes durante la sesión
- **Indicadores visuales**: Loading, typing indicators, estados de error
- **Diseño responsive**: CSS Grid y Flexbox para adaptabilidad

## 📦 Estructura Completa del Proyecto

```
inteligenicaArtificial/
├── 📁 backend/                      # 🔧 API FastAPI - Servidor Principal
│   ├── main.py                     # Servidor FastAPI con endpoints
│   ├── asistente_ia.py             # Módulo adicional de IA (10KB)
│   ├── best_model_20_clases.h5     # Modelo TensorFlow entrenado (13MB)
│   ├── classes.txt                 # Lista de 20 clases de alimentos
│   └── requirements.txt            # fastapi, uvicorn, tensorflow, etc.
│
├── 📁 asistente-gemini/             # 🤖 Asistente IA Conversacional
│   ├── app.py                      # Servidor Flask con Gemini AI (5KB)
│   ├── requirements.txt            # flask, flask-cors, google-generativeai
│   ├── venv-gemini/                # Entorno virtual específico
│   └── README.md                   # Documentación del asistente
│
├── 📁 frontend/                     # 🎨 Interfaz Web React
│   ├── package.json                # Dependencias: react, vite
│   ├── package-lock.json           # Lock de versiones (57KB)
│   ├── vite.config.js              # Configuración de Vite
│   ├── index.html                  # HTML base
│   ├── node_modules/               # Dependencias de Node.js
│   ├── 📁 src/                     # Código fuente React
│   │   ├── main.jsx                # Punto de entrada React
│   │   ├── App.jsx                 # Componente principal
│   │   ├── App.css                 # Estilos principales (3KB)
│   │   ├── index.css               # Estilos globales
│   │   ├── 📁 components/          # Componentes React
│   │   │   ├── ImageClassifier.jsx # Clasificador de imágenes (2KB)
│   │   │   ├── NutritionChatbot.jsx# Chat nutricional básico (2KB)
│   │   │   ├── GeminiChat.jsx      # Chat flotante Gemini (4KB)
│   │   │   └── GeminiChat.css      # Estilos del chat (3KB)
│   │   └── 📁 services/            # Servicios y APIs
│   │       └── api.js              # Funciones para llamadas API
│   └── 📁 public/                  # Archivos estáticos
│
├── 📁 entrenamineto/                # 🧠 Scripts de Machine Learning
│   ├── clasificador_alimentos.py   # Script principal de entrenamiento (8KB)
│   ├── best_model_20_clases.h5     # Mejor modelo entrenado (13MB)
│   ├── modelo.h5                   # Modelo backup (13MB)
│   └── classes.txt                 # Clases: Apple, Banana, Orange, etc.
│
├── 📁 dataset/                      # 📊 Dataset de Entrenamiento
│   ├── 📁 Training/                # Imágenes de entrenamiento
│   │   ├── 📁 Apple 10/            # ~1000 imágenes de manzanas
│   │   ├── 📁 Banana 1/            # ~1000 imágenes de bananas
│   │   ├── 📁 Orange 1/            # ~1000 imágenes de naranjas
│   │   └── ... (17 carpetas más)   # Resto de alimentos
│   └── 📁 Test/                    # Imágenes de prueba
│       ├── 📁 Apple 10/            # ~200 imágenes de test
│       └── ... (19 carpetas más)   # Resto de alimentos
│
├── 📁 .venv/                        # 🐍 Entorno Virtual Python
│   ├── Scripts/                    # Ejecutables (Windows)
│   ├── Lib/                       # Librerías instaladas
│   └── pyvenv.cfg                  # Configuración del entorno
│
├── 📁 .git/                        # 🔄 Control de Versiones Git
├── .gitignore                      # Archivos ignorados por Git
├── requirements.txt                # Dependencias globales del proyecto
├── README.md                       # Documentación original
└── README_COMPLETO.md              # 📖 Esta documentación completa
```



## 🚀 Instalación Completa y Configuración Detallada

### 📋 Prerrequisitos del Sistema

| Herramienta | Versión Mínima | Versión Recomendada | Propósito |
|-------------|----------------|---------------------|-----------|
| **Python** | 3.11.0 | 3.11.5+ | Backend y ML |
| **Node.js** | 16.0.0 | 18.17.0+ | Frontend React |
| **npm** | 8.0.0 | 9.8.0+ | Gestor de paquetes JS |
| **Git** | 2.30.0 | 2.41.0+ | Control de versiones |
| **RAM** | 8 GB | 16 GB+ | Para entrenamiento ML |
| **Almacenamiento** | 10 GB | 20 GB+ | Dataset + modelos |

### 🔧 Instalación Paso a Paso Detallada

#### **PASO 1: Preparación del Entorno**

```bash
# 1.1 Clonar el repositorio
git clone <repository-url>
cd inteligenicaArtificial

# 1.2 Verificar versiones instaladas
python --version          # Debe ser 3.11+
node --version           # Debe ser 16+
npm --version            # Debe ser 8+

# 1.3 Crear entorno virtual Python
python -m venv .venv

# 1.4 Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 1.5 Verificar activación (debe mostrar (.venv))
echo $VIRTUAL_ENV        # Linux/Mac
echo %VIRTUAL_ENV%       # Windows
```

#### **PASO 2: Configuración del Backend FastAPI**

```bash
# 2.1 Navegar al directorio backend
cd backend

# 2.2 Instalar dependencias específicas
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install tensorflow==2.13.0
pip install keras==2.13.1
pip install numpy==1.24.3
pip install opencv-python==4.8.1.78
pip install Pillow==10.0.1
pip install python-multipart==0.0.6

# 2.3 Verificar instalación
python -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')"
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"

# 2.4 Verificar que el modelo existe
ls -la best_model_20_clases.h5  # Linux/Mac
dir best_model_20_clases.h5     # Windows

# 2.5 Probar carga del modelo
python -c "
import tensorflow as tf
model = tf.keras.models.load_model('best_model_20_clases.h5')
print(f'Modelo cargado: {model.input_shape}')
"
```

#### **PASO 3: Configuración del Asistente Gemini**

```bash
# 3.1 Navegar al directorio del asistente
cd ../asistente-gemini

# 3.2 Instalar dependencias específicas
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install google-generativeai==0.3.2

# 3.3 Configurar API Key de Gemini
# IMPORTANTE: Reemplazar con tu API key real
export GEMINI_API_KEY="tu_api_key_aqui"  # Linux/Mac
set GEMINI_API_KEY=tu_api_key_aqui       # Windows

# 3.4 Verificar instalación
python -c "
import google.generativeai as genai
print('Gemini AI instalado correctamente')
"

# 3.5 Probar conectividad (opcional)
python -c "
import google.generativeai as genai
genai.configure(api_key='tu_api_key')
models = list(genai.list_models())
print(f'Modelos disponibles: {len(models)}')
"
```

#### **PASO 4: Configuración del Frontend React**

```bash
# 4.1 Navegar al directorio frontend
cd ../frontend

# 4.2 Verificar package.json
cat package.json  # Linux/Mac
type package.json  # Windows

# 4.3 Instalar dependencias de Node.js
npm install

# 4.4 Verificar instalación
npm list --depth=0

# 4.5 Verificar estructura de src/
ls -la src/           # Linux/Mac
dir src\              # Windows

# 4.6 Probar build de desarrollo
npm run dev --dry-run
```

#### **PASO 5: Configuración del Dataset (Opcional)**

```bash
# 5.1 Crear estructura del dataset
cd ../
mkdir -p dataset/Training dataset/Test

# 5.2 Estructura esperada del dataset
# dataset/
# ├── Training/
# │   ├── Apple 10/
# │   ├── Banana 1/
# │   └── ... (18 clases más)
# └── Test/
#     ├── Apple 10/
#     └── ... (19 clases más)

# 5.3 Verificar clases disponibles
cat entrenamineto/classes.txt
```

### 🔍 Verificación de la Instalación

#### **Test 1: Backend FastAPI**
```bash
cd backend
python -c "
from main import app
print('✅ Backend configurado correctamente')
"
```

#### **Test 2: Asistente Gemini**
```bash
cd asistente-gemini
python -c "
from app import app
print('✅ Asistente Gemini configurado correctamente')
"
```

#### **Test 3: Frontend React**
```bash
cd frontend
npm run build --dry-run
echo "✅ Frontend configurado correctamente"
```





## 🎮 Uso Completo del Sistema

### 🚀 Secuencia de Inicio Recomendada

#### **1. Iniciar Backend FastAPI (Servidor Principal)**
```bash
# Terminal 1
cd backend
python main.py

# Salida esperada:
# INFO:     Started server process [12345]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
- **URL**: http://localhost:8000
- **Documentación Automática**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

#### **2. Iniciar Asistente Gemini (Servidor IA)**
```bash
# Terminal 2
cd asistente-gemini
python app.py

# Salida esperada:
# * Running on http://127.0.0.1:5001
# * Debug mode: on
# * Restarting with stat
# * Debugger is active!
```
- **URL**: http://localhost:5001
- **Test Endpoint**: http://localhost:5001/test
- **Models Endpoint**: http://localhost:5001/models

#### **3. Iniciar Frontend React (Interfaz Web)**
```bash
# Terminal 3
cd frontend
npm run dev

# Salida esperada:
# VITE v5.0.8  ready in 1234 ms
# ➜  Local:   http://localhost:3000/
# ➜  Network: use --host to expose
# ➜  press h to show help
```
- **URL**: http://localhost:3000
- **Build de Producción**: `npm run build`
- **Preview**: `npm run preview`

### 🔄 Flujo de Trabajo del Usuario

1. **Acceder a la aplicación**: Abrir http://localhost:3000
2. **Subir imagen**: Seleccionar archivo de alimento
3. **Clasificar**: Hacer clic en "Clasificar" 
4. **Ver resultados**: Clase predicha + % de confianza
5. **Consultar nutrición**: Usar chat para preguntas específicas
6. **Chat con Gemini**: Botón flotante para consultas avanzadas

## 🛠️ Tecnologías Utilizadas - Análisis Completo

### 🐍 Backend Technologies

#### **FastAPI Framework**
```python
# Características utilizadas:
- Automatic API documentation (OpenAPI/Swagger)
- Type hints validation with Pydantic
- Async/await support for high performance
- CORS middleware for cross-origin requests
- File upload handling with python-multipart
- JSON response formatting
- Error handling and HTTP status codes
```

#### **TensorFlow & Keras Stack**
```python
# Versiones específicas:
tensorflow==2.13.0          # Core ML framework
keras==2.13.1               # High-level neural networks API

# Funcionalidades utilizadas:
- Model loading: tf.keras.models.load_model()
- Image preprocessing: tf.keras.preprocessing.image
- Predictions: model.predict()
- Transfer learning: MobileNetV2 base model
- Model callbacks: EarlyStopping, ModelCheckpoint
```

#### **Computer Vision Stack**
```python
# OpenCV (cv2) - Procesamiento de imágenes
opencv-python==4.8.1.78
# Funciones utilizadas:
- cv2.imread() - Cargar imágenes
- cv2.resize() - Redimensionar
- cv2.cvtColor() - Conversión de colores

# Pillow (PIL) - Manipulación de imágenes
Pillow==10.0.1
# Funciones utilizadas:
- Image.open() - Abrir desde bytes
- Image.convert('RGB') - Conversión de formato
- np.array() - Conversión a numpy array
```

### 🤖 Asistente IA Technologies

#### **Flask Microframework**
```python
flask==3.0.0                # Lightweight web framework
flask-cors==4.0.0           # Cross-Origin Resource Sharing

# Características utilizadas:
- Route decorators: @app.route()
- JSON request/response handling
- Error handling with try/except
- CORS configuration for frontend access
```

#### **Google Gemini AI**
```python
google-generativeai==0.3.2  # Google's generative AI SDK

# Funcionalidades utilizadas:
- Model initialization: genai.GenerativeModel()
- Content generation: model.generate_content()
- API key configuration: genai.configure()
- Model listing: genai.list_models()
- Prompt engineering for nutrition queries
```

### 🎨 Frontend Technologies

#### **React Ecosystem**
```json
{
  "react": "^18.2.0",           // Core React library
  "react-dom": "^18.2.0"       // DOM rendering
}

// Características utilizadas:
- Functional components with Hooks
- useState for state management
- useEffect for side effects (if needed)
- Event handling (onClick, onChange, onKeyPress)
- Conditional rendering
- Component composition
```

#### **Vite Build Tool**
```json
{
  "vite": "^5.0.8",            // Fast build tool
  "@vitejs/plugin-react": "^4.2.1"  // React plugin
}

// Características:
- Hot Module Replacement (HMR)
- Fast cold start
- Optimized builds
- ES modules support
- TypeScript support (ready)
```

#### **Modern JavaScript Features**
```javascript
// ES6+ Features utilizadas:
- Arrow functions: () => {}
- Destructuring: const [state, setState] = useState()
- Template literals: `Hello ${name}`
- Async/await: async () => await fetch()
- Modules: import/export
- Spread operator: {...prev, newItem}
```

### 🔧 Development & DevOps Tools

#### **Python Environment Management**
```bash
# Virtual Environment
python -m venv .venv         # Environment creation
.venv\Scripts\activate       # Windows activation
source .venv/bin/activate    # Linux/Mac activation

# Package Management
pip install -r requirements.txt  # Install dependencies
pip freeze > requirements.txt    # Export dependencies
pip list                         # List installed packages
```

#### **Node.js Package Management**
```bash
# NPM Commands
npm install                  # Install dependencies
npm run dev                  # Development server
npm run build               # Production build
npm run preview             # Preview build
npm list --depth=0          # List dependencies
```

#### **Git Version Control**
```bash
# Repository structure
.git/                       # Git metadata
.gitignore                  # Ignored files
# Common ignored items:
# .venv/, node_modules/, __pycache__/
# *.pyc, .env, .DS_Store
```

## 🛠️ Tecnologías Utilizadas

### Backend & Machine Learning
- **TensorFlow 2.13.0**: Framework principal de ML
- **Keras 2.13.1**: API de alto nivel para redes neuronales
- **FastAPI 0.104.1**: Framework web moderno y rápido
- **OpenCV 4.8.1**: Procesamiento de imágenes
- **Pillow 10.0.1**: Manipulación de imágenes
- **Uvicorn 0.24.0**: Servidor ASGI de alto rendimiento

### Asistente IA
- **Flask**: Framework web ligero para el asistente
- **Google Gemini AI**: Modelo de lenguaje avanzado (Gemini 2.5 Flash)
- **Flask-CORS**: Manejo de CORS para APIs

### Frontend
- **React 18.2.0**: Biblioteca de JavaScript para UI
- **Vite 5.0.8**: Build tool rápido y moderno
- **JavaScript ES6+**: Sintaxis moderna

