import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
from skimage.segmentation import watershed
from scipy import ndimage as ndi

def contar_granos(ruta_imagen, mostrar_resultado=True):
    # Cargar imagen en escala de grises
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("No se pudo cargar la imagen. Verificá la ruta.")

    # Paso 1: Preprocesamiento
    img_blur = cv2.GaussianBlur(img, (5, 5), 0)
    img_eq = cv2.equalizeHist(img_blur)

    # Paso 2: Umbral adaptativo
    thresh = cv2.adaptiveThreshold(img_eq, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 51, 2)

    # Paso 3: Limpieza morfológica
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Paso 4: Transformada de distancia y watershed
    distancia = cv2.distanceTransform(opened, cv2.DIST_L2, 5)
    _, marcadores_binarios = cv2.threshold(distancia, 0.3 * distancia.max(), 255, 0)
    marcadores_binarios = np.uint8(marcadores_binarios)

    # Etiquetado y segmentación
    etiquetas, _ = cv2.connectedComponents(marcadores_binarios)
    marcadores_ws = watershed(-distancia, etiquetas, mask=opened)

    # Conteo
    props = measure.regionprops(marcadores_ws)
    cantidad_granos = len(props)

    if mostrar_resultado:
        plt.figure(figsize=(10, 7))
        plt.imshow(img, cmap='gray')
        plt.title(f"Cantidad de granos detectados: {cantidad_granos}")
        for prop in props:
            y, x = prop.centroid
            plt.plot(x, y, 'r.', markersize=2)
        plt.axis("off")
        plt.show()

    return cantidad_granos

# Ejemplo de uso
if __name__ == "__main__":
    ruta = "latex-1\Tp 2-02\Del-Rio_7.tif"  # Cambiar por la ruta a tu imagen
    total = contar_granos(ruta)
    print(f"Cantidad total de granos detectados: {total}")
