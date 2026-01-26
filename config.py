"""
Configuración del Simulador ACO
Universidad Nacional de Chimborazo - Metaheurísticas
"""

# ============================================================================
# CONFIGURACIÓN DE LA VENTANA
# ============================================================================
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
GRID_SIZE = 20  # Tamaño de cada celda en píxeles
FPS = 60

# ============================================================================
# COLORES - TEMA OSCURO PROFESIONAL CON NEÓN
# ============================================================================
COLORS = {
    # Fondos
    'background': (15, 15, 25),
    'grid_line': (30, 30, 45),
    'panel_bg': (20, 20, 35),
    'panel_border': (60, 60, 100),
    
    # Elementos del mapa
    'obstacle': (40, 40, 60),
    'obstacle_border': (80, 80, 120),
    'start': (0, 255, 150),       # Verde neón - Nido
    'end': (255, 50, 100),        # Rosa neón - Objetivo
    'path': (100, 200, 255),      # Azul claro - Camino válido
    
    # Hormigas
    'ant': (255, 200, 50),        # Amarillo/Dorado
    'ant_trail': (255, 150, 50, 100),
    
    # Feromonas - Gradiente de calor
    'pheromone_low': (50, 0, 100),      # Púrpura oscuro
    'pheromone_mid': (150, 50, 200),    # Púrpura brillante
    'pheromone_high': (255, 100, 255),  # Magenta neón
    
    # Mejor ruta
    'best_path': (0, 255, 200),   # Cyan neón
    'best_path_glow': (0, 255, 200, 50),
    
    # UI
    'text_primary': (255, 255, 255),
    'text_secondary': (150, 150, 180),
    'button_bg': (50, 50, 80),
    'button_hover': (70, 70, 110),
    'button_active': (100, 100, 150),
    'slider_bg': (40, 40, 60),
    'slider_fill': (0, 200, 150),
    
    # Efectos
    'glow_green': (0, 255, 150, 30),
    'glow_pink': (255, 50, 100, 30),
    'particle': (255, 255, 100),
}

# ============================================================================
# PARÁMETROS DEL ALGORITMO ACO
# ============================================================================
class ACOParams:
    def __init__(self):
        self.num_ants = 30           # Número de hormigas
        self.alpha = 1.0             # Importancia de la feromona
        self.beta = 2.0              # Importancia de la heurística
        self.evaporation_rate = 0.1  # Tasa de evaporación (ρ)
        self.q = 100                 # Cantidad de feromona depositada
        self.initial_pheromone = 0.1 # Feromona inicial
        self.max_iterations = 500    # Máximo de iteraciones
        
    def reset(self):
        """Resetear a valores por defecto"""
        self.__init__()

# ============================================================================
# CONFIGURACIÓN DEL ENTORNO
# ============================================================================
GRID_COLS = 35  # Columnas de la grilla
GRID_ROWS = 30  # Filas de la grilla

# Direcciones de movimiento (8 direcciones)
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

# Costos de movimiento
COST_STRAIGHT = 1.0
COST_DIAGONAL = 1.414  # √2

# ============================================================================
# CONFIGURACIÓN DE ANIMACIÓN
# ============================================================================
ANT_SPEED = 5  # Velocidad de movimiento de hormigas (celdas por segundo)
TRAIL_FADE_SPEED = 0.02  # Velocidad de desvanecimiento del rastro
PHEROMONE_VISUAL_SCALE = 10  # Escala para visualización de feromonas

# ============================================================================
# TEXTOS DE LA INTERFAZ
# ============================================================================
TITLE = "🐜 SIMULADOR ACO - UNACH"
SUBTITLE = "Algoritmo de Colonia de Hormigas"
UNIVERSITY = "Universidad Nacional de Chimborazo"
COURSE = "Metaheurísticas"

# Descripciones de parámetros
PARAM_DESCRIPTIONS = {
    'alpha': 'α - Importancia de feromona',
    'beta': 'β - Importancia heurística',
    'evaporation': 'ρ - Tasa de evaporación',
    'ants': 'Número de hormigas',
}
