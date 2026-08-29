#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const required = [
  'SKILL.md','manifest.yaml','THIRD_PARTY_NOTICES.md','LICENSE.upstream-scrollcraft',
  'engine/scrollcraft.js','engine/scrollcraft.css','scripts/doctor.mjs','scripts/workspace.mjs',
  'scripts/encode.mjs','scripts/serve.mjs','scripts/shoot.mjs','references/3d-routing.md',
  'templates/BRIEF.md','templates/SOURCE_OF_TRUTH.md','templates/PLAN.md','templates/VALIDATION.md',
  'schema/asset-manifest.schema.json'
];
for (const f of required) {
  if (!fs.existsSync(path.join(root,f))) throw new Error(`missing ${f}`);
}
for (const f of ['engine/scrollcraft.js','scripts/doctor.mjs','scripts/workspace.mjs','scripts/encode.mjs','scripts/serve.mjs','scripts/shoot.mjs']) {
  execFileSync(process.execPath, ['--check', path.join(root,f)], { stdio:'inherit' });
}
const skill = fs.readFileSync(path.join(root,'SKILL.md'),'utf8');
if (!skill.startsWith('---\n')) throw new Error('SKILL.md missing YAML frontmatter');
if (!/name:\s*scrollcraft\b/.test(skill)) throw new Error('SKILL.md name must be scrollcraft');
if (/allowed-tools:\s*.*AskUserQuestion/.test(skill)) throw new Error('Claude-specific tool declaration present');
const schema = JSON.parse(fs.readFileSync(path.join(root,'schema/asset-manifest.schema.json'),'utf8'));
if (schema.properties?.schema_version?.const !== '1.0.0') throw new Error('asset schema version mismatch');
console.log('scrollcraft smoke: PASS');
