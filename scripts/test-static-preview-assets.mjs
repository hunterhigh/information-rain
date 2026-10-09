import assert from 'node:assert/strict';
import { existsSync, readFileSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { runInNewContext } from 'node:vm';

const output = resolve('dist/cloudflare-preview');
const source = readFileSync(join(output, 'content-pool/registry.generated.js'), 'utf8');
const context = { window: {} };
runInNewContext(source, context, { timeout: 1000 });
const worlds = context.window.InformationRainContentRegistry.worlds;
const manifest = JSON.parse(readFileSync(resolve('products/distribution/reader-web/content-pool/registry.json'), 'utf8'));
assert.equal(worlds.length, manifest.packs.length);
let optimizedBytes = 0;
for (const world of worlds) {
  for (const image of [world.image, world.thumbnail]) {
    assert.match(image, /^\.\/content-pool\/packs\/[a-z0-9_-]+\/images\/[a-z0-9_-]+(?:-thumb)?\.webp$/);
    const path = join(output, image.slice(2));
    assert.ok(existsSync(path), `${world.id}: missing ${image}`);
    optimizedBytes += statSync(path).size;
  }
  assert.ok(statSync(join(output, world.thumbnail.slice(2))).size <
    statSync(join(output, world.image.slice(2))).size, `${world.id}: thumbnail should be smaller`);
  assert.equal(world.data, undefined, `${world.id}: story prose should be loaded separately`);
  const story = JSON.parse(readFileSync(join(output, world.storyUrl.slice(2)), 'utf8'));
  assert.ok(story[world.startNode], `${world.id}: story start node missing`);
}
assert.ok(optimizedBytes < 25 * 1024 * 1024, `preview covers exceed 25 MiB: ${optimizedBytes}`);
console.log(`${worlds.length} stage covers and thumbnails: ${(optimizedBytes / 1048576).toFixed(1)} MiB`);
