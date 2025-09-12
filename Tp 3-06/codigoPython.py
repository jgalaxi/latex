import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- Constantes ---
R = 8.314
Q = 240e3
n = 4.0

def hoop_stress_MPa(p_bar, r_mm, t_mm):
    p_MPa = p_bar * 0.1
    return p_MPa * (r_mm / t_mm)

def calibrate_A(tr_minutes, T_C, sigma_MPa, Q=Q, n=n):
    T_K = T_C + 273.15
    tr_s = tr_minutes * 60.0
    return tr_s / ((sigma_MPa**(-n)) * np.exp(Q/(R*T_K)))

A = calibrate_A(15.0, 900.0, 50.0)

def rupture_time_minutes(T_C, sigma_MPa, A=A, Q=Q, n=n):
    T_K = T_C + 273.15
    return (A * (sigma_MPa**(-n)) * np.exp(Q/(R*T_K))) / 60.0

# --- Setup inicial ---
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)

temps_C = np.linspace(700, 1100, 300)

# Valores iniciales
T0 = 900
p0 = 50    # bar
r0 = 50    # mm
t0 = 5     # mm
sigma0 = hoop_stress_MPa(p0, r0, t0)

(line,) = ax.semilogy(temps_C, rupture_time_minutes(temps_C, sigma0), lw=2)
ax.set_xlabel("Temperatura (°C)")
ax.set_ylabel("Tiempo a rotura (min, escala log)")
ax.set_title("Tiempo a rotura en función de T con sliders de presión, radio y espesor")
ax.grid(True, which="both", linestyle=":")

# --- Sliders ---
ax_p = plt.axes([0.25, 0.20, 0.65, 0.03])
slider_p = Slider(ax_p, "Presión (bar)", 10, 100, valinit=p0)

ax_r = plt.axes([0.25, 0.15, 0.65, 0.03])
slider_r = Slider(ax_r, "Radio (mm)", 10, 100, valinit=r0)

ax_t = plt.axes([0.25, 0.10, 0.65, 0.03])
slider_t = Slider(ax_t, "Espesor (mm)", 2, 15, valinit=t0)

# Función de actualización
def update(val):
    sigma = hoop_stress_MPa(slider_p.val, slider_r.val, slider_t.val)
    line.set_ydata(rupture_time_minutes(temps_C, sigma))
    fig.canvas.draw_idle()

slider_p.on_changed(update)
slider_r.on_changed(update)
slider_t.on_changed(update)

plt.show()

