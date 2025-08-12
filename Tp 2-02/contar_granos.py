import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
image_path = "Tp 2-02\Del-Rio_7.tif"  # ← reemplazá esto por el path real de tu imagen
min_area = 50  # área mínima para considerar un objeto como grano

# === PASO 1: Cargar la imagen ===
img = Image.open(image_path)
img_np = np.array(img)

# Convertir a escala de grises si es RGB
if len(img_np.shape) == 3:
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
else:
    gray = img_np

# === PASO 2: Desenfoque para reducir ruido ===
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# === PASO 3: Umbralización automática con Otsu ===
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# === PASO 4: Encontrar contornos externos ===
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# === PASO 5: Filtrar contornos por tamaño mínimo ===
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

# === PASO 6: Contar granos ===
grain_count = len(filtered_contours)
print(f"Cantidad de granos detectados: {grain_count}")

# === PASO 7: Visualización de los granos detectados ===
output_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
cv2.drawContours(output_img, filtered_contours, -1, (0, 255, 0), 1)

plt.figure(figsize=(10, 10))
plt.imshow(output_img)
plt.title(f"Granos detectados: {grain_count}")
plt.axis('off')
plt.tight_layout()
plt.show()
