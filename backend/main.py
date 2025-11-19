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
    "manzana": {"calorias": 52, "carbs": 14, "proteina": 0.3, "grasa": 0.2},
    "banana": {"calorias": 89, "carbs": 23, "proteina": 1.1, "grasa": 0.3},
    "pan": {"calorias": 265, "carbs": 49, "proteina": 9, "grasa": 3.2},
    "pollo": {"calorias": 239, "carbs": 0, "proteina": 27, "grasa": 14},
    "arroz": {"calorias": 130, "carbs": 28, "proteina": 2.7, "grasa": 0.3},
    "tomate": {"calorias": 18, "carbs": 3.9, "proteina": 0.9, "grasa": 0.2},
    "lechuga": {"calorias": 15, "carbs": 2.9, "proteina": 1.4, "grasa": 0.2},
    "carne": {"calorias": 250, "carbs": 0, "proteina": 26, "grasa": 15},
    "pescado": {"calorias": 206, "carbs": 0, "proteina": 22, "grasa": 12},
    "huevo": {"calorias": 155, "carbs": 1.1, "proteina": 13, "grasa": 11}
}

def load_model():
    global model, classes
    try:
        model = tf.keras.models.load_model('modelo.h5')
        with open('classes.txt', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
    except:
        classes = ["manzana", "banana", "pan", "pollo", "arroz"]

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
    for food in nutricion.keys():
        if food in user_message:
            found_foods.append(food)
    
    if found_foods:
        response = "Información nutricional encontrada:\n\n"
        for food in found_foods:
            info = nutricion[food]
            response += f"🍎 {food.capitalize()}:\n"
            response += f"• Calorías: {info['calorias']} kcal\n"
            response += f"• Carbohidratos: {info['carbs']}g\n"
            response += f"• Proteína: {info['proteina']}g\n"
            response += f"• Grasa: {info['grasa']}g\n\n"
    else:
        response = "Lo siento, no encontré información nutricional específica en tu mensaje. Puedo ayudarte con información sobre: manzana, banana, pan, pollo, arroz, tomate, lechuga, carne, pescado, huevo."
    
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
