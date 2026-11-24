"""Week 12 (native page): screenshots for review, plus the cover thumb and the link-preview image.
Run from the repo root: python3 weeks/wk12-hairmetal/render12.py [outdir] [chromium path]"""
import sys, threading, functools, http.server, os
from playwright.sync_api import sync_playwright
out = sys.argv[1] if len(sys.argv) > 1 else 'weeks/wk12-hairmetal/shots'
exe = sys.argv[2] if len(sys.argv) > 2 else None
os.makedirs(out, exist_ok=True)
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory='site')
H.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8765), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = 'http://127.0.0.1:8765/issues/2026-wk12.html'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe, args=['--no-sandbox', '--single-process', '--no-zygote', '--disable-gpu'])
    def page(w, h, dpr=1, mobile=False):
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile)
        pg.goto(URL); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        return pg
    pg = page(390, 844, 2, True)
    pg.screenshot(path=f'{out}/wk12-phone-top.png')
    pg.screenshot(path=f'{out}/wk12-phone-full.png', full_page=True)
    pg = page(1280, 900)
    pg.screenshot(path=f'{out}/wk12-desktop-top.png')
    pg.screenshot(path=f'{out}/wk12-desktop-full.png', full_page=True)
    # cover-only shots: thumb (archive/home) and 1200x630 link preview
    for w, h, name in ((510, 660, 'site/thumbs/2026-wk12-1.jpg'), (1200, 630, 'site/thumbs/2026-wk12-og.jpg')):
        pg = page(w, h)
        css = '.mast,.jcard,.ix-top{display:none!important}.cover{min-height:%dpx;height:%dpx}.cover-in{padding:18px}' % (h, h)
        if w > h: css += '.coverlines,.pa{display:none}.logo{font-size:150px}.title{font-size:96px}'
        else: css += '.coverlines li:nth-child(n+3){display:none}.logo{font-size:118px}.title{font-size:66px}.pa{display:none}'
        pg.add_style_tag(content=css)
        pg.wait_for_timeout(200)
        pg.locator('#cover').screenshot(path=name, type='jpeg', quality=86)
    b.close()
srv.shutdown()
