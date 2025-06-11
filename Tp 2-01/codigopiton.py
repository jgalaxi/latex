import numpy as np
import matplotlib.pyplot as plt

# Rango de subenfriamiento (ΔT) en °C
delta_T = np.linspace(1, 40, 400)

# Materiales base con sus valores de B
materiales = {
    "Yoduro de plata (AgI)": 20,
    "Polvo mineral": 40,
    "Benceno": 100,
    "Ciclohexano": 110,
    "Agua pura (homogénea)": 150
}

# Función de nucleación
def probabilidad_nucleacion(B, delta_T):
    return np.exp(-B / (delta_T ** 2))

# Mostrar menú
def mostrar_menu():
    print("\n===== Menú de simulación de nucleación =====")
    print("1. Ver materiales actuales")
    print("2. Agregar nuevo material")
    print("3. Graficar")
    print("4. Salir")
    print("=============================================")

# Bucle de interacción
while True:
    mostrar_menu()
    opcion = input("Elegí una opción (1-4): ")

    if opcion == "1":
        print("\nMateriales actuales:")
        for nombre, B in materiales.items():
            print(f"- {nombre}: B = {B}")
    
    elif opcion == "2":
        nombre_nuevo = input("Nombre del nuevo material: ")
        try:
            B_nuevo = float(input("Valor de B para este material (mayor a 0): "))
            if B_nuevo <= 0:
                print("⚠️ El valor de B debe ser mayor a 0.")
            else:
                materiales[nombre_nuevo] = B_nuevo
                print(f"✅ Material '{nombre_nuevo}' agregado con B = {B_nuevo}")
        except ValueError:
            print("❌ Entrada inválida. Debe ser un número.")

    elif opcion == "3":
        plt.figure(figsize=(10, 6))
        for nombre, B in materiales.items():
            P = probabilidad_nucleacion(B, delta_T)
            plt.plot(delta_T, P, label=f"{nombre} (B={B})")
        plt.title("Probabilidad relativa de nucleación heterogénea vs Subenfriamiento")
        plt.xlabel("Subenfriamiento ΔT (°C)")
        plt.ylabel("Probabilidad relativa (valor adimensional)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    elif opcion == "4":
        print("👋 Saliendo del programa. ¡Hasta luego!")
        break

    else:
        print("❌ Opción inválida. Elegí entre 1 y 4.")
