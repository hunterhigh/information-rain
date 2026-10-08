import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const registry = join(root, 'products/distribution/reader-web/content-pool/registry.json');
const command = join(root, 'scripts/register-distribution-content.mjs');
const before = readFileSync(registry);
const temporary = mkdtempSync(join(tmpdir(), 'story-pack-validation-'));

try {
  const packageRoot = join(temporary, 'validation-fixture');
  mkdirSync(join(packageRoot, 'images'), { recursive: true });
  writeFileSync(join(packageRoot, 'images', 'cover.png'), Buffer.from(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScL/nwAAAABJRU5ErkJggg==',
    'base64',
  ));
  const valid = {
    id: 'validation-fixture', title: '验证样本', author: '测试', desc: '只用于校验。',
    duration: '1分钟', image: './images/cover.png', tags: ['测试'],
    theme: { bg: '#101820', accent: '#e3b66b', particles: 'rain' },
    nodes: 1, ends: 1, startNode: 'n01',
    data: {
      n01: { text: '开始。', exits: { left: 'e01' }, labels: { left: '结束' } },
      e01: { text: '结束。', isEnding: true, title: '终局', summary: '结束。' },
    },
  };
  const entry = join(packageRoot, 'world-entry.js');
  writeFileSync(entry, `${JSON.stringify(valid)}\n`);
  execFileSync(process.execPath, [command, '--validate', packageRoot], { stdio: 'pipe' });

  valid.data.n01.exits.left = 'missing';
  writeFileSync(entry, `${JSON.stringify(valid)}\n`);
  const invalid = spawnSync(process.execPath, [command, '--validate', packageRoot], { encoding: 'utf8' });
  assert.notEqual(invalid.status, 0, 'dangling choice must fail validation');
  assert.match(invalid.stderr, /目标 missing 不存在/);
  assert.deepEqual(readFileSync(registry), before, '--validate must not change the registry');
  console.log('Read-only content package validation tests passed');
} finally {
  assert.ok(resolve(temporary).startsWith(resolve(tmpdir()) + sep));
  rmSync(temporary, { recursive: true, force: true });
}
