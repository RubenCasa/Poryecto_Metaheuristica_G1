"""
=============================================================================
    SIMULADOR DE TRAYECTORIAS CON ALGORITMO ACO
    Universidad Nacional de Chimborazo - Metaheurísticas
=============================================================================

    Ant Colony Optimization (ACO) para encontrar rutas óptimas
    en un espacio 2D con obstáculos.

    Autor: Estudiante UNACH
    Fecha: 2026

    Uso:
        python main.py

    Controles:
        ESPACIO - Iniciar/Pausar simulación
        R       - Reiniciar simulación
        S       - Cambiar escenario
        P       - Mostrar/ocultar feromonas
        B       - Mostrar/ocultar mejor ruta

=============================================================================
"""

import sys


def check_dependencies():
    """Verificar que las dependencias están instaladas"""
    missing = []
    
    try:
        import pygame
    except ImportError:
        missing.append('pygame')
        
    try:
        import numpy
    except ImportError:
        missing.append('numpy')
        
    if missing:
        print("=" * 60)
        print("  ERROR: Faltan dependencias")
        print("=" * 60)
        print(f"\n  Por favor, instala las siguientes librerías:\n")
        for lib in missing:
            print(f"    pip install {lib}")
        print("\n  O ejecuta:")
        print(f"    pip install {' '.join(missing)}")
        print("=" * 60)
        sys.exit(1)


def print_banner():
    """Mostrar banner de inicio"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     🐜  SIMULADOR DE TRAYECTORIAS CON ALGORITMO ACO  🐜      ║
    ║                                                               ║
    ║         Universidad Nacional de Chimborazo (UNACH)            ║
    ║                    Metaheurísticas                            ║
    ║                                                               ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  El algoritmo ACO (Ant Colony Optimization) simula el         ║
    ║  comportamiento de colonias de hormigas para encontrar        ║
    ║  rutas óptimas entre dos puntos.                              ║
    ║                                                               ║
    ║  Las hormigas depositan feromonas en el camino y las rutas    ║
    ║  con más feromona atraen más hormigas, convergiendo hacia     ║
    ║  la solución óptima.                                          ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Función principal"""
    print_banner()
    
    print("  Verificando dependencias...")
    check_dependencies()
    print("  ✓ Dependencias OK\n")
    
    print("  Inicializando simulador...")
    
    # Importar módulos del proyecto
    from config import ACOParams, GRID_ROWS, GRID_COLS
    from environment import Environment
    from aco_algorithm import ACOSolver
    from visualization import Visualization
    from scenarios import load_scenario
    
    # Crear entorno
    print("  ✓ Creando entorno...")
    env = Environment(GRID_ROWS, GRID_COLS)
    
    # Cargar escenario inicial
    print("  ✓ Cargando escenario...")
    load_scenario(env, 0)
    
    # Crear parámetros y solver ACO
    print("  ✓ Inicializando algoritmo ACO...")
    params = ACOParams()
    solver = ACOSolver(env, params)
    
    # Crear visualización
    print("  ✓ Iniciando visualización...\n")
    viz = Visualization(env, solver)
    
    print("  ╔════════════════════════════════════════════╗")
    print("  ║  Simulador listo. ¡Presiona ESPACIO para   ║")
    print("  ║  iniciar la simulación!                    ║")
    print("  ╚════════════════════════════════════════════╝\n")
    
    # Ejecutar
    viz.run()
    
    print("\n  ¡Gracias por usar el Simulador ACO!")
    print("  Universidad Nacional de Chimborazo - 2026\n")


if __name__ == "__main__":
    main()
