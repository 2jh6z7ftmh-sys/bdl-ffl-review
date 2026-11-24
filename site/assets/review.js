// Native FFL Review issues (Week 12 on): issue nav plus the blocks that fill themselves from data.js.
// A page sets window.WEEK = {id, wk, last:[[away,home,pick],...], games:[[away,home,pick],...]} and marks
// containers with data-live="nav|scores|standings|tab|lows|tour|luck|streaks|through|receipts".
// When a week's final scores go into data.js, scores, receipts, standings, the tab and the lows update on their own.
(function(){
const D = window.BDL, U = window.U, W = window.WEEK || {};
const NAME = o => o === 'Derek' ? 'Ferries' : o;
const f1 = n => (Math.round(n * 10) / 10).toFixed(1);
const reg26 = D.games.filter(g => g[0] === 2026 && g[2] === 'reg');
const through = Math.max(0, ...reg26.map(g => g[1]));
const find = (wk, a, b) => { for (const g of reg26) if (g[1] === wk && ((g[3] === a && g[5] === b) || (g[3] === b && g[5] === a)))
  return g[3] === a ? {a: g[4], b: g[6]} : {a: g[6], b: g[4]}; return null; };
const logo = o => `<img class="lg" src="assets/logos/${o.toLowerCase()}.jpg" alt="">`;

function nav(){
  const list = ISSUES.current.filter(i => !i.missing), k = list.findIndex(i => i.id === W.id);
  const newer = list[k-1], older = list[k+1];
  const b = (i, t) => i ? `<a class="btn" href="${U.issueUrl(i.id)}">${t}</a>` : `<span class="btn off">${t}</span>`;
  return `${b(older, '← Week ' + (older ? older.wk : ''))}<a class="btn" href="review.html">All issues</a>${b(newer, newer ? 'Week ' + newer.wk + ' →' : 'Newer →')}`;
}
// last week's games: final score once it's in data.js, the printed pick either way
function scores(){
  return W.last.map(([a, h, pick]) => {
    const r = find(W.wk - 1, a, h);
    const win = r ? (r.a > r.b ? a : r.b > r.a ? h : null) : null;
    const grade = r && pick ? (pick === win ? '<b class="hit">Hit</b>' : '<b class="miss">Miss</b>') : '';
    return `<div class="box${r ? '' : ' pending'}">
      <div class="row${win === a ? ' w' : ''}">${logo(a)}<span>${NAME(a)}</span><b>${r ? f1(r.a) : '—'}</b></div>
      <div class="row${win === h ? ' w' : ''}">${logo(h)}<span>${NAME(h)}</span><b>${r ? f1(r.b) : '—'}</b></div>
      <div class="meta">${r ? 'Final' : 'Final score goes here'}${pick ? ` · We picked ${NAME(pick)} ${grade}` : ''}</div></div>`;
  }).join('');
}
function standings(){
  return [['Right', D.right], ['Left', D.left]].map(([lbl, div]) => {
    const rows = U.standings(div), top = rows[0];
    return `<div class="div"><h4>${lbl} Division</h4><table class="st"><thead><tr><th></th><th>Team</th><th class="n">W-L</th><th class="n">GB</th><th class="n">PF</th></tr></thead><tbody>${
      rows.map((r, n) => { const gb = ((top.W - r.W) + (r.L - top.L)) / 2;
        return `<tr class="${n === 2 ? 'cut' : ''}${n === 0 ? ' lead' : ''}"><td class="n">${n+1}</td><td>${logo(r.o)}${NAME(r.o)}${n === 0 ? ' <i class="tag">Runaway</i>' : ''}</td><td class="n">${U.recStr(r.W, r.L, r.T)}</td><td class="n">${gb ? gb : '—'}</td><td class="n">${f1(r.PF)}</td></tr>`; }).join('')
    }</tbody></table></div>`;
  }).join('') + `<p class="fine">Through Week ${through}.</p>`;
}
const byWeek = () => { const w = {}; for (const g of reg26) { (w[g[1]] = w[g[1]] || []).push([g[3], g[4]], [g[5], g[6]]); } return w; };
function tab(hi){
  const w = byWeek(), out = [];
  for (let k = 1; k < W.wk; k++) {
    if (!w[k]) { out.push(`<li class="pending"><span>Wk ${k}</span><b>—</b><em>goes here</em></li>`); continue; }
    const s = w[k].slice().sort((x, y) => hi ? y[1] - x[1] : x[1] - y[1])[0];
    out.push(`<li><span>Wk ${k}</span><b>${NAME(s[0])}</b><em>${f1(s[1])}</em></li>`);
  }
  return out.join('');
}
function tour(){
  return W.games.map(([a, h, pick, tagline], n) => {
    const s = U.series(a, h), last = s.games[s.games.length - 1];
    const lead = s.W === s.L ? `Series tied ${s.W}-${s.L}${s.T ? '-' + s.T : ''}` : `${NAME(s.W > s.L ? a : h)} leads ${Math.max(s.W, s.L)}-${Math.min(s.W, s.L)}${s.T ? '-' + s.T : ''}`;
    const lm = last ? `Last met ${U.gameLabel(last)}: ${NAME(a)} ${f1(last.s)}, ${NAME(h)} ${f1(last.os)}` : 'First meeting';
    const rec = o => { const x = D.s26[o]; return U.recStr(x.W, x.L, x.T); };
    return `<div class="act${n === 0 ? ' head' : ''}">${n === 0 ? '<div class="billing">Headliner · Big Game</div>' : ''}
      <div class="vs">${logo(a)}<b>${NAME(a)}</b><i>at</i><b>${NAME(h)}</b>${logo(h)}</div>
      <div class="recs">${rec(a)} · ${rec(h)}</div>
      ${tagline ? `<div class="tl">${tagline}</div>` : ''}
      <div class="ser">${lead} all-time. ${lm}.</div>
      <div class="pk">${pick ? 'Pick: ' + pick : 'Pick goes here once the odds are run'}</div></div>`;
  }).join('');
}
function luck(){
  const w = byWeek(), ap = {};
  for (const k in w) for (const [o, s] of w[k]) { const r = ap[o] = ap[o] || {W: 0, L: 0}; for (const [p, t] of w[k]) if (p !== o) { if (s > t) r.W++; else if (s < t) r.L++; } }
  const rows = Object.keys(ap).map(o => { const x = D.s26[o], pct = x.W / Math.max(1, x.W + x.L + x.T), apct = ap[o].W / Math.max(1, ap[o].W + ap[o].L); return {o, x, a: ap[o], d: pct - apct}; })
    .sort((p, q) => q.d - p.d);
  return rows.map(r => `<tr><td>${logo(r.o)}${NAME(r.o)}</td><td class="n">${U.recStr(r.x.W, r.x.L, r.x.T)}</td><td class="n">${r.a.W}-${r.a.L}</td><td class="n ${r.d > 0 ? 'up' : 'dn'}">${r.d > 0 ? '+' : ''}${Math.round(r.d * 100)}</td></tr>`).join('');
}
function streaks(){
  return Object.keys(D.s26).map(o => { const s = D.s26[o].res, c = s.slice(-1); let n = 0; for (let i = s.length - 1; i >= 0 && s[i] === c; i--) n++; return {o, c, n}; })
    .sort((p, q) => (q.c === 'W') - (p.c === 'W') || q.n - p.n)
    .map(r => `<li class="${r.c}"><span>${NAME(r.o)}</span><b>${r.c}${r.n}</b></li>`).join('');
}
const R = {nav, scores, standings, tab: () => tab(true), lows: () => tab(false), tour, luck, streaks, through: () => String(through)};
document.addEventListener('DOMContentLoaded', () => {
  for (const el of document.querySelectorAll('[data-live]')) { const f = R[el.dataset.live]; if (f) el.innerHTML = f(); }
  // the site uses <base href="/">, so point in-page links at this page
  for (const a of document.querySelectorAll('a[href^="#"]')) a.setAttribute('href', location.pathname + location.search + a.getAttribute('href'));
  // the floating "back to contents" button shows once you've scrolled past the top
  const top = document.querySelector('.ix-top');
  if (top) { const f = () => top.classList.toggle('show', scrollY > innerHeight * 1.2); addEventListener('scroll', f, {passive: true}); f(); }
});
window.REVIEW = {NAME, through};
})();
