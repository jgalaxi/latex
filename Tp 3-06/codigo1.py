import numpy as np
import matplotlib.pyplot as plt

# Parámetros geométricos y de operación
P = 5e6        # presión interna [Pa] = 50 bar
r = 0.05       # radio interno [m]
t = 0.005      # espesor [m]

sigma = (P * r) / t
print(f"Tensión de pared: {sigma/1e6:.2f} MPa")

# Datos dureza
dist = np.linspace(0, 10, 100)
hardness = 1.5 + 2.5*np.exp(-dist/2)

# Datos fluencia
R = 8.314
Q = 250e3
A = 1e20
def creep_time(T, sigma):
    return 1/(A*np.exp(-Q/(R*T))*sigma) / 60

temps = np.linspace(800+273, 1000+273, 100)
times = [creep_time(T, sigma) for T in temps]

# Crear figura con 2 subplots en una columna
fig, axs = plt.subplots(2, 1, figsize=(7, 10))

# Subplot 1: dureza
axs[0].plot(dist, hardness, 'r-', lw=2)
axs[0].set_xlabel("Distancia al borde [mm]")
axs[0].set_ylabel("Dureza [GPa]")
axs[0].set_title("Perfil de durezas en tubería rota")
axs[0].grid(True)

# Subplot 2: fluencia
axs[1].semilogy(temps-273, times, 'b-', lw=2)
axs[1].set_xlabel("Temperatura [°C]")
axs[1].set_ylabel("Tiempo a rotura [min]")
axs[1].set_title("Tiempo a rotura por fluencia vs Temperatura")
axs[1].grid(True, which="both")

plt.tight_layout()
plt.show()
