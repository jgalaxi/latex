import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label
from skimage.segmentation import watershed
from scipy import ndimage as ndi
import pandas as pd
import os

def contar_granos_con_areas(ruta_imagen, tam_pixel_um=3.2, guardar=True):
    # Cargar imagen en escala de grises
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {ruta_imagen}")

    # Suavizado y ecualización
    img_blur = cv2.GaussianBlur(img, (5, 5), 0)
    img_eq = cv2.equalizeHist(img_blur)

    # Umbral adaptativo
    binary = cv2.adaptiveThreshold(img_eq, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 51, 2)

    # Morfología para limpiar
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary_clean = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    # Transformada de distancia + watershed
    distance = cv2.distanceTransform(binary_clean, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(distance, 0.3 * distance.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    markers, _ = cv2.connectedComponents(sure_fg)
    labels = watershed(-distance, markers, mask=binary_clean)

    # Propiedades de cada grano
    regiones = regionprops(label(labels))
    num_granos = len(regiones)

    # Cálculo de áreas
    pixel_area_um2 = tam_pixel_um ** 2
    areas_um2 = [r.area * pixel_area_um2 for r in regiones]

    # Dibujar resultados sobre la imagen original
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for i, region in enumerate(regiones, 1):
        y, x = region.centroid
        cv2.circle(img_color, (int(x), int(y)), 4, (0, 0, 255), -1)
        cv2.putText(img_color, str(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, (0, 255, 0), 1, cv2.LINE_AA)

    # Mostrar
    plt.figure(figsize=(10, 7))
    plt.imshow(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))
    plt.title(f"Cantidad de granos detectados: {num_granos}")
    plt.axis("off")
    plt.show()

    # Guardar archivos
    if guardar:
        nombre_base = os.path.splitext(os.path.basename(ruta_imagen))[0]
        img_out_path = f"{nombre_base}_segmentado.png"
        csv_out_path = f"{nombre_base}_areas.csv"

        cv2.imwrite(img_out_path, img_color)
        pd.DataFrame({"Grano": np.arange(1, num_granos + 1),
                      "Área (µm²)": areas_um2}).to_csv(csv_out_path, index=False)

        print(f"✔ Imagen segmentada guardada como: {img_out_path}")
        print(f"✔ Datos de área guardados como: {csv_out_path}")

    return num_granos, areas_um2

# Ejemplo de uso
if __name__ == "__main__":
    imagen = "Tp 2-02\Del-Rio_7.tif"  # Cambiá el nombre por el tuyo
    contar_granos_con_areas(imagen, tam_pixel_um=3.2)
