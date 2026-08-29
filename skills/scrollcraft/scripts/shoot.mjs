#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const argv = process.argv.slice(2);
const arg = (n,d) => { const i = argv.indexOf(n); return i >= 0 && argv[i+1] ? argv[i+1] : d; };
const has = (n) => argv.includes(n);
const URL = arg('--url','http://127.0.0.1:4500');
const OUT = path.resolve(arg('--out','lab/shots'));
const W = Number(arg('--width','1440'));
const H = Number(arg('--height','900'));
const STEPS = Math.max(6, Number(arg('--steps','18')));
const REDUCED = has('--reduced-motion');

let chromium;
try { ({ chromium } = createRequire(path.join(process.cwd(),'package.json'))('playwright-core')); }
catch { console.error('playwright-core not found. Run: npm i -D playwright-core'); process.exit(1); }

const candidates = [
  process.env.SCROLLCRAFT_CHROME,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  '/usr/bin/google-chrome','/usr/bin/google-chrome-stable','/usr/bin/chromium','/usr/bin/chromium-browser'
].filter(Boolean);
const executablePath = candidates.find((p) => fs.existsSync(p));
if (!executablePath) { console.error('No installed Chromium browser found. Set SCROLLCRAFT_CHROME.'); process.exit(1); }

fs.mkdirSync(OUT,{recursive:true});
const browser = await chromium.launch({ executablePath, headless:true });
const page = await browser.newPage({ viewport:{width:W,height:H}, deviceScaleFactor:1, reducedMotion: REDUCED ? 'reduce' : 'no-preference' });
const errors=[]; const failed=[];
page.on('console', (m) => { if (m.type()==='error') errors.push(m.text()); });
page.on('pageerror', (e) => errors.push(String(e)));
page.on('requestfailed', (r) => failed.push(`${r.failure()?.errorText || 'failed'} ${r.url()}`));

await page.goto(URL,{waitUntil:'domcontentloaded'});
await page.evaluate(() => document.fonts?.ready);
await page.waitForTimeout(500);
const metrics = await page.evaluate(() => ({ height:document.documentElement.scrollHeight, vh:innerHeight, width:document.documentElement.scrollWidth, vw:innerWidth }));
const max = Math.max(0, metrics.height - metrics.vh);
const rows=[];
let prevHash=''; let dead=0;
for (let i=0;i<STEPS;i++) {
  const y = Math.round(max * (STEPS===1?0:i/(STEPS-1)));
  await page.evaluate((v) => scrollTo(0,v), y);
  await page.waitForTimeout(180);
  const info = await page.evaluate(() => ({
    y: scrollY,
    active: [...document.querySelectorAll('[data-sc-act]')].filter((el) => {
      const r=el.getBoundingClientRect(); return r.bottom>0 && r.top<innerHeight;
    }).map((el) => el.getAttribute('data-sc-act')),
    videos: [...document.querySelectorAll('video')].map((v) => ({t:v.currentTime,d:v.duration,ready:v.readyState,seeking:v.seeking})),
    text: document.body.innerText.slice(0,6000)
  }));
  const file = path.join(OUT, `${String(i).padStart(2,'0')}-${String(y).padStart(6,'0')}.png`);
  await page.screenshot({path:file,fullPage:false});
  const hash = JSON.stringify({active:info.active,videos:info.videos.map(v=>Math.round((v.t||0)*20)/20)});
  if (i>0 && hash===prevHash && y>0 && y<max) dead++;
  prevHash=hash;
  rows.push({index:i,y,...info,file:path.basename(file)});
}

const report = {
  url:URL, viewport:{width:W,height:H}, reducedMotion:REDUCED,
  document:metrics, horizontalOverflow:metrics.width>metrics.vw+2,
  possibleDeadTransitions:dead,
  consoleErrors:errors, failedRequests:failed, frames:rows
};
fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({
  frames:rows.length,
  horizontalOverflow:report.horizontalOverflow,
  possibleDeadTransitions:dead,
  consoleErrors:errors.length,
  failedRequests:failed.length,
  out:OUT
},null,2));
await browser.close();
