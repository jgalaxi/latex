import numpy as np
import matplotlib.pyplot as plt

# Rango de subenfriamiento (ΔT) en °C
delta_T = np.linspace(1, 40, 400)

# Constantes B para diferentes nucleantes
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

# Graficar
plt.figure(figsize=(10, 6))

for nombre, B in materiales.items():
    P = probabilidad_nucleacion(B, delta_T)
    plt.plot(delta_T, P, label=nombre)

plt.title("Probabilidad relativa de nucleación heterogénea vs Subenfriamiento")
plt.xlabel("Subenfriamiento ΔT (°C)")
plt.ylabel("Probabilidad relativa")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
