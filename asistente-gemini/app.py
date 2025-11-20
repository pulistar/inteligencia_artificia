from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import traceback

app = Flask(__name__)
CORS(app)

# Configurar Gemini AI
GEMINI_API_KEY = "AIzaSyAzpaL9kbChLb2hspMERS8xvKGTYewVo64"
genai.configure(api_key=GEMINI_API_KEY)

# Inicializar el modelo Gemini
model = genai.GenerativeModel('models/gemini-2.5-flash')

# Base de datos nutricional para contexto
nutricion_data = {
    "Apple 10": {"calorias": 52, "carbs": 14, "proteina": 0.3, "grasa": 0.2, "fibra": 2.4},
    "Banana 1": {"calorias": 89, "carbs": 23, "proteina": 1.1, "grasa": 0.3, "fibra": 2.6},
    "Orange 1": {"calorias": 47, "carbs": 12, "proteina": 0.9, "grasa": 0.1, "fibra": 2.4},
    "Tomato 1": {"calorias": 18, "carbs": 3.9, "proteina": 0.9, "grasa": 0.2, "fibra": 1.2},
    "Carrot 1": {"calorias": 41, "carbs": 10, "proteina": 0.9, "grasa": 0.2, "fibra": 2.8},
    "Cucumber 1": {"calorias": 16, "carbs": 4, "proteina": 0.7, "grasa": 0.1, "fibra": 0.5},
    "Onion 2": {"calorias": 40, "carbs": 9, "proteina": 1.1, "grasa": 0.1, "fibra": 1.7},
    "Peach 1": {"calorias": 39, "carbs": 10, "proteina": 0.9, "grasa": 0.3, "fibra": 1.5},
    "Pear 1": {"calorias": 57, "carbs": 15, "proteina": 0.4, "grasa": 0.1, "fibra": 3.1},
    "Cherry 1": {"calorias": 63, "carbs": 16, "proteina": 1.1, "grasa": 0.2, "fibra": 2.1},
    "Grape Blue 1": {"calorias": 62, "carbs": 16, "proteina": 0.6, "grasa": 0.2, "fibra": 0.9},
    "Pepper Green 1": {"calorias": 31, "carbs": 7, "proteina": 1, "grasa": 0.3, "fibra": 2.5},
    "Potato Red 1": {"calorias": 77, "carbs": 17, "proteina": 2, "grasa": 0.1, "fibra": 2.2},
    "Avocado 1": {"calorias": 160, "carbs": 9, "proteina": 2, "grasa": 15, "fibra": 7},
    "Mango 1": {"calorias": 60, "carbs": 15, "proteina": 0.8, "grasa": 0.4, "fibra": 1.6},
    "Strawberry 1": {"calorias": 32, "carbs": 8, "proteina": 0.7, "grasa": 0.3, "fibra": 2},
    "Lemon 1": {"calorias": 17, "carbs": 5, "proteina": 0.6, "grasa": 0.2, "fibra": 1.6},
    "Watermelon 1": {"calorias": 30, "carbs": 8, "proteina": 0.6, "grasa": 0.2, "fibra": 0.4},
    "Corn 1": {"calorias": 86, "carbs": 19, "proteina": 3.3, "grasa": 1.4, "fibra": 2.7},
    "Eggplant 1": {"calorias": 25, "carbs": 6, "proteina": 1, "grasa": 0.2, "fibra": 3}
}

def crear_prompt_nutricional(mensaje_usuario):
    """Crear prompt especializado en nutrición"""
    return f"""
Eres un asistente nutricional experto y amigable especializado en los siguientes 20 alimentos:

Base de datos nutricional:
{nutricion_data}

Instrucciones:
1. Responde de manera conversacional y amigable en español
2. Usa emojis para hacer las respuestas más atractivas
3. Proporciona información nutricional específica y precisa
4. Da consejos prácticos de salud y nutrición
5. Sugiere combinaciones saludables cuando sea apropiado
6. Si mencionan un alimento que no está en la base de datos, explica que te especializas en los 20 alimentos listados
7. Mantén las respuestas concisas pero informativas (máximo 200 palabras)

Mensaje del usuario: "{mensaje_usuario}"

Respuesta:
"""

@app.route('/models', methods=['GET'])
def list_models():
    """Listar modelos disponibles"""
    try:
        models = genai.list_models()
        model_names = [model.name for model in models]
        return jsonify({
            'models': model_names,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/test', methods=['GET'])
def test():
    """Endpoint de prueba para verificar que Gemini funciona"""
    try:
        # Usar el modelo más básico disponible
        response = model.generate_content("Di hola en español")
        return jsonify({
            'respuesta': response.text,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        mensaje = data.get('mensaje', '')
        
        if not mensaje:
            return jsonify({'error': 'Mensaje vacío'}), 400
        
        # Crear prompt especializado
        prompt = crear_prompt_nutricional(mensaje)
        
        # Generar respuesta con Gemini
        response = model.generate_content(prompt)
        respuesta_text = response.text
        
        return jsonify({
            'respuesta': respuesta_text,
            'success': True
        })
        
    except Exception as e:
        print(f"Error en chat: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': f'Error al procesar la consulta: {str(e)}',
            'success': False
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
