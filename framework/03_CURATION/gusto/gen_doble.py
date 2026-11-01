#!/usr/bin/env python3
"""gen_doble.py — espécimen comparable: 1440 y 390 en una sola imagen.

Dos columnas en la misma página: el sistema a ancho de escritorio y el mismo sistema
en una columna de 390 px (container queries, no media queries: así el ancho angosto
es real dentro de la página ancha). Una captura por sistema, ambas medidas visibles.

Uso:  python gen_doble.py <carpeta-templates> <carpeta-salida>
"""
import os
import re
import sys

from gen_specimen import features, lum

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#0E1112;color:#E8ECEC;font-family:"DM Sans",system-ui,sans-serif;padding:28px 32px 36px}
.head{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:18px}
.slug{font:600 13px/1 ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;color:#8E9B9C}
.est{font:400 13px/1.4 "DM Sans",sans-serif;color:#B9C2C2}
.medidas{font:500 11px/1 ui-monospace,monospace;color:#7C8889;margin-left:auto;letter-spacing:.08em}
.panes{display:grid;grid-template-columns:1fr 390px;gap:28px;align-items:start}
.pane{border:1px solid rgba(255,255,255,.10)}
.pane__tag{font:500 10px/1 ui-monospace,monospace;letter-spacing:.18em;color:#7C8889;padding:6px 8px;border-bottom:1px solid rgba(255,255,255,.10)}
.spec{container-type:inline-size;--bg:%BG%;--fg:%FG%;--ac:%AC%;--r:%R%;
      background:var(--bg);color:var(--fg);padding:44px 48px 52px}
.spec .eyebrow{font:600 10px/1 "%FONT%",system-ui,sans-serif;letter-spacing:.22em;text-transform:uppercase;opacity:.55}
.spec h1{font:600 clamp(30px,3.6cqw,50px)/1.04 "%FONT%",system-ui,sans-serif;letter-spacing:-.02em;margin:16px 0 12px;max-width:19ch}
.spec p{font:400 15px/1.6 "%FONT%",system-ui,sans-serif;opacity:.78;max-width:58ch;margin:0 0 8px}
.spec .row{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.spec .btn{font:600 13px/1 "%FONT%",system-ui,sans-serif;padding:12px 20px;background:var(--ac);color:%BTNFG%;border:0;border-radius:var(--r)}
.spec .btn2{font:600 13px/1 "%FONT%",system-ui,sans-serif;padding:12px 20px;background:transparent;color:var(--fg);
            border:1px solid var(--fg);border-radius:var(--r);opacity:.75}
.spec .card{margin-top:26px;padding:20px;border:1px solid rgba(128,128,128,.35);border-radius:var(--r);max-width:340px;%SHADOW%}
.spec .card b{font:600 14px/1.3 "%FONT%",system-ui,sans-serif}
.spec .card span{font:400 13px/1.5 "%FONT%",system-ui,sans-serif;opacity:.7;display:block;margin-top:5px}
.spec .sws{display:flex;gap:8px;flex-wrap:wrap;margin-top:30px}
.spec .sw{width:74px}
.spec .sw i{display:block;height:36px;border-radius:var(--r);border:1px solid rgba(128,128,128,.3)}
.spec .sw b{display:block;font:500 9px/1.7 ui-monospace,monospace;opacity:.6;letter-spacing:.03em}
.spec .meta{margin-top:30px;display:flex;gap:20px;flex-wrap:wrap;font:500 10px/1.6 ui-monospace,monospace;opacity:.5}
@container (max-width:420px){
  .spec{padding:26px 20px 30px}
  .spec h1{font-size:28px}
  .spec p{font-size:14px}
  .spec .sw{width:58px}
}
"""


def pane(titulo, clases="spec"):
    return ('<div class="pane"><div class="pane__tag">%s</div>'
            '<div class="%s">__CONTENIDO__</div></div>' % (titulo, clases))


def build(slug, sitio, estilo, f):
    bg = f["hexes"][0] if f["hexes"] else "#FFFFFF"
    fg = "#FFFFFF" if f["dark"] else "#111111"
    ac = next((h for h in f["hexes"][1:] if abs(lum(h) - lum(bg)) > 0.15), "#666666")
    sw = "".join('<div class="sw"><i style="background:%s"></i><b>%s</b></div>' % (h, h) for h in f["hexes"])
    css = (CSS.replace("%BG%", bg).replace("%FG%", fg).replace("%AC%", ac)
              .replace("%R%", f["radius"]).replace("%FONT%", f["font"])
              .replace("%BTNFG%", "#FFFFFF" if lum(ac) < 0.5 else "#111111")
              .replace("%SHADOW%", "box-shadow:0 1px 2px rgba(0,0,0,.18),0 14px 34px rgba(0,0,0,.10);"
                       if f["shadow"] else "box-shadow:none;"))
    contenido = (
        '<div class="eyebrow">%s</div>'
        '<h1>%s</h1>'
        '<p>Un sistema de diseño es una decisión repetida: la misma escala, el mismo filete, '
        'la misma distancia entre dos cosas.</p>'
        '<div class="row"><button class="btn">Acción primaria</button><button class="btn2">Secundaria</button></div>'
        '<div class="card"><b>Componente</b><span>Superficie con radio declarado y sin adorno extra.</span></div>'
        '<div class="sws">%s</div>'
        '<div class="meta"><span>tipo · %s</span><span>radio · %s</span><span>sombra · %s</span>'
        '<span>fondo · %s</span></div>'
    ) % (estilo, sitio, sw, f["font"], f["radius"],
         "sí" if f["shadow"] else "no", "oscuro" if f["dark"] else "claro")

    return """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s · 1440 / 390</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=%s:wght@400;600&display=swap" rel="stylesheet">
<style>%s
.spec{width:100%%}
</style></head>
<body>
  <div class="head"><span class="slug">%s</span><span class="est">%s</span>
    <span class="medidas">1440 px · 390 px</span></div>
  <div class="panes">
    <div class="pane"><div class="pane__tag">ESCRITORIO · 1440</div><div class="spec">%s</div></div>
    <div class="pane"><div class="pane__tag">MÓVIL · 390</div><div class="spec">%s</div></div>
  </div>
</body></html>
""" % (slug, f["font"].replace(" ", "+"), css, slug, estilo, contenido, contenido)


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
        open(os.path.join(outdir, slug + ".html"), "w", encoding="utf-8").write(build(slug, sitio, est, features(md)))
        n += 1
    print("dobles escritos:", n)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
