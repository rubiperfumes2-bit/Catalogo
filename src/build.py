"""Arma index.html de la web pública de Rubí desde los productos del Panel.

Uso:  python3 -I src/build.py <carpeta_con_productos_json> [carpeta_blobs]
- <carpeta_con_productos_json>: un .json por producto (como los guarda ArtifactData list con out_dir).
- [carpeta_blobs]: opcional, imágenes del Panel bajadas (nombre = id del blob) para perfumes sin foto en src/img.
Imprime los ids de perfumes sin foto (MISSING_IMG) para que se puedan bajar.
"""
import json, glob, os, sys, base64
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(R, 'src')
pdir = sys.argv[1]
bdir = sys.argv[2] if len(sys.argv) > 2 else None
URL = 'https://rubiperfumes2-bit.github.io/Catalogo/'

def img_for(pid, img):
    p = os.path.join(SRC, 'img', pid + '.webp')
    if os.path.exists(p):
        return p
    if bdir and img.startswith('/_blob/'):
        bid = img.split('/')[-1]
        for f in glob.glob(os.path.join(bdir, bid + '*')):
            try:
                from PIL import Image
                im = Image.open(f).convert('RGBA')
                bb = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
                if bb: im = im.crop(bb)
                im.thumbnail((640, 640)); im.save(p, 'WEBP', quality=82, method=6)
                return p
            except Exception as e:
                print('IMG_ERROR', pid, e)
    return None

out, missing = [], []
for f in sorted(glob.glob(os.path.join(pdir, '*.json'))):
    d = json.load(open(f))
    d = d.get('data', d) if isinstance(d.get('data'), dict) else d
    pid = os.path.basename(f)[:-5]
    if d.get('tipo') != 'perfume':
        continue
    ip = img_for(pid, d.get('img') or '')
    if not ip:
        missing.append(pid)
    out.append(dict(id=pid, n=d.get('nombre', ''), m=d.get('marca', ''), dis=d.get('linea') == 'diseñador',
                    para=d.get('para', ''), est=d.get('estilo', ''), p=d.get('precio', 0) or 0,
                    notas=d.get('notas', ''), o=d.get('orden', 0) or 0,
                    img=('data:image/webp;base64,' + base64.b64encode(open(ip, 'rb').read()).decode()) if ip else '',
                    f=d.get('ficha') or {}))
out.sort(key=lambda x: (x['dis'], x['o'], x['n']))
t = open(os.path.join(SRC, 'tpl.html')).read()
html = t.replace('__DATA__', json.dumps(out, ensure_ascii=False))
og = f'''<meta property="og:title" content="Rubí Perfumes">
<meta property="og:description" content="Perfumes originales y sellados en Neuquén capital y Aluminé. Elegí, armá tu pedido y pedilo por WhatsApp.">
<meta property="og:type" content="website">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#B3132B">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'%3E%3Cpath d='M14 8 H46 L56 22 L30 54 L4 22 Z' fill='%23B3132B'/%3E%3C/svg%3E">'''
html = html.replace('<meta name="claude:viewport-fit-sides" content="cover">', '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n' + og)
html = '<!doctype html>\n<html lang="es">\n<head>\n' + html.replace('<style>', '<style>\n[hidden]{display:none!important}img{max-width:100%}body{margin:0}', 1).replace('</style>', '</style>\n</head>\n<body>', 1) + '\n</body>\n</html>\n'
open(os.path.join(R, 'index.html'), 'w').write(html)
print('PERFUMES', len(out))
print('MISSING_IMG', ' '.join(missing) if missing else '-')
