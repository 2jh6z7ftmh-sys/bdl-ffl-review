(function(){
const D = window.BDL;
const NAV = [['index.html','Home'],['review.html','FFL Review'],['records.html','Records'],['owners.html','Owners'],['rules.html','Rules']];
const here = (location.pathname.split('/').pop() || 'index.html');
const page = here === 'owner.html' ? 'owners.html' : here;
document.addEventListener('DOMContentLoaded', () => {
  const m = document.createElement('header'); m.className = 'mast';
  m.innerHTML = `<div class="mast-in"><a class="brand" href="index.html"><b>Bullwinkle's</b><span>Dance League · Est. 1990</span></a>
    <nav class="top">${NAV.map(([h,t]) => `<a href="${h}"${h===page?' class="on"':''}>${t}</a>`).join('')}</nav></div>`;
  document.body.prepend(m);
  const f = document.createElement('footer'); f.className = 'footer';
  f.innerHTML = `<div><span>Bullwinkle's Dance League · Since 1990</span><span>${D.updated}</span></div>`;
  document.body.append(f);
});

const CUR = D.cur;
const isReg = t => t === 'reg';
const fmt = n => (Math.round(n * 10) / 10).toLocaleString('en-US', {minimumFractionDigits: 1, maximumFractionDigits: 1});
const fmt2 = n => Number.isInteger(n) ? String(n) : (Math.round(n*100)/100).toString();
const logo = o => CUR.includes(o) ? `assets/logos/${o.toLowerCase()}.jpg` : null;
const teamCell = (o, sub) => {
  const l = logo(o);
  const link = CUR.includes(o) ? `owner.html?o=${o}` : null;
  const inner = `${l ? `<img src="${l}" alt="">` : ''}<span class="nm">${o}${sub ? `<small>${sub}</small>` : ''}</span>`;
  return link ? `<a class="team" href="${link}" style="color:inherit">${inner}</a>` : `<span class="team">${inner}</span>`;
};
const TYPE = {reg:'Week', QF:'Quarterfinal', SF:'Semifinal', Final:'Final'};
const gameLabel = g => g.t === 'reg' ? `${g.y} Wk ${g.w}` : `${g.y} ${TYPE[g.t] || g.t}`;
const recStr = (w,l,t) => `${w}-${l}${t ? '-' + t : ''}`;

// all games involving a and b, from a's side
function series(a, b) {
  const out = [];
  for (const [y,w,t,x,sx,z,sz,ph] of D.games) {
    if (x === a && z === b) out.push({y,w,t,s:sx,os:sz,ph});
    else if (x === b && z === a) out.push({y,w,t,s:sz,os:sx,ph});
  }
  out.sort((p,q) => p.y - q.y || p.w - q.w);
  let W=0,L=0,T=0, rW=0,rL=0,rT=0, pW=0,pL=0;
  for (const g of out) {
    g.r = g.s > g.os ? 'W' : g.s < g.os ? 'L' : 'T';
    if (g.r==='W') W++; else if (g.r==='L') L++; else T++;
    if (isReg(g.t)) { if (g.r==='W') rW++; else if (g.r==='L') rL++; else rT++; }
    else { if (g.r==='W') pW++; else if (g.r==='L') pL++; }
  }
  let streak = '';
  if (out.length) { const last = out[out.length-1].r; let k=0; for (let i=out.length-1;i>=0 && out[i].r===last;i--) k++; streak = last + k; }
  return {games: out, W, L, T, rW, rL, rT, pW, pL, streak};
}
function ownerGames(o) {
  const out = [];
  for (const [y,w,t,x,sx,z,sz,ph] of D.games) {
    if (x === o) out.push({y,w,t,s:sx,opp:z,os:sz,ph});
    else if (z === o) out.push({y,w,t,s:sz,opp:x,os:sx,ph});
  }
  return out;
}
// 2026 standings, ordered by record, head-to-head (two-way), division record, points for
function standings(div) {
  const S = D.s26;
  const rows = div.map(o => ({o, ...S[o], pct: (S[o].W + S[o].T/2) / Math.max(1, S[o].W + S[o].L + S[o].T)}));
  const h2h26 = (a,b) => { let d = 0; for (const [y,w,t,x,sx,z,sz] of D.games) { if (y!==2026) continue; if (x===a&&z===b) d += Math.sign(sx-sz); if (x===b&&z===a) d += Math.sign(sz-sx); } return d; };
  rows.sort((a,b) => (b.pct - a.pct) || (-h2h26(a.o,b.o)) || ((b.dw-b.dl)-(a.dw-a.dl)) || (b.PF - a.PF));
  return rows;
}
window.U = {D, CUR, fmt, fmt2, logo, teamCell, gameLabel, recStr, series, ownerGames, standings, TYPE};
})();
