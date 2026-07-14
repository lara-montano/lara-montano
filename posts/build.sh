#!/usr/bin/env bash
# =====================================================================
#  build.sh — Compila un post de "Ruta de Ciencia" y exporta las
#  láminas como PNG de 1080x1350 px, listas para subir a Instagram.
#
#  Uso:
#     ./build.sh post-01-cerebro-10-porciento
#     ./build.sh                 # compila todos los post-*.tex
#
#  Requisitos: pdflatex (TeX Live) y pdftoppm (poppler-utils).
# =====================================================================
set -euo pipefail
cd "$(dirname "$0")"

build_one() {
  local post="${1%.tex}"
  echo "▶ Compilando $post ..."
  pdflatex -interaction=nonstopmode -halt-on-error "$post.tex" >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error "$post.tex" >/dev/null
  mkdir -p "export/$post"
  cp "$post.pdf" "export/$post.pdf"
  pdftoppm -scale-to-x 1080 -scale-to-y -1 -png "$post.pdf" "export/$post/slide" >/dev/null
  rm -f "$post".aux "$post".log "$post".nav "$post".snm "$post".toc "$post".out
  echo "  ✔ export/$post/slide-*.png  ($(ls export/"$post"/slide-*.png | wc -l | tr -d ' ') láminas)"
}

if [[ $# -ge 1 ]]; then
  build_one "$1"
else
  for f in post-*.tex; do build_one "$f"; done
fi
echo "Listo."
