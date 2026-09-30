import { cp, mkdir, readdir, rm, stat } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const source = path.join(repoRoot, 'products/distribution/reader-web')
const output = path.resolve(repoRoot, 'dist/cloudflare-preview')

if (!output.startsWith(path.join(repoRoot, 'dist') + path.sep)) {
  throw new Error('Refusing to write outside the repository dist directory.')
}

await rm(output, { recursive: true, force: true })
await mkdir(output, { recursive: true })

for (const directory of ['images', 'content-pool/packs', 'design']) {
  await mkdir(path.join(output, directory), { recursive: true })
}

await cp(path.join(source, 'index.html'), path.join(output, 'index.html'))
await cp(path.join(source, 'content-pool/registry.generated.js'), path.join(output, 'content-pool/registry.generated.js'))
await cp(path.join(source, 'images'), path.join(output, 'images'), { recursive: true })
await cp(path.join(source, 'design/home-tab-ambient.jpg'), path.join(output, 'design/home-tab-ambient.jpg'))
await cp(path.join(source, 'design/mobile-swipe-motion-comparison.html'), path.join(output, 'design/mobile-swipe-motion-comparison.html'))

const packsRoot = path.join(source, 'content-pool/packs')
for (const entry of await readdir(packsRoot, { withFileTypes: true })) {
  if (!entry.isDirectory()) continue
  const sourceImages = path.join(packsRoot, entry.name, 'images')
  try {
    if ((await stat(sourceImages)).isDirectory()) {
      await cp(sourceImages, path.join(output, 'content-pool/packs', entry.name, 'images'), { recursive: true })
    }
  } catch (error) {
    if (error.code !== 'ENOENT') throw error
  }
}

await cp(path.join(repoRoot, 'scripts/cloudflare-preview-headers'), path.join(output, '_headers'))
console.log(`Static preview prepared at ${path.relative(repoRoot, output)}`)
