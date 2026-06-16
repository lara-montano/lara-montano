"""
CASS — Certified Anytime Stochastic Search (instancia: TSP simétrico)
====================================================================

Implementacion de referencia, auto-contenida y SIN solver comercial.

Acopla dos procesos (ver docs/CASS-busqueda-estocastica-anytime-certificada.md):

  * PRIMAL: busqueda local estocastica tipo Metropolis con movimientos 2-opt.
  * DUAL  : cota inferior de Held-Karp (1-arbol) calculada por nosotros mismos
            mediante ascenso de subgradiente sobre potenciales de nodo.

La brecha certificada g_k = (U_k - L_k)/|L_k| (i) guia un enfriamiento que
PRESERVA la condicion de convergencia de Hajek por construccion, y (ii) da un
certificado de optimalidad en todo momento: el tour devuelto es <= (1+g_k)*OPT.

Dependencias: numpy.   Uso:  python examples/cass_tsp.py
"""

from __future__ import annotations
import numpy as np


# --------------------------------------------------------------------------- #
#  PROCESO DUAL: cota inferior de Held-Karp via 1-arbol minimo (teoria de      #
#  grafos pura; ningun solver externo).                                        #
# --------------------------------------------------------------------------- #
def min_one_tree(C: np.ndarray):
    """1-arbol minimo bajo la matriz de costos C (simetrica, diagonal +inf).

    Devuelve (costo, grados): el costo del 1-arbol y el vector de grados de
    cada nodo. Un 1-arbol = MST sobre los nodos {1..n-1} + las dos aristas mas
    baratas incidentes al nodo 0. Todo tour es un 1-arbol con todos los grados
    iguales a 2, por lo que el 1-arbol minimo acota por debajo al tour optimo.
    """
    n = C.shape[0]
    deg = np.zeros(n)

    # --- MST sobre {1,...,n-1} por Prim O(n^2) ---
    nodes = np.arange(1, n)
    in_tree = np.zeros(n, dtype=bool)
    in_tree[1] = True
    # mejor arista de conexion al arbol para cada nodo restante
    best_cost = C[1, :].copy()
    best_from = np.full(n, 1)
    mst_cost = 0.0
    for _ in range(len(nodes) - 1):
        # elegir el nodo fuera del arbol (en {1..n-1}) mas barato de conectar
        cand = [j for j in nodes if not in_tree[j]]
        j = min(cand, key=lambda v: best_cost[v])
        in_tree[j] = True
        mst_cost += best_cost[j]
        deg[j] += 1
        deg[best_from[j]] += 1
        for v in nodes:
            if not in_tree[v] and C[j, v] < best_cost[v]:
                best_cost[v] = C[j, v]
                best_from[v] = j

    # --- conectar el nodo 0 con sus dos aristas mas baratas ---
    edges0 = C[0, 1:]
    order = np.argsort(edges0)
    a, b = order[0] + 1, order[1] + 1
    one_tree_cost = mst_cost + edges0[order[0]] + edges0[order[1]]
    deg[0] += 2
    deg[a] += 1
    deg[b] += 1
    return one_tree_cost, deg


class HeldKarpDual:
    """Cota inferior de Held-Karp por subgradiente sobre potenciales de nodo."""

    def __init__(self, dist: np.ndarray):
        self.dist = dist
        self.n = dist.shape[0]
        self.pi = np.zeros(self.n)
        self.lam = 1.0          # factor de Polyak, se reduce ante estancamiento
        self.best_L = -np.inf
        self._stall = 0

    def step(self, U: float) -> float:
        """Una iteracion de subgradiente. Devuelve la mejor cota inferior vista."""
        # costos modificados c'_ij = c_ij + pi_i + pi_j
        Cp = self.dist + self.pi[:, None] + self.pi[None, :]
        np.fill_diagonal(Cp, np.inf)
        cost, deg = min_one_tree(Cp)
        L = cost - 2.0 * self.pi.sum()           # L(pi) <= OPT  (dualidad debil)

        if L > self.best_L + 1e-9:
            self.best_L = L
            self._stall = 0
        else:
            self._stall += 1
            if self._stall >= 20:                # reducir paso ante estancamiento
                self.lam *= 0.5
                self._stall = 0

        # subgradiente g_i = deg_i - 2 ; paso de Polyak con objetivo U
        g = deg - 2.0
        gnorm2 = float(g @ g)
        if gnorm2 > 0 and np.isfinite(U):
            t = self.lam * max(U - L, 1e-9) / gnorm2
            self.pi = self.pi + t * g
        return self.best_L


# --------------------------------------------------------------------------- #
#  PROCESO PRIMAL: busqueda local estocastica (Metropolis) con 2-opt.          #
# --------------------------------------------------------------------------- #
def tour_length(tour: np.ndarray, dist: np.ndarray) -> float:
    return float(dist[tour, np.roll(tour, -1)].sum())


def two_opt_delta(tour, dist, i, j):
    """Cambio de longitud al invertir el segmento tour[i+1..j] (0<=i<j<=n-1)."""
    n = len(tour)
    a, b = tour[i], tour[(i + 1) % n]
    c, d = tour[j], tour[(j + 1) % n]
    return (dist[a, c] + dist[b, d]) - (dist[a, b] + dist[c, d])


# --------------------------------------------------------------------------- #
#  CASS: acoplamiento primal-dual + enfriamiento guiado por la brecha.         #
# --------------------------------------------------------------------------- #
def cass_tsp(dist: np.ndarray, c: float = 0.1, beta: float = 1.0,
             eps: float = 0.01, max_iter: int = 20000, seed: int = 0,
             eps0: float = 1e-9, verbose: bool = True):
    """Resuelve un TSP simetrico con CASS.

    Parametros
    ----------
    c     : constante de enfriamiento (>= profundidad critica para la garantia).
    beta  : intensidad del acoplamiento dual (beta=0  => recocido puro; ablacion).
    eps   : tolerancia del certificado de paro (g_k <= eps  =>  eps-optimo).
    Devuelve dict con tour, longitud (U), cota inferior (L) y brecha g.

    Nota de diseno: el enfriamiento usa la brecha NORMALIZADA  ghat = g/g0 in [0,1]
    (fraccion de la brecha inicial que aun queda). Asi el factor de inflacion vive
    en el intervalo ACOTADO [1, 1+beta], lo que (i) evita el lazo auto-saboteador
    que produce la brecha cruda al inicio (g0 puede ser de cientos de %) y (ii)
    deja la temperatura dentro de la envolvente admisible de Hajek
    [c/log(k+2), c(1+beta)/log(k+2)], preservando la prueba de convergencia.
    """
    rng = np.random.default_rng(seed)
    n = dist.shape[0]

    tour = rng.permutation(n)
    U = tour_length(tour, dist)
    best_tour, best_U = tour.copy(), U

    dual = HeldKarpDual(dist)
    L = dual.step(best_U)
    g0 = max((best_U - L) / max(abs(L), eps0), eps0)   # brecha inicial (referencia)

    for k in range(max_iter):
        # --- DUAL: una iteracion de subgradiente (cota inferior valida) ---
        L = dual.step(best_U)

        # --- brecha certificada y temperatura (envolvente admisible de Hajek) ---
        g = max((best_U - L) / max(abs(L), eps0), 0.0)
        ghat = min(g / g0, 1.0)                          # brecha normalizada in [0,1]
        T = c * (1.0 + beta * ghat) / np.log(k + 2)

        # --- PRIMAL: un paso Metropolis con movimiento 2-opt ---
        i, j = sorted(rng.integers(0, n, size=2))
        if j - i >= 1 and not (i == 0 and j == n - 1):
            delta = two_opt_delta(tour, dist, i, j)
            if delta <= 0 or rng.random() < np.exp(-delta / T):
                tour[i + 1:j + 1] = tour[i + 1:j + 1][::-1]
                U = U + delta
                if U < best_U:
                    best_U, best_tour = U, tour.copy()

        # --- paro certificado ---
        if g <= eps:
            if verbose:
                print(f"[k={k}] PARO CERTIFICADO: g={g:.4%} <= eps={eps:.2%}")
            break

        if verbose and k % 2000 == 0:
            print(f"[k={k:6d}] U={best_U:10.3f}  L={L:10.3f}  "
                  f"gap_certificada={g:7.3%}  T={T:.4f}")

    g = (best_U - L) / max(abs(L), eps0)
    return {"tour": best_tour, "U": best_U, "L": L, "gap": max(g, 0.0), "iters": k}


# --------------------------------------------------------------------------- #
#  Demo reproducible: instancia euclidiana aleatoria.                          #
# --------------------------------------------------------------------------- #
def _euclidean_instance(n: int, seed: int = 1):
    rng = np.random.default_rng(seed)
    pts = rng.random((n, 2))
    D = np.sqrt(((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1))
    np.fill_diagonal(D, np.inf)
    return D


if __name__ == "__main__":
    D = _euclidean_instance(n=30, seed=1)
    print("=== CASS (acoplado, beta=1) ===")
    res = cass_tsp(D, c=0.1, beta=1.0, eps=0.02, max_iter=40000, seed=0)
    print(f"\nResultado CASS:")
    print(f"  Longitud (U)        : {res['U']:.4f}")
    print(f"  Cota inferior (L)   : {res['L']:.4f}   <-- calculada por nosotros")
    print(f"  Brecha certificada  : {res['gap']:.3%}")
    print(f"  Garantia            : tour <= (1 + {res['gap']:.4f}) * OPT")
    print(f"  Iteraciones         : {res['iters']}")
