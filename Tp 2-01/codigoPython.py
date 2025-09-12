import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Datos iniciales
DeltaT = np.linspace(0.1, 100, 500)
B_init = 20

# Función
def P_deltaT(B):
    return np.exp(-B / DeltaT)

# Crear figura
fig, ax = plt.subplots(figsize=(8,6))
plt.subplots_adjust(left=0.1, bottom=0.25)

# Gráfico inicial
line, = plt.plot(DeltaT, P_deltaT(B_init), lw=2)
ax.set_title("Probabilidad de nucleación heterogénea")
ax.set_xlabel("ΔT (subenfriamiento)")
ax.set_ylabel("P(ΔT)")
ax.set_ylim(0, 1.05)
ax.grid(True)

# Slider
ax_B = plt.axes([0.1, 0.1, 0.65, 0.03])
slider_B = Slider(ax_B, 'B', 1, 100, valinit=B_init)

# Actualización
def update(val):
    B = slider_B.val
    line.set_ydata(P_deltaT(B))
    fig.canvas.draw_idle()

slider_B.on_changed(update)

plt.show()
