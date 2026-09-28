import { readFileSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { runInNewContext, Script } from 'node:vm';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const folder = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(folder, 'index.html'), 'utf8');
const start = html.indexOf('const worlds = [');
const end = html.indexOf('\n        ];', start);
if (start < 0 || end < 0) throw new Error('找不到作品数据区');

const source = html.slice(start + 'const worlds = '.length, end + '\n        ]'.length);
const worlds = runInNewContext(`(${source})`, {}, { timeout: 1000 });
const contentHash = createHash('sha256').update(JSON.stringify(worlds)).digest('hex');
const scriptStart = html.lastIndexOf('<script>');
const scriptEnd = html.indexOf('</script>', scriptStart);
if (scriptStart < 0 || scriptEnd < 0) throw new Error('找不到交互脚本');
new Script(html.slice(scriptStart + '<script>'.length, scriptEnd), { filename: 'index.html:inline-script' });

if (process.argv.includes('--print-hash')) {
  console.log(contentHash);
  process.exit(0);
}

const expectedHash = '5e3e623b261ac5168a294503f3799f06ae6a3d1f5e0d8a9fa0a563de2a8bf57d';
const expectedImagesHash = 'af10359c94143a7dd7ee5f4087aeb841df8971dcf5be78f9fadf921b8c12a250';
const expectedMissingTargetsHash = '724774754c64b38da37ea44c45437c040f2701a87bf1b9950e55a5416f878f6b';
const errors = [];
if (contentHash !== expectedHash) errors.push('作品数据与导入基线不一致');
if (worlds.length !== 30) errors.push(`应有 30 个作品，现有 ${worlds.length} 个`);

const imageNames = new Set(readdirSync(join(folder, 'images')));
const imageEntries = [...imageNames].sort().map(name =>
  `${name}:${createHash('sha256').update(readFileSync(join(folder, 'images', name))).digest('hex')}`
);
const imagesHash = createHash('sha256').update(JSON.stringify(imageEntries)).digest('hex');
if (imagesHash !== expectedImagesHash) errors.push('封面图与导入基线不一致');
const ids = new Set();
const missingTargets = [];
for (const world of worlds) {
  if (ids.has(world.id)) errors.push(`${world.id}: 重复作品 ID`);
  ids.add(world.id);
  if (!world.data[world.startNode]) errors.push(`${world.id}: 起点不存在`);
  const imageName = world.image?.replace(/^\.\/images\//, '');
  if (!imageName || !imageNames.has(imageName)) errors.push(`${world.id}: 封面图不存在`);

  for (const [nodeId, node] of Object.entries(world.data)) {
    for (const [direction, target] of Object.entries(node.exits || {})) {
      if (!world.data[target]) missingTargets.push(`${world.id}/${nodeId}/${direction}/${target}`);
    }
  }
}

const missingTargetsHash = createHash('sha256').update(JSON.stringify(missingTargets.sort())).digest('hex');
if (missingTargetsHash !== expectedMissingTargetsHash) errors.push('失效路径与源文件不一致，需重新审查内容');
if (process.argv.includes('--strict-content') && missingTargets.length) {
  errors.push(`原始作品仍有 ${missingTargets.length} 条失效路径`);
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else {
  console.log(`内容保持原样：${worlds.length} 个作品、${imageNames.size} 张封面；原始内容仍有 ${missingTargets.length} 条失效路径（--strict-content 可令其失败）`);
}
