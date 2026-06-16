# CASS — Búsqueda Estocástica *Anytime* Certificada

> **Certified Anytime Stochastic Search**
> Una metaheurística diseñada explícitamente para superar las críticas metodológicas
> que se le hacen al área (metáfora-manía, ausencia de garantías, rigor experimental
> débil, *No Free Lunch* mal entendido). **No usa ninguna metáfora** ni ningún
> *solver* comercial: las garantías provienen de teoremas que se demuestran y de una
> cota inferior que el propio algoritmo calcula.

---

## 0. Resumen en una frase

CASS ejecuta de forma **acoplada** un proceso **primal** (búsqueda local estocástica
tipo Metropolis sobre un espacio combinatorio) y un proceso **dual** (una cota inferior
lagrangiana maximizada por subgradiente). La **brecha certificada** entre la mejor
solución y la mejor cota se usa para (i) modular un programa de enfriamiento que
**preserva la condición de convergencia de Hajek** y (ii) emitir, en cualquier instante,
un **certificado de optimalidad** $g_k$ que acota la distancia al óptimo. El resultado
es una metaheurística *anytime*, **auto-certificante** y **sin dependencias comerciales**.

---

## 1. Posicionamiento honesto (qué es nuevo y qué no)

Una de las críticas más severas al área (Sörensen, 2015, *"Metaheuristics—the metaphor
exposed"*) es que se presentan como "novedad" cosas viejas disfrazadas de metáfora. Para
no incurrir en lo mismo, declaramos explícitamente la procedencia de cada pieza.

| Componente | ¿Nuevo? | Origen / referencia |
|---|---|---|
| Aceptación Metropolis + convergencia por enfriamiento logarítmico | **No** | Metropolis (1953); Geman & Geman (1984); **Hajek (1988)** |
| Cota inferior de Held–Karp vía relajación lagrangiana del grado, optimizada por subgradiente | **No** | Held & Karp (1970, 1971); cota del 1-árbol |
| *Drift analysis* para acotar tiempo esperado | **No** | He & Yao (2001); Doerr et al. |
| **Acoplamiento primal–dual con enfriamiento guiado por la brecha certificada, que preserva la condición de Hajek por construcción** | **Sí** | Contribución de este diseño (§4) |
| **Criterio de paro con certificado $\varepsilon$ y comportamiento *anytime* auto-certificante** | **Sí** | Contribución de este diseño (§5) |

> En otras palabras: **no inventamos una metáfora ni un operador "mágico".** Tomamos dos
> resultados clásicos y rigurosos (uno primal, uno dual) y la aportación está en **cómo se
> acoplan** para obtener un algoritmo que se certifica a sí mismo sin perder la garantía de
> convergencia. Esa honestidad de atribución es, en sí misma, parte de superar las críticas.

---

## 2. Marco formal (sin metáfora)

Trabajamos un problema de **minimización combinatoria**:

$$
\min_{x \in S} f(x), \qquad S \text{ finito},\quad f: S \to \mathbb{R}.
$$

Se define:

- **Estructura de vecindad** $N: S \to 2^S$, **simétrica** ($y \in N(x) \iff x \in N(y)$)
  e **irreducible** (el grafo de vecindad es conexo: desde cualquier $x$ se alcanza cualquier
  $x'$ por una cadena de movimientos). Esto garantiza que la cadena de Markov subyacente sea
  ergódica.
- Un **operador de propuesta** $q(\cdot\mid x)$ uniforme sobre $N(x)$. Si $|N(x)|$ no es
  constante se aplica la corrección de Metropolis–Hastings $\;\min\{1,\frac{|N(x)|}{|N(y)|}e^{-\Delta/T}\}$.

Todo lo anterior es lenguaje de **cadenas de Markov y optimización combinatoria**, no de
animales, planetas ni fenómenos naturales.

---

## 3. Los dos procesos

### 3.1 Proceso PRIMAL — búsqueda local estocástica (Metropolis)

En la iteración $k$, con estado $x_k$:

1. Proponer $y \sim \text{Unif}(N(x_k))$.
2. Sea $\Delta = f(y) - f(x_k)$. Aceptar $x_{k+1} = y$ con probabilidad
$$
A(x_k, y) = \min\!\big\{1,\; e^{-\Delta / T_k}\big\},
$$
en otro caso $x_{k+1} = x_k$.
3. Actualizar el incumbente $U_k = \min(U_{k-1}, f(x_{k+1}))$ (mejor cota **superior**).

$T_k > 0$ es la **temperatura** (programa de enfriamiento), que se fija en §4.

### 3.2 Proceso DUAL — cota inferior auto-calculada (relajación lagrangiana)

El proceso dual produce, **sin ningún solver externo**, una sucesión de cotas inferiores
válidas $L_k \le \text{OPT}$. La construcción depende del problema; aquí se detalla la
instancia de referencia (TSP simétrico), pero el patrón es general (relajar restricciones
con multiplicadores y maximizar por subgradiente).

**TSP simétrico.** Costos $c_{ij}$ sobre $n$ nodos. Se relajan las restricciones de grado-2
con **potenciales de nodo** $\pi \in \mathbb{R}^n$. Costos modificados:
$$
c'_{ij} = c_{ij} + \pi_i + \pi_j .
$$
Para **cualquier** $\pi$, el costo de un **1-árbol mínimo** bajo $c'$ produce una cota
inferior (dualidad débil):
$$
L(\pi) = \Big(\text{costo del 1-árbol mínimo bajo } c'\Big) - 2\sum_{i} \pi_i \;\le\; \text{OPT}.
$$

> Un **1-árbol** es un árbol de expansión mínima sobre los nodos $\{2,\dots,n\}$ más las dos
> aristas más baratas incidentes al nodo $1$. Todo recorrido (*tour*) es un 1-árbol en el que
> cada nodo tiene grado 2; por eso el 1-árbol mínimo **acota por debajo** al *tour* óptimo.
> Su cálculo es **teoría de grafos pura** (un MST por Prim/Kruskal): sin licencias.

Se maximiza $L(\pi)$ por **ascenso de subgradiente**. Un subgradiente de $L$ en $\pi$ es
$$
\big(\nabla L\big)_i = d_i(\pi) - 2,
$$
donde $d_i(\pi)$ es el **grado** del nodo $i$ en el 1-árbol mínimo actual. Paso de Polyak:
$$
\pi \leftarrow \pi + t_k\,(d(\pi) - 2), \qquad
t_k = \lambda_k\,\frac{U_k - L(\pi)}{\lVert d(\pi)-2 \rVert^2},\quad \lambda_k \in (0,2],
$$
con $\lambda_k$ decreciente (p. ej. se reduce a la mitad tras varias iteraciones sin mejora).
Se mantiene la mejor cota vista:
$$
L_k = \max_{j \le k} L(\pi_j) \le \text{OPT}.
$$

> La cota $L_k$ converge a la **cota de Held–Karp**, que en la práctica está típicamente a
> ~1 % del óptimo del TSP. Y, repito, **la calcula el propio algoritmo**.

---

## 4. La pieza nueva: enfriamiento guiado por la brecha (preserva Hajek)

Definimos la **brecha certificada relativa** en la iteración $k$:
$$
g_k = \frac{U_k - L_k}{\max(\lvert L_k\rvert,\ \epsilon_0)} \in [0, \infty),
\qquad g_k \text{ es no creciente (las cotas sólo mejoran).}
$$

Y su versión **normalizada** respecto a la brecha inicial $g_0$:
$$
\hat g_k = \min\!\Big\{\frac{g_k}{g_0},\ 1\Big\} \in [0, 1].
$$

El programa de enfriamiento de CASS es:
$$
\boxed{\,T_k = \dfrac{c\,\big(1 + \beta\, \hat g_k\big)}{\log(k+2)}\,}, \qquad c \ge d^\*,\ \ \beta \ge 0 .
$$

Interpretación **sin metáfora**: el factor $1+\beta \hat g_k$ **infla la constante de
enfriamiento cuando aún queda fracción grande de la brecha inicial** (mucho por ganar ⇒ más
exploración) y la relaja a $c$ cuando la brecha se cierra (cerca del óptimo certificado ⇒
intensificar). El factor $1/\log(k+2)$ garantiza el enfriamiento asintótico.

> **¿Por qué normalizar?** Usar la brecha *cruda* $g_k$ es un error de diseño: al inicio
> $g_0$ puede ser de cientos de por ciento (en la instancia de prueba, ~300 %), de modo que
> $1+\beta g_k$ dispara la temperatura, el primal nunca intensifica, la brecha no baja y el
> sistema **se sabotea a sí mismo** en un lazo. La normalización $\hat g_k\in[0,1]$ confina el
> factor de inflación al intervalo **acotado** $[1,\,1+\beta]$ y elimina ese lazo. (Esto se
> descubrió ejecutando la implementación de referencia: ver el registro de diseño en §7.1.)

### 4.1 Teorema (convergencia en probabilidad al óptimo)

**Hipótesis.** $N$ simétrica e irreducible; $c \ge d^\*$, donde $d^\*$ es la **profundidad
crítica** (la máxima profundidad de un mínimo local no global, en el sentido de Hajek);
$\beta \ge 0$. (La señal de enfriamiento $\hat g_k$ está acotada en $[0,1]$ **por
construcción**, sin necesidad de hipótesis adicional.)

**Tesis.** $\displaystyle \lim_{k\to\infty} \Pr\big[x_k \in S^\*\big] = 1$, donde $S^\*$ es el
conjunto de óptimos globales.

**Demostración (esquema).** Por el teorema de Hajek (1988), un recocido con programa
$T_k \downarrow 0$ converge al conjunto de mínimos globales **si y sólo si**
$$
\sum_{k=0}^{\infty} \exp\!\big(-d^\*/T_k\big) = \infty .
$$
Basta verificar las dos condiciones:

1. **$T_k \to 0$.** Como $0 \le \hat g_k \le 1$, se tiene $c \le c(1+\beta \hat g_k) \le c(1+\beta)$,
   un factor **acotado**; dividido por $\log(k+2)\to\infty$ da $T_k \to 0$. ✔

2. **Divergencia de la suma.** Por construcción $T_k \ge \dfrac{c}{\log(k+2)}$ (pues $\hat g_k\ge 0$).
   Con $c \ge d^\*$:
   $$
   \exp\!\Big(\!-\frac{d^\*}{T_k}\Big) \;\ge\; \exp\!\Big(\!-\frac{d^\*\log(k+2)}{c}\Big)
   = (k+2)^{-d^\*/c} \;\ge\; (k+2)^{-1},
   $$
   y $\sum_k (k+2)^{-1} = \infty$. Por tanto la suma diverge. ✔

Como **ambas** condiciones de Hajek se satisfacen **para todo** comportamiento admisible de
$\hat g_k$, la adaptación guiada por la brecha **no puede romper la convergencia**: la garantía
es *invariante* a la adaptación. $\qquad\blacksquare$

> **Esta es la idea de diseño central.** En la literatura, "adaptar la temperatura con
> información del estado" suele **destruir** las pruebas de convergencia. Aquí la adaptación
> se confina, por construcción, dentro de la *envolvente admisible de Hajek*
> $\big[\frac{c}{\log(k+2)},\ \frac{c(1+\beta)}{\log(k+2)}\big]$, de modo que **el teorema
> sigue valiendo sin cambios**. Ganamos adaptatividad **sin sacrificar el rigor**.

### 4.2 Cota de tiempo (drift) para la instancia de juguete

Para mostrar que aportamos también análisis de complejidad —no sólo convergencia
asintótica— se incluye un resultado tipo *runtime analysis*. Sobre el problema unimodal
de referencia OneMax con vecindad de 1-*flip* y $\beta=0$ (CASS se reduce a recocido), el
análisis de deriva multiplicativa da un tiempo esperado de golpe
$\mathbb{E}[T_{\text{hit}}] = O(n\log n)$, coincidente con el conocido para el `(1+1)`-EA
(Droste, Jansen & Wegener, 2002). *(La verificación empírica de esta tasa está pendiente; se
añadirá como `examples/cass_drift.py`.)*

---

## 5. Comportamiento *anytime* y criterio de paro certificado

En **cualquier** iteración $k$, CASS puede detenerse y devolver:

- la mejor solución $x_k^{\text{best}}$ con valor $U_k$;
- una **cota inferior válida** $L_k$;
- un **certificado**: $\;f(x_k^{\text{best}}) \le (1 + g_k)\,\text{OPT}$ cuando $L_k>0$,
  es decir, la solución está **demostrablemente** dentro de un factor $g_k$ del óptimo.

**Regla de paro $\varepsilon$-certificada.** Detenerse cuando $g_k \le \varepsilon$. Entonces
la solución devuelta es $\varepsilon$-óptima **con certificado**, algo que **ninguna
metaheurística basada en metáforas ofrece**. (Si $g_k$ no baja de $\varepsilon$, se reporta
honestamente el mejor $g_k$ alcanzado: rigor también en el "no sé".)

---

## 6. Cómo CASS responde a cada crítica

| Crítica al área (cf. §1) | Respuesta de CASS |
|---|---|
| **Metáfora-manía** | Cero metáforas. Definido con cadenas de Markov, relajación lagrangiana y teoría de grafos. §1 atribuye cada pieza. |
| **Sin garantías teóricas** | Teorema de convergencia (§4.1) + cota de tiempo (§4.2) + **certificado de optimalidad anytime** (§5). |
| **Rigor experimental débil** | Protocolo preregistrado (§7): *benchmarks* públicos, calibración justa con `irace`, tests estadísticos, ablación, semillas y código abierto. |
| **No Free Lunch mal usado** | No se afirma superioridad universal. Se declara la **clase** (problemas con relajación lagrangiana que produzca buena cota) y *por qué* funciona allí. |
| **Ingeniería disfrazada de ciencia** | Estudio de **ablación** obligatorio: medir la contribución real del acoplamiento primal–dual ($\beta=0$ vs $\beta>0$) frente a *baselines* fuertes (ILS, recocido puro). |

---

## 7. Protocolo experimental (preregistrado)

Para no caer en el "rigor débil", el plan de validación se fija **antes** de correr nada:

1. **Instancias**: TSPLIB (subconjunto público estándar); reportar *todas*, no sólo las favorables.
2. ***Baselines* fuertes**: recocido simulado puro, 2-opt multiarranque, *Iterated Local Search* (ILS).
   No basta superar a un algoritmo débil.
3. **Presupuesto justo**: mismo número de evaluaciones de $f$ para todos (no "mismo tiempo en mi PC").
4. **Calibración imparcial**: parámetros de *todos* los métodos ajustados con el mismo
   procedimiento automático (`irace`/SMAC) sobre instancias de entrenamiento disjuntas.
5. **Estadística**: $\ge 30$ corridas con semillas registradas; test de Wilcoxon (pareado) y
   Friedman + post-hoc para comparaciones múltiples; reportar tamaños de efecto, no sólo $p$.
6. **Ablación**: $\beta=0$ (sin guía dual) vs $\beta>0$; con y sin certificado de paro.
   Aísla la contribución de la pieza nueva (§4).
7. **Reproducibilidad**: código abierto, semillas, instancias y *scripts* publicados.
   La métrica estrella es **el factor de aproximación certificado $g_k$**, no sólo el valor medio.

---

### 7.1 Registro de diseño y resultado preliminar (honesto)

La implementación de referencia ([`examples/cass_tsp.py`](../examples/cass_tsp.py)) y la
ablación ([`examples/cass_ablation.py`](../examples/cass_ablation.py)) ya revelaron dos
cosas que **se reportan en vez de ocultarse**:

1. **Hubo que corregir el enfriamiento.** La versión inicial con brecha *cruda* se saboteaba
   (lazo de temperatura alta descrito en §4). La normalización $\hat g_k$ lo resolvió. El
   *bug* y su corrección quedan documentados como parte del método científico, no borrados.

2. **El certificado es la contribución robusta; el acoplamiento $\beta>0$ es hipótesis
   abierta.** En 15 corridas sobre una instancia euclidiana $n=30$:
   - El **certificado de optimalidad** (cota inferior propia + brecha válida) se emitió en
     **todas** las corridas, con $\beta=0$ y con $\beta=1$. Esa parte es sólida.
   - El **beneficio de $\beta>0$ fue mixto**: mejoró la brecha en sólo **5/15** corridas, con
     mediana ligeramente peor y un caso claramente peor. **No** se reclama superioridad del
     acoplamiento: queda como hipótesis a evaluar con el protocolo completo (más instancias,
     calibración de $\beta$, tests estadísticos).

   > Reportar un resultado *mixto* en lugar de elegir la instancia/semilla favorable es,
   > precisamente, lo contrario de la mala práctica que critica Sörensen. La aportación que
   > **sí** se sostiene es la **auto-certificación anytime**.

---

## 8. Limitaciones (declaradas)

- La calidad del **certificado** depende de que la relajación dual sea ajustada. Donde no
  exista una buena relajación lagrangiana, CASS sigue convergiendo (proceso primal), pero el
  certificado $g_k$ puede ser flojo. Esto se reporta, no se oculta.
- La convergencia del §4.1 es **asintótica**; en presupuesto finito CASS es una heurística
  —pero, a diferencia de las demás, **una que dice cuán lejos puede estar del óptimo.**
- $d^\*$ (profundidad crítica) raramente se conoce; en la práctica se usa $c$ como
  hiperparámetro calibrado, y la garantía se interpreta como "existe $c$ finito que la activa".

---

## 9. Pseudocódigo

```
Entrada: f, N (vecindad), proceso dual D (subgradiente lagrangiano), c, β, ε
x ← solución inicial factible;  U ← f(x);  x_best ← x
π ← 0;  L ← D.cota_inicial()
para k = 0, 1, 2, ... :
    # --- DUAL: una iteración de subgradiente (cota inferior válida) ---
    (Lπ, grad) ← D.evaluar(π)                 # 1-árbol mínimo + subgradiente
    L ← max(L, Lπ)
    π ← π + paso_polyak(U, Lπ, grad)
    # --- brecha certificada y temperatura (preserva Hajek) ---
    g ← (U − L) / max(|L|, ε0)
    T ← c·(1 + β·g) / log(k+2)
    # --- PRIMAL: paso Metropolis ---
    y ← propuesta_uniforme(N(x))
    si aceptar(f(y) − f(x), T):  x ← y
    si f(x) < U:  U ← f(x);  x_best ← x
    # --- paro certificado ---
    si g ≤ ε:  devolver (x_best, U, L, g)   # solución ε-óptima CON certificado
devolver (x_best, U, L, g)                  # anytime: certificado en todo momento
```

---

## 10. Referencias

- Hajek, B. (1988). *Cooling schedules for optimal annealing.* Mathematics of Operations Research, 13(2), 311–329.
- Geman, S., & Geman, D. (1984). *Stochastic relaxation, Gibbs distributions, and the Bayesian restoration of images.* IEEE TPAMI.
- Held, M., & Karp, R. M. (1970, 1971). *The traveling-salesman problem and minimum spanning trees, I & II.* Operations Research / Mathematical Programming.
- Sörensen, K. (2015). *Metaheuristics—the metaphor exposed.* International Transactions in Operational Research, 22(1), 3–18.
- Droste, S., Jansen, T., & Wegener, I. (2002). *On the analysis of the (1+1) evolutionary algorithm.* Theoretical Computer Science, 276(1–2), 51–81.
- Wolpert, D. H., & Macready, W. G. (1997). *No free lunch theorems for optimization.* IEEE TEC.

---

*Documento de diseño v0.1 — borrador inicial. La implementación de referencia
auto-contenida (sin solver comercial) está en [`examples/cass_tsp.py`](../examples/cass_tsp.py).*
