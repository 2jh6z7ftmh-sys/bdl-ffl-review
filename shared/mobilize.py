"""Turn a built FFL Review issue (fixed Letter pages) into a phone-friendly web page."""
import re, sys
src, dst, title = sys.argv[1], sys.argv[2], sys.argv[3]
h = open(src).read()
MOB = """
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
html{scroll-behavior:smooth}
.nav{position:sticky;top:0;z-index:9;background:#121218;display:flex;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch}
.nav a{color:#d4a017;font-family:OS;font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;text-decoration:none;padding:11px 13px;flex:none}
.page{margin:0 auto 18px;box-shadow:0 1px 0 #cfc6b4;scroll-margin-top:44px}
 .mc *{white-space:normal!important} .mc .t{font-size:22px!important} body{overflow-x:hidden} .page{overflow-x:hidden!important}
@media (max-width:820px){
 body{-webkit-text-size-adjust:100%}
 .page{width:100%!important;height:auto!important;overflow:visible!important;padding:14px 16px 0!important;font-size:16px!important;margin-bottom:10px}
 .row{flex-direction:column!important}
 .row>*{margin-left:0!important;margin-right:0!important;width:auto!important;flex:none!important;margin-bottom:12px}
 .c1,.c2,.ch{margin:0 0 12px 0!important}
 .wm{font-size:68px!important} .sub{font-size:17px!important}
 .h{font-size:26px!important} .phw{font-size:34px!important} .big{font-size:56px!important}
 .mc .t{font-size:24px!important} .quote{font-size:18px!important}
 .note{font-size:15.5px!important} table.st{font-size:14.5px!important}
 .belt{border-radius:22px!important;padding:10px 14px!important} .belt .plate{width:66px!important;height:66px!important;font-size:17px!important}
 .foot{margin-left:-16px!important;margin-right:-16px!important;font-size:11px!important;letter-spacing:.12em!important}
 .sp{display:none}
 .ph{flex-wrap:wrap}
}
</style>"""
h = h.replace('<head>', '<head>' + MOB, 1) if '<head>' in h else MOB + h
if '<title>' not in h: h = h.replace('<head>', f'<head><title>{title}</title>', 1)
# anchor each page and add a jump bar
n = 0
def tag(m):
    global n; n += 1; return f'<div id="p{n}" class="page'
h = re.sub(r'<div class="page', tag, h)
links = ['<a href="#p1">Front</a>', '<a href="#p2">Results</a>', '<a href="#p3">Odds</a>']
labels = []
for pid, body in re.findall(r'id="p(\d+)" class="page(.*?)(?=id="p\d+" class="page|$)', h, flags=re.S):
    m = re.search(r'<div class="mc">.*?<div class="t">(.*?)</div>', body, flags=re.S)
    if m:
        t = re.sub('<[^>]+>', ' ', m.group(1)); t = re.sub(r'\s+', ' ', t).strip()
        import data9
        own = [o for o, tn in sorted(data9.OWNER.items(), key=lambda kv: t.find(kv[1])) if tn in t]
        a = ' v '.join(own[:2]) if own else t[:20]
        labels.append(a); links.append(f'<a href="#p{pid}">{a}</a>')
links.append(f'<a href="#p{n}">Trades</a>')
h = re.sub(r'(<body[^>]*>)', r'\1<nav class="nav">' + ''.join(links) + '</nav>', h, count=1)
open(dst, 'w').write(h)
print('pages', n, 'matchups', len(labels))
