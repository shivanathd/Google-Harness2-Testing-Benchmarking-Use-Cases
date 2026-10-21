const DATA = /*__DATA__*/{};
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const fmt = (x, d = 2) => (x == null ? "–" : Number(x).toFixed(d));
const sgn = (x) => (x >= 0 ? "+" : "") + fmt(x);
const tip = $("#tip");
function showTip(e, html) {
  tip.innerHTML = html; tip.hidden = false;
  const r = tip.getBoundingClientRect();
  let x = e.clientX + 14, y = e.clientY + 14;
  if (x + r.width > innerWidth - 8) x = e.clientX - r.width - 14;
  if (y + r.height > innerHeight - 8) y = e.clientY - r.height - 14;
  tip.style.left = x + "px"; tip.style.top = y + "px";
}
function bindTips(root) {
  root.querySelectorAll("[data-tip]").forEach((n) => {
    n.addEventListener("mousemove", (e) => showTip(e, n.dataset.tip));
    n.addEventListener("mouseleave", () => (tip.hidden = true));
    n.addEventListener("focus", (e) => { const r = n.getBoundingClientRect(); showTip({ clientX: r.right, clientY: r.top }, n.dataset.tip); });
    n.addEventListener("blur", () => (tip.hidden = true));
  });
}
const B = (label) => DATA.board.find((r) => r.label === label) || null;
const line = (r) => r ? `${sgn(r.delta)} (95% CI ${fmt(r.lo)} to ${fmt(r.hi)}; ${r.up} up, ${r.down} down of ${r.n})` : "pending";

/* ---------------------------------------------------------------- verdict */
function verdict() {
  const g = (l) => B(l);
  const s2v = g("ADK, fresh-seed variants") && DATA.board.filter((r) => r.study.startsWith("Study 2") && r.label === "ADK, fresh-seed variants")[0];
  const fl = (DATA.flips.find((f) => f.comparison === "Haiku improver vs base, ITT") || { per_task: [] }).per_task.find((p) => p.lost > 0);
  const demo = ((DATA.lab.arm_a || {}).per_task || []).find((p) => p.task.startsWith("draft-markup-of-procedural-order"));
  const chk = (v) => fmt(v * demo.n_checks, 1);
  const V = DATA.voids;
  const items = [
    `<b>It works where there is headroom and a stronger improver.</b> A weak local model (ADK + qwen3:8b) with the leak guard on: ${line(s2v)} on fresh instances its improver never saw. Claude Code capped at four turns: ${line(g("Claude Code (4-turn cap), Sonnet improver"))}. Full-strength Claude Code was already at ceiling, and Harness² correctly changed nothing.`,
    `<b>Self-improvement is real but weaker.</b> With Haiku improving its own harness instead of Sonnet: ${line(g("Claude Code (4-turn cap), Haiku improves itself (ITT)"))}, about half the gain, and Haiku minus Sonnet is ${line(g("Haiku minus Sonnet as improver (ITT)"))}. ${fl ? `One task regressed (${fl.task} ${fmt(fl.base)} → ${fmt(fl.treat)}).` : ""} On the legal tasks, Haiku as its own improver: ${line(g("Haiku improves itself, in-task"))}${demo ? `; the ${demo.n_checks}-check demo task fell from ${chk(demo.base)} to ${chk(demo.treat)} checks` : ""}.`,
    `<b>Each job is its own jump, not a staircase.</b> A harness adapted on an easy task, reused on harder ones: ${line(DATA.board.filter((r) => r.study.startsWith("Study 2") && r.label === "ADK, easy harness on medium/hard")[0])}. Turning the lesson library off: ${line(g("ADK, library off minus on (ITT)"))}, all of it on one task. Skipping the probe step: ${line(g("ADK, no probe minus probe (ITT)"))}, so we did not reproduce the paper's claim that probing first matters.`,
    `<b>It leaks unless you stop it.</b> Unguarded, ${V.study1.void} of ${V.study1.of} adopted harnesses carried the task's own answers or ids. With the guard, ${V.study2.void} of ${V.study2.of} did, and the gain held. On the legal tasks, both Sonnet and Haiku improvers wrote answer keys for the matter in front of them without ever seeing the rubric; the layer-2 guard rejected one live.`,
    `<b>On Google's own legal tasks the gain is real but small, and partly format.</b> Sonnet harnesses on matters their improver never saw: ${line(g("Sonnet harnesses on unseen matters (held-out)"))}; without the leaky harness ${line(g("Held-out, leaky harness removed"))}. It is concentrated in redline-to-redline transfer, much of it teaching the deliverable format the judge's reader expects. In-task: ${line(g("Sonnet improver, in-task"))}, or ${line(g("Sonnet improver, in-task, leaky task removed"))} clean. The harness2 README reports up to +11.8 points for one step (quoted, not measured here).`,
  ];
  $("#verdict-body").innerHTML = `<ul>${items.map((i) => `<li>${i}</li>`).join("")}</ul>`;
  $("#lab-status").textContent = "LAB: final (36 held-out runs, R=3)";
}

/* ---------------------------------------------------------------- scoreboard (HTML forest plot) */
const KIND = {
  primary: ["Main result", "var(--accent)"], baseline: ["Autoresearch baseline", "var(--s-ar)"],
  diff: ["Variant minus variant", "var(--s-h2)"], null: ["At ceiling (negative control)", "var(--ink-3)"],
  leaky: ["As run, includes leaked cells", "var(--warn)"],
};
function board() {
  const lo = -0.6, hi = 1.3, pct = (v) => ((Math.max(lo, Math.min(hi, v)) - lo) / (hi - lo)) * 100;
  $("#board-legend").innerHTML = Object.entries(KIND).map(([k, [n, c]]) => `<span class="${k === "leaky" ? "hollow" : ""}" style="--c:${c}">${n}</span>`).join("");
  let h = `<div class="forest"><div class="f-axis"><span></span><div class="f-scale">${[-0.5, 0, 0.5, 1].map((t) => `<i style="left:${pct(t)}%">${t > 0 ? "+" : ""}${t}</i>`).join("")}</div></div>`;
  let study = null;
  for (const r of DATA.board) {
    if (r.study !== study) { study = r.study; h += `<div class="f-group">${esc(study)}</div>`; }
    const [kn, col] = KIND[r.kind] || KIND.primary;
    const tipHtml = `<b>${esc(r.label)}</b><br>Δ ${sgn(r.delta)} · 95% CI ${fmt(r.lo)} to ${fmt(r.hi)}<br>${r.up} up, ${r.down} down of ${r.n} tasks · sign-flip p=${fmt(r.p, 3)}${r.note ? `<br><i>${esc(r.note)}</i>` : ""}`;
    h += `<div class="f-row" tabindex="0" data-tip="${esc(tipHtml)}"><span class="f-label">${esc(r.label)}</span><div class="f-strip">
      <b class="f-zero" style="left:${pct(0)}%"></b>
      <b class="f-ci" style="left:${pct(r.lo)}%;width:${Math.max(0.4, pct(r.hi) - pct(r.lo))}%;background:${col}"></b>
      <b class="f-pt ${r.kind === "leaky" ? "hollow" : ""}" style="left:${pct(r.delta)}%;--c:${col}"></b>
      <em class="f-val" style="left:${pct(Math.max(r.hi, r.delta))}%">${sgn(r.delta)}</em></div></div>`;
  }
  $("#board-chart").innerHTML = h + "</div>";
  bindTips($("#board-chart"));
  $("#board-table").innerHTML = `<table><thead><tr><th>Study</th><th>Comparison</th><th class="r">Δ</th><th class="r">95% CI</th><th class="r">Up / down</th><th class="r">Tasks</th><th class="r">p</th></tr></thead><tbody>${DATA.board.map((r) => `<tr><td>${esc(r.study)}</td><td>${esc(r.label)}</td><td class="r">${sgn(r.delta)}</td><td class="r">[${fmt(r.lo)}, ${fmt(r.hi)}]</td><td class="r">${r.up} / ${r.down}</td><td class="r">${r.n}</td><td class="r">${fmt(r.p, 3)}</td></tr>`).join("")}</tbody></table>`;
}

/* ---------------------------------------------------------------- job after job */
function jobs() {
  const W = 300, H = 220, L = 34, R = 14, T = 16, Bm = 34;
  const x = (i) => L + i * ((W - L - R) / 2), y = (v) => T + (1 - v) * (H - T - Bm);
  const out = [];
  for (const d of ["data", "ops", "swe"]) {
    const js = DATA.jobs.filter((j) => j.domain === d);
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${d}: score per job">`;
    for (const v of [0, 0.5, 1]) s += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="var(--rule)"/><text x="${L - 6}" y="${y(v) + 4}" text-anchor="end" class="tk">${v}</text>`;
    js.forEach((j, i) => (s += `<text x="${x(i)}" y="${H - 12}" text-anchor="middle" class="tk">${j.tier}</text>`));
    const carried = js.map((j, i) => (i === 0 ? { ...j, carried: j.adapted } : j));
    const series = [["base", "var(--s-base)", "", js, "Base harness"], ["adapted", "var(--s-h2)", "", js, "Adapted on this job"],
                    ["carried", "var(--ink-3)", 'stroke-dasharray="4 4"', carried, "Easy-job harness carried forward"], ["nolib", "var(--s-ar)", "", js, "Adapted, library off"]];
    for (const [key, col, dash, arr, name] of series) {
      const pts = arr.map((j, i) => (j[key] == null ? null : [x(i), y(j[key]), j])).filter(Boolean);
      if (pts.length > 1 && key !== "nolib") s += `<polyline fill="none" stroke="${col}" stroke-width="2" ${dash} points="${pts.map((p) => p[0] + "," + p[1]).join(" ")}"/>`;
      const off = { base: -5, adapted: 0, carried: 5, nolib: 9 }[key];
      for (const [px, py, j] of pts) s += `<circle cx="${px + off}" cy="${py}" r="${key === "adapted" ? 5 : 4}" fill="${key === "carried" ? "var(--paper)" : col}" stroke="${col}" stroke-width="2" tabindex="0" data-tip="${esc(`<b>${j.task}</b> · ${name}: ${fmt(j[key])}`)}"/>`;
    }
    out.push(`<figure class="chart"><h3>${d}</h3>${s}</svg></figure>`);
  }
  $("#jobs-charts").innerHTML = out.join("");
  bindTips($("#jobs-charts"));
  const dh = DATA.jobs.find((j) => j.task === "data-h");
  $("#jobs-caption").innerHTML = `Orange reaches the top on almost every job, but only because each job is adapted afresh. The gray dashed line, the easy job's harness reused unchanged, falls back to base or below on harder jobs. Switching the library off (aqua) left most jobs where they were; the exception is data-hard (${fmt(dh?.adapted)} with the library, ${fmt(dh?.nolib)} without). swe stays low: the 8B model rarely fixes multi-file repos even with help.`;
}

/* ---------------------------------------------------------------- check flips */
function flips() {
  const out = [];
  for (const f of DATA.flips) {
    const max = Math.max(1, ...f.per_task.map((p) => Math.max(p.gained, p.lost)));
    const rows = f.per_task.map((p) => {
      const tipHtml = `<b>${esc(p.task)}</b><br>${p.gained} checks gained, ${p.lost} lost<br>mean ${fmt(p.base)} → ${fmt(p.treat)}${p.n_checks ? ` of ${p.n_checks} checks` : ""}`;
      return `<div class="fl-row" tabindex="0" data-tip="${esc(tipHtml)}"><span class="fl-task">${esc(p.task.replace(/^draft-markup-of-/, "markup: ").replace(/^identify-arbitration-agreement-issues/, "agreement issues"))}</span>
        <span class="fl-lost"><b style="width:${(p.lost / max) * 100}%"></b><em>${p.lost || ""}</em></span>
        <span class="fl-gain"><b style="width:${(p.gained / max) * 100}%"></b><em>${p.gained || ""}</em></span></div>`;
    }).join("");
    out.push(`<figure class="chart flipfig"><h3>${esc(f.comparison)}</h3><div class="fl-head"><span></span><span>lost</span><span>gained</span></div>${rows}</figure>`);
  }
  $("#flip-charts").innerHTML = out.join("");
  bindTips($("#flip-charts"));
}

/* ---------------------------------------------------------------- cost vs gain */
function cost() {
  const pts = DATA.cost.filter((c) => c.per_task != null && c.delta != null);
  const W = 760, H = 330, L = 52, R = 24, T = 18, Bm = 44;
  const xmax = Math.max(0.8, ...pts.map((p) => p.per_task)) * 1.08;
  const x = (v) => L + (v / xmax) * (W - L - R), y = (v) => T + (1 - (v + 0.1) / 1.15) * (H - T - Bm);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Improver dollars per task against score change">`;
  for (const v of [0, 0.25, 0.5, 0.75, 1]) s += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="var(--rule)"/><text x="${L - 8}" y="${y(v) + 4}" text-anchor="end" class="tk">${v > 0 ? "+" : ""}${v}</text>`;
  for (let v = 0; v <= xmax; v += 0.25) s += `<text x="${x(v)}" y="${H - 22}" text-anchor="middle" class="tk">$${v.toFixed(2)}</text>`;
  s += `<text x="${(L + W - R) / 2}" y="${H - 4}" text-anchor="middle" class="tk">improver spend per task</text><text x="12" y="${T + 6}" class="tk">Δ</text>`;
  const placed = [];
  for (const p of pts.sort((a, b) => b.delta - a.delta)) {
    const px = x(p.per_task), py = y(p.delta);
    let ly = py + 4, lx = px + 10, anchor = "start";
    if (lx + 230 > W) { lx = px - 10; anchor = "end"; }
    while (placed.some((q) => Math.abs(q - ly) < 15 && true)) ly += 15;
    placed.push(ly);
    const col = p.arm.startsWith("CC") ? "var(--s-base)" : p.arm.startsWith("LAB") ? "var(--accent)" : p.arm.includes("autoresearch") ? "var(--s-ar)" : "var(--s-h2)";
    s += `<circle cx="${px}" cy="${py}" r="6" fill="${col}" stroke="var(--paper)" stroke-width="2" tabindex="0" data-tip="${esc(`<b>${p.arm}</b><br>$${fmt(p.per_task)} per task · Δ ${sgn(p.delta)} (${p.metric})`)}"/>`;
    s += `<text x="${lx}" y="${ly}" text-anchor="${anchor}" class="lbl">${esc(p.arm)}</text>`;
  }
  $("#cost-chart").innerHTML = s + "</svg><figcaption>Blue: Claude Code arms. Orange: ADK Harness² arms. Aqua: autoresearch. Violet: LAB legal tasks (Claude rubric judge costs, about $4 per judged run, not included).</figcaption>";
  bindTips($("#cost-chart"));
}

/* ---------------------------------------------------------------- lineage */
const TYPES = { ask: ["You asked", "var(--ink-2)", "◇"], decision: ["Decision", "var(--accent)", "■"], finding: ["Finding", "var(--s-base)", "●"], bug: ["Bug caught", "var(--bad)", "▲"], amendment: ["Pre-reg amendment", "var(--warn)", "◆"] };
let lineageFilter = "all";
function lineage() {
  const ev = [...DATA.lineage.events].sort((a, b) => a.t.localeCompare(b.t));
  $("#lineage-filters").innerHTML = [["all", "All", ""], ...Object.entries(TYPES).map(([k, v]) => [k, v[0], v[2]])]
    .map(([k, n, g]) => `<button type="button" id="lf-${k}" class="${k === lineageFilter ? "on" : ""}" data-k="${k}">${g ? `<span aria-hidden="true">${g}</span> ` : ""}${n} <small>${k === "all" ? ev.length : ev.filter((e) => e.type === k).length}</small></button>`).join("");
  $("#lineage-filters").querySelectorAll("button").forEach((b) => b.addEventListener("click", () => { lineageFilter = b.dataset.k; lineage(); }));
  const mins = (t) => { const [h, m] = t.split(":").map(Number); return h * 60 + m; };
  const t0 = 0, t1 = Math.max(...ev.map((e) => mins(e.t))) + 20, W = 900, H = 120, L = 112, R = 12;
  const x = (t) => L + ((mins(t) - t0) / (t1 - t0)) * (W - L - R);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Events over time by type">`;
  Object.keys(TYPES).forEach((k, i) => (s += `<text x="0" y="${16 + i * 20 + 4}" class="tk">${TYPES[k][0]}</text><line x1="${L}" x2="${W - R}" y1="${16 + i * 20}" y2="${16 + i * 20}" stroke="var(--rule)"/>`));
  for (let h = 0; h * 60 <= t1; h += 2) s += `<text x="${L + ((h * 60) / (t1 - t0)) * (W - L - R)}" y="${H - 4}" text-anchor="middle" class="tk">${String(h).padStart(2, "0")}:00</text>`;
  ev.forEach((e) => {
    const i = Object.keys(TYPES).indexOf(e.type); if (i < 0) return;
    const dim = lineageFilter !== "all" && lineageFilter !== e.type;
    s += `<circle cx="${x(e.t)}" cy="${16 + i * 20}" r="5" fill="${TYPES[e.type][1]}" opacity="${dim ? 0.15 : 0.9}" tabindex="0" data-tip="${esc(`<b>${e.t} · ${TYPES[e.type][0]}</b><br>${e.title}`)}"/>`;
  });
  $("#lineage-strip").innerHTML = s + "</svg>";
  bindTips($("#lineage-strip"));
  $("#lineage-list").innerHTML = ev.filter((e) => lineageFilter === "all" || e.type === lineageFilter).map((e) => {
    const [n, c, g] = TYPES[e.type] || ["Event", "var(--ink-3)", "•"];
    const meta = [e.why && `<b>Why:</b> ${esc(e.why)}`, e.found_by && `<b>Found by:</b> ${esc(e.found_by)}`, e.evidence && `<b>Evidence:</b> <span class="mono">${esc(e.evidence)}</span>`].filter(Boolean).join(" · ");
    return `<li><time>${e.t}</time><span class="chip" style="color:${c}"><span aria-hidden="true">${g}</span> ${n}</span><div><h3>${esc(e.title)}</h3>${e.what ? `<p>${esc(e.what)}</p>` : ""}${meta ? `<p class="meta2">${meta}</p>` : ""}</div></li>`;
  }).join("");
}

/* ---------------------------------------------------------------- learnings, exhibit, comparisons */
function learnings() {
  const L = DATA.lineage.learnings, names = { harness2: "About Harness²", benchmarking: "About benchmarking agents", claude_code: "About Claude Code" };
  $("#learnings-body").innerHTML = Object.entries(names).map(([k, n]) => `<div><h3>${n}</h3><ul class="tight">${(L[k] || []).map((x) => `<li>${esc(x)}</li>`).join("")}</ul></div>`).join("");
}
function exhibit() {
  const hl = (t) => esc(t).replace(/^(.*(?:Workspace fact|workspace fact|errors=\d+|users=\d+|top_code=E\d+).*)$/gm, '<mark>$1</mark>');
  const { before, after } = DATA.exhibit;
  $("#exhibit").innerHTML = `<figure><figcaption>Study 1, no guard · <span class="mono">${esc(before?.path)}</span></figcaption><pre class="code">${before ? hl(before.text) : "–"}</pre></figure>
    <figure><figcaption>Study 2, leak guard on · <span class="mono">${esc(after?.path)}</span></figcaption><pre class="code">${after ? esc(after.text) : "–"}</pre></figure>`;
}
function comparisons() {
  const s2 = (l) => DATA.board.find((r) => r.study.startsWith("Study 2") && r.label === l);
  $("#vs-h2").textContent = `Fresh-seed: ${line(s2("ADK, fresh-seed variants"))}`;
  $("#vs-ar").textContent = `Tuned task: ${line(B("Autoresearch (grader in loop), tuned task"))}`;
  $("#vs-h2t").textContent = line(s2("ADK, easy harness on medium/hard"));
  $("#vs-art").textContent = line(B("Autoresearch, medium/hard"));
  $("#prereg").textContent = DATA.prereg || "";
}

window.addEventListener("DOMContentLoaded", () => { verdict(); board(); jobs(); flips(); cost(); lineage(); learnings(); exhibit(); comparisons(); });
