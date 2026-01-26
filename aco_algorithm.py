"""
Algoritmo de Colonia de Hormigas (ACO)
Universidad Nacional de Chimborazo - Metaheurísticas

Implementación del algoritmo Ant Colony Optimization para
encontrar rutas óptimas en un espacio 2D con obstáculos.
"""

import numpy as np
import random
from config import ACOParams


class Ant:
    """
    Representa una hormiga individual en la colonia.
    
    Atributos:
        position: Posición actual (fila, columna)
        path: Lista de posiciones visitadas
        path_cost: Costo total del camino recorrido
        reached_goal: Si llegó al objetivo
    """
    
    def __init__(self, start_position):
        self.position = start_position
        self.path = [start_position]
        self.path_cost = 0.0
        self.reached_goal = False
        self.stuck = False
        
    def move_to(self, new_position, cost):
        """Mover la hormiga a una nueva posición"""
        self.position = new_position
        self.path.append(new_position)
        self.path_cost += cost
        
    def reset(self, start_position):
        """Reiniciar la hormiga al inicio"""
        self.position = start_position
        self.path = [start_position]
        self.path_cost = 0.0
        self.reached_goal = False
        self.stuck = False
        
    def has_visited(self, position):
        """Verificar si ya visitó una posición"""
        return position in self.path


class ACOSolver:
    """
    Motor principal del algoritmo ACO.
    
    Implementa:
    - Construcción de soluciones por hormigas
    - Actualización de feromonas
    - Evaporación
    - Seguimiento de mejores rutas
    """
    
    def __init__(self, environment, params=None):
        self.env = environment
        self.params = params if params else ACOParams()
        
        # Colonia de hormigas
        self.ants = []
        self.initialize_ants()
        
        # Estadísticas
        self.best_path = None
        self.best_cost = float('inf')
        self.iteration = 0
        self.history = []  # Historial de mejores costos
        
        # Estado de la simulación
        self.running = False
        self.completed = False
        
    def initialize_ants(self):
        """Crear la colonia de hormigas"""
        self.ants = [Ant(self.env.start) for _ in range(self.params.num_ants)]
        
    def reset(self):
        """Reiniciar la simulación"""
        self.env.reset_pheromones(self.params.initial_pheromone)
        self.initialize_ants()
        self.best_path = None
        self.best_cost = float('inf')
        self.iteration = 0
        self.history = []
        self.running = False
        self.completed = False
        
    def select_next_cell(self, ant):
        """
        Seleccionar la siguiente celda usando la regla de transición de ACO.
        
        La probabilidad de elegir una celda vecina se calcula como:
        P(j) = (τ_j^α * η_j^β) / Σ(τ_k^α * η_k^β)
        
        Donde:
        - τ: nivel de feromona
        - η: heurística (1/distancia al objetivo)
        - α: importancia de la feromona
        - β: importancia de la heurística
        """
        current = ant.position
        neighbors = self.env.get_neighbors(*current)
        
        # Filtrar vecinos no visitados
        unvisited = [(r, c, cost) for r, c, cost in neighbors 
                     if not ant.has_visited((r, c))]
        
        if not unvisited:
            ant.stuck = True
            return None
            
        # Calcular probabilidades
        probabilities = []
        for row, col, cost in unvisited:
            pheromone = self.env.get_pheromone(row, col)
            heuristic = 1.0 / (self.env.get_heuristic(row, col) + 0.1)
            
            # Fórmula ACO
            attractiveness = (pheromone ** self.params.alpha) * (heuristic ** self.params.beta)
            probabilities.append(attractiveness)
            
        # Normalizar probabilidades
        total = sum(probabilities)
        if total == 0:
            probabilities = [1.0 / len(unvisited)] * len(unvisited)
        else:
            probabilities = [p / total for p in probabilities]
            
        # Selección por ruleta
        r = random.random()
        cumulative = 0
        for i, prob in enumerate(probabilities):
            cumulative += prob
            if r <= cumulative:
                return unvisited[i]
                
        return unvisited[-1]
    
    def move_ant(self, ant):
        """
        Mover una hormiga un paso.
        
        Returns:
            True si la hormiga se movió, False si está atascada o llegó
        """
        if ant.reached_goal or ant.stuck:
            return False
            
        # Verificar si llegó al objetivo
        if ant.position == self.env.end:
            ant.reached_goal = True
            return False
            
        # Seleccionar siguiente celda
        next_cell = self.select_next_cell(ant)
        
        if next_cell is None:
            return False
            
        row, col, cost = next_cell
        ant.move_to((row, col), cost)
        
        # Verificar si llegó
        if (row, col) == self.env.end:
            ant.reached_goal = True
            
        return True
    
    def move_all_ants_one_step(self):
        """
        Mover todas las hormigas un paso.
        
        Returns:
            True si al menos una hormiga se movió
        """
        any_moved = False
        for ant in self.ants:
            if self.move_ant(ant):
                any_moved = True
        return any_moved
    
    def all_ants_finished(self):
        """Verificar si todas las hormigas terminaron"""
        return all(ant.reached_goal or ant.stuck for ant in self.ants)
    
    def update_pheromones(self):
        """
        Actualizar feromonas basándose en los caminos de las hormigas.
        
        Solo las hormigas que llegaron al objetivo depositan feromona.
        La cantidad depositada es inversamente proporcional al costo del camino.
        """
        # Evaporación
        self.env.evaporate_pheromones(self.params.evaporation_rate)
        
        # Depósito de feromonas
        for ant in self.ants:
            if ant.reached_goal:
                # Cantidad de feromona a depositar
                deposit = self.params.q / ant.path_cost
                
                # Depositar en cada celda del camino
                for pos in ant.path:
                    self.env.update_pheromone(pos[0], pos[1], deposit)
                    
                # Actualizar mejor camino
                if ant.path_cost < self.best_cost:
                    self.best_cost = ant.path_cost
                    self.best_path = ant.path.copy()
                    
    def run_iteration(self):
        """
        Ejecutar una iteración completa del algoritmo.
        
        1. Mover todas las hormigas hasta que terminen
        2. Actualizar feromonas
        3. Reiniciar hormigas para siguiente iteración
        """
        # Mover hormigas hasta que todas terminen
        max_steps = self.env.rows * self.env.cols * 2  # Límite de pasos
        steps = 0
        
        while not self.all_ants_finished() and steps < max_steps:
            self.move_all_ants_one_step()
            steps += 1
            
        # Actualizar feromonas
        self.update_pheromones()
        
        # Registrar historial
        self.history.append(self.best_cost if self.best_path else float('inf'))
        
        # Reiniciar hormigas
        for ant in self.ants:
            ant.reset(self.env.start)
            
        self.iteration += 1
        
        # Verificar convergencia
        if self.iteration >= self.params.max_iterations:
            self.completed = True
            self.running = False
            
    def step(self):
        """
        Ejecutar un paso de simulación (para animación paso a paso).
        
        Returns:
            'moving' - Hormigas moviéndose
            'updating' - Actualizando feromonas
            'new_iteration' - Nueva iteración iniciada
            'completed' - Simulación terminada
        """
        if self.completed:
            return 'completed'
            
        if not self.all_ants_finished():
            self.move_all_ants_one_step()
            return 'moving'
        else:
            self.update_pheromones()
            self.history.append(self.best_cost if self.best_path else float('inf'))
            
            # Reiniciar hormigas
            for ant in self.ants:
                ant.reset(self.env.start)
                
            self.iteration += 1
            
            if self.iteration >= self.params.max_iterations:
                self.completed = True
                return 'completed'
                
            return 'new_iteration'
            
    def get_statistics(self):
        """Obtener estadísticas actuales"""
        successful_ants = sum(1 for ant in self.ants if ant.reached_goal)
        return {
            'iteration': self.iteration,
            'best_cost': self.best_cost if self.best_path else None,
            'best_path_length': len(self.best_path) if self.best_path else 0,
            'successful_ants': successful_ants,
            'total_ants': len(self.ants),
            'max_pheromone': self.env.get_max_pheromone(),
            'avg_pheromone': np.mean(self.env.pheromones),
        }
