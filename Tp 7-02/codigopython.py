

# -*- coding: utf-8 -*-
"""
Análisis de viga en voladizo con una carga puntual en el extremo.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- Parámetros iniciales ---
F0 = 1000          # Fuerza inicial [Kg]
L0 = 3             # Longitud inicial [m]
delta_max = 1e-2   # Deflexión máxima permitida [m]

# Lista de materiales Genéricos
materiales = [
    ('Acero',    210e9, 7850),
    ('Aluminio',  70e9, 2700),
    ('Titanio',  115e9, 4500),
    ('Madera',    11e9,  600),
    ('Polimero',   2e9, 1200)
]

def calcular_resultados(F, L):
    """Calcula espesor, masa e índice de Ashby para cada material."""
    resultados = []
    for nombre, E, rho in materiales:
        t = (4 * F * 10 * L**3 / (E * delta_max))**0.25
        m = rho * L * t**2
        M = np.sqrt((rho ^ 2) / (E))
        resultados.append((nombre, t, m, M))
    df = pd.DataFrame(resultados, columns=['Material', 'Espesor_m', 'Masa_kg', 'Indice_Ashby'])
    df = df.sort_values(by='Masa_kg', ascending=True).reset_index(drop=True)
    return df

# --- Cálculo inicial ---
T = calcular_resultados(F0, L0)

# --- Figura y gráfico ---
fig, ax = plt.subplots(figsize=(8,5))
plt.subplots_adjust(bottom=0.25)  # deja espacio para sliders

bars = ax.bar(T['Material'], T['Indice_Ashby'])
ax.set_ylabel(r'Índice de Ashby $E^{1/2} / \rho$')
ax.set_title(f'Eficiencia de materiales (F={F0:.0f} Kg, L={L0:.2f} m)')
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

# --- Sliders ---
ax_F = plt.axes([0.2, 0.10, 0.65, 0.03])
ax_L = plt.axes([0.2, 0.05, 0.65, 0.03])

slider_F = Slider(ax_F, 'F [Kg]', 100, 5000, valinit=F0, valstep=100)
slider_L = Slider(ax_L, 'L [m]', 1, 6, valinit=L0, valstep=0.1)

# --- Función de actualización ---
def actualizar(val):
    F = slider_F.val
    L = slider_L.val
    Tn = calcular_resultados(F, L)

    # Actualizar gráfico
    for rect, new_h in zip(bars, Tn['Indice_Ashby']):
        rect.set_height(new_h)

    ax.set_title(f'Eficiencia de materiales (F={F:.0f} Kg, L={L:.2f} m)')
    fig.canvas.draw_idle()

    # Mostrar tabla en consola
    print("\n=== Resultados ordenados por masa mínima ===")
    print(Tn.to_string(index=False, justify='center', col_space=12))
    mejor = Tn.loc[0, 'Material']
    print(f"\n👉 El material más eficiente en peso (menor masa) es: {mejor}")

# Conectar sliders
slider_F.on_changed(actualizar)
slider_L.on_changed(actualizar)

# Mostrar tabla inicial
print("\n=== Resultados iniciales (F=1000 Kg, L=3 m) ===")
print(T.to_string(index=False, justify='center', col_space=12))
print(f"\n👉 El material más eficiente en peso (menor masa) es: {T.loc[0, 'Material']}")

plt.show()
