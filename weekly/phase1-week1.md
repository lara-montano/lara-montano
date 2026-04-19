# Fase 1 · Semana 1 — Convex sets & convex functions

**Objetivo de la semana.** Identificar con fluidez conjuntos y funciones convexas, y justificar convexidad vía operaciones que la preservan (sin siempre recurrir al Hessiano).

**Lectura (obligatoria).** Boyd & Vandenberghe, *Convex Optimization*, secciones 2.1–2.3 y 3.1–3.2.
**Lectura (opcional).** §2.4 (generalized inequalities) y §3.2.4 (log-sum-exp y log-det).

---

## 1. Mini-lección

### 1.1 Conjunto convexo

Un conjunto $C \subseteq \mathbb{R}^n$ es **convex** si $\forall x,y \in C,\; \forall \theta \in [0,1]:\; \theta x + (1-\theta) y \in C$. Geométricamente: todo segmento entre dos puntos del conjunto queda dentro.

**Ejemplos canónicos** (memorízalos):

- Hyperplane: $\{x : a^\top x = b\}$.
- Halfspace: $\{x : a^\top x \le b\}$.
- Norm ball: $\{x : \|x - x_c\| \le r\}$ (cualquier norma).
- Polyhedron: $\{x : Ax \le b,\; Cx = d\}$.
- PSD cone: $\mathbb{S}^n_+ = \{X \in \mathbb{S}^n : X \succeq 0\}$.
- Second-order cone: $\{(x,t) : \|x\|_2 \le t\}$.

**Operaciones que preservan convexidad** (tu caja de herramientas principal):

1. Intersección arbitraria.
2. Imagen afín y preimagen afín.
3. Suma y producto cartesiano.
4. Perspective function $P(x,t) = x/t$ sobre dom $= \{t>0\}$.
5. Proyección sobre subespacios.

### 1.2 Función convexa

$f:\mathbb{R}^n \to \mathbb{R}$ es convexa si dom $f$ es convexo y
$$f(\theta x + (1-\theta) y) \le \theta f(x) + (1-\theta) f(y),\quad \theta\in[0,1].$$

**Caracterización por epígrafo.** $f$ es convexa $\iff$ $\text{epi}\, f = \{(x,t) : f(x) \le t\}$ es convexo. Esto une ambos mundos (conjuntos ↔ funciones).

**Condiciones diferenciables.**

- Primer orden: $f(y) \ge f(x) + \nabla f(x)^\top (y-x)$ (la tangente queda por debajo).
- Segundo orden: $\nabla^2 f(x) \succeq 0$ en dom $f$ (abierto y convexo).

**Desigualdad de Jensen.** Si $f$ es convexa y $X$ v.a. con valores en dom $f$: $f(\mathbb{E}[X]) \le \mathbb{E}[f(X)]$. Base conceptual de mucha teoría estocástica y de información.

**Operaciones que preservan convexidad de funciones.**

1. Suma no negativa ponderada: $\alpha f + \beta g$ con $\alpha,\beta \ge 0$.
2. Composición con afín: $f(Ax+b)$ es convexa si $f$ lo es.
3. Pointwise máximo/supremo: $\max_i f_i$, $\sup_{y\in\mathcal{Y}} f(x,y)$.
4. Composición escalar $h\circ g$: reglas de monotonía de $h$ y convex/concavidad de $g$ (tabla en B&V §3.2.4).
5. Perspective: $g(x,t) = t f(x/t)$ con $t>0$.
6. Minimización parcial sobre conjunto convexo conjunto.

### 1.3 Intuición para la práctica

Cuando modeles, no intentes derivar Hessianos: **pregúntate qué building blocks estás combinando**. 90 % de los problemas "prácticos" se resuelven identificando suma/máximo/afín/perspective sobre funciones atómicas conocidas (norms, log-sum-exp, quadratic-over-linear, etc.).

---

## 2. Ejercicios graduados

Trabaja a lápiz. Si te atoras más de 15 min en uno, anótalo como "duda abierta" en `study-log.md`.

1. **(calentamiento)** Demuestra que la intersección arbitraria de conjuntos convexos es convexa.
2. **(operaciones)** Sea $C = \{x \in \mathbb{R}^n : \|Ax - b\|_2 \le c^\top x + d\}$. ¿Bajo qué condiciones es convexo? Clasifícalo (¿LP? ¿SOCP?).
3. **(funciones)** Determina convexidad/concavidad de $f(x,y) = x^2/y$ en $\{y>0\}$. Dos vías: Hessiano y perspective.
4. **(log-sum-exp)** Prueba que $f(x) = \log \sum_{i=1}^n e^{x_i}$ es convexa. *Hint:* Cauchy–Schwarz o analizar $\nabla^2 f = \text{diag}(z) - zz^\top$ con $z_i = e^{x_i}/\sum_j e^{x_j}$.
5. **(máximo)** Muestra que $f(x) = \max_{i=1,\dots,m} (a_i^\top x + b_i)$ es convexa. ¿Es diferenciable?
6. **(reto)** Sea $f(x) = \lambda_{\max}(A_0 + \sum_i x_i A_i)$ con $A_i \in \mathbb{S}^n$. Prueba que $f$ es convexa. *Hint:* $\lambda_{\max}(M) = \sup_{\|v\|=1} v^\top M v$.

---

## 3. Reto de código

Objetivo doble: visualizar y usar CVXPY para verificar.

**A. Visualización.** En Python, dibuja en 2D:
- La intersección de 4 halfspaces (un polígono).
- La bola $\|x\|_1 \le 1$ y $\|x\|_\infty \le 1$.
- Muestreando 10 000 puntos, verifica empíricamente que el segmento entre cualquier par queda dentro (contador de violaciones).

**B. Chebyshev center.** Dado el polítopo $P = \{x : Ax \le b\}$ con
```python
A = np.array([[ 1, 0],[-1, 0],[ 0, 1],[ 0,-1],[ 1, 1]])
b = np.array([1, 1, 1, 1, 1.5])
```
formula y resuelve con CVXPY el problema de Chebyshev center:
$$\max_{x_c,\,r}\; r \quad \text{s.a.}\quad a_i^\top x_c + r\|a_i\|_2 \le b_i,\; r \ge 0.$$
Grafica el polítopo y el círculo inscrito.

**C. Mini-experimento.** Para $f(x) = \log\sum e^{x_i}$ en $\mathbb{R}^3$: toma 1000 pares $(x,y)$ aleatorios y verifica numéricamente $f(\tfrac{x+y}{2}) \le \tfrac{f(x)+f(y)}{2}$. Reporta conteo de violaciones (debe ser 0 salvo error numérico).

---

## 4. Autoevaluación (responde en 2 líneas cada una)

- ¿Por qué la caracterización por epígrafo es útil?
- Da un ejemplo donde el Hessiano no exista pero la función sea convexa.
- ¿Por qué el máximo puntual preserva convexidad pero el mínimo no necesariamente?
- Si $f$ es convexa, ¿$-f$ lo es? ¿Y $1/f$?

---

## 5. Cierre

Cuando termines: actualiza `study-log.md` con estado `done`, dudas abiertas y el tiempo real invertido. En la siguiente sesión te reviso los ejercicios (pegas tus respuestas o el notebook) y pasamos a **Semana 2: LP y dualidad**.
