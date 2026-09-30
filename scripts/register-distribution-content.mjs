import {
  cpSync,
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  renameSync,
  rmSync,
  statSync,
  writeFileSync,
} from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, extname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptFolder = dirname(fileURLToPath(import.meta.url));
const projectRoot = resolve(scriptFolder, '..');
const demoRoot = join(projectRoot, 'products', 'distribution', 'reader-web');
const poolRoot = join(demoRoot, 'content-pool');
const packsRoot = join(poolRoot, 'packs');
const registryPath = join(poolRoot, 'registry.json');
const generatedPath = join(poolRoot, 'registry.generated.js');
const orderPath = join(poolRoot, 'display-order.json');
const allowedDirections = new Set(['left', 'right', 'up', 'down']);

const args = process.argv.slice(2);
const replace = args.includes('--replace');
const checkOnly = args.includes('--check');
const rebuild = args.includes('--rebuild');
const sources = args.filter(arg => !arg.startsWith('--')).map(source => resolve(source));

if (args.some(arg => arg.startsWith('--') && !['--replace', '--check', '--rebuild'].includes(arg))) {
  fail('未知选项。可用选项：--check、--replace、--rebuild');
}
if ((checkOnly && (replace || rebuild || sources.length)) || (rebuild && (replace || sources.length))) {
  fail('--check 或 --rebuild 不能与内容来源及其他选项同时使用');
}
if (!checkOnly && !rebuild && !sources.length) {
  fail('请提供至少一个已解压的内容包目录；ZIP 请使用 register-distribution-content.ps1');
}

function fail(message) {
  throw new Error(message);
}

function sha256(buffer) {
  return createHash('sha256').update(buffer).digest('hex');
}

function hashableBytes(path) {
  const bytes = readFileSync(path);
  if (['.js', '.json', '.md'].includes(extname(path).toLowerCase())) {
    return Buffer.from(bytes.toString('utf8').replace(/\r\n/g, '\n'));
  }
  return bytes;
}

function normalizedRelative(from, to) {
  return relative(from, to).split(sep).join('/');
}

function isInside(parent, child) {
  const parentWithSeparator = resolve(parent) + sep;
  return resolve(child).startsWith(parentWithSeparator);
}

function findEntryFiles(root, results = []) {
  if (!existsSync(root)) fail(`来源不存在：${root}`);
  const info = statSync(root);
  if (info.isFile()) {
    if (root.endsWith('.zip')) fail(`Node 注册器不直接解压 ZIP：${root}`);
    if (root.endsWith('world-entry.js')) results.push(root);
    return results;
  }
  for (const name of readdirSync(root).sort()) {
    const fullPath = join(root, name);
    const child = statSync(fullPath);
    if (child.isDirectory()) findEntryFiles(fullPath, results);
    else if (name === 'world-entry.js') results.push(fullPath);
  }
  return results;
}

function readImageDimensions(path) {
  const bytes = readFileSync(path);
  if (bytes.length >= 24 && bytes.toString('ascii', 1, 4) === 'PNG') {
    return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
  }
  if (bytes.length < 4 || bytes[0] !== 0xff || bytes[1] !== 0xd8) {
    fail(`封面不是受支持的 JPEG/PNG：${path}`);
  }
  let offset = 2;
  while (offset + 9 < bytes.length) {
    if (bytes[offset] !== 0xff) {
      offset += 1;
      continue;
    }
    const marker = bytes[offset + 1];
    if (marker === 0xd8 || marker === 0xd9) {
      offset += 2;
      continue;
    }
    const size = bytes.readUInt16BE(offset + 2);
    if (size < 2 || offset + size + 2 > bytes.length) break;
    if ([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf].includes(marker)) {
      return { height: bytes.readUInt16BE(offset + 5), width: bytes.readUInt16BE(offset + 7) };
    }
    offset += size + 2;
  }
  fail(`无法读取封面尺寸：${path}`);
}

function packageHash(root) {
  const files = [];
  const walk = folder => {
    for (const name of readdirSync(folder).sort()) {
      const fullPath = join(folder, name);
      const info = statSync(fullPath);
      if (info.isDirectory()) walk(fullPath);
      else files.push(fullPath);
    }
  };
  walk(root);
  const hash = createHash('sha256');
  for (const file of files) {
    hash.update(normalizedRelative(root, file));
    hash.update('\0');
    hash.update(hashableBytes(file));
    hash.update('\0');
  }
  return hash.digest('hex');
}

function validatePackage(entryPath) {
  const root = dirname(entryPath);
  let world;
  try {
    world = JSON.parse(readFileSync(entryPath, 'utf8'));
  } catch (error) {
    fail(`${entryPath} 必须是纯 JSON 对象：${error.message}`);
  }

  for (const field of ['id', 'title', 'author', 'desc', 'duration', 'image', 'startNode']) {
    if (typeof world[field] !== 'string' || !world[field].trim()) fail(`${entryPath}: 缺少 ${field}`);
  }
  if (!/^[a-z0-9][a-z0-9_-]*$/.test(world.id)) fail(`${world.id}: id 只允许小写字母、数字、_、-`);
  if (!Array.isArray(world.tags) || !world.tags.length || world.tags.some(tag => typeof tag !== 'string' || !tag.trim())) {
    fail(`${world.id}: tags 必须是非空字符串数组`);
  }
  if (!world.theme || typeof world.theme !== 'object') fail(`${world.id}: 缺少 theme`);
  if (!world.data || typeof world.data !== 'object' || Array.isArray(world.data)) fail(`${world.id}: data 必须是节点对象`);
  if (!Number.isInteger(world.nodes) || !Number.isInteger(world.ends)) fail(`${world.id}: nodes/ends 必须是整数`);

  const imageRelative = world.image.replace(/^\.\//, '');
  const imagePath = resolve(root, imageRelative);
  if (!world.image.startsWith('./images/') || !isInside(root, imagePath) || !existsSync(imagePath)) {
    fail(`${world.id}: 封面必须位于内容包的 ./images/ 目录`);
  }
  if (!['.jpg', '.jpeg', '.png'].includes(extname(imagePath).toLowerCase())) fail(`${world.id}: 封面只支持 JPEG/PNG`);
  const dimensions = readImageDimensions(imagePath);
  if (!dimensions.width || !dimensions.height) fail(`${world.id}: 封面尺寸无效`);

  const nodeIds = Object.keys(world.data);
  if (!nodeIds.length || !world.data[world.startNode]) fail(`${world.id}: 起点不存在`);
  const endings = nodeIds.filter(id => world.data[id]?.isEnding === true);
  if (world.nodes !== nodeIds.length - endings.length) fail(`${world.id}: nodes 元数据与非结局节点数不符`);
  if (world.ends !== endings.length || !endings.length) fail(`${world.id}: ends 元数据与结局数不符`);

  for (const nodeId of nodeIds) {
    if (!/^[A-Za-z0-9_-]+$/.test(nodeId)) fail(`${world.id}/${nodeId}: 节点 ID 含不支持字符`);
    const node = world.data[nodeId];
    if (!node || typeof node.text !== 'string' || !node.text.trim()) fail(`${world.id}/${nodeId}: 缺少正文`);
    const exits = Object.entries(node.exits || {});
    if (node.isEnding) {
      if (exits.length) fail(`${world.id}/${nodeId}: 结局不能再有出口`);
      if (!node.title?.trim() || !node.summary?.trim()) fail(`${world.id}/${nodeId}: 结局缺少标题或摘要`);
    } else if (!exits.length) {
      fail(`${world.id}/${nodeId}: 非结局节点没有出口`);
    }
    for (const [direction, target] of exits) {
      if (!allowedDirections.has(direction)) fail(`${world.id}/${nodeId}: 不支持方向 ${direction}`);
      if (!world.data[target]) fail(`${world.id}/${nodeId}/${direction}: 目标 ${target} 不存在`);
      if (typeof node.labels?.[direction] !== 'string' || !node.labels[direction].trim()) {
        fail(`${world.id}/${nodeId}/${direction}: 缺少选项文案`);
      }
    }
  }

  const reached = new Set([world.startNode]);
  const queue = [world.startNode];
  while (queue.length) {
    const nodeId = queue.shift();
    for (const target of Object.values(world.data[nodeId].exits || {})) {
      if (!reached.has(target)) {
        reached.add(target);
        queue.push(target);
      }
    }
  }
  const unreachable = nodeIds.filter(id => !reached.has(id));
  if (unreachable.length) fail(`${world.id}: 存在不可达节点 ${unreachable.join(', ')}`);

  return {
    world,
    root,
    entryPath,
    imagePath,
    imageRelative,
    dimensions,
    entrySha256: sha256(hashableBytes(entryPath)),
    coverSha256: sha256(readFileSync(imagePath)),
    packageSha256: packageHash(root),
  };
}

function readRegisteredPackages() {
  if (!existsSync(packsRoot)) return [];
  return readdirSync(packsRoot, { withFileTypes: true })
    .filter(entry => entry.isDirectory())
    .map(entry => {
      const item = validatePackage(join(packsRoot, entry.name, 'world-entry.js'));
      if (entry.name !== item.world.id) fail(`${entry.name}: 目录名与作品 ID 不一致`);
      return item;
    })
    .sort((a, b) => a.world.id.localeCompare(b.world.id));
}

function readDisplayOrder(packages, appendMissing = false) {
  if (!existsSync(orderPath)) fail('缺少 display-order.json');
  const order = JSON.parse(readFileSync(orderPath, 'utf8'));
  if (order.schemaVersion !== 1 || !Array.isArray(order.worldIds)) fail('display-order.json 格式无效');
  const ids = new Set(packages.map(item => item.world.id));
  const seen = new Set();
  for (const id of order.worldIds) {
    if (typeof id !== 'string' || seen.has(id) || !ids.has(id)) fail(`展示顺序中存在重复或未知作品：${id}`);
    seen.add(id);
  }
  const missing = packages.map(item => item.world.id).filter(id => !seen.has(id));
  if (missing.length && !appendMissing) fail(`展示顺序缺少作品：${missing.join(', ')}`);
  return { schemaVersion: 1, worldIds: [...order.worldIds, ...missing] };
}

function inDisplayOrder(packages, order) {
  const byId = new Map(packages.map(item => [item.world.id, item]));
  return order.worldIds.map(id => byId.get(id));
}

function registryOutputs(packages) {
  const manifest = {
    schemaVersion: 1,
    generatedBy: 'scripts/register-distribution-content.mjs',
    packs: packages.map(item => ({
      id: item.world.id,
      title: item.world.title,
      entry: `packs/${item.world.id}/world-entry.js`,
      image: `packs/${item.world.id}/${item.imageRelative}`,
      width: item.dimensions.width,
      height: item.dimensions.height,
      entrySha256: item.entrySha256,
      coverSha256: item.coverSha256,
      packageSha256: item.packageSha256,
    })),
  };
  const browserWorlds = packages.map(item => ({
    ...item.world,
    image: `./content-pool/packs/${item.world.id}/${item.imageRelative}`,
  }));
  const registryJson = `${JSON.stringify(manifest, null, 2)}\n`;
  const generatedJs = [
    '// Generated by scripts/register-distribution-content.mjs. Do not edit by hand.',
    `window.InformationRainContentRegistry = ${JSON.stringify({ schemaVersion: 1, worlds: browserWorlds }, null, 2)};`,
    '',
  ].join('\n');
  return { registryJson, generatedJs };
}

function writeAtomically(path, content) {
  mkdirSync(dirname(path), { recursive: true });
  const temporary = `${path}.tmp`;
  writeFileSync(temporary, content, 'utf8');
  if (existsSync(path)) rmSync(path);
  renameSync(temporary, path);
}

function assertUnique(packages) {
  const seen = new Set();
  for (const item of packages) {
    const id = item.world.id;
    if (seen.has(id)) fail(`${id}: 内容池中存在重复 ID`);
    seen.add(id);
  }
}

if (checkOnly) {
  const packages = readRegisteredPackages();
  assertUnique(packages);
  const order = readDisplayOrder(packages);
  const expected = registryOutputs(inDisplayOrder(packages, order));
  if (!existsSync(registryPath) || readFileSync(registryPath, 'utf8') !== expected.registryJson) {
    fail('registry.json 与内容包不一致，请重新运行注册器');
  }
  if (!existsSync(generatedPath) || readFileSync(generatedPath, 'utf8') !== expected.generatedJs) {
    fail('registry.generated.js 与内容包不一致，请重新运行注册器');
  }
  console.log(`内容注册表通过：${packages.length} 部作品`);
  process.exit(0);
}

if (rebuild) {
  const packages = readRegisteredPackages();
  assertUnique(packages);
  const order = readDisplayOrder(packages);
  const outputs = registryOutputs(inDisplayOrder(packages, order));
  writeAtomically(registryPath, outputs.registryJson);
  writeAtomically(generatedPath, outputs.generatedJs);
  console.log(`已按展示顺序生成 ${packages.length} 部作品`);
  process.exit(0);
}

const entryFiles = [...new Set(sources.flatMap(source => findEntryFiles(source)))];
if (!entryFiles.length) fail('没有找到 world-entry.js');
const incoming = entryFiles.map(validatePackage);
assertUnique(incoming);
const incomingIds = new Set();
for (const item of incoming) {
  if (incomingIds.has(item.world.id)) fail(`${item.world.id}: 本次输入中重复`);
  incomingIds.add(item.world.id);
}

mkdirSync(packsRoot, { recursive: true });
for (const item of incoming) {
  const target = join(packsRoot, item.world.id);
  if (existsSync(target)) {
    const current = validatePackage(join(target, 'world-entry.js'));
    if (current.packageSha256 === item.packageSha256) {
      console.log(`${item.world.id}: 已注册且内容相同，跳过复制`);
      continue;
    }
    if (!replace) fail(`${item.world.id}: 已存在不同版本；确认替换时使用 --replace`);
    rmSync(target, { recursive: true, force: true });
  }
  cpSync(item.root, target, { recursive: true, errorOnExist: true });
  console.log(`${item.world.id}: 已注册`);
}

const registered = readRegisteredPackages();
assertUnique(registered);
const order = readDisplayOrder(registered, true);
const outputs = registryOutputs(inDisplayOrder(registered, order));
writeAtomically(orderPath, `${JSON.stringify(order, null, 2)}\n`);
writeAtomically(registryPath, outputs.registryJson);
writeAtomically(generatedPath, outputs.generatedJs);
console.log(`注册完成：内容池现有 ${registered.length} 部作品`);
