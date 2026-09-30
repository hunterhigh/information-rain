import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { runInNewContext, Script } from 'node:vm';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const folder = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(folder, 'index.html'), 'utf8');
const start = html.indexOf('const worlds = [');
const end = html.indexOf('\n        ];', start);
if (start < 0 || end < 0) throw new Error('找不到作品数据区');

const source = html.slice(start + 'const worlds = '.length, end + '\n        ]'.length);
const builtInWorlds = runInNewContext(`(${source})`, {}, { timeout: 1000 });
const registrySource = readFileSync(join(folder, 'content-pool', 'registry.generated.js'), 'utf8');
const registryContext = { window: {} };
runInNewContext(registrySource, registryContext, { timeout: 1000 });
const registeredWorlds = registryContext.window.InformationRainContentRegistry?.worlds;
if (!Array.isArray(registeredWorlds)) throw new Error('内容注册表没有 worlds 数组');
const registryManifest = JSON.parse(readFileSync(join(folder, 'content-pool', 'registry.json'), 'utf8'));
const worlds = [...builtInWorlds, ...registeredWorlds];
const contentHash = createHash('sha256').update(JSON.stringify(worlds)).digest('hex');
const scriptStart = html.lastIndexOf('<script>');
const scriptEnd = html.indexOf('</script>', scriptStart);
if (scriptStart < 0 || scriptEnd < 0) throw new Error('找不到交互脚本');
new Script(html.slice(scriptStart + '<script>'.length, scriptEnd), { filename: 'index.html:inline-script' });

if (process.argv.includes('--print-hash')) {
  console.log(contentHash);
  process.exit(0);
}

// This is the owner's 19-work editorial selection, not the 30-work import baseline.
// The original hashes and missing-path inventory remain in SOURCE.md and Git history.
const expectedBuiltInIds = [
  'apocalypse', 'garden', 'building', 'midnight', 'neon', 'wuxia',
  'space', 'abyss', 'western', 'campus', 'loop', 'dream',
  'lotr', 'twilight', 'meta_comic', 'er', 'aot', 'hp', 'got'
];
const expectedRegisteredIds = registryManifest.packs.map(pack => pack.id);
const expectedIds = [...expectedBuiltInIds, ...expectedRegisteredIds];
const errors = [];
const actualIds = worlds.map(world => world.id);
if (JSON.stringify(actualIds) !== JSON.stringify(expectedIds)) {
  errors.push(`作品清单与内置内容及注册表不一致：${actualIds.join(', ')}`);
}
if (new Set(actualIds).size !== actualIds.length) errors.push('作品 ID 存在重复');
if (JSON.stringify(registeredWorlds.map(world => world.id)) !== JSON.stringify(expectedRegisteredIds)) {
  errors.push('浏览器注册表与 registry.json 的顺序或 ID 不一致');
}

const imageNames = new Set(readdirSync(join(folder, 'images')));
const expectedBuiltInImages = new Set(expectedBuiltInIds.map(id => `${id}.jpg`));
for (const imageName of imageNames) {
  if (!expectedBuiltInImages.has(imageName)) errors.push(`内置目录含未登记封面：${imageName}`);
}
for (const imageName of expectedBuiltInImages) {
  if (!imageNames.has(imageName)) errors.push(`保留作品缺少封面：${imageName}`);
}

let nodes = 0;
let endings = 0;
let exits = 0;
for (const world of worlds) {
  const data = world.data || {};
  const nodeIds = Object.keys(data);
  nodes += nodeIds.length;
  const endingIds = nodeIds.filter(id => data[id].isEnding);
  const sceneCount = nodeIds.length - endingIds.length;
  endings += endingIds.length;
  if (!data[world.startNode]) errors.push(`${world.id}: 起点不存在`);
  if (!endingIds.length) errors.push(`${world.id}: 没有结局`);
  if (world.nodes !== sceneCount) errors.push(`${world.id}: nodes 元数据 ${world.nodes} 与非结局节点 ${sceneCount} 不符`);
  if (world.ends !== endingIds.length) errors.push(`${world.id}: ends 元数据 ${world.ends} 与实际 ${endingIds.length} 不符`);
  const imagePath = world.image?.startsWith('./') ? resolve(folder, world.image.slice(2)) : null;
  if (!imagePath || !existsSync(imagePath)) errors.push(`${world.id}: 封面图不存在`);

  const reached = new Set();
  const stack = [world.startNode];
  while (stack.length) {
    const nodeId = stack.pop();
    if (reached.has(nodeId) || !data[nodeId]) continue;
    reached.add(nodeId);
    const node = data[nodeId];
    const choices = Object.entries(node.exits || {});
    exits += choices.length;
    if (!node.text?.trim()) errors.push(`${world.id}/${nodeId}: 缺少正文`);
    if (!node.isEnding && !choices.length) errors.push(`${world.id}/${nodeId}: 非结局没有后续`);
    if (node.isEnding && choices.length) errors.push(`${world.id}/${nodeId}: 结局仍有后续`);
    if (node.isEnding && (!node.title?.trim() || !node.summary?.trim())) {
      errors.push(`${world.id}/${nodeId}: 结局缺少标题或摘要`);
    }
    for (const [direction, target] of choices) {
      if (!data[target]) errors.push(`${world.id}/${nodeId}/${direction}: 目标 ${target} 不存在`);
      if (!node.labels?.[direction]) errors.push(`${world.id}/${nodeId}/${direction}: 缺少选项文案`);
      stack.push(target);
    }
  }
  for (const nodeId of nodeIds) {
    if (!reached.has(nodeId)) errors.push(`${world.id}/${nodeId}: 从开头不可到达`);
  }
  for (const endingId of endingIds) {
    if (!reached.has(endingId)) errors.push(`${world.id}/${endingId}: 结局不可到达`);
  }
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else {
  console.log(`内容结构通过：${worlds.length} 部作品（${builtInWorlds.length} 部内置 + ${registeredWorlds.length} 部注册）、${nodes} 个节点、${endings} 个结局、${exits} 条选择、${worlds.length} 张使用中的封面`);
  console.log(`当前内容 SHA-256: ${contentHash}`);
}
