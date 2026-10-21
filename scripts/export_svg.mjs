// Usage: node scripts/export_svg.mjs <archify.html> <out.svg>   (needs Google Chrome)
// Drive Archify's own in-viewer "svg" export (auto light/dark theme) in headless Chrome and save the blob.
import { spawn } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
const [html, out] = process.argv.slice(2);
const prof = mkdtempSync(join(tmpdir(), 'svgexp-'));
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${prof}`, '--window-size=1440,900', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let port; for (let i = 0; i < 100 && !port; i++) { await sleep(100); const f = join(prof, 'DevToolsActivePort'); if (existsSync(f)) port = readFileSync(f, 'utf8').split('\n')[0]; }
const page = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(t => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pending = {};
ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pending[d.id]) { pending[d.id](d); delete pending[d.id]; } };
const send = (method, params = {}) => new Promise(r => { pending[++id] = r; ws.send(JSON.stringify({ id, method, params })); });
const ev = async expr => (await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result.result.value;
await send('Page.navigate', { url: 'file://' + resolve(html) }); await sleep(2500);
const svg = await ev(`new Promise((res, rej) => {
  const orig = URL.createObjectURL;
  URL.createObjectURL = b => { b.text().then(res); return orig.call(URL, b); };
  const btn = document.querySelector('button[data-format="svg"]');
  if (!btn) return rej('no svg export button');
  btn.click(); setTimeout(() => rej('timeout'), 8000);
})`);
ws.close(); chrome.kill();
if (!svg || !svg.startsWith('<svg') && !svg.startsWith('<?xml')) { console.error('export failed:', String(svg).slice(0, 200)); process.exit(1); }
writeFileSync(out, svg); console.log(out, svg.length, 'bytes');
