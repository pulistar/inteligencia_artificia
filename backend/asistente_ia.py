import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

# Configurar OpenAI (necesitas API key)
# openai.api_key = "tu-api-key-aqui"

class ChatMessage(BaseModel):
    message: str

# Base de datos nutricional exacta para las 20 clases del modelo
nutricion_completa = {
    "Apple 10": {"calorias": 52, "carbs": 14, "proteina": 0.3, "grasa": 0.2, "fibra": 2.4, "vitamina_c": 4.6},
    "Banana 1": {"calorias": 89, "carbs": 23, "proteina": 1.1, "grasa": 0.3, "fibra": 2.6, "potasio": 358},
    "Orange 1": {"calorias": 47, "carbs": 12, "proteina": 0.9, "grasa": 0.1, "fibra": 2.4, "vitamina_c": 53.2},
    "Tomato 1": {"calorias": 18, "carbs": 3.9, "proteina": 0.9, "grasa": 0.2, "fibra": 1.2, "licopeno": "alto"},
    "Carrot 1": {"calorias": 41, "carbs": 10, "proteina": 0.9, "grasa": 0.2, "fibra": 2.8, "vitamina_a": "muy_alto"},
    "Cucumber 1": {"calorias": 16, "carbs": 4, "proteina": 0.7, "grasa": 0.1, "fibra": 0.5, "agua": "95%"},
    "Onion 2": {"calorias": 40, "carbs": 9, "proteina": 1.1, "grasa": 0.1, "fibra": 1.7, "antioxidantes": "alto"},
    "Peach 1": {"calorias": 39, "carbs": 10, "proteina": 0.9, "grasa": 0.3, "fibra": 1.5, "vitamina_a": "alto"},
    "Pear 1": {"calorias": 57, "carbs": 15, "proteina": 0.4, "grasa": 0.1, "fibra": 3.1, "vitamina_k": "alto"},
    "Cherry 1": {"calorias": 63, "carbs": 16, "proteina": 1.1, "grasa": 0.2, "fibra": 2.1, "antioxidantes": "muy_alto"},
    "Grape Blue 1": {"calorias": 62, "carbs": 16, "proteina": 0.6, "grasa": 0.2, "fibra": 0.9, "resveratrol": "alto"},
    "Pepper Green 1": {"calorias": 31, "carbs": 7, "proteina": 1, "grasa": 0.3, "fibra": 2.5, "vitamina_c": "muy_alto"},
    "Potato Red 1": {"calorias": 77, "carbs": 17, "proteina": 2, "grasa": 0.1, "fibra": 2.2, "potasio": "alto"},
    "Avocado 1": {"calorias": 160, "carbs": 9, "proteina": 2, "grasa": 15, "fibra": 7, "grasas_saludables": "muy_alto"},
    "Mango 1": {"calorias": 60, "carbs": 15, "proteina": 0.8, "grasa": 0.4, "fibra": 1.6, "vitamina_a": "muy_alto"},
    "Strawberry 1": {"calorias": 32, "carbs": 8, "proteina": 0.7, "grasa": 0.3, "fibra": 2, "vitamina_c": "muy_alto"},
    "Lemon 1": {"calorias": 17, "carbs": 5, "proteina": 0.6, "grasa": 0.2, "fibra": 1.6, "vitamina_c": "extremo"},
    "Watermelon 1": {"calorias": 30, "carbs": 8, "proteina": 0.6, "grasa": 0.2, "fibra": 0.4, "agua": "92%"},
    "Corn 1": {"calorias": 86, "carbs": 19, "proteina": 3.3, "grasa": 1.4, "fibra": 2.7, "antioxidantes": "alto"},
    "Eggplant 1": {"calorias": 25, "carbs": 6, "proteina": 1, "grasa": 0.2, "fibra": 3, "antioxidantes": "alto"}
}

def crear_prompt_nutricional(mensaje_usuario, alimento_detectado=None):
    """Crea un prompt inteligente para el asistente nutricional"""
    
    prompt = f"""
Eres un asistente nutricional experto y amigable. Tu trabajo es ayudar a las personas con información nutricional precisa y consejos de salud.

Base de datos nutricional disponible:
{json.dumps(nutricion_completa, indent=2)}

Mensaje del usuario: "{mensaje_usuario}"

{f"Alimento detectado en imagen: {alimento_detectado}" if alimento_detectado else ""}

Instrucciones:
1. Responde de manera conversacional y amigable
2. Proporciona información nutricional específica cuando sea relevante
3. Da consejos prácticos de salud y nutrición
4. Si mencionan un alimento de la base de datos, incluye sus valores nutricionales
5. Sugiere combinaciones saludables cuando sea apropiado
6. Usa emojis para hacer la respuesta más atractiva
7. Mantén las respuestas concisas pero informativas

Respuesta:
"""
    return prompt

async def chat_con_ia(mensaje: str, alimento_detectado=None):
    """Función para chat con IA usando OpenAI"""
    try:
        prompt = crear_prompt_nutricional(mensaje, alimento_detectado)
        
        # Comentado porque necesitas API key
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": prompt}],
        #     max_tokens=500,
        #     temperature=0.7
        # )
        # return response.choices[0].message.content
        
        # Simulación de respuesta IA (para demo sin API key)
        return simular_respuesta_ia(mensaje, alimento_detectado)
        
    except Exception as e:
        return f"Lo siento, hubo un error procesando tu consulta: {str(e)}"

def simular_respuesta_ia(mensaje: str, alimento_detectado=None):
    """Simulación de IA más inteligente que la implementación básica"""
    mensaje_lower = mensaje.lower()
    
    # Detectar intención
    if any(word in mensaje_lower for word in ["calorias", "calórico", "energía"]):
        return generar_respuesta_calorias(mensaje_lower, alimento_detectado)
    elif any(word in mensaje_lower for word in ["proteina", "proteínas", "músculo"]):
        return generar_respuesta_proteinas(mensaje_lower)
    elif any(word in mensaje_lower for word in ["vitamina", "nutrientes", "beneficios"]):
        return generar_respuesta_vitaminas(mensaje_lower)
    elif any(word in mensaje_lower for word in ["dieta", "bajar peso", "adelgazar"]):
        return generar_respuesta_dieta(mensaje_lower)
    else:
        return generar_respuesta_general(mensaje_lower, alimento_detectado)

def generar_respuesta_calorias(mensaje, alimento_detectado):
    """Genera respuesta enfocada en calorías"""
    if alimento_detectado:
        # Buscar coincidencia exacta primero
        if alimento_detectado in nutricion_completa:
            alimento_key = alimento_detectado
        else:
            # Buscar por palabra clave si no hay coincidencia exacta
            alimento_key = None
            for key in nutricion_completa.keys():
                if any(word.lower() in key.lower() for word in alimento_detectado.split()):
                    alimento_key = key
                    break
        
        if alimento_key:
            info = nutricion_completa[alimento_key]
            return f"""
🍎 **Información Calórica de {alimento_detectado.title()}:**

• **Calorías**: {info['calorias']} kcal por 100g
• **Carbohidratos**: {info['carbs']}g (energía rápida)
• **Proteínas**: {info['proteina']}g (construcción muscular)
• **Grasas**: {info['grasa']}g (energía sostenida)

💡 **Consejo**: Este alimento aporta {info['calorias']} calorías, ideal para {'snacks ligeros' if info['calorias'] < 50 else 'comidas principales' if info['calorias'] > 100 else 'snacks moderados'}.

¿Te gustaría saber sobre combinaciones saludables con este alimento?
"""
    
    return """
📊 **Información General sobre Calorías:**

Las calorías son unidades de energía que tu cuerpo necesita para funcionar. 

🎯 **Recomendaciones diarias**:
• Mujeres: 1,800-2,000 kcal
• Hombres: 2,200-2,500 kcal

🥗 **Alimentos bajos en calorías** de nuestra base:
• Pepino: 16 kcal
• Limón: 17 kcal  
• Tomate: 18 kcal

¿Hay algún alimento específico del que quieras conocer las calorías?
"""

def generar_respuesta_proteinas(mensaje):
    """Genera respuesta enfocada en proteínas"""
    return """
💪 **Todo sobre Proteínas:**

Las proteínas son esenciales para construir y reparar tejidos.

🏆 **Alimentos ricos en proteína** de nuestra base:
• Maíz: 3.3g por 100g
• Papa: 2g por 100g
• Aguacate: 2g por 100g

🌱 **Dato curioso**: Aunque las frutas y verduras no son las principales fuentes de proteína, ¡sí aportan aminoácidos esenciales!

💡 **Consejo**: Combina estos alimentos con legumbres, nueces o semillas para obtener proteínas completas.

¿Te interesa saber sobre algún alimento específico?
"""

def generar_respuesta_vitaminas(mensaje):
    """Genera respuesta enfocada en vitaminas"""
    return """
🌟 **Vitaminas y Nutrientes Esenciales:**

Nuestros alimentos son ricos en vitaminas naturales:

🍊 **Vitamina C (antioxidante)**:
• Limón: Nivel extremo
• Fresa: Muy alto
• Pimiento: Muy alto

🥕 **Vitamina A (visión y piel)**:
• Zanahoria: Muy alto
• Mango: Muy alto
• Durazno: Alto

🍇 **Antioxidantes (anti-envejecimiento)**:
• Cereza: Muy alto
• Uva: Alto (resveratrol)
• Berenjena: Alto

💧 **Hidratación natural**:
• Sandía: 92% agua
• Pepino: 95% agua

¿Qué vitamina específica te interesa más?
"""

def generar_respuesta_dieta(mensaje):
    """Genera respuesta para consultas de dieta"""
    return """
🎯 **Consejos para una Dieta Saludable:**

**Alimentos ideales para control de peso** de nuestra base:

🥒 **Muy bajos en calorías**:
• Pepino: 16 kcal (95% agua)
• Limón: 17 kcal (desintoxicante)
• Tomate: 18 kcal (saciante)

🍓 **Ricos en fibra** (te mantienen lleno):
• Aguacate: 7g fibra
• Pera: 3.1g fibra
• Zanahoria: 2.8g fibra

💡 **Estrategia inteligente**:
1. Llena la mitad del plato con vegetales bajos en calorías
2. Incluye frutas como snacks naturales
3. El aguacate aporta grasas saludables que dan saciedad

¿Quieres un plan específico con estos alimentos?
"""

def generar_respuesta_general(mensaje, alimento_detectado):
    """Respuesta general inteligente"""
    if alimento_detectado:
        return f"""
🔍 **Detecté: {alimento_detectado.title()}**

¡Excelente elección! Este alimento tiene múltiples beneficios nutricionales.

🤔 **¿Qué te gustaría saber específicamente?**
• 📊 Información nutricional completa
• 🍽️ Ideas para combinarlo en comidas
• 💪 Beneficios para la salud
• 🎯 Si es adecuado para tu dieta

Solo pregúntame: "¿Cuántas calorías tiene?" o "¿Qué vitaminas aporta?"
"""
    
    return """
👋 **¡Hola! Soy tu asistente nutricional inteligente**

Puedo ayudarte con:
🔍 **Análisis de alimentos** (sube una foto)
📊 **Información nutricional** detallada  
🍽️ **Consejos de alimentación** saludable
🎯 **Planes personalizados** de nutrición

**Ejemplos de preguntas**:
• "¿Cuántas calorías tiene una manzana?"
• "¿Qué alimentos son ricos en vitamina C?"
• "¿Cómo puedo incluir más fibra en mi dieta?"

¡Pregúntame lo que necesites! 😊
"""

# Función principal para integrar con FastAPI
async def asistente_nutricional_ia(mensaje: str, alimento_detectado: str = None):
    """Función principal del asistente con IA"""
    return await chat_con_ia(mensaje, alimento_detectado)
