"""Builds the generated assets a weekly build needs, into the current folder:
  ff/   web fonts (woff2) copied from npm @fontsource packages
  img/  square team logos named by owner (img/Derek.jpg, ...), from shared/logos
Run from a week folder:  python3 ../../shared/make_assets.py"""
import os, shutil, subprocess, glob
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
PKGS = ['anton', 'oswald', 'bungee', 'courier-prime', 'barlow', 'barlow-condensed']
NPM = os.path.join(HERE, '.npm_fonts')
if not os.path.isdir(os.path.join(NPM, 'node_modules', '@fontsource', 'anton')):
    os.makedirs(NPM, exist_ok=True)
    subprocess.run(['npm', 'install', '--silent', '--prefix', NPM] + ['@fontsource/' + p for p in PKGS], check=True)
os.makedirs('ff', exist_ok=True)
for p in PKGS:
    for f in glob.glob(os.path.join(NPM, 'node_modules', '@fontsource', p, 'files', '*-latin-*.woff*')):
        shutil.copy(f, 'ff/')
OWNERS = ['Ricer', 'Derek', 'Chad', 'Rusty', 'Tom', 'Giff', 'Schwanz', 'Frenches', 'Abeln', 'Craig']
os.makedirs('img', exist_ok=True)
for o in OWNERS:
    src = glob.glob(os.path.join(HERE, 'logos', o.lower() + '.*'))[0]
    im = Image.open(src).convert('RGB'); w, h = im.size; s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((160, 160), Image.LANCZOS)
    im.save(f'img/{o}.jpg', quality=85)
print('fonts:', len(os.listdir('ff')), 'logos:', len(os.listdir('img')))
