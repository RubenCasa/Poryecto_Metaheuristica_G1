"""
Entorno de Simulación para ACO
Universidad Nacional de Chimborazo - Metaheurísticas
"""

import numpy as np
from config import GRID_ROWS, GRID_COLS, DIRECTIONS, COST_STRAIGHT, COST_DIAGONAL


class Environment:
    """
    Representa el entorno 2D donde las hormigas buscan rutas.
    
    Atributos:
        grid: Matriz 2D donde 0=libre, 1=obstáculo
        start: Tupla (fila, columna) del punto de inicio (nido)
        end: Tupla (fila, columna) del objetivo (comida)
        pheromones: Matriz 2D con niveles de feromona
    """
    
    def __init__(self, rows=GRID_ROWS, cols=GRID_COLS):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.start = (1, 1)
        self.end = (rows - 2, cols - 2)
        self.pheromones = None
        self.reset_pheromones()
        
    def reset_pheromones(self, initial_value=0.1):
        """Inicializar matriz de feromonas"""
        self.pheromones = np.full((self.rows, self.cols), initial_value)
        
    def is_valid_cell(self, row, col):
        """Verificar si una celda es válida y transitable"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row, col] == 0
        return False
    
    def get_neighbors(self, row, col):
        """
        Obtener vecinos válidos de una celda.
        
        Returns:
            Lista de tuplas (fila, columna, costo)
        """
        neighbors = []
        for i, (dr, dc) in enumerate(DIRECTIONS):
            new_row, new_col = row + dr, col + dc
            if self.is_valid_cell(new_row, new_col):
                # Costo diagonal o recto
                cost = COST_DIAGONAL if abs(dr) + abs(dc) == 2 else COST_STRAIGHT
                neighbors.append((new_row, new_col, cost))
        return neighbors
    
    def get_heuristic(self, row, col):
        """
        Calcular heurística (distancia al objetivo).
        Usa distancia euclidiana.
        """
        return np.sqrt((row - self.end[0])**2 + (col - self.end[1])**2)
    
    def add_obstacle(self, row, col):
        """Agregar un obstáculo en una celda"""
        if (row, col) != self.start and (row, col) != self.end:
            self.grid[row, col] = 1
            
    def remove_obstacle(self, row, col):
        """Remover un obstáculo de una celda"""
        self.grid[row, col] = 0
        
    def add_obstacle_rect(self, row1, col1, row2, col2):
        """Agregar un rectángulo de obstáculos"""
        for r in range(min(row1, row2), max(row1, row2) + 1):
            for c in range(min(col1, col2), max(col1, col2) + 1):
                self.add_obstacle(r, c)
                
    def add_obstacle_line(self, row1, col1, row2, col2):
        """Agregar una línea de obstáculos usando algoritmo de Bresenham"""
        dx = abs(col2 - col1)
        dy = abs(row2 - row1)
        x, y = col1, row1
        sx = 1 if col1 < col2 else -1
        sy = 1 if row1 < row2 else -1
        
        if dx > dy:
            err = dx / 2
            while x != col2:
                self.add_obstacle(y, x)
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2
            while y != row2:
                self.add_obstacle(y, x)
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        self.add_obstacle(row2, col2)
        
    def clear_obstacles(self):
        """Limpiar todos los obstáculos"""
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        
    def set_start(self, position):
        """Establecer punto de inicio (acepta tupla (row, col))"""
        row, col = position
        if self.is_valid_cell(row, col) and (row, col) != self.end:
            self.start = (row, col)
            
    def set_end(self, position):
        """Establecer punto objetivo (acepta tupla (row, col))"""
        row, col = position
        if self.is_valid_cell(row, col) and (row, col) != self.start:
            self.end = (row, col)
            
    def update_pheromone(self, row, col, amount):
        """Actualizar feromona en una celda"""
        self.pheromones[row, col] += amount
        
    def evaporate_pheromones(self, evaporation_rate):
        """Aplicar evaporación a todas las feromonas"""
        self.pheromones *= (1 - evaporation_rate)
        # Mantener un mínimo de feromona
        self.pheromones = np.maximum(self.pheromones, 0.01)
        
    def get_pheromone(self, row, col):
        """Obtener nivel de feromona en una celda"""
        return self.pheromones[row, col]
    
    def get_max_pheromone(self):
        """Obtener el máximo nivel de feromona actual"""
        return np.max(self.pheromones)
    
    def path_exists(self):
        """
        Verificar si existe un camino del inicio al fin usando BFS.
        """
        from collections import deque
        
        visited = set()
        queue = deque([self.start])
        visited.add(self.start)
        
        while queue:
            current = queue.popleft()
            if current == self.end:
                return True
                
            for neighbor in self.get_neighbors(*current):
                pos = (neighbor[0], neighbor[1])
                if pos not in visited:
                    visited.add(pos)
                    queue.append(pos)
                    
        return False
    
    def copy(self):
        """Crear una copia del entorno"""
        new_env = Environment(self.rows, self.cols)
        new_env.grid = self.grid.copy()
        new_env.start = self.start
        new_env.end = self.end
        new_env.pheromones = self.pheromones.copy()
        return new_env
