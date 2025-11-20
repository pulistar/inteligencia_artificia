import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
import os

def create_data_generators_20_clases(dataset_path, batch_size=32, img_size=(224, 224)):
    train_path = os.path.join(dataset_path, 'Training')
    test_path = os.path.join(dataset_path, 'Test')
    
    # 20 clases principales que queremos reconocer
    clases_principales = [
        'Apple', 'Banana', 'Orange', 'Tomato', 'Carrot', 
        'Cucumber', 'Onion', 'Peach', 'Pear', 'Cherry',
        'Grape', 'Pepper', 'Potato', 'Avocado', 'Mango',
        'Strawberry', 'Lemon', 'Watermelon', 'Corn', 'Eggplant'
    ]
    
    # Encontrar carpetas que coincidan con nuestras clases principales
    all_classes = os.listdir(train_path)
    selected_classes = []
    
    for clase_principal in clases_principales:
        for folder_name in all_classes:
            if clase_principal.lower() in folder_name.lower():
                if folder_name not in selected_classes:
                    selected_classes.append(folder_name)
                    break
    
    # Limitar a 20 clases máximo
    selected_classes = selected_classes[:20]
    
    print(f"Clases seleccionadas ({len(selected_classes)}):")
    for i, clase in enumerate(selected_classes):
        print(f"  {i+1}. {clase}")
    
    # Data augmentation para training (SIN cargar todo en memoria)
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        validation_split=0.2  # 20% para validación
    )
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Generadores que cargan imágenes bajo demanda (NO en memoria)
    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',  # 80% para entrenamiento
        classes=selected_classes  # Solo las 20 clases seleccionadas
    )
    
    val_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',  # 20% para validación
        classes=selected_classes  # Solo las 20 clases seleccionadas
    )
    
    test_generator = test_datagen.flow_from_directory(
        test_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False,
        classes=selected_classes  # Solo las 20 clases seleccionadas
    )
    
    return train_generator, val_generator, test_generator

def create_model(num_classes):
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False

    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model_optimizado(model, train_gen, val_gen, epochs=10):
    callbacks = [
        keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3, min_lr=1e-7),
        keras.callbacks.ModelCheckpoint('best_model_20_clases.h5', save_best_only=True)
    ]
    
    print("Entrenando con generadores de datos (sin cargar todo en memoria)...")
    
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )
    
    return history

def plot_training_history(history):
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.tight_layout()
    plt.show()

def evaluate_model_optimizado(model, test_gen):
    print("Evaluando modelo...")
    test_loss, test_accuracy = model.evaluate(test_gen, verbose=1)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    return test_loss, test_accuracy

def save_model_and_classes(model, class_names, model_path='modelo.h5', classes_path='classes.txt'):
    model.save(model_path)
    
    with open(classes_path, 'w') as f:
        for class_name in class_names:
            f.write(class_name + '\n')
    
    print(f"Modelo guardado en: {model_path}")
    print(f"Clases guardadas en: {classes_path}")

def predecir_imagen(ruta_imagen, model_path='modelo.h5', classes_path='classes.txt'):
    import cv2
    
    modelo = tf.keras.models.load_model(model_path)
    
    with open(classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    
    image = cv2.imread(ruta_imagen)
    if image is None:
        raise ValueError(f"No se pudo cargar la imagen: {ruta_imagen}")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = image.astype(np.float32) / 255.0
    image = np.expand_dims(image, axis=0)
    
    predictions = modelo.predict(image)
    predicted_class = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_class])
    
    return classes[predicted_class], confidence * 100

def main():
    print("=== CLASIFICADOR 20 CLASES CON GENERADORES ===")
    print("Usando generadores de datos para no cargar todo en memoria")
    print("Configurando generadores de datos...")
    
    # Batch size optimizado para 20 clases
    batch_size = 32
    
    train_gen, val_gen, test_gen = create_data_generators_20_clases('dataset', batch_size=batch_size)
    
    num_classes = train_gen.num_classes
    class_names = list(train_gen.class_indices.keys())
    
    print(f"\nDataset configurado:")
    print(f"- Clases: {num_classes}")
    print(f"- Imágenes de entrenamiento: {train_gen.samples}")
    print(f"- Imágenes de validación: {val_gen.samples}")
    print(f"- Imágenes de test: {test_gen.samples}")
    print(f"- Batch size: {batch_size}")
    
    print("\nCreando modelo...")
    model = create_model(num_classes)
    
    print("Iniciando entrenamiento...")
    print("(Los generadores cargan imágenes bajo demanda, no satura la memoria)")
    
    # Entrenar con generadores
    history = train_model_optimizado(model, train_gen, val_gen, epochs=10)
    
    print("\nMostrando gráficas de entrenamiento...")
    plot_training_history(history)
    
    print("\nEvaluando modelo...")
    evaluate_model_optimizado(model, test_gen)
    
    print("\nGuardando modelo...")
    save_model_and_classes(model, class_names)
    
    print("¡Entrenamiento completado!")
    print("Archivos generados:")
    print("- modelo.h5")
    print("- best_model_20_clases.h5")
    print("- classes.txt")
    print(f"\nEste método NO carga todo en memoria, solo procesa por lotes de {batch_size}")

if __name__ == "__main__":
    main()
