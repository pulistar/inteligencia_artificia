import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
import os

def create_data_generators_simple(dataset_path, batch_size=32, img_size=(224, 224)):
    train_path = os.path.join(dataset_path, 'Training')
    test_path = os.path.join(dataset_path, 'Test')
    
    # Usar 20% del training como validación automáticamente
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.1,
        validation_split=0.2  # 20% para validación
    )
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'  # 80% para entrenamiento
    )
    
    val_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'  # 20% para validación
    )
    
    test_generator = test_datagen.flow_from_directory(
        test_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )
    
    return train_generator, val_generator, test_generator

def create_model(num_classes):
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False

    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model_simple(model, train_gen, val_gen, epochs=8):
    callbacks = [
        keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=2, min_lr=1e-7),
        keras.callbacks.ModelCheckpoint('best_model_simple.h5', save_best_only=True)
    ]
    
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

def evaluate_model_simple(model, test_gen):
    print("Evaluando modelo...")
    test_loss, test_accuracy = model.evaluate(test_gen, verbose=1)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    return test_loss, test_accuracy

def save_model_and_classes(model, class_names, model_path='modelo_simple.h5', classes_path='classes_simple.txt'):
    model.save(model_path)
    
    with open(classes_path, 'w') as f:
        for class_name in class_names:
            f.write(class_name + '\n')
    
    print(f"Modelo guardado en: {model_path}")
    print(f"Clases guardadas en: {classes_path}")

def main():
    print("=== CLASIFICADOR SIMPLE (TRAINING + TEST) ===")
    print("Configurando generadores de datos...")
    
    # Batch size más grande para dataset más pequeño
    batch_size = 32
    
    train_gen, val_gen, test_gen = create_data_generators_simple('dataset_simple', batch_size=batch_size)
    
    num_classes = train_gen.num_classes
    class_names = list(train_gen.class_indices.keys())
    
    print(f"Dataset configurado:")
    print(f"- Clases: {num_classes}")
    print(f"- Imágenes de entrenamiento: {train_gen.samples}")
    print(f"- Imágenes de validación: {val_gen.samples}")
    print(f"- Imágenes de test: {test_gen.samples}")
    print(f"- Batch size: {batch_size}")
    
    print("\nCreando modelo...")
    model = create_model(num_classes)
    
    print("Iniciando entrenamiento...")
    print("(Dataset más pequeño = entrenamiento más rápido)")
    
    # Más épocas porque es más rápido
    history = train_model_simple(model, train_gen, val_gen, epochs=8)
    
    print("\nMostrando gráficas de entrenamiento...")
    plot_training_history(history)
    
    print("\nEvaluando modelo...")
    evaluate_model_simple(model, test_gen)
    
    print("\nGuardando modelo...")
    save_model_and_classes(model, class_names)
    
    print("¡Entrenamiento completado!")
    print("Archivos generados:")
    print("- modelo_simple.h5")
    print("- best_model_simple.h5")
    print("- classes_simple.txt")

if __name__ == "__main__":
    main()
