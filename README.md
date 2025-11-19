# Clasificación de Alimentos para Asistentes de Nutrición

## Estructura del Proyecto

```
clasificacion-alimentos/
├── clasificacion_alimentos.ipynb    # Notebook de entrenamiento
├── backend/
│   ├── main.py                     # FastAPI backend
│   └── requirements.txt            # Dependencias Python
├── frontend/
│   ├── package.json               # Configuración React
│   ├── vite.config.js            # Configuración Vite
│   ├── index.html                # HTML principal
│   └── src/
│       ├── main.jsx              # Punto de entrada React
│       ├── App.jsx               # Componente principal
│       ├── App.css               # Estilos principales
│       ├── index.css             # Estilos globales
│       ├── components/
│       │   ├── ImageClassifier.jsx    # Clasificador de imágenes
│       │   └── NutritionChatbot.jsx   # Chatbot nutricional
│       └── services/
│           └── api.js            # Servicios API
└── dataset/
    ├── train/
    ├── val/
    └── test/
```

## Instalación y Ejecución

### 1. Entrenamiento del Modelo
```bash
jupyter notebook clasificacion_alimentos.ipynb
```

### 2. Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

## Funcionalidades

- Clasificación de imágenes de alimentos usando MobileNetV2
- Chatbot nutricional con información de alimentos
- Interface web completa con React
- API REST con FastAPI
