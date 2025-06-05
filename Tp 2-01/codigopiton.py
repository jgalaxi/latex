import numpy as np
import matplotlib.pyplot as plt

def probabilidad_nucleacion_simplificada(temperatura_celsius, temp_nucleacion_minima):
    """
    Función simplificada para representar la "probabilidad" o "facilidad" de nucleación.
    Se asume una probabilidad muy baja por encima de la temperatura mínima,
    y que aumenta exponencialmente a medida que la temperatura desciende por debajo de ella,
    llegando a 1 (o un valor alto) muy por debajo.
    """
    if temperatura_celsius >= temp_nucleacion_minima:
        return 0.01  # Muy baja probabilidad si está por encima o justo en la temp mínima
    else:
        # Usamos una función sigmoide inversa o algo similar para que crezca rápido
        # Cuanto más frío, mayor la "probabilidad"
        delta_t = temp_nucleacion_minima - temperatura_celsius
        # Ajustamos el factor para que la curva sea significativa
        return 1.0 - np.exp(-delta_t / 5) # El '5' controla la pendiente de la curva

# Temperaturas de nucleación dadas en el texto [cite: 12, 24]
TEMP_HOMOGENEA = -40  # °C [cite: 12]
TEMP_HETEROGENEA_AGI = -4  # °C (con yoduro de plata) [cite: 24]

# Rango de temperaturas a simular
temperaturas = np.arange(-50, 5, 0.5) # Desde -50°C hasta 5°C

# Calcular la "probabilidad" o "facilidad" para cada escenario
prob_homogenea = [probabilidad_nucleacion_simplificada(T, TEMP_HOMOGENEA) for T in temperaturas]
prob_heterogenea = [probabilidad_nucleacion_simplificada(T, TEMP_HETEROGENEA_AGI) for T in temperaturas]

# Graficar los resultados
plt.figure(figsize=(10, 6))
plt.plot(temperaturas, prob_homogenea, label=f'Nucleación Homogénea (sin catalizador, umbral: {TEMP_HOMOGENEA}°C)', color='blue')
plt.plot(temperaturas, prob_heterogenea, label=f'Nucleación Heterogénea (con Yoduro de Plata, umbral: {TEMP_HETEROGENEA_AGI}°C)', color='red', linestyle='--')

# Marcar las temperaturas umbral
plt.axvline(x=TEMP_HOMOGENEA, color='blue', linestyle=':', label=f'Umbral Homogéneo ({TEMP_HOMOGENEA}°C)')
plt.axvline(x=TEMP_HETEROGENEA_AGI, color='red', linestyle=':', label=f'Umbral Heterogéneo ({TEMP_HETEROGENEA_AGI}°C)')

plt.title('Facilidad de Nucleación de Hielo vs. Temperatura')
plt.xlabel('Temperatura (°C)')
plt.ylabel('Facilidad de Nucleación (Valor relativo)')
plt.grid(True)
plt.legend()
plt.annotate(f'Las nubes rara vez se enfrían a {TEMP_HOMOGENEA}°C[cite: 13].', xy=(TEMP_HOMOGENEA, 0.8), xytext=(TEMP_HOMOGENEA + 5, 0.9),
             arrowprops=dict(facecolor='black', shrink=0.05),
             ha='left', va='center')
plt.annotate(f'El yoduro de plata reduce el subenfriamiento a {abs(TEMP_HETEROGENEA_AGI)}°C[cite: 24].', xy=(TEMP_HETEROGENEA_AGI, 0.8), xytext=(TEMP_HETEROGENEA_AGI - 15, 0.7),
             arrowprops=dict(facecolor='black', shrink=0.05),
             ha='right', va='center')

plt.tight_layout()
plt.show()

# Explicación de los resultados
print("\nAnálisis de los resultados:")
print(f"El gráfico muestra cómo la 'facilidad' o 'probabilidad' de nucleación de hielo cambia con la temperatura.")
print(f"Para la nucleación homogénea (sin impurezas/catalizadores), el hielo solo se forma si la nube se enfría hasta una temperatura muy baja de {TEMP_HOMOGENEA}°C[cite: 12].")
print(f"Las nubes rara vez alcanzan esta temperatura tan baja[cite: 13].")
print(f"Sin embargo, con la introducción de un catalizador como el yoduro de plata, la nucleación heterogénea puede ocurrir a temperaturas mucho más cercanas a 0°C, específicamente a tan solo {TEMP_HETEROGENEA_AGI}°C de subenfriamiento[cite: 24].")
print(f"Esto demuestra por qué el yoduro de plata es tan efectivo para provocar lluvia artificial: reduce drásticamente el requerimiento de temperatura para que las gotas de agua se congelen y formen núcleos de hielo[cite: 24].")
print("La polución industrial, con sus impurezas, también puede catalizar la nucleación a temperaturas cercanas a 0°C, lo que explica el aumento de precipitaciones a favor del viento de las chimeneas industriales[cite: 20, 21].")