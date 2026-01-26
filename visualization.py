"""
Sistema de Visualización con Pygame
Universidad Nacional de Chimborazo - Metaheurísticas

Visualización avanzada del algoritmo ACO con efectos visuales profesionales.
"""

import pygame
import numpy as np
import math
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, FPS, COLORS,
    TITLE, SUBTITLE, UNIVERSITY, COURSE, GRID_COLS, GRID_ROWS,
    PHEROMONE_VISUAL_SCALE, PARAM_DESCRIPTIONS
)


class Button:
    """Botón interactivo para la interfaz"""
    
    def __init__(self, x, y, width, height, text, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.pressed = False
        self.enabled = True
        
    def draw(self, screen, font):
        if not self.enabled:
            color = COLORS['panel_bg']
        elif self.pressed:
            color = COLORS['button_active']
        elif self.hovered:
            color = COLORS['button_hover']
        else:
            color = COLORS['button_bg']
            
        # Dibujar botón con bordes redondeados
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, COLORS['panel_border'], self.rect, 2, border_radius=8)
        
        # Texto
        text_color = COLORS['text_primary'] if self.enabled else COLORS['text_secondary']
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if not self.enabled:
            return False
            
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                if self.callback:
                    self.callback()
                return True
            self.pressed = False
        return False


class Slider:
    """Control deslizante para parámetros"""
    
    def __init__(self, x, y, width, height, min_val, max_val, value, label, step=0.1):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.label = label
        self.step = step
        self.dragging = False
        
    def draw(self, screen, font):
        # Fondo del slider
        pygame.draw.rect(screen, COLORS['slider_bg'], self.rect, border_radius=4)
        
        # Barra de progreso
        progress = (self.value - self.min_val) / (self.max_val - self.min_val)
        fill_width = int(self.rect.width * progress)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, COLORS['slider_fill'], fill_rect, border_radius=4)
        
        # Borde
        pygame.draw.rect(screen, COLORS['panel_border'], self.rect, 1, border_radius=4)
        
        # Etiqueta y valor
        label_text = f"{self.label}: {self.value:.2f}"
        text_surface = font.render(label_text, True, COLORS['text_primary'])
        screen.blit(text_surface, (self.rect.x, self.rect.y - 20))
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._update_value(event.pos[0])
                
    def _update_value(self, mouse_x):
        progress = (mouse_x - self.rect.x) / self.rect.width
        progress = max(0, min(1, progress))
        raw_value = self.min_val + progress * (self.max_val - self.min_val)
        # Redondear al step más cercano
        self.value = round(raw_value / self.step) * self.step
        self.value = max(self.min_val, min(self.max_val, self.value))


class Visualization:
    """
    Motor de visualización principal.
    
    Maneja:
    - Renderizado del mapa y obstáculos
    - Animación de hormigas
    - Visualización de feromonas
    - Panel de control
    """
    
    def __init__(self, environment, aco_solver):
        pygame.init()
        pygame.display.set_caption(TITLE)
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.env = environment
        self.solver = aco_solver
        
        # Fuentes
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)
        
        # Cálculos de layout
        self.panel_width = 280
        self.grid_area_width = WINDOW_WIDTH - self.panel_width
        self.cell_size = min(
            (self.grid_area_width - 40) // self.env.cols,
            (WINDOW_HEIGHT - 80) // self.env.rows
        )
        self.grid_offset_x = 20
        self.grid_offset_y = 60
        
        # Estado
        self.running = True
        self.simulation_active = False
        self.speed = 1.0
        self.show_pheromones = True
        self.show_best_path = True
        self.current_scenario = 0
        
        # Partículas para efectos
        self.particles = []
        
        # Crear controles
        self._create_controls()
        
        # Superficies pre-renderizadas
        self.pheromone_surface = pygame.Surface(
            (self.env.cols * self.cell_size, self.env.rows * self.cell_size),
            pygame.SRCALPHA
        )
        
    def _create_controls(self):
        """Crear botones y sliders del panel"""
        panel_x = WINDOW_WIDTH - self.panel_width + 20
        
        # Botones
        self.btn_start = Button(panel_x, 200, 120, 40, "▶ INICIAR", self._toggle_simulation)
        self.btn_reset = Button(panel_x + 130, 200, 100, 40, "↻ RESET", self._reset_simulation)
        self.btn_scenario = Button(panel_x, 250, 230, 40, "Cambiar Escenario", self._next_scenario)
        
        # Sliders
        slider_y = 340
        slider_height = 20
        slider_spacing = 60
        
        self.slider_alpha = Slider(
            panel_x, slider_y, 200, slider_height,
            0.1, 5.0, self.solver.params.alpha, "α (Feromona)", 0.1
        )
        self.slider_beta = Slider(
            panel_x, slider_y + slider_spacing, 200, slider_height,
            0.1, 5.0, self.solver.params.beta, "β (Heurística)", 0.1
        )
        self.slider_evap = Slider(
            panel_x, slider_y + slider_spacing * 2, 200, slider_height,
            0.01, 0.5, self.solver.params.evaporation_rate, "ρ (Evaporación)", 0.01
        )
        self.slider_ants = Slider(
            panel_x, slider_y + slider_spacing * 3, 200, slider_height,
            5, 100, self.solver.params.num_ants, "Hormigas", 5
        )
        
        self.buttons = [self.btn_start, self.btn_reset, self.btn_scenario]
        self.sliders = [self.slider_alpha, self.slider_beta, self.slider_evap, self.slider_ants]
        
    def _toggle_simulation(self):
        """Iniciar/pausar simulación"""
        self.simulation_active = not self.simulation_active
        self.btn_start.text = "⏸ PAUSAR" if self.simulation_active else "▶ INICIAR"
        
    def _reset_simulation(self):
        """Reiniciar simulación"""
        self.simulation_active = False
        self.btn_start.text = "▶ INICIAR"
        self.solver.params.num_ants = int(self.slider_ants.value)
        self.solver.reset()
        self.particles = []
        
    def _next_scenario(self):
        """Cambiar al siguiente escenario"""
        from scenarios import SCENARIOS, load_scenario
        self.current_scenario = (self.current_scenario + 1) % len(SCENARIOS)
        load_scenario(self.env, self.current_scenario)
        self._reset_simulation()
        
    def _update_params_from_sliders(self):
        """Actualizar parámetros del solver desde los sliders"""
        self.solver.params.alpha = self.slider_alpha.value
        self.solver.params.beta = self.slider_beta.value
        self.solver.params.evaporation_rate = self.slider_evap.value
        
    def run(self):
        """Bucle principal de la visualización"""
        from scenarios import load_scenario, get_scenario_names
        
        # Cargar escenario inicial
        self.scenario_names = get_scenario_names()
        load_scenario(self.env, 0)
        self.solver.reset()
        
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(FPS)
            
        pygame.quit()
        
    def _handle_events(self):
        """Manejar eventos de entrada"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._toggle_simulation()
                elif event.key == pygame.K_r:
                    self._reset_simulation()
                elif event.key == pygame.K_s:
                    self._next_scenario()
                elif event.key == pygame.K_p:
                    self.show_pheromones = not self.show_pheromones
                elif event.key == pygame.K_b:
                    self.show_best_path = not self.show_best_path
                    
            # Manejar botones
            for btn in self.buttons:
                btn.handle_event(event)
                
            # Manejar sliders
            for slider in self.sliders:
                slider.handle_event(event)
                
    def _update(self):
        """Actualizar estado de la simulación"""
        self._update_params_from_sliders()
        
        if self.simulation_active and not self.solver.completed:
            # Ejecutar varios pasos por frame para mayor velocidad
            for _ in range(int(5 * self.speed)):
                result = self.solver.step()
                if result == 'completed':
                    self.simulation_active = False
                    self._spawn_celebration_particles()
                    break
                elif result == 'new_iteration':
                    # Agregar algunas partículas cuando se encuentra mejor ruta
                    if self.solver.best_path:
                        self._spawn_path_particles()
                        
        # Actualizar partículas
        self._update_particles()
        
    def _spawn_path_particles(self):
        """Crear partículas en el mejor camino"""
        if self.solver.best_path and len(self.solver.best_path) > 0:
            import random
            for pos in self.solver.best_path[::3]:  # Cada 3 posiciones
                x = self.grid_offset_x + pos[1] * self.cell_size + self.cell_size // 2
                y = self.grid_offset_y + pos[0] * self.cell_size + self.cell_size // 2
                self.particles.append({
                    'x': x,
                    'y': y,
                    'vx': random.uniform(-1, 1),
                    'vy': random.uniform(-2, -1),
                    'life': 1.0,
                    'color': COLORS['best_path']
                })
                
    def _spawn_celebration_particles(self):
        """Crear partículas de celebración"""
        import random
        end_x = self.grid_offset_x + self.env.end[1] * self.cell_size + self.cell_size // 2
        end_y = self.grid_offset_y + self.env.end[0] * self.cell_size + self.cell_size // 2
        
        for _ in range(50):
            self.particles.append({
                'x': end_x,
                'y': end_y,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-5, 5),
                'life': 1.0,
                'color': COLORS['particle']
            })
            
    def _update_particles(self):
        """Actualizar y eliminar partículas muertas"""
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 0.02
            if p['life'] <= 0:
                self.particles.remove(p)
                
    def _render(self):
        """Renderizar todo"""
        self.screen.fill(COLORS['background'])
        
        self._render_grid()
        
        if self.show_pheromones:
            self._render_pheromones()
            
        self._render_obstacles()
        self._render_start_end()
        
        if self.show_best_path and self.solver.best_path:
            self._render_best_path()
            
        self._render_ants()
        self._render_particles()
        self._render_panel()
        
        pygame.display.flip()
        
    def _render_grid(self):
        """Dibujar líneas de la grilla"""
        for r in range(self.env.rows + 1):
            y = self.grid_offset_y + r * self.cell_size
            pygame.draw.line(
                self.screen, COLORS['grid_line'],
                (self.grid_offset_x, y),
                (self.grid_offset_x + self.env.cols * self.cell_size, y)
            )
        for c in range(self.env.cols + 1):
            x = self.grid_offset_x + c * self.cell_size
            pygame.draw.line(
                self.screen, COLORS['grid_line'],
                (x, self.grid_offset_y),
                (x, self.grid_offset_y + self.env.rows * self.cell_size)
            )
            
    def _render_pheromones(self):
        """Renderizar mapa de calor de feromonas"""
        max_pher = max(self.env.get_max_pheromone(), 0.1)
        
        for r in range(self.env.rows):
            for c in range(self.env.cols):
                if self.env.grid[r, c] == 0:  # Solo celdas libres
                    pher = self.env.pheromones[r, c]
                    intensity = min(pher / max_pher, 1.0)
                    
                    if intensity > 0.05:  # Solo mostrar si hay feromona significativa
                        # Interpolar color
                        if intensity < 0.5:
                            t = intensity * 2
                            color = self._lerp_color(COLORS['pheromone_low'], COLORS['pheromone_mid'], t)
                        else:
                            t = (intensity - 0.5) * 2
                            color = self._lerp_color(COLORS['pheromone_mid'], COLORS['pheromone_high'], t)
                            
                        # Dibujar celda con transparencia
                        alpha = int(intensity * 180)
                        x = self.grid_offset_x + c * self.cell_size
                        y = self.grid_offset_y + r * self.cell_size
                        
                        s = pygame.Surface((self.cell_size - 1, self.cell_size - 1), pygame.SRCALPHA)
                        s.fill((*color, alpha))
                        self.screen.blit(s, (x + 1, y + 1))
                        
    def _lerp_color(self, c1, c2, t):
        """Interpolar entre dos colores"""
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        
    def _render_obstacles(self):
        """Dibujar obstáculos"""
        for r in range(self.env.rows):
            for c in range(self.env.cols):
                if self.env.grid[r, c] == 1:
                    x = self.grid_offset_x + c * self.cell_size
                    y = self.grid_offset_y + r * self.cell_size
                    
                    rect = pygame.Rect(x + 1, y + 1, self.cell_size - 2, self.cell_size - 2)
                    pygame.draw.rect(self.screen, COLORS['obstacle'], rect, border_radius=3)
                    pygame.draw.rect(self.screen, COLORS['obstacle_border'], rect, 1, border_radius=3)
                    
    def _render_start_end(self):
        """Dibujar punto de inicio y fin con efectos de brillo"""
        # Inicio (nido)
        sx = self.grid_offset_x + self.env.start[1] * self.cell_size
        sy = self.grid_offset_y + self.env.start[0] * self.cell_size
        
        # Efecto de brillo pulsante
        pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
        glow_size = int(self.cell_size * (1.2 + pulse * 0.3))
        glow_offset = (self.cell_size - glow_size) // 2
        
        # Dibujar brillo
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*COLORS['start'], 50), (0, 0, glow_size, glow_size), border_radius=8)
        self.screen.blit(glow_surf, (sx + glow_offset, sy + glow_offset))
        
        # Celda principal
        rect = pygame.Rect(sx + 2, sy + 2, self.cell_size - 4, self.cell_size - 4)
        pygame.draw.rect(self.screen, COLORS['start'], rect, border_radius=5)
        
        # Emoji de hormiga
        ant_text = self.font_medium.render("🏠", True, (0, 0, 0))
        self.screen.blit(ant_text, (sx + 2, sy + 2))
        
        # Fin (objetivo)
        ex = self.grid_offset_x + self.env.end[1] * self.cell_size
        ey = self.grid_offset_y + self.env.end[0] * self.cell_size
        
        # Brillo
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*COLORS['end'], 50), (0, 0, glow_size, glow_size), border_radius=8)
        self.screen.blit(glow_surf, (ex + glow_offset, ey + glow_offset))
        
        rect = pygame.Rect(ex + 2, ey + 2, self.cell_size - 4, self.cell_size - 4)
        pygame.draw.rect(self.screen, COLORS['end'], rect, border_radius=5)
        
        target_text = self.font_medium.render("🎯", True, (0, 0, 0))
        self.screen.blit(target_text, (ex + 2, ey + 2))
        
    def _render_best_path(self):
        """Dibujar el mejor camino encontrado"""
        if len(self.solver.best_path) < 2:
            return
            
        # Dibujar línea del camino
        points = []
        for pos in self.solver.best_path:
            x = self.grid_offset_x + pos[1] * self.cell_size + self.cell_size // 2
            y = self.grid_offset_y + pos[0] * self.cell_size + self.cell_size // 2
            points.append((x, y))
            
        if len(points) > 1:
            # Efecto de brillo
            pygame.draw.lines(self.screen, COLORS['best_path'], False, points, 4)
            
            # Línea principal más fina
            pygame.draw.lines(self.screen, (255, 255, 255), False, points, 2)
            
    def _render_ants(self):
        """Dibujar hormigas con su rastro"""
        for ant in self.solver.ants:
            if ant.stuck:
                continue
                
            x = self.grid_offset_x + ant.position[1] * self.cell_size + self.cell_size // 2
            y = self.grid_offset_y + ant.position[0] * self.cell_size + self.cell_size // 2
            
            # Color según estado
            if ant.reached_goal:
                color = COLORS['best_path']
            else:
                color = COLORS['ant']
                
            # Dibujar hormiga
            pygame.draw.circle(self.screen, color, (x, y), self.cell_size // 3)
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), self.cell_size // 3, 1)
            
    def _render_particles(self):
        """Dibujar partículas de efectos"""
        for p in self.particles:
            alpha = int(p['life'] * 255)
            size = int(p['life'] * 6) + 2
            
            s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p['color'][:3], alpha), (size, size), size)
            self.screen.blit(s, (p['x'] - size, p['y'] - size))
            
    def _render_panel(self):
        """Dibujar panel lateral con estadísticas y controles"""
        panel_x = WINDOW_WIDTH - self.panel_width
        
        # Fondo del panel
        panel_rect = pygame.Rect(panel_x, 0, self.panel_width, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, COLORS['panel_bg'], panel_rect)
        pygame.draw.line(self.screen, COLORS['panel_border'], (panel_x, 0), (panel_x, WINDOW_HEIGHT), 2)
        
        # Título
        title = self.font_large.render("🐜 ACO SIMULATOR", True, COLORS['text_primary'])
        self.screen.blit(title, (panel_x + 20, 20))
        
        subtitle = self.font_small.render(UNIVERSITY, True, COLORS['text_secondary'])
        self.screen.blit(subtitle, (panel_x + 20, 55))
        
        course = self.font_small.render(COURSE, True, COLORS['text_secondary'])
        self.screen.blit(course, (panel_x + 20, 75))
        
        # Escenario actual
        from scenarios import get_scenario_names
        scenario_name = get_scenario_names()[self.current_scenario]
        scenario_text = self.font_medium.render(f"📍 {scenario_name}", True, COLORS['start'])
        self.screen.blit(scenario_text, (panel_x + 20, 110))
        
        # Separador
        pygame.draw.line(
            self.screen, COLORS['panel_border'],
            (panel_x + 20, 140), (panel_x + self.panel_width - 20, 140)
        )
        
        # Estadísticas
        stats = self.solver.get_statistics()
        
        stat_y = 155
        stat_spacing = 28
        
        stats_to_show = [
            ("Iteración", str(stats['iteration'])),
            ("Mejor costo", f"{stats['best_cost']:.2f}" if stats['best_cost'] else "---"),
            ("Longitud ruta", str(stats['best_path_length']) if stats['best_path_length'] else "---"),
            ("Hormigas exitosas", f"{stats['successful_ants']}/{stats['total_ants']}"),
            ("Max feromona", f"{stats['max_pheromone']:.3f}"),
        ]
        
        for label, value in stats_to_show:
            label_surf = self.font_small.render(label + ":", True, COLORS['text_secondary'])
            value_surf = self.font_small.render(value, True, COLORS['text_primary'])
            self.screen.blit(label_surf, (panel_x + 20, stat_y))
            self.screen.blit(value_surf, (panel_x + 150, stat_y))
            stat_y += stat_spacing
            
        # Botones
        for btn in self.buttons:
            btn.draw(self.screen, self.font_medium)
            
        # Separador
        pygame.draw.line(
            self.screen, COLORS['panel_border'],
            (panel_x + 20, 310), (panel_x + self.panel_width - 20, 310)
        )
        
        # Título de parámetros
        params_title = self.font_medium.render("⚙️ PARÁMETROS", True, COLORS['text_primary'])
        self.screen.blit(params_title, (panel_x + 20, 320))
        
        # Sliders
        for slider in self.sliders:
            slider.draw(self.screen, self.font_small)
            
        # Controles de teclado
        help_y = WINDOW_HEIGHT - 120
        pygame.draw.line(
            self.screen, COLORS['panel_border'],
            (panel_x + 20, help_y - 10), (panel_x + self.panel_width - 20, help_y - 10)
        )
        
        help_title = self.font_medium.render("⌨️ ATAJOS", True, COLORS['text_primary'])
        self.screen.blit(help_title, (panel_x + 20, help_y))
        
        shortcuts = [
            "ESPACIO - Iniciar/Pausar",
            "R - Reiniciar",
            "S - Cambiar escenario",
            "P - Mostrar feromonas",
            "B - Mostrar mejor ruta"
        ]
        
        for i, shortcut in enumerate(shortcuts):
            text = self.font_small.render(shortcut, True, COLORS['text_secondary'])
            self.screen.blit(text, (panel_x + 20, help_y + 25 + i * 18))
