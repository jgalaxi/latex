import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def simular_dispersao_agente_nucleante(
    pos_inicial_x, pos_inicial_y,
    vel_viento_x, vel_viento_y,
    coef_difusion,
    tiempo_simulacion_seg,
    num_particulas,
    limite_x, limite_y
):
    """
    Simula la dispersión de partículas de agente nucleante (ej. AgI) en un espacio 2D.
    
    pos_inicial_x, pos_inicial_y: Coordenadas iniciales del punto de liberación.
    vel_viento_x, vel_viento_y: Componentes de la velocidad del viento (unidades/seg).
    coef_difusion: Coeficiente de difusión (dispersión aleatoria) de las partículas.
    tiempo_simulacion_seg: Duración total de la simulación en segundos.
    num_particulas: Número de partículas a simular.
    limite_x, limite_y: Dimensiones del área de simulación (e.g., tamaño de la nube).
    """

    # Posiciones iniciales de todas las partículas
    # np.full crea un array lleno con el valor especificado
    pos_x = np.full(num_particulas, pos_inicial_x, dtype=float)
    pos_y = np.full(num_particulas, pos_inicial_y, dtype=float)

    # Lista para almacenar las posiciones de las partículas en cada paso de tiempo
    historial_posiciones = []

    # Bucle de simulación por pasos de tiempo
    for t in range(tiempo_simulacion_seg + 1):
        # Almacenar las posiciones actuales
        historial_posiciones.append((pos_x.copy(), pos_y.copy()))

        # Movimiento debido al viento (componente determinista)
        pos_x += vel_viento_x
        pos_y += vel_viento_y

        # Movimiento debido a la difusión (componente aleatoria)
        # np.random.normal(media, desviacion_estandar, tamaño)
        # La desviación estándar está relacionada con el coeficiente de difusión y el tiempo
        # sqrt(2 * D * dt) donde D es el coeficiente de difusión y dt es el paso de tiempo (aquí 1 segundo)
        pos_x += np.random.normal(0, np.sqrt(2 * coef_difusion * 1), num_particulas)
        pos_y += np.random.normal(0, np.sqrt(2 * coef_difusion * 1), num_particulas)

        # Rebotar en los límites del área de simulación
        # Si una partícula supera un límite, la movemos hacia adentro
        pos_x[pos_x < 0] = 0
        pos_x[pos_x > limite_x] = limite_x
        pos_y[pos_y < 0] = 0
        pos_y[pos_y > limite_y] = limite_y

    return historial_posiciones, limite_x, limite_y

# --- Parámetros de la simulación ---
POS_INICIAL_X = 50   # Centro de la nube, en unidades arbitrarias (e.g., km)
POS_INICIAL_Y = 50
VEL_VIENTO_X = 2     # Velocidad del viento en eje X (e.g., km/seg)
VEL_VIENTO_Y = 0.5   # Velocidad del viento en eje Y (e.g., km/seg)
COEF_DIFUSION = 5    # Grado de dispersión aleatoria (unidades^2/seg)
TIEMPO_SIMULACION_SEG = 100 # Segundos
NUM_PARTICULAS = 500 # Número de partículas de AgI a simular
LIMITE_X = 200       # Tamaño de la nube en X
LIMITE_Y = 100       # Tamaño de la nube en Y

# --- Ejecutar la simulación ---
historial_pos, lx, ly = simular_dispersao_agente_nucleante(
    POS_INICIAL_X, POS_INICIAL_Y,
    VEL_VIENTO_X, VEL_VIENTO_Y,
    COEF_DIFUSION,
    TIEMPO_SIMULACION_SEG,
    NUM_PARTICULAS,
    LIMITE_X, LIMITE_Y
)

# --- Visualización de la simulación (Animación) ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, lx)
ax.set_ylim(0, ly)
ax.set_title('Dispersión de Agente Nucleante (AgI) en una Nube')
ax.set_xlabel('Posición X (km)')
ax.set_ylabel('Posición Y (km)')
ax.grid(True)

# Crear el scatter plot inicial
scatter = ax.scatter([], [], s=5, alpha=0.6, color='blue')

# Función para actualizar la animación
def update(frame):
    current_pos_x, current_pos_y = historial_pos[frame]
    scatter.set_offsets(np.c_[current_pos_x, current_pos_y])
    ax.set_title(f'Dispersión de Agente Nucleante (AgI) en una Nube\nTiempo: {frame} segundos')
    return scatter,

# Crear la animación