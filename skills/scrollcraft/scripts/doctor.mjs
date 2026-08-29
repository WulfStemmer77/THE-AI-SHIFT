#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { paths } from './workspace.mjs';

const rows = [];
const add = (level, name, ok, detail, fix = '') => rows.push({ level, name, ok, detail, fix });
const run = (cmd, args) => {
  try { return execFileSync(cmd, args, { encoding: 'utf8', stdio: ['ignore','pipe','ignore'] }); }
  catch { return null; }
};

const major = Number(process.versions.node.split('.')[0]);
add('required', 'Node', major >= 18, `v${process.versions.node}`, 'Install Node 18+');

const chromeCandidates = [
  process.env.SCROLLCRAFT_CHROME,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser',
].filter(Boolean);
const chrome = chromeCandidates.find((p) => fs.existsSync(p));
add('verify', 'Chrome/Edge/Chromium', Boolean(chrome), chrome || 'not found', 'Install a Chromium browser or set SCROLLCRAFT_CHROME.');

const ffCandidates = [process.env.SCROLLCRAFT_FFMPEG, 'ffmpeg', '/opt/homebrew/bin/ffmpeg', '/usr/local/bin/ffmpeg', '/usr/bin/ffmpeg'].filter(Boolean);
let ffmpeg = null; let filters = 0;
for (const candidate of ffCandidates) {
  const out = run(candidate, ['-hide_banner','-filters']);
  if (!out) continue;
  const count = out.split(/\r?\n/).length;
  if (count > filters) { filters = count; ffmpeg = candidate; }
}
add('media', 'ffmpeg (full build)', filters > 200, ffmpeg ? `${ffmpeg} (${filters} filter lines)` : 'not found', 'Install a full ffmpeg build or set SCROLLCRAFT_FFMPEG. Required for scrub-media encoding.');

let pw = false;
try { createRequire(path.join(process.cwd(), 'package.json'))('playwright-core'); pw = true; } catch {}
add('verify', 'playwright-core', pw, pw ? 'resolves from current project' : 'not installed', 'Run npm i -D playwright-core in the build project.');

try {
  const ws = paths();
  add('required', 'workspace', true, `${ws.workspace} via ${ws.via}`);
} catch (e) {
  add('required', 'workspace', false, e.message, 'Fix .scrollcraft.json or SCROLLCRAFT_HOME.');
}

const pkg = path.join(process.cwd(), 'package.json');
if (fs.existsSync(pkg)) {
  try {
    const p = JSON.parse(fs.readFileSync(pkg, 'utf8'));
    const deps = { ...(p.dependencies || {}), ...(p.devDependencies || {}) };
    const stack = ['next','react','vite','astro','three','@react-three/fiber'].filter((d) => deps[d]);
    add('info', 'detected stack', true, stack.length ? stack.join(', ') : 'package.json present; no known scrollcraft stack detected');
  } catch {}
} else {
  add('info', 'detected stack', true, 'no package.json; vanilla/static is available');
}

console.log('\nscrollcraft preflight\n');
for (const r of rows) {
  const mark = r.ok ? ' ok ' : r.level === 'required' ? 'FAIL' : 'warn';
  console.log(`[${mark}] ${r.name.padEnd(22)} ${r.detail}`);
  if (!r.ok && r.fix) console.log(`       ${r.fix}`);
}
const hard = rows.filter((r) => r.level === 'required' && !r.ok);
console.log('');
if (hard.length) process.exit(1);
console.log('Ready for planning. Media/browser warnings only block the corresponding later phase.\n');
