# Plan completo para aprender optimización (teoría + práctica)

**Perfil destino:** nivel intermedio (cálculo, álgebra lineal y Python sólidos).
**Tiempo:** 3–5 h/semana durante ~10 meses (~40 semanas, ~160 h totales).
**Objetivo:** investigación académica con proyección a aplicaciones reales, cubriendo optimización continua, convexa, no lineal, combinatoria, metaheurísticas, estocástica y **robusta**.

Cada fase incluye: (i) núcleo teórico, (ii) lecturas/cursos, (iii) práctica con código, (iv) entregable. Los entregables forman un portafolio reutilizable para papers o tesis.

---

## Mapa general

| Fase | Semanas | Horas | Tema |
|------|---------|-------|------|
| 0 | 1–2 | 8 | Preparación matemática y del entorno |
| 1 | 3–8 | 25 | Optimización convexa y LP |
| 2 | 9–14 | 25 | Optimización no lineal (NLP) sin y con restricciones |
| 3 | 15–20 | 25 | Optimización entera y combinatoria (MILP/MINLP) |
| 4 | 21–26 | 25 | Metaheurísticas y optimización global |
| 5 | 27–30 | 15 | Optimización para ML/DL y bayesiana |
| 6 | 31–35 | 20 | Optimización bajo incertidumbre: estocástica y **robusta** |
| 7 | 36–40 | 20 | Proyecto capstone + difusión |

---

## Fase 0 — Preparación (semanas 1–2)

**Objetivos.** Refrescar bases matemáticas y dejar el entorno listo.

**Teoría (revisión rápida).**
- Álgebra lineal: subespacios, proyecciones, SVD, condicionamiento.
- Cálculo multivariable: gradiente, Hessiano, serie de Taylor, regla de la cadena.
- Análisis básico: continuidad, diferenciabilidad, teorema de Weierstrass.
- Probabilidad: esperanza, varianza, desigualdades (Markov, Chebyshev, Jensen).

**Recursos.**
- Strang, *Linear Algebra and Learning from Data* (cap. 1–4).
- 3Blue1Brown — Essence of Linear Algebra / Calculus (repaso visual).

**Entorno técnico.**
- Python: `numpy`, `scipy.optimize`, `cvxpy`, `pyomo`, `networkx`, `matplotlib`.
- Solvers: HiGHS (open), IPOPT, Bonmin, SCIP; GLPK; opcional Gurobi/CPLEX académico.
- Julia (opcional, recomendado para investigación): `JuMP.jl`, `Convex.jl`, `Optim.jl`.
- Git + reproducibilidad: `uv`/`poetry`, notebooks versionados con `jupytext`.

**Entregable.** Repo plantilla con solvers funcionando y un "hello world" que resuelva un LP y un NLP pequeño.

---

## Fase 1 — Optimización convexa y programación lineal (semanas 3–8)

**Núcleo teórico.**
- Conjuntos y funciones convexas; epígrafo; operaciones que preservan convexidad.
- LP: forma estándar, vértices, dualidad, simplex, método de punto interior.
- Dualidad Lagrangiana, condiciones KKT, slater, sensibilidad.
- Problemas canónicos: LP, QP, SOCP, SDP; geometría.

**Lectura principal.**
- Boyd & Vandenberghe, *Convex Optimization* (caps. 1–5, 9). Gratuito online.
- Curso Stanford EE364a (videos + problem sets).

**Práctica.**
- Implementar simplex revisado y gradiente proyectado en NumPy.
- Modelar con CVXPY: LP de dieta, portafolio Markowitz, SVM dual, Chebyshev center.
- Verificar KKT a mano y comparar con el solver.

**Entregable.** Notebook comparando solver propio vs HiGHS en 3 LPs y 2 QPs, con análisis de sensibilidad del dual.

---

## Fase 2 — Optimización no lineal (semanas 9–14)

**Núcleo teórico.**
- Métodos de descenso: gradiente, Newton, cuasi-Newton (BFGS, L-BFGS), gradiente conjugado.
- Búsqueda de línea (Wolfe) y regiones de confianza.
- Restricciones: penalización, barrera, Lagrangiano aumentado, SQP, punto interior primal-dual.
- Teoría de convergencia: tasas lineal/superlineal/cuadrática.

**Lectura principal.**
- Nocedal & Wright, *Numerical Optimization* (caps. 2–6, 10–12, 15, 17–19).
- Bertsekas, *Nonlinear Programming* (complemento).

**Práctica.**
- Implementar BFGS y Lagrangiano aumentado desde cero; comparar con `scipy.optimize`.
- Resolver problemas clásicos: Rosenbrock, Himmelblau, benchmark CUTEst.
- Modelar NLP de ingeniería (diseño de intercambiador, reactor) en Pyomo + IPOPT.

**Entregable.** Reporte corto (4–6 pp.) comparando BFGS vs L-BFGS vs SQP en un NLP aplicado, con curvas de convergencia.

---

## Fase 3 — Optimización entera y combinatoria (semanas 15–20)

**Núcleo teórico.**
- MILP: formulación, relajación LP, branch-and-bound, cutting planes (Gomory), branch-and-cut.
- Big-M y disjunctive programming; formulaciones fuertes vs débiles.
- MINLP: outer approximation, GBD, branch-and-bound espacial (BARON, Couenne).
- Grafos y flujos: caminos mínimos, flujo máximo, matching, TSP, VRP.
- Complejidad: P, NP, aproximaciones.

**Lectura principal.**
- Wolsey, *Integer Programming* (2e).
- Conforti, Cornuéjols, Zambelli, *Integer Programming*.
- Floudas, *Nonlinear and Mixed-Integer Optimization* (para MINLP).

**Práctica.**
- Resolver TSP y VRP pequeños en Pyomo/JuMP con HiGHS/SCIP.
- Scheduling de unidades de proceso (ejemplo aplicable a ingeniería química).
- Implementar branch-and-bound propio para knapsack binario.

**Entregable.** Caso MINLP real (e.g., síntesis de red de intercambiadores) modelado y resuelto, discutiendo formulaciones alternativas.

---

## Fase 4 — Metaheurísticas y optimización global (semanas 21–26)

**Núcleo teórico.**
- Familias: evolutivas (GA, DE, ES, CMA-ES), enjambre (PSO, ACO, SBOA), basadas en físicas (SA, GSA), Memetic.
- Exploración vs explotación; diversidad; convergencia prematura.
- Teorema No-Free-Lunch; benchmarking riguroso (CEC suites, BBOB/COCO).
- Manejo de restricciones: penalización, reparación, ε-constraint, estocástica.
- Multiobjetivo: Pareto, NSGA-II/III, MOEA/D, hipervolumen.

**Lectura principal.**
- Talbi, *Metaheuristics: From Design to Implementation*.
- Deb, *Multi-Objective Optimization using Evolutionary Algorithms*.
- Papers de referencia del área (incluidos trabajos sobre SBOA y benchmarking moderno).

**Práctica.**
- Implementar DE y PSO desde cero; reproducir un paper reciente de metaheurística.
- Usar `pymoo` para NSGA-II multiobjetivo.
- Benchmark estadísticamente riguroso: tests Friedman + Holm, perfiles de rendimiento.

**Entregable.** Estudio comparativo (estilo paper) de 3–4 metaheurísticas en una función de diseño realista con análisis estadístico.

---

## Fase 5 — Optimización para ML y bayesiana (semanas 27–30)

**Núcleo teórico.**
- SGD y variantes: momentum, Nesterov, AdaGrad, RMSProp, Adam, AdamW.
- Convergencia estocástica; varianza reducida (SVRG, SAGA).
- No convexa en deep learning: puntos de silla, sharpness, generalización.
- Optimización bayesiana: GP, funciones de adquisición (EI, UCB, TS).
- AutoML / HPO: Hyperband, BOHB, Optuna.

**Lectura principal.**
- Bottou, Curtis, Nocedal, *Optimization Methods for Large-Scale Machine Learning* (SIAM Review, 2018).
- Shahriari et al., *Taking the Human Out of the Loop* (BO tutorial).

**Práctica.**
- Implementar Adam y compararlo con SGD en un MLP pequeño (PyTorch).
- HPO con Optuna en un modelo aplicado (sustituto/surrogate de un simulador).

**Entregable.** Notebook que entrene una red neuronal sustituta para un proceso y use BO para ajustar hiperparámetros del proceso optimizado.

---

## Fase 6 — Optimización bajo incertidumbre: estocástica y robusta (semanas 31–35)

Eje central dado tu interés en RBDO y optimización robusta.

**Núcleo teórico.**
- Programación estocástica: two-stage, multi-stage, value of perfect information, VSS/EVPI.
- SAA (Sample Average Approximation); descomposición de Benders.
- Optimización robusta (Ben-Tal, Nemirovski): conjuntos de incertidumbre (box, elipsoidal, poliédrico, budget de Bertsimas–Sim); contrapartes robustas.
- Chance constraints y aproximaciones convexas (Nemirovski–Shapiro).
- Distributionally Robust Optimization (DRO): Wasserstein, momentos.
- RBDO: índice β, FORM/SORM, métodos de bucle anidado vs desacoplados (SORA, SLA).

**Lectura principal.**
- Ben-Tal, El Ghaoui, Nemirovski, *Robust Optimization*.
- Birge & Louveaux, *Introduction to Stochastic Programming*.
- Shapiro, Dentcheva, Ruszczyński, *Lectures on Stochastic Programming*.
- Du & Chen, papers seminales de SORA para RBDO.

**Práctica.**
- Resolver un LP robusto con incertidumbre elipsoidal en CVXPY (comparar con nominal).
- Two-stage stochastic program con Benders en Pyomo.
- RBDO de un componente mecánico/térmico con FORM + metaheurística.

**Entregable.** Estudio comparativo nominal vs estocástico vs robusto vs DRO en un mismo problema aplicado, discutiendo precio de robustez.

---

## Fase 7 — Proyecto capstone y difusión (semanas 36–40)

**Proyecto.** Elegir un problema de tu línea de investigación (p. ej. síntesis óptima de una red de intercambiadores bajo incertidumbre de propiedades, con modelo sustituto ANN y resolución híbrida metaheurística + NLP) y:
1. Formularlo como MINLP determinista.
2. Extenderlo con enfoque robusto o estocástico.
3. Resolverlo con al menos dos estrategias (determinista + metaheurística o híbrido).
4. Validar y analizar estadísticamente.

**Entregables.**
- Repositorio público, reproducible, con tests.
- Manuscrito corto (borrador de paper o capítulo de tesis).
- Charla/seminario de 30 min.

---

## Rutina semanal sugerida (3–5 h)

- **Día 1 (1 h):** lectura teórica activa, notas propias.
- **Día 2 (1 h):** ejercicios a lápiz (demostraciones, KKT, duales).
- **Día 3 (1–2 h):** programación: implementar o modelar.
- **Día 4 (0.5–1 h):** revisión y bitácora; preguntas abiertas para la siguiente semana.

Cada 4 semanas: mini-revisión y ajuste del plan.

---

## Stack recomendado por tema

| Tema | Herramientas |
|------|--------------|
| Modelado algebraico | Pyomo, JuMP, GAMS, AMPL |
| Convexa | CVXPY, Convex.jl, MOSEK |
| LP/MILP | HiGHS, SCIP, Gurobi, CPLEX |
| NLP | IPOPT, KNITRO, SNOPT |
| MINLP | Bonmin, Couenne, BARON, SHOT |
| Metaheurísticas | pymoo, DEAP, pyswarms, NiaPy |
| Estocástica | mpi-sppy, PySP (legacy), StochasticPrograms.jl |
| Robusta | ROmodel (Pyomo), JuMPeR (Julia) |
| ML/BO | PyTorch, JAX, Optuna, BoTorch, GPyOpt |
| RBDO | OpenTURNS, scikit-reliability |

---

## Libros de referencia (orden de prioridad)

1. Boyd & Vandenberghe — *Convex Optimization*.
2. Nocedal & Wright — *Numerical Optimization*.
3. Wolsey — *Integer Programming*.
4. Bertsimas & Tsitsiklis — *Introduction to Linear Optimization*.
5. Ben-Tal, El Ghaoui, Nemirovski — *Robust Optimization*.
6. Birge & Louveaux — *Introduction to Stochastic Programming*.
7. Talbi — *Metaheuristics*.
8. Floudas — *Deterministic Global Optimization*.

---

## Criterios de éxito

Al final del plan deberías poder:
- Reconocer y clasificar un problema (LP, QP, SOCP, MILP, MINLP, SP, RO, DRO).
- Formularlo en Pyomo/JuMP con la formulación más fuerte que conozcas.
- Elegir solver y método adecuados, justificando la decisión.
- Aplicar análisis de sensibilidad, dualidad y robustez.
- Diseñar experimentos computacionales estadísticamente defendibles.
- Escribir un manuscrito que incluya modelo, método, experimentos y discusión.
