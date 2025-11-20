# 🍎 Sistema Completo de Clasificación de Alimentos con IA

## 📖 Guía Completa Paso a Paso

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
│                 │    │                  │    │                 │
│   Frontend      │◄──►│   Backend        │◄──►│  Asistente      │
│   (React)       │    │   (FastAPI)      │    │  Gemini AI      │
│   Puerto: 3000  │    │   Puerto: 8000   │    │  (Flask)        │
│                 │    │                  │    │  Puerto: 5001   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │                  │    │                 │
│   Vite Build    │    │  TensorFlow      │    │  Google         │
│   System        │    │  Model (.h5)     │    │  Gemini API     │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔬 Proceso Completo de Desarrollo - Paso a Paso

### **PASO 1: Entrenamiento del Modelo de Machine Learning** 🧠

#### 1.1 Preparación del Dataset
- **Ubicación**: `entrenamineto/clasificador_alimentos.py`
- **20 clases de alimentos**: Apple, Banana, Orange, Tomato, Carrot, Cucumber, Onion, Peach, Pear, Cherry, Grape, Pepper, Potato, Avocado, Mango, Strawberry, Lemon, Watermelon, Corn, Eggplant
- **Estructura esperada del dataset**:
```
dataset/
├── Training/
│   ├── Apple 10/
│   ├── Banana 1/
│   ├── Orange 1/
│   └── ... (18 clases más)
└── Test/
    ├── Apple 10/
    ├── Banana 1/
    └── ... (18 clases más)
├── 📁 entrenamineto/           # Scripts de entrenamiento
│   ├── modelo.h5              # Modelo de entrenamiento
│   ├── best_model_20_clases.h5 # Mejor modelo
│   └── classes.txt            # Clases del modelo
├── 📁 dataset/                 # Dataset de entrenamiento
├── .venv/                     # Entorno virtual Python
├── requirements.txt           # Dependencias globales
└── README.md                  # Este archivo
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.11 o superior
- Node.js 16 o superior
- Git

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd inteligenicaArtificial
```

### 2. Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 3. Instalar Dependencias del Backend
```bash
cd backend
pip install -r requirements.txt
```

### 4. Instalar Dependencias del Asistente Gemini
```bash
cd ../asistente-gemini
pip install -r requirements.txt
```

### 5. Configurar Frontend
```bash
cd ../frontend
npm install
```

## 🎮 Uso del Sistema

### Iniciar Backend (FastAPI)
```bash
cd backend
python main.py
```
- **URL**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs

### Iniciar Asistente Gemini
```bash
cd asistente-gemini
python app.py
```
- **URL**: http://localhost:5001

### Iniciar Frontend
```bash
cd frontend
npm run dev
```
- **URL**: http://localhost:3000

## 📡 API Endpoints

### Backend FastAPI (Puerto 8000)

#### `POST /predict`
Clasifica una imagen de alimento
```json
{
  "file": "imagen.jpg"
}
```
**Respuesta:**
```json
{
  "clase": "Apple 10",
  "probabilidad": 95.67
}
```

#### `POST /chat`
Consulta información nutricional
```json
{
  "message": "¿Cuántas calorías tiene una manzana?"
}
```

### Asistente Gemini (Puerto 5001)

#### `POST /chat`
Chat inteligente con Gemini AI
```json
{
  "mensaje": "Dame información nutricional sobre manzanas"
}
```

#### `GET /test`
Prueba de conectividad con Gemini
```json
{
  "respuesta": "¡Hola! Gemini funcionando correctamente",
  "success": true
}
```

## 🍎 Alimentos Soportados

El sistema puede reconocer los siguientes 20 alimentos:

| Alimento | Calorías (por 100g) | Características Nutricionales |
|----------|---------------------|-------------------------------|
| 🍎 Apple | 52 kcal | Alto en fibra y vitamina C |
| 🍌 Banana | 89 kcal | Rico en potasio |
| 🍊 Orange | 47 kcal | Excelente fuente de vitamina C |
| 🍅 Tomato | 18 kcal | Alto en licopeno |
| 🥕 Carrot | 41 kcal | Rico en vitamina A |
| 🥒 Cucumber | 16 kcal | 95% agua, muy hidratante |
| 🧅 Onion | 40 kcal | Alto en antioxidantes |
| 🍑 Peach | 39 kcal | Buena fuente de vitamina A |
| 🍐 Pear | 57 kcal | Alto en fibra |
| 🍒 Cherry | 63 kcal | Muy alto en antioxidantes |
| 🍇 Grape | 62 kcal | Rico en resveratrol |
| 🫑 Green Pepper | 31 kcal | Muy alto en vitamina C |
| 🥔 Red Potato | 77 kcal | Alto en potasio |
| 🥑 Avocado | 160 kcal | Rico en grasas saludables |
| 🥭 Mango | 60 kcal | Muy alto en vitamina A |
| 🍓 Strawberry | 32 kcal | Muy alto en vitamina C |
| 🍋 Lemon | 17 kcal | Extremo en vitamina C |
| 🍉 Watermelon | 30 kcal | 92% agua |
| 🌽 Corn | 86 kcal | Alto en antioxidantes |
| 🍆 Eggplant | 25 kcal | Alto en antioxidantes |

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# .env file
GEMINI_API_KEY=tu_api_key_aqui
MODEL_PATH=./best_model_20_clases.h5
CLASSES_PATH=./classes.txt
```

### Configuración de CORS
El sistema está configurado para aceptar requests desde cualquier origen durante desarrollo. Para producción, modificar:

```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Solo frontend
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 🧪 Testing

### Probar Backend
```bash
# Endpoint de salud
curl http://localhost:8000/

# Probar predicción
curl -X POST -F "file=@imagen.jpg" http://localhost:8000/predict
```

### Probar Asistente Gemini
```bash
# Test endpoint
curl http://localhost:5001/test

# Chat endpoint
curl -X POST -H "Content-Type: application/json" \
     -d '{"mensaje":"Hola"}' \
     http://localhost:5001/chat
```

## 🚀 Despliegue en Producción

### Usando Docker (Recomendado)
```dockerfile
# Dockerfile para backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Usando Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [TuGitHub](https://github.com/tuusuario)

## 🙏 Agradecimientos

- TensorFlow team por el framework de ML
- Google por Gemini AI
- FastAPI por el excelente framework web
- React team por la biblioteca de UI
- Comunidad open source por las herramientas utilizadas

## 📞 Soporte

Si tienes preguntas o necesitas ayuda:

- 📧 Email: tu-email@ejemplo.com
- 🐛 Issues: [GitHub Issues](https://github.com/tuusuario/proyecto/issues)
- 📖 Documentación: [Wiki del Proyecto](https://github.com/tuusuario/proyecto/wiki)

---

⭐ ¡Si este proyecto te fue útil, no olvides darle una estrella en GitHub!