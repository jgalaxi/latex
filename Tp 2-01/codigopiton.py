import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider
from IPython.display import display, Markdown

# Punto de congelación del agua
T_f = 0  # °C

# Función de probabilidad
def probabilidad_nucleacion(B, T):
    delta_T = T_f - T
    if delta_T <= 0:
        return 0  # No hay nucleación si no hay subenfriamiento
    return np.exp(-B / (delta_T ** 2))

# Función de visualización
def graficar_interactivo(B=50, T=-10):
    delta_T_range = np.linspace(1, 40, 400)
    P_curve = np.exp(-B / (delta_T_range ** 2))

    P_puntual = probabilidad_nucleacion(B, T)

    # Gráfica
    plt.figure(figsize=(9, 5))
    plt.plot(delta_T_range, P_curve, label=f"Curva completa (B = {B})")
    plt.axvline(T_f - T, color="red", linestyle="--", label=f"ΔT actual = {T_f - T:.1f} °C")
    plt.axhline(P_puntual, color="green", linestyle="--", label=f"P(ΔT) = {P_puntual:.4f}")
    plt.title("Probabilidad relativa de nucleación vs Subenfriamiento")
    plt.xlabel("ΔT (°C)")
    plt.ylabel("Probabilidad relativa")
    plt.ylim(0, 1.05)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Mostrar en texto la interpretación
    display(Markdown(f"""
**Datos actuales:**

- Material (B): `{B}`
- Temperatura actual: `{T} °C`
- Subenfriamiento: `{T_f - T:.1f} °C`
- Probabilidad relativa de nucleación: `{P_puntual:.4f}`
"""))

# Sliders
interact(
    graficar_interactivo,
    B=FloatSlider(value=50, min=10, max=200, step=1, description="B (material)"),
    T=FloatSlider(value=-10, min=-40, max=0, step=0.5, description="Temperatura (°C)")
);
