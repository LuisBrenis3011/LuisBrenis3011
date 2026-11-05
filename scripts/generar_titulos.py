"""Genera los títulos SVG del perfil con una fuente de puntos de cinco por siete."""

from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

GLIFOS = {
    "A": "01110 10001 10001 11111 10001 10001 10001",
    "C": "01111 10000 10000 10000 10000 10000 01111",
    "D": "11110 10001 10001 10001 10001 10001 11110",
    "E": "11111 10000 10000 11110 10000 10000 11111",
    "H": "10001 10001 10001 11111 10001 10001 10001",
    "I": "11111 00100 00100 00100 00100 00100 11111",
    "L": "10000 10000 10000 10000 10000 10000 11111",
    "N": "10001 11001 10101 10011 10001 10001 10001",
    "O": "01110 10001 10001 10001 10001 10001 01110",
    "P": "11110 10001 10001 11110 10000 10000 10000",
    "Q": "01110 10001 10001 10001 10101 10010 01101",
    "R": "11110 10001 10001 11110 10100 10010 10001",
    "S": "01111 10000 10000 01110 00001 00001 11110",
    "T": "11111 00100 00100 00100 00100 00100 00100",
    "U": "10001 10001 10001 10001 10001 10001 01110",
    "B": "11110 10001 10001 11110 10001 10001 11110",
}
TITULOS = {
    "preliquidacion.svg": "Preliquidación por horas",
    "eats-hub.svg": "Eats Hub",
}
PASO = 7
MARGEN = 13


def puntos_por_columna(texto):
    columnas = defaultdict(list)
    cursor = 0
    for letra in texto.upper():
        if letra == " ":
            cursor += 3
            continue
        if letra == "Ó":
            columnas[cursor + 2].append(1)
            columnas[cursor + 3].append(0)
        matriz = GLIFOS["O" if letra == "Ó" else letra]
        for fila, celdas in enumerate(matriz.split(), start=2):
            for columna, celda in enumerate(celdas):
                if celda == "1":
                    columnas[cursor + columna].append(fila)
        cursor += 6
    return columnas


def generar_svg(texto):
    columnas = puntos_por_columna(texto)
    ancho = 2 * MARGEN + max(columnas) * PASO
    alto = 2 * MARGEN + 8 * PASO
    lineas = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}"',
        f'     viewBox="0 0 {ancho} {alto}" role="img" aria-labelledby="titulo">',
        f'  <title id="titulo">{escape(texto)}</title>',
        '  <style>',
        '    @media (prefers-reduced-motion: no-preference) {',
        '      .columna { animation: iluminar 480ms ease-out var(--espera) both; }',
        '      @keyframes iluminar { from { opacity: .45; } to { opacity: 1; } }',
        '    }',
        '  </style>',
        f'  <rect width="{ancho}" height="{alto}" rx="12" fill="#173c36"/>',
    ]
    for columna, filas in sorted(columnas.items()):
        x = MARGEN + columna * PASO
        lineas.append(f'  <g class="columna" fill="#efaa8e" style="--espera:{columna * 23}ms">')
        for fila in filas:
            y = MARGEN + fila * PASO
            lineas.append(f'    <circle cx="{x}" cy="{y}" r="2.65"/>')
        lineas.append("  </g>")
    return "\n".join([*lineas, "</svg>", ""])


def main():
    carpeta = Path(__file__).resolve().parents[1] / "assets"
    for nombre, titulo in TITULOS.items():
        (carpeta / nombre).write_text(generar_svg(titulo), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
