import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const file = process.argv[2];

if (!file) {
  console.error('用法：node scripts/check-experiment-design.mjs <产品 DESIGN.md>');
  process.exit(2);
}

let source;
try {
  source = readFileSync(resolve(file), 'utf8');
} catch (error) {
  console.error(`无法读取设计文件：${error.message}`);
  process.exit(2);
}

let inCodeFence = false;
let section = null;
let body = '';
let needsAndTech = '';

for (const line of source.split(/\r?\n/)) {
  if (/^\s*(```|~~~)/.test(line)) {
    inCodeFence = !inCodeFence;
    continue;
  }
  if (inCodeFence) continue;

  const heading = line.match(/^##\s+(\d+)\./);
  if (heading) {
    section = Number(heading[1]);
    continue;
  }
  if (/^\s*#/.test(line) || /^\s*>/.test(line) || /^\s*\|/.test(line)) continue;
  if (/^\s*(?:[-*_]\s*){3,}$/.test(line)) continue;

  const prose = line
    .replace(/`[^`]*`/g, '')
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/<[^>]+>/g, '');

  body += prose;
  if (section === 1 || section === 2) needsAndTech += prose;
}

const hanCount = (text) => [...text.matchAll(/\p{Script=Han}/gu)].length;
const total = hanCount(body);
const foundation = hanCount(needsAndTech);
const passed = total >= 10000 && foundation >= 3000;

console.log(`设计正文：${total} / 10000 汉字`);
console.log(`第 1、2 章（市场需求＋技术理解）：${foundation} / 3000 汉字`);
console.log(passed ? '篇幅门槛：通过。仍需人工审阅论证质量。' : '篇幅门槛：未通过。');

if (!passed) process.exitCode = 1;
