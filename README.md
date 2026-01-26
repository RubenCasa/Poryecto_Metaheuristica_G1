# 🐜 Simulador de Trayectorias con Algoritmo ACO

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)](https://www.pygame.org/)
[![Universidad](https://img.shields.io/badge/UNACH-Metaheurísticas-red.svg)](https://www.unach.edu.ec/)

> **Universidad Nacional de Chimborazo**  
> Asignatura: Metaheurísticas

---

## 📋 Descripción

Este proyecto implementa un **simulador visual interactivo** del algoritmo **Ant Colony Optimization (ACO)** para encontrar trayectorias óptimas en un espacio 2D con obstáculos.

El algoritmo ACO está inspirado en el comportamiento de las colonias de hormigas reales:
- Las hormigas exploran el espacio en busca de comida
- Depositan **feromonas** en su camino
- Las rutas con más feromona atraen más hormigas
- Con el tiempo, la colonia converge hacia la ruta óptima

---

## ✨ Características

- 🎨 **Interfaz visual moderna** con tema oscuro y colores neón
- 🔥 **Mapa de calor de feromonas** en tiempo real
- 🐜 **Animación fluida** de las hormigas explorando
- 📊 **Panel de estadísticas** con métricas en vivo
- 🎮 **Controles interactivos** para ajustar parámetros
- 🗺️ **7 escenarios predefinidos** incluyendo laberintos y trampas
- ✨ **Efectos de partículas** cuando se encuentra la mejor ruta

---

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar o descargar el proyecto**
```bash
git clone https://github.com/tu-usuario/aco-simulator.git
cd aco-simulator
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar el simulador**
```bash
python main.py
```

---

## 🎮 Controles

| Tecla | Acción |
|-------|--------|
| `ESPACIO` | Iniciar/Pausar simulación |
| `R` | Reiniciar simulación |
| `S` | Cambiar escenario |
| `P` | Mostrar/ocultar feromonas |
| `B` | Mostrar/ocultar mejor ruta |

También puedes usar los **botones y sliders** en el panel lateral para controlar la simulación.

---

## ⚙️ Parámetros del Algoritmo

| Parámetro | Símbolo | Descripción | Rango |
|-----------|---------|-------------|-------|
| Alpha | α | Importancia de la feromona | 0.1 - 5.0 |
| Beta | β | Importancia de la heurística | 0.1 - 5.0 |
| Evaporación | ρ | Tasa de evaporación de feromonas | 0.01 - 0.5 |
| Hormigas | - | Número de hormigas en la colonia | 5 - 100 |

---

## 🗺️ Escenarios Disponibles

1. **Laberinto Simple** - Obstáculos básicos para aprender
2. **Laberinto Complejo** - Múltiples caminos posibles
3. **Campo Abierto** - Sin obstáculos, ideal para ver convergencia
4. **La Trampa** - Un camino aparentemente corto pero bloqueado
5. **Espiral** - Las hormigas deben seguir un camino curvo
6. **Aleatorio** - Obstáculos generados aleatoriamente
7. **Logo UNACH** - Obstáculos formando las iniciales

---

## 📁 Estructura del Proyecto

```
PRO_METAHERISTICA/
├── main.py              # Punto de entrada principal
├── aco_algorithm.py     # Implementación del algoritmo ACO
├── environment.py       # Entorno y manejo de obstáculos
├── visualization.py     # Visualización con Pygame
├── config.py            # Configuración y constantes
├── scenarios.py         # Escenarios predefinidos
├── requirements.txt     # Dependencias
└── README.md            # Este archivo
```

---

## 🔬 El Algoritmo ACO

### Fórmula de Probabilidad

La probabilidad de que una hormiga elija moverse a la celda `j` desde `i` es:

```
P(i,j) = (τ_ij^α × η_ij^β) / Σ(τ_ik^α × η_ik^β)
```

Donde:
- `τ_ij` = Nivel de feromona en el camino i→j
- `η_ij` = Heurística (1/distancia al objetivo)
- `α` = Peso de la feromona
- `β` = Peso de la heurística

### Actualización de Feromonas

Después de cada iteración:
1. **Evaporación**: `τ_new = (1 - ρ) × τ_old`
2. **Depósito**: Las hormigas que llegaron al objetivo depositan feromona proporcional a la calidad de su ruta

---

## 📸 Capturas de Pantalla

*El simulador presenta una interfaz moderna con:*
- Panel lateral con estadísticas y controles
- Mapa de calor de feromonas con gradientes de color
- Animación de hormigas buscando la ruta óptima
- Efectos visuales de partículas

---

## 👨‍💻 Autor

**Estudiante de la Universidad Nacional de Chimborazo**  
Carrera: Ingeniería en Sistemas / Computación  
Asignatura: Metaheurísticas  
Año: 2026

---

## 📚 Referencias

- Dorigo, M., & Stützle, T. (2004). *Ant Colony Optimization*. MIT Press.
- Colorni, A., Dorigo, M., & Maniezzo, V. (1991). *Distributed Optimization by Ant Colonies*.

---

## 📄 Licencia

Este proyecto es de uso académico para la Universidad Nacional de Chimborazo.

---

<p align="center">
  <b>🐜 "Las hormigas pequeñas pueden mover montañas grandes" 🐜</b>
</p>
