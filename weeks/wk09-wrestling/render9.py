import asyncio, os, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 984, 'height': 1268})
        await pg.goto('file://' + os.path.abspath('ffl_wk9.html'))
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(900)
        m = await pg.evaluate('''() => [...document.querySelectorAll('.page')].map((p,i)=>{const t=p.getBoundingClientRect().top; let mx=0;
          [...p.children].forEach(e=>{ if(e.classList.contains('foot')) return;
            e.querySelectorAll('*').forEach(c=>{const r=c.getBoundingClientRect(); if(r.height>0) mx=Math.max(mx,r.bottom-t)}); const r=e.getBoundingClientRect(); mx=Math.max(mx,r.bottom-t)});
          return [i+1, Math.round(mx)]; })''')
        for i, v in m: print('page', i, 'content bottom', v, 'OVER' if v > 1228 else '')
        await pg.pdf(path='FFL_Review_Wk9_Wrestling.pdf', width='8.5in', height='11in', scale=0.7673,
                     margin={'top': '8mm', 'bottom': '8mm', 'left': '8mm', 'right': '8mm'}, print_background=True)
        await b.close()
asyncio.run(main())
