from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import cv2
import io
from PIL import Image
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
classes = []

nutricion = {
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

def load_model():
    global model, classes
    try:
        model = tf.keras.models.load_model('best_model_20_clases.h5')
        with open('classes.txt', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
    except:
        classes = ["Apple 10", "Banana 1", "Orange 1", "Tomato 1", "Carrot 1"]

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert('RGB')
    image_array = np.array(image)
    image_array = cv2.resize(image_array, (224, 224))
    image_array = image_array.astype(np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

@app.on_event("startup")
async def startup_event():
    load_model()

class ChatMessage(BaseModel):
    message: str

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        image_bytes = await file.read()
        processed_image = preprocess_image(image_bytes)
        
        if model is None:
            return {"clase": "modelo_no_cargado", "probabilidad": 0.0}
        
        predictions = model.predict(processed_image)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        clase = classes[predicted_class] if predicted_class < len(classes) else "desconocido"
        
        return {"clase": clase, "probabilidad": round(confidence * 100, 2)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_nutrition(message: ChatMessage):
    user_message = message.message.lower()
    found_foods = []
    
    # Buscar alimentos mencionados en el mensaje
    for food in nutricion.keys():
        if food.lower() in user_message:
            found_foods.append(food)
    
    if found_foods:
        response = "Información nutricional encontrada:\n\n"
        for food in found_foods:
            info = nutricion[food]
            response += f"🍎 {food}:\n"
            response += f"• Calorías: {info['calorias']} kcal\n"
            response += f"• Carbohidratos: {info['carbs']}g\n"
            response += f"• Proteína: {info['proteina']}g\n"
            response += f"• Grasa: {info['grasa']}g\n"
            if 'fibra' in info:
                response += f"• Fibra: {info['fibra']}g\n"
            response += "\n"
    else:
        response = "Lo siento, no encontré información nutricional específica en tu mensaje. Puedo ayudarte con información sobre: Apple, Banana, Orange, Tomato, Carrot, Cucumber, Onion, Peach, Pear, Cherry, Grape, Pepper, Potato, Avocado, Mango, Strawberry, Lemon, Watermelon, Corn, Eggplant."
    
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
