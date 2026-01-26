"""
Escenarios Predefinidos para Simulación ACO
Universidad Nacional de Chimborazo - Metaheurísticas
"""

from environment import Environment


def create_simple_maze(env):
    """
    Escenario 1: Laberinto Simple
    Un camino con algunos obstáculos básicos.
    """
    env.clear_obstacles()
    env.set_start((2, 2))
    env.set_end((env.rows - 3, env.cols - 3))
    
    # Pared vertical en el centro
    for r in range(5, env.rows - 8):
        env.add_obstacle(r, env.cols // 2)
    
    # Pared horizontal
    for c in range(8, env.cols - 12):
        env.add_obstacle(env.rows // 2, c)
        
    return "Laberinto Simple"


def create_complex_maze(env):
    """
    Escenario 2: Laberinto Complejo
    Múltiples caminos posibles con varios obstáculos.
    """
    env.clear_obstacles()
    env.set_start((2, 2))
    env.set_end((env.rows - 3, env.cols - 3))
    
    # Múltiples paredes verticales
    for i in range(3):
        col = 8 + i * 8
        if col < env.cols - 3:
            start_row = 3 if i % 2 == 0 else 8
            end_row = env.rows - 8 if i % 2 == 0 else env.rows - 3
            for r in range(start_row, end_row):
                env.add_obstacle(r, col)
    
    # Paredes horizontales
    for c in range(5, 15):
        env.add_obstacle(10, c)
    for c in range(20, 30):
        env.add_obstacle(15, c)
    for c in range(8, 18):
        env.add_obstacle(22, c)
        
    return "Laberinto Complejo"


def create_open_field(env):
    """
    Escenario 3: Campo Abierto
    Sin obstáculos para visualizar la convergencia de feromonas.
    """
    env.clear_obstacles()
    env.set_start((env.rows // 2, 3))
    env.set_end((env.rows // 2, env.cols - 4))
    
    return "Campo Abierto"


def create_trap_scenario(env):
    """
    Escenario 4: La Trampa
    Un camino aparentemente corto pero que es un callejón sin salida.
    Las hormigas deben encontrar el camino largo pero viable.
    """
    env.clear_obstacles()
    env.set_start((env.rows // 2, 3))
    env.set_end((env.rows // 2, env.cols - 4))
    
    # Camino directo bloqueado casi al final
    wall_col = env.cols - 8
    for r in range(3, env.rows - 3):
        env.add_obstacle(r, wall_col)
    
    # Pequeña abertura arriba
    env.remove_obstacle(4, wall_col)
    env.remove_obstacle(5, wall_col)
    
    # Trampa: parece un atajo pero es un callejón
    trap_row = env.rows // 2
    for c in range(12, wall_col - 2):
        env.add_obstacle(trap_row - 3, c)
        env.add_obstacle(trap_row + 3, c)
    
    # Cerrar la trampa
    for r in range(trap_row - 3, trap_row + 4):
        env.add_obstacle(r, wall_col - 2)
        
    return "La Trampa"


def create_spiral(env):
    """
    Escenario 5: Espiral
    Las hormigas deben seguir un camino en espiral.
    """
    env.clear_obstacles()
    env.set_start((env.rows // 2, env.cols // 2))
    env.set_end((2, 2))
    
    # Crear espiral desde afuera hacia adentro
    margin = 3
    
    # Capa exterior
    for c in range(margin, env.cols - margin):
        env.add_obstacle(margin, c)
    for r in range(margin, env.rows - margin):
        env.add_obstacle(r, env.cols - margin - 1)
    for c in range(margin, env.cols - margin):
        env.add_obstacle(env.rows - margin - 1, c)
    for r in range(margin + 5, env.rows - margin):
        env.add_obstacle(r, margin)
        
    # Segunda capa
    margin2 = 7
    for c in range(margin2, env.cols - margin2):
        env.add_obstacle(margin2, c)
    for r in range(margin2, env.rows - margin2):
        env.add_obstacle(r, env.cols - margin2 - 1)
    for c in range(margin2 + 5, env.cols - margin2):
        env.add_obstacle(env.rows - margin2 - 1, c)
        
    # Abrir entradas
    env.remove_obstacle(margin, margin + 3)
    env.remove_obstacle(margin + 1, margin + 3)
    
    return "Espiral"


def create_random_obstacles(env, density=0.25):
    """
    Escenario 6: Obstáculos Aleatorios
    Obstáculos distribuidos aleatoriamente.
    """
    import random
    
    env.clear_obstacles()
    env.set_start((2, 2))
    env.set_end((env.rows - 3, env.cols - 3))
    
    # Añadir obstáculos aleatorios
    for r in range(env.rows):
        for c in range(env.cols):
            if random.random() < density:
                # No bloquear cerca del inicio o fin
                if abs(r - env.start[0]) > 3 or abs(c - env.start[1]) > 3:
                    if abs(r - env.end[0]) > 3 or abs(c - env.end[1]) > 3:
                        env.add_obstacle(r, c)
    
    # Verificar que existe un camino
    if not env.path_exists():
        # Si no hay camino, crear uno básico
        return create_simple_maze(env)
    
    return "Obstáculos Aleatorios"


def create_university_logo(env):
    """
    Escenario 7: Logo UNACH
    Obstáculos formando las letras U-N-A-C-H de forma simplificada.
    """
    env.clear_obstacles()
    env.set_start((env.rows - 3, 2))
    env.set_end((env.rows - 3, env.cols - 3))
    
    # Crear marco
    for c in range(env.cols):
        env.add_obstacle(0, c)
        env.add_obstacle(env.rows - 1, c)
    for r in range(env.rows):
        env.add_obstacle(r, 0)
        env.add_obstacle(r, env.cols - 1)
    
    # Letra U (simplificada)
    start_col = 5
    for r in range(5, 15):
        env.add_obstacle(r, start_col)
        env.add_obstacle(r, start_col + 4)
    for c in range(start_col, start_col + 5):
        env.add_obstacle(15, c)
        
    # Letra N
    start_col = 12
    for r in range(5, 16):
        env.add_obstacle(r, start_col)
        env.add_obstacle(r, start_col + 5)
    env.add_obstacle(7, start_col + 1)
    env.add_obstacle(9, start_col + 2)
    env.add_obstacle(11, start_col + 3)
    env.add_obstacle(13, start_col + 4)
    
    return "Logo UNACH"


# Lista de todos los escenarios disponibles
SCENARIOS = [
    ("Laberinto Simple", create_simple_maze),
    ("Laberinto Complejo", create_complex_maze),
    ("Campo Abierto", create_open_field),
    ("La Trampa", create_trap_scenario),
    ("Espiral", create_spiral),
    ("Aleatorio", create_random_obstacles),
    ("Logo UNACH", create_university_logo),
]


def get_scenario_names():
    """Obtener lista de nombres de escenarios"""
    return [name for name, _ in SCENARIOS]


def load_scenario(env, index):
    """Cargar un escenario por su índice"""
    if 0 <= index < len(SCENARIOS):
        name, func = SCENARIOS[index]
        func(env)
        return name
    return None
