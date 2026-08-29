#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

function findGitRoot(start) {
  let dir = path.resolve(start);
  for (;;) {
    if (fs.existsSync(path.join(dir, '.git'))) return dir;
    const up = path.dirname(dir);
    if (up === dir) return path.resolve(start);
    dir = up;
  }
}

function findConfig(start) {
  let dir = path.resolve(start);
  for (;;) {
    const file = path.join(dir, '.scrollcraft.json');
    if (fs.existsSync(file)) return file;
    const up = path.dirname(dir);
    if (up === dir) return null;
    dir = up;
  }
}

export function paths(cwd = process.cwd()) {
  let workspace;
  let via;
  if (process.env.SCROLLCRAFT_HOME) {
    workspace = path.resolve(process.env.SCROLLCRAFT_HOME);
    via = 'SCROLLCRAFT_HOME';
  } else {
    const cfg = findConfig(cwd);
    if (cfg) {
      const parsed = JSON.parse(fs.readFileSync(cfg, 'utf8'));
      if (!parsed.workspace || typeof parsed.workspace !== 'string') {
        throw new Error(`${cfg} must contain { "workspace": "..." }`);
      }
      workspace = path.resolve(path.dirname(cfg), parsed.workspace);
      via = cfg;
    } else {
      const root = findGitRoot(cwd);
      workspace = path.join(root, 'scrollcraft');
      via = 'project default';
    }
  }
  return {
    workspace,
    builds: path.join(workspace, 'builds'),
    fingerprints: path.join(workspace, 'FINGERPRINTS.md'),
    via,
  };
}

function ensure() {
  const p = paths();
  fs.mkdirSync(p.builds, { recursive: true });
  if (!fs.existsSync(p.fingerprints)) {
    const here = path.dirname(fileURLToPath(import.meta.url));
    const template = path.resolve(here, '../templates/FINGERPRINTS.md');
    const content = fs.existsSync(template)
      ? fs.readFileSync(template, 'utf8')
      : '# Scrollcraft fingerprints\n\n| Build | Grammar | Nav | Hero | Act shape | Close | Signature move |\n|---|---|---|---|---|---|---|\n';
    fs.writeFileSync(p.fingerprints, content);
  }
  return p;
}

const invoked = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invoked) {
  const p = process.argv.includes('--ensure') ? ensure() : paths();
  console.log(JSON.stringify(p, null, 2));
}
