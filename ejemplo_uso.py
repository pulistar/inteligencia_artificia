from clasificador_imagenes import predecir_imagen, main, load_dataset, evaluate_model

# Ejemplo 1: Entrenar un nuevo modelo con train/val/test
# Descomenta las siguientes líneas para entrenar
# print("Entrenando modelo...")
# main()

# Ejemplo 2: Usar modelo ya entrenado para predicción
def ejemplo_prediccion():
    """
    Ejemplo de cómo usar el modelo para hacer predicciones.
    """
    # Ruta a la imagen que quieres clasificar
    ruta_imagen = "ruta/a/tu/imagen.jpg"
    
    try:
        clase, confianza = predecir_imagen(ruta_imagen)
        print(f"Predicción: {clase}")
        print(f"Confianza: {confianza:.2f}%")
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")

# Ejemplo 3: Solo cargar y ver estadísticas del dataset
def ver_estadisticas_dataset():
    """
    Muestra estadísticas del dataset sin entrenar.
    """
    try:
        train_images, train_labels, val_images, val_labels, test_images, test_labels, classes, num_classes = load_dataset('dataset')
        
        print("=== ESTADÍSTICAS DEL DATASET ===")
        print(f"Número de clases: {num_classes}")
        print(f"Clases: {classes}")
        print(f"Imágenes de entrenamiento: {len(train_images)}")
        print(f"Imágenes de validación: {len(val_images)}")
        print(f"Imágenes de test: {len(test_images)}")
        print(f"Total de imágenes: {len(train_images) + len(val_images) + len(test_images)}")
        
    except Exception as e:
        print(f"Error al cargar dataset: {e}")
        print("Asegúrate de tener la estructura:")
        print("dataset/")
        print("├── train/")
        print("│   ├── clase1/")
        print("│   └── clase2/")
        print("├── val/")
        print("│   ├── clase1/")
        print("│   └── clase2/")
        print("└── test/")
        print("    ├── clase1/")
        print("    └── clase2/")

if __name__ == "__main__":
    # Descomenta la función que quieras probar:
    
    # ver_estadisticas_dataset()  # Para ver info del dataset
    ejemplo_prediccion()  # Para hacer predicciones
