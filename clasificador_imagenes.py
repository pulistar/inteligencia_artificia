import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import glob


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"No se pudo cargar la imagen: {image_path}")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = image.astype(np.float32) / 255.0
    return image


def load_dataset(dataset_path):
    train_path = os.path.join(dataset_path, 'Training')
    val_path = os.path.join(dataset_path, 'Validation')
    test_path = os.path.join(dataset_path, 'Test')
    
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Carpeta de entrenamiento no encontrada: {train_path}")
    if not os.path.exists(val_path):
        raise FileNotFoundError(f"Carpeta de validación no encontrada: {val_path}")
    
    classes = os.listdir(train_path)
    num_classes = len(classes)
    
    train_images = []
    train_labels = []
    
    for i, class_name in enumerate(classes):
        class_path = os.path.join(train_path, class_name)
        image_files = glob.glob(os.path.join(class_path, '*.jpg')) + glob.glob(os.path.join(class_path, '*.png')) + glob.glob(os.path.join(class_path, '*.jpeg'))
        for image_path in image_files:
            try:
                image = preprocess_image(image_path)
                train_images.append(image)
                train_labels.append(i)
            except ValueError:
                print(f"Error cargando imagen: {image_path}")
                continue
    
    val_images = []
    val_labels = []
    
    for i, class_name in enumerate(classes):
        class_path = os.path.join(val_path, class_name)
        image_files = glob.glob(os.path.join(class_path, '*.jpg')) + glob.glob(os.path.join(class_path, '*.png')) + glob.glob(os.path.join(class_path, '*.jpeg'))
        for image_path in image_files:
            try:
                image = preprocess_image(image_path)
                val_images.append(image)
                val_labels.append(i)
            except ValueError:
                print(f"Error cargando imagen: {image_path}")
                continue
    
    test_images = []
    test_labels = []
    
    for i, class_name in enumerate(classes):
        class_path = os.path.join(test_path, class_name)
        if os.path.exists(class_path):
            image_files = glob.glob(os.path.join(class_path, '*.jpg')) + glob.glob(os.path.join(class_path, '*.png')) + glob.glob(os.path.join(class_path, '*.jpeg'))
            for image_path in image_files:
                try:
                    image = preprocess_image(image_path)
                    test_images.append(image)
                    test_labels.append(i)
                except ValueError:
                    print(f"Error cargando imagen: {image_path}")
                    continue
    
    train_images = np.array(train_images)
    train_labels = tf.keras.utils.to_categorical(train_labels, num_classes)
    val_images = np.array(val_images)
    val_labels = tf.keras.utils.to_categorical(val_labels, num_classes)
    test_images = np.array(test_images)
    test_labels = tf.keras.utils.to_categorical(test_labels, num_classes)
    
    return train_images, train_labels, val_images, val_labels, test_images, test_labels, classes, num_classes


def create_model(num_classes):
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False

    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def train_model(model, train_images, train_labels, val_images, val_labels, epochs=10, batch_size=32):
    callbacks = [
        keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=2)
    ]
    
    history = model.fit(
        train_images, train_labels,
        validation_data=(val_images, val_labels),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks
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


def evaluate_model(model, test_images, test_labels):
    if len(test_images) > 0:
        test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
        print(f"Test Loss: {test_loss:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        return test_loss, test_accuracy
    else:
        print("No hay imágenes de test disponibles")
        return None, None


def save_model_and_classes(model, classes, model_path='modelo.h5', classes_path='classes.txt'):
    model.save(model_path)
    
    with open(classes_path, 'w') as f:
        for class_name in classes:
            f.write(class_name + '\n')


def predecir_imagen(ruta_imagen, model_path='modelo.h5', classes_path='classes.txt'):
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
    print("Cargando dataset...")
    train_images, train_labels, val_images, val_labels, test_images, test_labels, classes, num_classes = load_dataset('dataset')
    
    print(f"Dataset cargado: {len(classes)} clases")
    print(f"Imágenes de entrenamiento: {len(train_images)}")
    print(f"Imágenes de validación: {len(val_images)}")
    print(f"Imágenes de test: {len(test_images)}")
    
    print("Creando modelo...")
    model = create_model(num_classes)
    
    print("Entrenando modelo...")
    history = train_model(model, train_images, train_labels, val_images, val_labels)
    
    plot_training_history(history)
    
    print("\nEvaluando modelo en conjunto de test...")
    evaluate_model(model, test_images, test_labels)
    
    print("Guardando modelo...")
    save_model_and_classes(model, classes)
    
    print("¡Entrenamiento completado!")


if __name__ == "__main__":
    main()
