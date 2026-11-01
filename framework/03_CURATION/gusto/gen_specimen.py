#!/usr/bin/env python3
"""gen_specimen.py — convierte las 54 fichas de popular-web-designs en especímenes HTML.

Un espécimen no imita el sitio: muestra lo que la ficha declara —paleta, tipografía,
radio, sombra y densidad— para poder comparar sistemas de un vistazo.

Uso:  python gen_specimen.py <carpeta-templates> <carpeta-salida>
"""
import os
import re
import sys
import unicodedata

HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
FONT_FAMILY = re.compile(r"font-family:\s*([^;\"'}\n]+)")
GFAMILY = re.compile(r"family=([A-Za-z+0-9]+)")
RADIUS = re.compile(r"border-radius:\s*([0-9.]+(?:px|rem))")
RADIO_CTX = re.compile(r"radi[oa]s?[^\n|]{0,40}?([0-9]+(?:px|rem))", re.I)


def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def features(md):
    hexes = []
    for h in HEX.findall(md):
        h = h.upper()
        if h not in hexes:
            hexes.append(h)
    fams = []
    for f in FONT_FAMILY.findall(md):
        f = f.strip().strip('"').split(",")[0].strip().strip('"')
        if f and "var(" not in f and f not in fams:
            fams.append(f)
    gf = [g.replace("+", " ") for g in GFAMILY.findall(md)]
    radii = RADIUS.findall(md) or RADIO_CTX.findall(md)
    return {
        "hexes": hexes[:8],
        "font": (gf[0] if gf else (fams[0] if fams else "Inter")),
        "mono": next((f for f in fams if "mono" in f.lower()), "monospace"),
        "radius": radii[0] if radii else "0px",
        "shadow": "box-shadow" in md,
        "dark": bool(hexes) and lum(hexes[0]) < 0.18,
    }


def specimen(slug, titulo, estilo, f):
    bg = f["hexes"][0] if f["hexes"] else "#FFFFFF"
    fg = "#FFFFFF" if f["dark"] else "#111111"
    accent = next((h for h in f["hexes"][1:] if abs(lum(h) - lum(bg)) > 0.15), "#666666")
    sw = "".join(
        '<div class="sw"><i style="background:%s"></i><b>%s</b></div>' % (h, h) for h in f["hexes"]
    )
    fam_url = f["font"].replace(" ", "+")
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{slug}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={fam_url}:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
  :root{{--bg:{bg};--fg:{fg};--ac:{accent};--r:{r}}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--fg);font-family:"{font}",system-ui,sans-serif;
       padding:56px 64px 72px;line-height:1.5;-webkit-font-smoothing:antialiased}}
  .eyebrow{{font:600 11px/1 "{font}";letter-spacing:.22em;text-transform:uppercase;opacity:.55}}
  h1{{font:600 clamp(32px,4.4vw,54px)/1.04 "{font}";letter-spacing:-.02em;margin:18px 0 14px;max-width:19ch}}
  p{{font:400 16px/1.6 "{font}";opacity:.78;max-width:60ch;margin:0 0 10px}}
  .mono{{font-family:"{mono}";font-size:13px;opacity:.6}}
  .row{{display:flex;gap:14px;flex-wrap:wrap;margin-top:34px}}
  .btn{{font:600 14px/1 "{font}";padding:13px 22px;background:var(--ac);color:{btnfg};border:0;border-radius:var(--r)}}
  .btn2{{font:600 14px/1 "{font}";padding:13px 22px;background:transparent;color:var(--fg);
        border:1px solid var(--fg);border-radius:var(--r);opacity:.75}}
  .card{{margin-top:34px;padding:24px;border:1px solid {fgdim};border-radius:var(--r);max-width:360px;
        {shadow}}}
  .card b{{font:600 15px/1.3 "{font}"}}
  .card span{{font:400 14px/1.55 "{font}";opacity:.7;display:block;margin-top:6px}}
  .sws{{display:flex;gap:10px;flex-wrap:wrap;margin-top:38px}}
  .sw{{width:96px}}
  .sw i{{display:block;height:44px;border-radius:var(--r);border:1px solid {fgdim}}}
  .sw b{{display:block;font:500 10px/1.6 "{mono}";opacity:.6;letter-spacing:.04em}}
  .meta{{margin-top:40px;display:flex;gap:26px;flex-wrap:wrap;font:500 11px/1.6 "{mono}";opacity:.5}}
  @media(max-width:600px){{body{{padding:32px 22px 44px}}h1{{font-size:30px}}}}
</style>
</head>
<body>
  <div class="eyebrow">{estilo}</div>
  <h1>{titulo}</h1>
  <p>Un sistema de diseño es una decisión repetida: la misma escala, el mismo filete, la misma
     distancia entre dos cosas. Esto muestra lo que la ficha declara, no el sitio terminado.</p>
  <div class="row">
    <button class="btn">Acción primaria</button>
    <button class="btn2">Secundaria</button>
  </div>
  <div class="card"><b>Componente</b><span>Superficie con radio declarado y sin adorno extra.</span></div>
  <div class="sws">{swatches}</div>
  <div class="meta"><span>tipo · {font}</span><span>radio · {r}</span><span>sombra · {sombra}</span><span>fondo · {modo}</span></div>
</body>
</html>
""".format(
        slug=slug, titulo=titulo, estilo=estilo, bg=bg, fg=fg, accent=accent,
        fam_url=fam_url,
        r=f["radius"], font=f["font"], mono=f["mono"],
        btnfg="#FFFFFF" if lum(accent) < 0.5 else "#111111",
        fgdim="rgba(128,128,128,.35)",
        shadow="box-shadow:0 1px 2px rgba(0,0,0,.18),0 12px 32px rgba(0,0,0,.10);" if f["shadow"] else "box-shadow:none;",
        swatches=sw,
        shadow_txt="sí" if f["shadow"] else "no",
        sombra="sí" if f["shadow"] else "no",
        modo="oscuro" if f["dark"] else "claro",
    )


def main(tdir, outdir):
    os.makedirs(outdir, exist_ok=True)
    style = {}
    for line in open(os.path.join(tdir, "..", "SKILL.md"), encoding="utf-8"):
        m = re.match(r"\| `([\w.\-]+)\.md` \| ([^|]+)\|([^|]+)\|", line)
        if m:
            style[m.group(1)] = (m.group(2).strip(), m.group(3).strip())
    n = 0
    for f in sorted(os.listdir(tdir)):
        if not f.endswith(".md"):
            continue
        slug = f[:-3]
        md = open(os.path.join(tdir, f), encoding="utf-8").read()
        sitio, est = style.get(slug, (slug, "sistema de diseño"))
        # nombre del sistema: primera línea con "# "
        titulo = re.search(r"^#\s+(.+)$", md, re.M)
        titulo = titulo.group(1).strip() if titulo else sitio
        html = specimen(slug, titulo, est, features(md))
        open(os.path.join(outdir, slug + ".html"), "w", encoding="utf-8").write(html)
        n += 1
    print("especímenes escritos:", n)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
