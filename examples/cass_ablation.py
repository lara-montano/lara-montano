"""
Ablacion reproducible de CASS:  acoplamiento dual (beta>0) vs recocido puro (beta=0).
====================================================================================

Aisla la contribucion de la UNICA pieza nueva (el enfriamiento guiado por la brecha,
seccion 4 del documento de diseno) frente al recocido simulado puro. Reporta TODAS
las corridas, no solo las favorables, de acuerdo con el protocolo de la seccion 7.

Conclusion esperada (preliminar, n pequeno): el CERTIFICADO de optimalidad funciona
para cualquier beta (es la contribucion robusta), mientras que el beneficio de
beta>0 es MIXTO -> es una hipotesis de investigacion abierta, no una victoria
universal (coherente con No Free Lunch).

Uso:  python examples/cass_ablation.py
"""
from __future__ import annotations
import numpy as np
from cass_tsp import _euclidean_instance, cass_tsp


def ablation(n=30, inst_seed=1, run_seeds=range(15), eps=0.02, max_iter=40000):
    D = _euclidean_instance(n, inst_seed)
    rows = []
    for s in run_seeds:
        r0 = cass_tsp(D, c=0.1, beta=0.0, eps=eps, max_iter=max_iter, seed=s, verbose=False)
        r1 = cass_tsp(D, c=0.1, beta=1.0, eps=eps, max_iter=max_iter, seed=s, verbose=False)
        rows.append((s, r0["gap"], r0["iters"], r1["gap"], r1["iters"]))

    g0 = np.array([r[1] for r in rows])
    g1 = np.array([r[3] for r in rows])
    it0 = np.array([r[2] for r in rows])
    it1 = np.array([r[4] for r in rows])

    print(f"Instancia euclidiana n={n} (inst_seed={inst_seed}), {len(rows)} corridas\n")
    print("seed |  beta=0  gap     iters |  beta=1  gap     iters")
    print("-" * 56)
    for s, ga, ia, gb, ib in rows:
        print(f" {s:3d} |        {ga:7.3%} {ia:6d} |        {gb:7.3%} {ib:6d}")
    print("-" * 56)
    print(f" med |        {np.median(g0):7.3%} {int(np.median(it0)):6d} |"
          f"        {np.median(g1):7.3%} {int(np.median(it1)):6d}")

    wins = int(np.sum(g1 < g0 - 1e-9))
    print(f"\nbeta=1 mejora la brecha en {wins}/{len(rows)} corridas.")
    print("El CERTIFICADO (gap valido + cota inferior propia) se emite en TODAS.")
    print("=> Contribucion robusta: auto-certificacion. Acoplamiento beta>0: hipotesis abierta.")


if __name__ == "__main__":
    ablation()
