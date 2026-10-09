import { readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

const packs = resolve('products/distribution/reader-web/content-pool/packs');
const rows = [];
for (const directory of readdirSync(packs, { withFileTypes: true }).filter(item => item.isDirectory())) {
  const world = JSON.parse(readFileSync(join(packs, directory.name, 'world-entry.js'), 'utf8'));
  const scenes = Object.values(world.data).filter(node => !node.isEnding);
  const threeWay = scenes.filter(node => Object.keys(node.exits || {}).length > 2).length;
  const verticalStoryExits = scenes.reduce((sum, node) => sum + Number(Boolean(node.exits?.up)) + Number(Boolean(node.exits?.down)), 0);
  const reached = new Set();
  const pending = [world.startNode];
  while (pending.length) {
    const id = pending.pop();
    if (reached.has(id) || !world.data[id]) continue;
    reached.add(id);
    pending.push(...Object.values(world.data[id].exits || {}));
  }
  rows.push({
    id: world.id,
    scenes: scenes.length,
    endings: Object.values(world.data).length - scenes.length,
    threeWay,
    verticalStoryExits,
    unreachable: Object.keys(world.data).length - reached.size,
  });
}

rows.sort((a, b) => a.id.localeCompare(b.id));
if (process.argv.includes('--json')) console.log(JSON.stringify(rows, null, 2));
else {
  console.log('id\tscenes\tendings\t3+ choices\tvertical exits\tunreachable');
  for (const row of rows) console.log(Object.values(row).join('\t'));
  console.log(`Total: ${rows.length} worlds; ${rows.filter(row => row.scenes < 10).length} below 10 scenes; ` +
    `${rows.reduce((n, row) => n + row.threeWay, 0)} nodes with 3+ choices; ` +
    `${rows.reduce((n, row) => n + row.verticalStoryExits, 0)} vertical story exits`);
}
if (process.argv.includes('--strict') && rows.some(row => row.scenes < 10 || row.threeWay || row.verticalStoryExits || row.unreachable)) {
  process.exitCode = 1;
}
