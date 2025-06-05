import numpy as np
import matplotlib.pyplot as plt

def simular_crecimiento_cristal_hielo(radio_inicial_nm, tasa_crecimiento_nm_por_seg, tiempo_simulacion_seg):
    """
    Simula el crecimiento del radio de un cristal de hielo.
    radio_inicial_nm: Radio inicial del núcleo (en nanómetros).
    tasa_crecimiento_nm_por_seg: Tasa a la que el radio aumenta (en nm/seg).
                                  Esta tasa es simplificada y representa la atracción de vapor de agua.
    tiempo_simulacion_seg: Duración total de la simulación (en segundos).
    """
    tiempos = np.arange(0, tiempo_simulacion_seg + 1, 1) # Pasos de 1 segundo
    radios = []

    for t in tiempos:
        radio_actual = radio_inicial_nm + (t * tasa_crecimiento_nm_por_seg)
        radios.append(radio_actual)

    return np.array(tiempos), np.array(radios)

# --- Parámetros de la simulación ---
RADIO_INICIAL_NUCLEO_NM = 0.5  # Asumiendo un núcleo pequeño, por ejemplo, el tamaño de AgI
# Radio crítico para que la gota caiga (aproximadamente 100 micrómetros = 100,000 nanómetros)
RADIO_CRITICO_PARA_CAER_NM = 100 * 1000 # 100 micrómetros, un valor de referencia simplificado

TIEMPO_SIMULACION_SEG = 600 # 10 minutos para ver mejor el crecimiento

# --- Ejemplos concretos de tasas de crecimiento (reflejando condiciones de la nube) ---
# Caso 1: Nube con ALTA HUMEDAD y MAYOR SUBENFRIAMIENTO (e.g., -15°C) -> TASA DE CRECIMIENTO RÁPIDA
TASA_CRECIMIENTO_CONDICIONES_FAVORABLES = 300 # nm/seg (valor hipotético alto)

# Caso 2: Nube con BAJA HUMEDAD y MENOR SUBENFRIAMIENTO (e.g., -5°C) -> TASA DE CRECIMIENTO LENTA
TASA_CRECIMIENTO_CONDICIONES_DESFAVORABLES = 50 # nm/seg (valor hipotético bajo)

# --- Ejecutar simulaciones ---
tiempos_favorables, radios_favorables = simular_crecimiento_cristal_hielo(
    RADIO_INICIAL_NUCLEO_NM, TASA_CRECIMIENTO_CONDICIONES_FAVORABLES, TIEMPO_SIMULACION_SEG
)

tiempos_desfavorables, radios_desfavorables = simular_crecimiento_cristal_hielo(
    RADIO_INICIAL_NUCLEO_NM, TASA_CRECIMIENTO_CONDICIONES_DESFAVORABLES, TIEMPO_SIMULACION_SEG
)

# --- Graficar resultados ---
plt.figure(figsize=(10, 6))
plt.plot(tiempos_favorables, radios_favorables, label=f'Condiciones Favorables (Alta humedad, Mayor subenfriamiento)', color='green')
plt.plot(tiempos_desfavorables, radios_desfavorables, label=f'Condiciones Desfavorables (Baja humedad, Menor subenfriamiento)', color='orange', linestyle='--')

# Marcar el radio crítico
plt.axhline(y=RADIO_CRITICO_PARA_CAER_NM, color='red', linestyle=':', label=f'Radio Crítico para Caer ({RADIO_CRITICO_PARA_CAER_NM/1000:.0f} µm)')

plt.title('Simulación del Crecimiento de un Cristal de Hielo en Diferentes Condiciones de Nube')
plt.xlabel('Tiempo (segundos)')
plt.ylabel('Radio del Cristal de Hielo (nanómetros)')
plt.grid(True)
plt.legend()
plt.ylim(bottom=0) # Asegurar que el eje y empiece en 0
plt.ticklabel_format(style='plain', axis='y') # Evita notación científica en el eje Y

# Anotaciones
idx_caer_favorables = np.where(radios_favorables >= RADIO_CRITICO_PARA_CAER_NM)[0]
if len(idx_caer_favorables) > 0:
    tiempo_caer_favorables = tiempos_favorables[idx_caer_favorables[0]]
    plt.annotate(f'Caída esperada en: {tiempo_caer_favorables:.0f} s',
                 xy=(tiempo_caer_favorables, RADIO_CRITICO_PARA_CAER_NM),
                 xytext=(tiempo_caer_favorables + 50, RADIO_CRITICO_PARA_CAER_NM * 0.8),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 ha='left')
else:
    plt.annotate(f'No alcanza radio crítico en {TIEMPO_SIMULACION_SEG} s',
                 xy=(TIEMPO_SIMULACION_SEG, radios_favorables[-1]),
                 xytext=(TIEMPO_SIMULACION_SEG - 100, radios_favorables[-1] * 1.2),
                 color='blue', fontsize=10)

idx_caer_desfavorables = np.where(radios_desfavorables >= RADIO_CRITICO_PARA_CAER_NM)[0]
if len(idx_caer_desfavorables) > 0:
    tiempo_caer_desfavorables = tiempos_desfavorables[idx_caer_desfavorables[0]]
    plt.annotate(f'Caída esperada en: {tiempo_caer_desfavorables:.0f} s',
                 xy=(tiempo_caer_desfavorables, RADIO_CRITICO_PARA_CAER_NM),
                 xytext=(tiempo_caer_desfavorables - 150, RADIO_CRITICO_PARA_CAER_NM * 1.1),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 ha='right')
else:
    plt.annotate(f'No alcanza radio crítico en {TIEMPO_SIMULACION_SEG} s',
                 xy=(TIEMPO_SIMULACION_SEG, radios_desfavorables[-1]),
                 xytext=(TIEMPO_SIMULACION_SEG - 100, radios_desfavorables[-1] * 1.2),
                 color='red', fontsize=10)


plt.tight_layout()
plt.show()

print("\nAnálisis de los resultados de la simulación de crecimiento de cristal de hielo:")
print(f"Esta simulación demuestra cómo la 'tasa de crecimiento' de los cristales de hielo, influenciada por factores como la humedad y el subenfriamiento de la nube, afecta el tiempo necesario para que las partículas de hielo alcancen un tamaño suficiente para caer como precipitación.")
print(f"Bajo 'condiciones favorables' (alta humedad, mayor subenfriamiento, representado por una tasa de crecimiento de {TASA_CRECIMIENTO_CONDICIONES_FAVORABLES} nm/s), los cristales crecen mucho más rápido y alcanzan el tamaño de caída de {RADIO_CRITICO_PARA_CAER_NM/1000:.0f} µm en un tiempo menor.")
print(f"Por el contrario, bajo 'condiciones desfavorables' (baja humedad, menor subenfriamiento, representado por una tasa de crecimiento de {TASA_CRECIMIENTO_CONDICIONES_DESFAVORABLES} nm/s), el crecimiento es más lento, y puede que los cristales no alcancen el tamaño de caída deseado en el mismo período de tiempo.")
print(f"Esto resalta que, incluso con la nucleación, el crecimiento del cristal es un paso crítico para que la lluvia ocurra.")