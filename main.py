import os
from PIL import Image
import cv2


# Función para detectar y recortar fotos
def extract_photos_from_page(image_path, output_folder):
    # Leer la imagen
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, GREY_LEVEL_MIN, GREY_LEVEL_MAX, cv2.THRESH_BINARY_INV)

    # Detectar contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Asegurarse de que el nombre de la carpeta sea el nombre del archivo
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    photo_output_folder = os.path.join(output_folder, base_name)
    os.makedirs(photo_output_folder, exist_ok=True)

    # Recortar y guardar cada foto detectada
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if w > WIDTH_MIN and h > HEIGHT_MIN:  # Ignorar pequeños recortes
            cropped = image[y:y + h, x:x + w]
            output_path = os.path.join(photo_output_folder, f"photo_{i + 1}.tif")
            cv2.imwrite(output_path, cropped)


GREY_LEVEL_MIN = 150
GREY_LEVEL_MAX = 255
WIDTH_MIN = 400
HEIGHT_MIN = 400

# Rutas de entrada y salida
input_folder = "pages"  # Carpeta con las imágenes TIFF
output_folder = "output_images"  # Carpeta donde se guardarán las fotos recortadas

# Crear carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)


# Procesar todas las imágenes en la carpeta
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith((".tiff", ".tif")):
        file_path = os.path.join(input_folder, file_name)
        extract_photos_from_page(file_path, output_folder)

print(f"Fotos recortadas y guardadas en: {output_folder}")
