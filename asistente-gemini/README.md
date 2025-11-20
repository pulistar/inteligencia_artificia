# 🤖 Asistente Nutricional IA con Gemini

Asistente nutricional inteligente powered by Google Gemini con interfaz de botón flotante.

## ✨ Características

- 🧠 **IA Avanzada**: Powered by Google Gemini
- 🥗 **Especializado**: Base de datos de 20 alimentos
- 💬 **Chat Inteligente**: Conversación natural
- 📱 **Botón Flotante**: Interfaz moderna y accesible
- 🎨 **Diseño Responsivo**: Funciona en móviles y desktop

## 🚀 Instalación y Uso

### 1. Instalar dependencias
```bash
cd asistente-gemini
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación
```bash
python app.py
```

### 3. Abrir en navegador
```
http://localhost:5001
```

## 🎯 Funcionalidades

### Botón Flotante
- **Posición**: Esquina inferior derecha
- **Acción**: Clic para abrir/cerrar chat
- **Animaciones**: Hover y transiciones suaves

### Chat Inteligente
- **Respuestas**: Generadas por Gemini AI
- **Contexto**: Especializado en 20 alimentos
- **UI**: Interfaz moderna tipo WhatsApp

### Alimentos Soportados
- Apple 10, Banana 1, Orange 1, Tomato 1
- Carrot 1, Cucumber 1, Onion 2, Peach 1
- Pear 1, Cherry 1, Grape Blue 1, Pepper Green 1
- Potato Red 1, Avocado 1, Mango 1, Strawberry 1
- Lemon 1, Watermelon 1, Corn 1, Eggplant 1

## 🔧 Configuración

### API Key
La API key de Gemini está configurada en `app.py`:
```python
GEMINI_API_KEY = "AIzaSyAzpaL9kbChLb2hspMERS8xvKGTYewVo64"
```

### Puerto
La aplicación corre en el puerto 5001 para no interferir con tu backend principal.

## 📱 Uso

1. **Abrir chat**: Clic en el botón flotante 🤖
2. **Hacer preguntas**: Sobre nutrición y alimentos
3. **Recibir respuestas**: IA especializada en nutrición
4. **Cerrar chat**: Clic en la X o fuera del modal

## 🎨 Personalización

### Colores
- **Primario**: #667eea (azul)
- **Secundario**: #764ba2 (púrpura)
- **Fondo**: Gradiente azul-púrpura

### Responsive
- **Desktop**: Modal de 400px
- **Móvil**: Ancho completo menos márgenes

## 🔗 Integración

Este asistente es **independiente** de tu backend principal y puede:
- Ejecutarse en paralelo (puerto 5001)
- Integrarse en cualquier página web
- Funcionar como widget embebido

¡Disfruta tu asistente nutricional inteligente! 🍎🤖
