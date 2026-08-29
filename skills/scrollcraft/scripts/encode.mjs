#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const argv = process.argv.slice(2);
const [input, output] = argv;
const mobile = argv.includes('--mobile');
if (!input || !output) {
  console.error('Usage: node encode.mjs <input> <output> [--mobile]');
  process.exit(1);
}
if (!fs.existsSync(input)) throw new Error(`Input not found: ${input}`);

const ff = process.env.SCROLLCRAFT_FFMPEG || 'ffmpeg';
fs.mkdirSync(path.dirname(path.resolve(output)), { recursive: true });
const scale = mobile ? 'scale=960:-2:flags=lanczos,fps=30' : 'scale=min(1920\\,iw):-2:flags=lanczos,fps=30';
const gop = mobile ? '4' : '8';
const crf = mobile ? '24' : '21';
const args = [
  '-y','-i',input,
  '-vf',scale,
  '-an',
  '-c:v','libx264','-preset','medium','-crf',crf,
  '-g',gop,'-keyint_min',gop,'-sc_threshold','0',
  '-pix_fmt','yuv420p','-movflags','+faststart',
  output,
];
try {
  execFileSync(ff, args, { stdio: 'inherit' });
} catch (e) {
  console.error(`Encoding failed with ${ff}. Set SCROLLCRAFT_FFMPEG to a full ffmpeg executable if needed.`);
  process.exit(e.status || 1);
}
