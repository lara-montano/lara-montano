# 🧭 Posts de Ruta de Ciencia — hechos en LaTeX

Sistema para producir los carruseles de Instagram de **Ruta de Ciencia**
(*ciencia con sentido crítico*) de forma **100% en LaTeX**, con un estilo de
marca consistente. Cada post se compila a un PDF y se exporta a imágenes
**1080 × 1350 px** (formato vertical 4:5 de Instagram), listas para subir.

---

## 📁 Estructura

```
posts/
├── ruta-de-ciencia.sty              ← el TEMA de marca (colores, fuente, láminas)
├── post-01-cerebro-10-porciento.tex ← contenido del post #1
├── post-01-cerebro-10-porciento.caption.md  ← caption + hashtags para IG
├── build.sh                         ← compila y exporta a PNG
├── .gitignore
└── export/                          ← salida lista para Instagram (PDF + PNG)
    ├── post-01-cerebro-10-porciento.pdf
    └── post-01-cerebro-10-porciento/
        ├── slide-1.png … slide-8.png
```

La idea clave: **el estilo vive en `ruta-de-ciencia.sty`**. Cada post nuevo solo
escribe *contenido*; nunca vuelves a diseñar desde cero.

---

## ⚙️ Requisitos (una sola vez)

- **TeX Live** con `pdflatex` y los paquetes `beamer`, `tikz`, `montserrat`,
  `fontawesome5`.
- **poppler-utils** (para `pdftoppm`, que exporta a PNG).

En Debian/Ubuntu:
```bash
sudo apt-get install texlive-latex-recommended texlive-latex-extra \
  texlive-pictures texlive-fonts-extra poppler-utils
```

> Se compila con **pdfLaTeX** (no xelatex).

---

## ▶️ Compilar y exportar

```bash
./build.sh post-01-cerebro-10-porciento   # un post
./build.sh                                 # todos los post-*.tex
```

Esto genera `export/<post>/slide-1.png … slide-N.png` a 1080×1350 px.
Súbelas a Instagram **en orden** y pega el texto de `*.caption.md`.

---

## ✍️ Crear un post nuevo (plantilla)

1. Copia un post existente:
   ```bash
   cp post-01-cerebro-10-porciento.tex post-02-mi-tema.tex
   ```
2. Cambia el contenido usando las tres láminas disponibles (abajo).
3. Compila: `./build.sh post-02-mi-tema`
4. Escribe su caption en `post-02-mi-tema.caption.md`.

### Las 3 láminas del tema

```latex
% --- PORTADA ---
% \rdccover{SELLO}{TÍTULO (usa \\ para saltos)}{subtítulo}
\rdccover{MITO}{``Tu titular\\ aquí''}{Frase de enganche.}

% --- CONTENIDO (repite las que necesites) ---
% \rdccontent{núm}{\faIcono}{ETIQUETA}{TITULAR}{cuerpo}
\rdccontent{2}{\faBrain}{LA EVIDENCIA}{Un titular corto}{Texto del cuerpo.}

% --- CIERRE / VEREDICTO ---
% \rdcclosing{núm}{VEREDICTO}{cuerpo}{fuente}
\rdcclosing{8}{El veredicto claro.}{Frase de cierre.}{Fuentes: …}
```

### Metadatos por post (arriba del `.tex`)

```latex
\renewcommand{\rdchandle}{@rutadeciencia}      % tu handle real
\renewcommand{\rdccategory}{MITO vs.\ EVIDENCIA} % etiqueta superior
\renewcommand{\rdctotalslides}{8}               % nº total de láminas
```

Para cambiar el color de acento de la categoría (p. ej. otro pilar):
```latex
\renewcommand{\rdcaccent}{rdcamber}   % rdccyan · rdcred · rdcamber
```

---

## 🎨 Marca (definida en `ruta-de-ciencia.sty`)

| Elemento | Valor |
|---|---|
| Fondo | Azul noche `#0C1B2A` |
| Acento / marca | Cian `#2DD4BF` |
| Mito / alerta | Coral `#FF6B6B` |
| Resaltado | Ámbar `#FFC857` |
| Tipografía | Montserrat (Black para titulares) |
| Lienzo | 1080 × 1350 px (4:5) |

Iconos: cualquiera de **Font Awesome 5** con `\fa...`
(p. ej. `\faBrain`, `\faBolt`, `\faFlask`, `\faSearch`, `\faQuoteRight`).
Catálogo: https://fontawesome.com/v5/search?o=r&m=free

---

## ✅ Checklist antes de publicar
- [ ] El titular de la portada engancha en 2 segundos.
- [ ] Cada afirmación fuerte tiene su fuente en la última lámina.
- [ ] El caption (`*.caption.md`) está actualizado con hashtags.
- [ ] `@handle` correcto en el `.tex`.
- [ ] Subir las láminas **en orden**.
