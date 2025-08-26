import numpy as np
import matplotlib.pyplot as plt

# Constantes
R = 8.314        # J/mol-K
Q = 240e3        # J/mol
n = 4.0          # exponente de tensión (aceros ferríticos)

# ---------------- Funciones básicas ----------------
def hoop_stress_MPa(p_bar, r_mm, t_mm):
    """Tensión circunferencial de un tubo de pared delgada (MPa)."""
    p_MPa = p_bar * 0.1
    return p_MPa * (r_mm / t_mm)

def calibrate_A(tr_minutes, T_C, sigma_MPa, Q=Q, n=n):
    """Calibrar constante A según un punto experimental."""
    T_K = T_C + 273.15
    tr_s = tr_minutes * 60.0
    return tr_s / ((sigma_MPa**(-n)) * np.exp(Q/(R*T_K)))

# Calibración con el caso de estudio: 900°C, 50 MPa → 15 min
A = calibrate_A(15.0, 900.0, 50.0)

def rupture_time_seconds(T_C, sigma_MPa, A=A, Q=Q, n=n):
    """Tiempo a rotura por fluencia (segundos)."""
    T_K = T_C + 273.15
    return A * (sigma_MPa**(-n)) * np.exp(Q/(R*T_K))

# ---------------- Ejemplos numéricos ----------------
if __name__ == "__main__":
    # Ejemplo: condiciones del caso
    r = 50.0   # mm
    t = 5.0    # mm
    p = 50.0   # bar
    sigma = hoop_stress_MPa(p, r, t)
    tr = rupture_time_seconds(900, sigma)
    print(f"Tensión circunferencial: {sigma:.1f} MPa")
    print(f"Tiempo a rotura estimado: {tr/60:.1f} min")

    # ---------------- Gráficos ----------------
    temps_C = np.linspace(800, 1000, 81)
    stresses = [30, 40, 50, 60]

    # 1) Tiempo a rotura vs Temperatura
    plt.figure()
    for s in stresses:
        tr = rupture_time_seconds(temps_C, s)
        plt.semilogy(temps_C, tr/60, label=f"{s} MPa")
    plt.xlabel("Temperatura (°C)")
    plt.ylabel("Tiempo a rotura (min, log)")
    plt.title("t_r vs T para distintas tensiones")
    plt.legend()
    plt.grid(True, which="both", linestyle=":")
    plt.show()

    # 2) Tiempo a rotura vs Tensión
    sigmas = np.linspace(20, 80, 200)
    temps2 = [850, 900, 950]
    plt.figure()
    for T in temps2:
        tr = rupture_time_seconds(T, sigmas)
        plt.semilogy(sigmas, tr/60, label=f"{T} °C")
    plt.xlabel("Tensión circunferencial (MPa)")
    plt.ylabel("Tiempo a rotura (min, log)")
    plt.title("t_r vs σ para distintas temperaturas")
    plt.legend()
    plt.grid(True, which="both", linestyle=":")
    plt.show()

    # 3) Sensibilidad a espesor
    t_vals = np.linspace(3.0, 8.0, 100)
    plt.figure()
    trs = []
    for t in t_vals:
        sigma = hoop_stress_MPa(50, r, t)
        trs.append(rupture_time_seconds(900, sigma)/60)
    plt.semilogy(t_vals, trs, 'r')
    plt.xlabel("Espesor (mm)")
    plt.ylabel("Tiempo a rotura (min, log)")
    plt.title("Sensibilidad a espesor (p=50 bar, T=900 °C)")
    plt.grid(True, which="both", linestyle=":")
    plt.show()

    # 4) Sensibilidad a presión
    p_vals = np.linspace(30, 70, 100)
    plt.figure()
    trs = []
    for p in p_vals:
        sigma = hoop_stress_MPa(p, r, 5.0)
        trs.append(rupture_time_seconds(900, sigma)/60)
    plt.semilogy(p_vals, trs, 'b')
    plt.xlabel("Presión (bar)")
    plt.ylabel("Tiempo a rotura (min, log)")
    plt.title("Sensibilidad a presión (t=5 mm, T=900 °C)")
    plt.grid(True, which="both", linestyle=":")
    plt.show()
