import os
from PIL import Image

# Cargar las imágenes
img1_path = "D:/Descargas/Latex/latex/Tp 4-01/Figuras/image copy 6.png"
img2_path = "D:/Descargas/Latex/latex/Tp 4-01/Figuras/image copy 7.png"

img1 = Image.open(img1_path)
img2 = Image.open(img2_path)

# Igualar alturas para alinear filas
new_height = max(img1.height, img2.height)
img1_resized = img1.resize((int(img1.width * new_height / img1.height), new_height))
img2_resized = img2.resize((int(img2.width * new_height / img2.height), new_height))

# Crear imagen combinada (horizontal)
combined_width = img1_resized.width + img2_resized.width
combined_img = Image.new("RGB", (combined_width, new_height), (255, 255, 255))

# Pegar imágenes lado a lado
combined_img.paste(img1_resized, (0, 0))
combined_img.paste(img2_resized, (img1_resized.width, 0))

# Guardar resultado
output_path = "D:/Descargas/Latex/latex/Tp 4-01/Figuras/imagenes_unidas.png"
combined_img.save(output_path)

# Nombre base
output_path = "imagenes_unidas.png"

# Si existe, agregar un número al final
counter = 1
base, ext = os.path.splitext(output_path)
while os.path.exists(output_path):
    output_path = f"{base}_{counter}{ext}"
    counter += 1

combined_img.save(output_path)
print("Imagen guardada en:", output_path)
