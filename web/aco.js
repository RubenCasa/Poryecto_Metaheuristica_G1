/**
 * =============================================================================
 * SIMULADOR ACO - Algoritmo de Colonia de Hormigas
 * Universidad Nacional de Chimborazo - Metaheurísticas
 * =============================================================================
 */

// ============================================================================
// CONFIGURACIÓN
// ============================================================================
const CONFIG = {
    // Grid
    GRID_ROWS: 25,
    GRID_COLS: 35,
    CELL_SIZE: 25,

    // Convergencia
    CONVERGENCE_ITERATIONS: 15,

    // Colores
    COLORS: {
        background: '#0a0a12',
        grid: '#1a1a2e',
        obstacle: '#2a2a45',
        obstacleBorder: '#4a4a70',
        start: '#00ff96',
        end: '#ff3264',
        ant: '#ffc832',
        antBorder: '#000000',
        bestPath: '#00ffd5',
        bestPathGlow: 'rgba(0, 255, 213, 0.3)',
        pheromone: {
            low: [61, 0, 102],
            mid: [153, 50, 204],
            high: [255, 105, 255]
        }
    },

    // Direcciones de movimiento
    DIRECTIONS: [
        [-1, -1], [-1, 0], [-1, 1],
        [0, -1], [0, 1],
        [1, -1], [1, 0], [1, 1]
    ]
};

// ============================================================================
// ESCENARIOS
// ============================================================================
const SCENARIOS = [
    {
        name: "Laberinto Simple",
        description: "Un laberinto básico con paredes verticales y horizontales",
        setup: (env) => {
            env.setStart(2, 2);
            env.setEnd(env.rows - 3, env.cols - 3);
            for (let r = 5; r < env.rows - 8; r++) {
                env.addObstacle(r, Math.floor(env.cols / 2));
            }
            for (let c = 8; c < env.cols - 12; c++) {
                env.addObstacle(Math.floor(env.rows / 2), c);
            }
        }
    },
    {
        name: "Laberinto Complejo",
        description: "Múltiples caminos posibles con varios obstáculos",
        setup: (env) => {
            env.setStart(2, 2);
            env.setEnd(env.rows - 3, env.cols - 3);
            for (let i = 0; i < 3; i++) {
                const col = 8 + i * 8;
                if (col < env.cols - 3) {
                    const startRow = i % 2 === 0 ? 3 : 8;
                    const endRow = i % 2 === 0 ? env.rows - 8 : env.rows - 3;
                    for (let r = startRow; r < endRow; r++) {
                        env.addObstacle(r, col);
                    }
                }
            }
            for (let c = 5; c < 15; c++) env.addObstacle(8, c);
            for (let c = 18; c < 28; c++) env.addObstacle(12, c);
            for (let c = 8; c < 18; c++) env.addObstacle(18, c);
        }
    },
    {
        name: "Campo Abierto",
        description: "Sin obstáculos, ideal para ver la convergencia de feromonas",
        setup: (env) => {
            env.setStart(Math.floor(env.rows / 2), 3);
            env.setEnd(Math.floor(env.rows / 2), env.cols - 4);
        }
    },
    {
        name: "La Trampa",
        description: "Un camino aparentemente corto que es un callejón sin salida",
        setup: (env) => {
            env.setStart(Math.floor(env.rows / 2), 3);
            env.setEnd(Math.floor(env.rows / 2), env.cols - 4);
            const wallCol = env.cols - 8;
            for (let r = 3; r < env.rows - 3; r++) {
                env.addObstacle(r, wallCol);
            }
            env.removeObstacle(4, wallCol);
            env.removeObstacle(5, wallCol);
            const trapRow = Math.floor(env.rows / 2);
            for (let c = 12; c < wallCol - 2; c++) {
                env.addObstacle(trapRow - 3, c);
                env.addObstacle(trapRow + 3, c);
            }
            for (let r = trapRow - 3; r < trapRow + 4; r++) {
                env.addObstacle(r, wallCol - 2);
            }
        }
    },
    {
        name: "Espiral",
        description: "Las hormigas deben seguir un camino en espiral",
        setup: (env) => {
            env.setStart(Math.floor(env.rows / 2), Math.floor(env.cols / 2));
            env.setEnd(2, 2);
            const margin = 3;
            for (let c = margin; c < env.cols - margin; c++) env.addObstacle(margin, c);
            for (let r = margin; r < env.rows - margin; r++) env.addObstacle(r, env.cols - margin - 1);
            for (let c = margin; c < env.cols - margin; c++) env.addObstacle(env.rows - margin - 1, c);
            for (let r = margin + 5; r < env.rows - margin; r++) env.addObstacle(r, margin);
            const margin2 = 7;
            for (let c = margin2; c < env.cols - margin2; c++) env.addObstacle(margin2, c);
            for (let r = margin2; r < env.rows - margin2; r++) env.addObstacle(r, env.cols - margin2 - 1);
            env.removeObstacle(margin, margin + 3);
        }
    },
    {
        name: "Aleatorio",
        description: "Obstáculos distribuidos aleatoriamente",
        setup: (env) => {
            env.setStart(2, 2);
            env.setEnd(env.rows - 3, env.cols - 3);
            const density = 0.2;
            for (let r = 0; r < env.rows; r++) {
                for (let c = 0; c < env.cols; c++) {
                    if (Math.random() < density) {
                        const distStart = Math.abs(r - env.start.row) + Math.abs(c - env.start.col);
                        const distEnd = Math.abs(r - env.end.row) + Math.abs(c - env.end.col);
                        if (distStart > 4 && distEnd > 4) env.addObstacle(r, c);
                    }
                }
            }
        }
    },
    {
        name: "Logo UNACH",
        description: "Obstáculos formando las letras U-N-A-C-H",
        setup: (env) => {
            env.setStart(env.rows - 3, 2);
            env.setEnd(env.rows - 3, env.cols - 3);
            // Marco
            for (let c = 0; c < env.cols; c++) {
                env.addObstacle(0, c);
                env.addObstacle(env.rows - 1, c);
            }
            for (let r = 0; r < env.rows; r++) {
                env.addObstacle(r, 0);
                env.addObstacle(r, env.cols - 1);
            }
            // Letra U
            let startCol = 3;
            for (let r = 5; r < 14; r++) {
                env.addObstacle(r, startCol);
                env.addObstacle(r, startCol + 3);
            }
            for (let c = startCol; c < startCol + 4; c++) env.addObstacle(14, c);
            // Letra N
            startCol = 9;
            for (let r = 5; r < 15; r++) {
                env.addObstacle(r, startCol);
                env.addObstacle(r, startCol + 4);
            }
            env.addObstacle(7, startCol + 1);
            env.addObstacle(9, startCol + 2);
            env.addObstacle(11, startCol + 3);
            // Letra A
            startCol = 16;
            for (let r = 5; r < 15; r++) {
                env.addObstacle(r, startCol);
                env.addObstacle(r, startCol + 3);
            }
            for (let c = startCol; c < startCol + 4; c++) {
                env.addObstacle(5, c);
                env.addObstacle(10, c);
            }
            // Letra C
            startCol = 22;
            for (let r = 5; r < 15; r++) {
                env.addObstacle(r, startCol);
            }
            for (let c = startCol; c < startCol + 4; c++) {
                env.addObstacle(5, c);
                env.addObstacle(14, c);
            }
            // Letra H
            startCol = 28;
            for (let r = 5; r < 15; r++) {
                env.addObstacle(r, startCol);
                env.addObstacle(r, startCol + 3);
            }
            for (let c = startCol; c < startCol + 4; c++) {
                env.addObstacle(10, c);
            }
        }
    }
];

// ============================================================================
// CLASE: ENTORNO
// ============================================================================
class Environment {
    constructor(rows = CONFIG.GRID_ROWS, cols = CONFIG.GRID_COLS) {
        this.rows = rows;
        this.cols = cols;
        this.grid = this.createGrid();
        this.pheromones = this.createPheromoneGrid();
        this.start = { row: 1, col: 1 };
        this.end = { row: rows - 2, col: cols - 2 };
    }

    createGrid() {
        return Array(this.rows).fill(null).map(() => Array(this.cols).fill(0));
    }

    createPheromoneGrid(initialValue = 0.1) {
        return Array(this.rows).fill(null).map(() => Array(this.cols).fill(initialValue));
    }

    resetPheromones(initialValue = 0.1) {
        this.pheromones = this.createPheromoneGrid(initialValue);
    }

    isValidCell(row, col) {
        return row >= 0 && row < this.rows && col >= 0 && col < this.cols && this.grid[row][col] === 0;
    }

    getNeighbors(row, col) {
        const neighbors = [];
        for (const [dr, dc] of CONFIG.DIRECTIONS) {
            const newRow = row + dr;
            const newCol = col + dc;
            if (this.isValidCell(newRow, newCol)) {
                const cost = Math.abs(dr) + Math.abs(dc) === 2 ? 1.414 : 1;
                neighbors.push({ row: newRow, col: newCol, cost });
            }
        }
        return neighbors;
    }

    getHeuristic(row, col) {
        return Math.sqrt(Math.pow(row - this.end.row, 2) + Math.pow(col - this.end.col, 2));
    }

    addObstacle(row, col) {
        if (!(row === this.start.row && col === this.start.col) &&
            !(row === this.end.row && col === this.end.col)) {
            if (row >= 0 && row < this.rows && col >= 0 && col < this.cols) {
                this.grid[row][col] = 1;
            }
        }
    }

    removeObstacle(row, col) {
        if (row >= 0 && row < this.rows && col >= 0 && col < this.cols) {
            this.grid[row][col] = 0;
        }
    }

    clearObstacles() {
        this.grid = this.createGrid();
    }

    setStart(row, col) {
        if (this.isValidCell(row, col)) {
            this.start = { row, col };
        }
    }

    setEnd(row, col) {
        if (this.isValidCell(row, col)) {
            this.end = { row, col };
        }
    }

    evaporatePheromones(rate) {
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                this.pheromones[r][c] *= (1 - rate);
                this.pheromones[r][c] = Math.max(this.pheromones[r][c], 0.01);
            }
        }
    }

    getMaxPheromone() {
        let max = 0;
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                if (this.pheromones[r][c] > max) max = this.pheromones[r][c];
            }
        }
        return max;
    }
}

// ============================================================================
// CLASE: HORMIGA
// ============================================================================
class Ant {
    constructor(startRow, startCol) {
        this.row = startRow;
        this.col = startCol;
        this.path = [{ row: startRow, col: startCol }];
        this.pathCost = 0;
        this.reachedGoal = false;
        this.stuck = false;
        this.visited = new Set();
        this.visited.add(`${startRow},${startCol}`);
    }

    moveTo(row, col, cost) {
        this.row = row;
        this.col = col;
        this.path.push({ row, col });
        this.pathCost += cost;
        this.visited.add(`${row},${col}`);
    }

    hasVisited(row, col) {
        return this.visited.has(`${row},${col}`);
    }

    reset(startRow, startCol) {
        this.row = startRow;
        this.col = startCol;
        this.path = [{ row: startRow, col: startCol }];
        this.pathCost = 0;
        this.reachedGoal = false;
        this.stuck = false;
        this.visited = new Set();
        this.visited.add(`${startRow},${startCol}`);
    }
}

// ============================================================================
// CLASE: SOLUCIONADOR ACO
// ============================================================================
class ACOSolver {
    constructor(environment, params = {}) {
        this.env = environment;
        this.params = {
            numAnts: params.numAnts || 30,
            alpha: params.alpha || 1.0,
            beta: params.beta || 2.0,
            evaporationRate: params.evaporationRate || 0.1,
            Q: params.Q || 100,
            initialPheromone: params.initialPheromone || 0.1
        };

        this.ants = [];
        this.bestPath = null;
        this.bestCost = Infinity;
        this.iteration = 0;
        this.running = false;
        this.converged = false;
        this.iterationsWithoutImprovement = 0;

        this.initializeAnts();
    }

    initializeAnts() {
        this.ants = [];
        for (let i = 0; i < this.params.numAnts; i++) {
            this.ants.push(new Ant(this.env.start.row, this.env.start.col));
        }
    }

    reset() {
        this.env.resetPheromones(this.params.initialPheromone);
        this.initializeAnts();
        this.bestPath = null;
        this.bestCost = Infinity;
        this.iteration = 0;
        this.running = false;
        this.converged = false;
        this.iterationsWithoutImprovement = 0;
    }

    selectNextCell(ant) {
        const neighbors = this.env.getNeighbors(ant.row, ant.col);
        const unvisited = neighbors.filter(n => !ant.hasVisited(n.row, n.col));

        if (unvisited.length === 0) {
            ant.stuck = true;
            return null;
        }

        const probabilities = [];
        let total = 0;

        for (const neighbor of unvisited) {
            const pheromone = this.env.pheromones[neighbor.row][neighbor.col];
            const heuristic = 1.0 / (this.env.getHeuristic(neighbor.row, neighbor.col) + 0.1);
            const attractiveness = Math.pow(pheromone, this.params.alpha) * Math.pow(heuristic, this.params.beta);
            probabilities.push(attractiveness);
            total += attractiveness;
        }

        if (total === 0) {
            return unvisited[Math.floor(Math.random() * unvisited.length)];
        }

        const r = Math.random();
        let cumulative = 0;

        for (let i = 0; i < unvisited.length; i++) {
            cumulative += probabilities[i] / total;
            if (r <= cumulative) return unvisited[i];
        }

        return unvisited[unvisited.length - 1];
    }

    moveAnt(ant) {
        if (ant.reachedGoal || ant.stuck) return false;

        if (ant.row === this.env.end.row && ant.col === this.env.end.col) {
            ant.reachedGoal = true;
            return false;
        }

        const next = this.selectNextCell(ant);
        if (!next) return false;

        ant.moveTo(next.row, next.col, next.cost);

        if (ant.row === this.env.end.row && ant.col === this.env.end.col) {
            ant.reachedGoal = true;
        }

        return true;
    }

    moveAllAnts() {
        let anyMoved = false;
        for (const ant of this.ants) {
            if (this.moveAnt(ant)) anyMoved = true;
        }
        return anyMoved;
    }

    allAntsFinished() {
        return this.ants.every(ant => ant.reachedGoal || ant.stuck);
    }

    updatePheromones() {
        this.env.evaporatePheromones(this.params.evaporationRate);

        let improved = false;

        for (const ant of this.ants) {
            if (ant.reachedGoal) {
                const deposit = this.params.Q / ant.pathCost;

                for (const pos of ant.path) {
                    this.env.pheromones[pos.row][pos.col] += deposit;
                }

                if (ant.pathCost < this.bestCost) {
                    this.bestCost = ant.pathCost;
                    this.bestPath = [...ant.path];
                    improved = true;
                }
            }
        }

        // Verificar convergencia
        if (improved) {
            this.iterationsWithoutImprovement = 0;
        } else {
            this.iterationsWithoutImprovement++;
        }

        if (this.iterationsWithoutImprovement >= CONFIG.CONVERGENCE_ITERATIONS && this.bestPath) {
            this.converged = true;
        }
    }

    step() {
        if (this.converged) {
            return 'converged';
        }

        if (!this.allAntsFinished()) {
            this.moveAllAnts();
            return 'moving';
        } else {
            this.updatePheromones();

            if (this.converged) {
                return 'converged';
            }

            for (const ant of this.ants) {
                ant.reset(this.env.start.row, this.env.start.col);
            }

            this.iteration++;
            return 'new_iteration';
        }
    }

    getStatistics() {
        const successful = this.ants.filter(a => a.reachedGoal).length;
        return {
            iteration: this.iteration,
            bestCost: this.bestCost === Infinity ? null : this.bestCost,
            pathLength: this.bestPath ? this.bestPath.length : 0,
            successfulAnts: successful,
            totalAnts: this.ants.length,
            maxPheromone: this.env.getMaxPheromone(),
            converged: this.converged,
            iterationsWithoutImprovement: this.iterationsWithoutImprovement
        };
    }
}

// ============================================================================
// CLASE: VISUALIZACIÓN
// ============================================================================
class Visualization {
    constructor(canvas, environment, solver) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.env = environment;
        this.solver = solver;

        this.setupCanvas();
        this.particles = [];
        this.celebrationActive = false;
    }

    setupCanvas() {
        const width = this.env.cols * CONFIG.CELL_SIZE;
        const height = this.env.rows * CONFIG.CELL_SIZE;

        this.canvas.width = width;
        this.canvas.height = height;
        this.canvas.style.width = width + 'px';
        this.canvas.style.height = height + 'px';
    }

    clear() {
        this.ctx.fillStyle = CONFIG.COLORS.background;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }

    drawGrid() {
        this.ctx.strokeStyle = CONFIG.COLORS.grid;
        this.ctx.lineWidth = 0.5;

        for (let r = 0; r <= this.env.rows; r++) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, r * CONFIG.CELL_SIZE);
            this.ctx.lineTo(this.canvas.width, r * CONFIG.CELL_SIZE);
            this.ctx.stroke();
        }

        for (let c = 0; c <= this.env.cols; c++) {
            this.ctx.beginPath();
            this.ctx.moveTo(c * CONFIG.CELL_SIZE, 0);
            this.ctx.lineTo(c * CONFIG.CELL_SIZE, this.canvas.height);
            this.ctx.stroke();
        }
    }

    lerpColor(c1, c2, t) {
        return [
            Math.round(c1[0] + (c2[0] - c1[0]) * t),
            Math.round(c1[1] + (c2[1] - c1[1]) * t),
            Math.round(c1[2] + (c2[2] - c1[2]) * t)
        ];
    }

    drawPheromones() {
        const maxPher = Math.max(this.env.getMaxPheromone(), 0.1);

        for (let r = 0; r < this.env.rows; r++) {
            for (let c = 0; c < this.env.cols; c++) {
                if (this.env.grid[r][c] === 0) {
                    const pher = this.env.pheromones[r][c];
                    const intensity = Math.min(pher / maxPher, 1.0);

                    if (intensity > 0.05) {
                        let color;
                        if (intensity < 0.5) {
                            color = this.lerpColor(CONFIG.COLORS.pheromone.low, CONFIG.COLORS.pheromone.mid, intensity * 2);
                        } else {
                            color = this.lerpColor(CONFIG.COLORS.pheromone.mid, CONFIG.COLORS.pheromone.high, (intensity - 0.5) * 2);
                        }

                        const alpha = intensity * 0.7;
                        this.ctx.fillStyle = `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${alpha})`;
                        this.ctx.fillRect(c * CONFIG.CELL_SIZE + 1, r * CONFIG.CELL_SIZE + 1, CONFIG.CELL_SIZE - 2, CONFIG.CELL_SIZE - 2);
                    }
                }
            }
        }
    }

    drawObstacles() {
        for (let r = 0; r < this.env.rows; r++) {
            for (let c = 0; c < this.env.cols; c++) {
                if (this.env.grid[r][c] === 1) {
                    const x = c * CONFIG.CELL_SIZE;
                    const y = r * CONFIG.CELL_SIZE;

                    this.ctx.fillStyle = CONFIG.COLORS.obstacle;
                    this.ctx.fillRect(x + 1, y + 1, CONFIG.CELL_SIZE - 2, CONFIG.CELL_SIZE - 2);

                    this.ctx.strokeStyle = CONFIG.COLORS.obstacleBorder;
                    this.ctx.lineWidth = 1;
                    this.ctx.strokeRect(x + 1, y + 1, CONFIG.CELL_SIZE - 2, CONFIG.CELL_SIZE - 2);
                }
            }
        }
    }

    drawStartEnd() {
        const cellSize = CONFIG.CELL_SIZE;
        const time = Date.now() / 200;
        const pulse = (Math.sin(time) + 1) / 2;

        // Inicio
        const sx = this.env.start.col * cellSize;
        const sy = this.env.start.row * cellSize;

        const glowSize = 4 + pulse * 3;
        this.ctx.shadowColor = CONFIG.COLORS.start;
        this.ctx.shadowBlur = glowSize;

        this.ctx.fillStyle = CONFIG.COLORS.start;
        this.ctx.fillRect(sx + 2, sy + 2, cellSize - 4, cellSize - 4);

        this.ctx.shadowBlur = 0;
        this.ctx.font = `${cellSize * 0.6}px Arial`;
        this.ctx.fillText('🏠', sx + 2, sy + cellSize - 4);

        // Fin
        const ex = this.env.end.col * cellSize;
        const ey = this.env.end.row * cellSize;

        this.ctx.shadowColor = CONFIG.COLORS.end;
        this.ctx.shadowBlur = glowSize;

        this.ctx.fillStyle = CONFIG.COLORS.end;
        this.ctx.fillRect(ex + 2, ey + 2, cellSize - 4, cellSize - 4);

        this.ctx.shadowBlur = 0;
        this.ctx.fillText('🎯', ex + 2, ey + cellSize - 4);
    }

    drawBestPath() {
        if (!this.solver.bestPath || this.solver.bestPath.length < 2) return;

        const cellSize = CONFIG.CELL_SIZE;
        const isConverged = this.solver.converged;

        this.ctx.beginPath();
        this.ctx.strokeStyle = isConverged ? '#00ff00' : CONFIG.COLORS.bestPath;
        this.ctx.lineWidth = isConverged ? 5 : 3;
        this.ctx.shadowColor = isConverged ? '#00ff00' : CONFIG.COLORS.bestPath;
        this.ctx.shadowBlur = isConverged ? 20 : 10;

        const first = this.solver.bestPath[0];
        this.ctx.moveTo(first.col * cellSize + cellSize / 2, first.row * cellSize + cellSize / 2);

        for (let i = 1; i < this.solver.bestPath.length; i++) {
            const pos = this.solver.bestPath[i];
            this.ctx.lineTo(pos.col * cellSize + cellSize / 2, pos.row * cellSize + cellSize / 2);
        }

        this.ctx.stroke();
        this.ctx.shadowBlur = 0;

        // Dibujar puntos en el camino si está convergido
        if (isConverged) {
            for (let i = 0; i < this.solver.bestPath.length; i += 3) {
                const pos = this.solver.bestPath[i];
                const x = pos.col * cellSize + cellSize / 2;
                const y = pos.row * cellSize + cellSize / 2;

                this.ctx.beginPath();
                this.ctx.arc(x, y, 4, 0, Math.PI * 2);
                this.ctx.fillStyle = '#ffffff';
                this.ctx.fill();
            }
        }
    }

    drawAnts() {
        // No dibujar hormigas si ya convergió
        if (this.solver.converged) return;

        const cellSize = CONFIG.CELL_SIZE;

        for (const ant of this.solver.ants) {
            if (ant.stuck) continue;

            const x = ant.col * cellSize + cellSize / 2;
            const y = ant.row * cellSize + cellSize / 2;
            const radius = cellSize / 3;

            const color = ant.reachedGoal ? CONFIG.COLORS.bestPath : CONFIG.COLORS.ant;

            this.ctx.beginPath();
            this.ctx.arc(x, y, radius, 0, Math.PI * 2);
            this.ctx.fillStyle = color;
            this.ctx.fill();

            this.ctx.strokeStyle = CONFIG.COLORS.antBorder;
            this.ctx.lineWidth = 1;
            this.ctx.stroke();
        }
    }

    spawnCelebrationParticles() {
        const cellSize = CONFIG.CELL_SIZE;
        const endX = this.env.end.col * cellSize + cellSize / 2;
        const endY = this.env.end.row * cellSize + cellSize / 2;

        for (let i = 0; i < 50; i++) {
            this.particles.push({
                x: endX,
                y: endY,
                vx: (Math.random() - 0.5) * 10,
                vy: (Math.random() - 0.5) * 10,
                life: 1.0,
                color: ['#00ff00', '#00ff96', '#00ffd5', '#ffc832', '#ff69ff'][Math.floor(Math.random() * 5)]
            });
        }
    }

    updateParticles() {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.1; // gravedad
            p.life -= 0.015;

            if (p.life <= 0) {
                this.particles.splice(i, 1);
            }
        }
    }

    drawParticles() {
        for (const p of this.particles) {
            const alpha = p.life;
            const size = p.life * 8 + 2;

            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
            this.ctx.fillStyle = p.color.replace(')', `, ${alpha})`).replace('rgb', 'rgba').replace('#', '');

            // Convertir hex a rgba
            const hex = p.color;
            const r = parseInt(hex.slice(1, 3), 16);
            const g = parseInt(hex.slice(3, 5), 16);
            const b = parseInt(hex.slice(5, 7), 16);
            this.ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${alpha})`;
            this.ctx.fill();
        }
    }

    drawConvergedBanner() {
        if (!this.solver.converged) return;

        const centerX = this.canvas.width / 2;
        const bannerY = 30;

        // Fondo del banner
        this.ctx.fillStyle = 'rgba(0, 255, 0, 0.2)';
        this.ctx.fillRect(centerX - 150, bannerY - 20, 300, 40);

        // Borde
        this.ctx.strokeStyle = '#00ff00';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(centerX - 150, bannerY - 20, 300, 40);

        // Texto
        this.ctx.font = 'bold 18px Orbitron, sans-serif';
        this.ctx.fillStyle = '#00ff00';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('✅ ¡RUTA ÓPTIMA ENCONTRADA!', centerX, bannerY + 5);
        this.ctx.textAlign = 'left';
    }

    render() {
        this.clear();
        this.drawGrid();
        this.drawPheromones();
        this.drawObstacles();
        this.drawBestPath();
        this.drawStartEnd();
        this.drawAnts();
        this.updateParticles();
        this.drawParticles();
        this.drawConvergedBanner();
    }
}

// ============================================================================
// APLICACIÓN PRINCIPAL
// ============================================================================
class App {
    constructor() {
        this.canvas = document.getElementById('acoCanvas');
        this.env = new Environment();
        this.solver = new ACOSolver(this.env);
        this.viz = new Visualization(this.canvas, this.env, this.solver);

        this.running = false;
        this.speed = 1;
        this.currentScenario = 0;
        this.hasShownConvergence = false;

        this.setupUI();
        this.loadScenario(0);
        this.createBackgroundParticles();
        this.animate();
    }

    setupUI() {
        document.getElementById('btnStart').addEventListener('click', () => this.toggleSimulation());
        document.getElementById('btnReset').addEventListener('click', () => this.reset());
        document.getElementById('btnScenario').addEventListener('click', () => this.nextScenario());

        this.setupSlider('alpha', 'alphaValue', (v) => { this.solver.params.alpha = parseFloat(v); return v; });
        this.setupSlider('beta', 'betaValue', (v) => { this.solver.params.beta = parseFloat(v); return v; });
        this.setupSlider('evap', 'evapValue', (v) => { this.solver.params.evaporationRate = parseFloat(v); return v; });
        this.setupSlider('ants', 'antsValue', (v) => { this.solver.params.numAnts = parseInt(v); return v; });
        this.setupSlider('speed', 'speedValue', (v) => { this.speed = parseFloat(v); return v + 'x'; });
    }

    setupSlider(sliderId, valueId, callback) {
        const slider = document.getElementById(sliderId + 'Slider');
        const valueEl = document.getElementById(valueId);

        if (slider && valueEl) {
            slider.addEventListener('input', () => {
                const formatted = callback(slider.value);
                valueEl.textContent = typeof formatted === 'number' ? formatted.toFixed(2) : formatted;
            });
        }
    }

    toggleSimulation() {
        if (this.solver.converged) {
            // Si ya convergió, resetear antes de iniciar
            this.reset();
        }

        this.running = !this.running;
        const btn = document.getElementById('btnStart');

        if (this.running) {
            btn.innerHTML = '<span class="btn-icon">⏸</span><span class="btn-text">PAUSAR</span>';
            btn.classList.add('running');
        } else {
            btn.innerHTML = '<span class="btn-icon">▶</span><span class="btn-text">INICIAR</span>';
            btn.classList.remove('running');
        }
    }

    reset() {
        this.running = false;
        this.hasShownConvergence = false;
        const btn = document.getElementById('btnStart');
        btn.innerHTML = '<span class="btn-icon">▶</span><span class="btn-text">INICIAR</span>';
        btn.classList.remove('running');

        this.solver.params.numAnts = parseInt(document.getElementById('antsSlider')?.value || 30);
        this.solver.reset();
        this.viz.particles = [];
        this.updateStats();

        // Remover banner de convergencia
        document.getElementById('convergenceBanner')?.classList.add('hidden');
    }

    loadScenario(index) {
        this.env.clearObstacles();
        this.env.resetPheromones();
        SCENARIOS[index].setup(this.env);
        document.getElementById('scenarioName').textContent = SCENARIOS[index].name;
        this.solver.reset();
        this.hasShownConvergence = false;
        this.updateStats();
    }

    nextScenario() {
        this.currentScenario = (this.currentScenario + 1) % SCENARIOS.length;
        this.loadScenario(this.currentScenario);
        this.running = false;
        this.hasShownConvergence = false;
        const btn = document.getElementById('btnStart');
        btn.innerHTML = '<span class="btn-icon">▶</span><span class="btn-text">INICIAR</span>';
        btn.classList.remove('running');
    }

    updateStats() {
        const stats = this.solver.getStatistics();

        document.getElementById('iterationValue').textContent = stats.iteration;
        document.getElementById('bestCost').textContent = stats.bestCost ? stats.bestCost.toFixed(2) : '---';
        document.getElementById('pathLength').textContent = stats.pathLength || '---';
        document.getElementById('successfulAnts').textContent = `${stats.successfulAnts}/${stats.totalAnts}`;
        document.getElementById('maxPheromone').textContent = stats.maxPheromone.toFixed(2);

        // Actualizar estado visual
        const statusEl = document.getElementById('simulationStatus');
        if (statusEl) {
            if (stats.converged) {
                statusEl.textContent = '✅ CONVERGIDO';
                statusEl.className = 'status-converged';
            } else if (this.running) {
                statusEl.textContent = '🔄 Buscando...';
                statusEl.className = 'status-running';
            } else {
                statusEl.textContent = '⏸ Pausado';
                statusEl.className = 'status-paused';
            }
        }
    }

    handleConvergence() {
        if (this.hasShownConvergence) return;
        this.hasShownConvergence = true;

        // Detener simulación
        this.running = false;
        const btn = document.getElementById('btnStart');
        btn.innerHTML = '<span class="btn-icon">▶</span><span class="btn-text">INICIAR</span>';
        btn.classList.remove('running');

        // Efectos de celebración
        this.viz.spawnCelebrationParticles();

        // Mostrar banner
        const banner = document.getElementById('convergenceBanner');
        if (banner) {
            banner.classList.remove('hidden');
        }
    }

    createBackgroundParticles() {
        const container = document.getElementById('particles');
        if (!container) return;

        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 15 + 's';
            particle.style.animationDuration = (10 + Math.random() * 10) + 's';
            container.appendChild(particle);
        }
    }

    animate() {
        if (this.running && !this.solver.converged) {
            const steps = Math.floor(5 * this.speed);
            for (let i = 0; i < steps; i++) {
                const result = this.solver.step();

                if (result === 'converged') {
                    this.handleConvergence();
                    break;
                }
            }
            this.updateStats();
        }

        // Verificar convergencia incluso si no está corriendo
        if (this.solver.converged && !this.hasShownConvergence) {
            this.handleConvergence();
        }

        this.viz.render();
        requestAnimationFrame(() => this.animate());
    }
}

// ============================================================================
// INICIALIZACIÓN
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    new App();
});
