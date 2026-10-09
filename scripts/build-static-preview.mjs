import { cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { execFileSync } from 'node:child_process'
import { runInNewContext } from 'node:vm'

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const source = path.join(repoRoot, 'products/distribution/reader-web')
const output = path.resolve(repoRoot, 'dist/cloudflare-preview')

execFileSync(process.execPath, [path.join(repoRoot, 'scripts/register-distribution-content.mjs'), '--check'], { stdio: 'inherit' })

if (!output.startsWith(path.join(repoRoot, 'dist') + path.sep)) {
  throw new Error('Refusing to write outside the repository dist directory.')
}

await rm(output, { recursive: true, force: true })
await mkdir(output, { recursive: true })

for (const directory of ['content-pool/packs', 'design']) {
  await mkdir(path.join(output, directory), { recursive: true })
}
await mkdir(path.join(output, 'content-pool/stories'), { recursive: true })

await cp(path.join(source, 'index.html'), path.join(output, 'index.html'))
const registrySource = await readFile(path.join(source, 'content-pool/registry.generated.js'), 'utf8')
const registryContext = { window: {} }
runInNewContext(registrySource, registryContext, { timeout: 1000 })
const runtimeWorlds = registryContext.window.InformationRainContentRegistry.worlds.map(world => {
  const image = world.image.replace(/\.(?:jpe?g|png)$/i, '.webp')
  return {
    ...world,
    image,
    thumbnail: image.replace(/\.webp$/i, '-thumb.webp'),
    storyUrl: `./content-pool/stories/${world.id}.json`,
    data: undefined,
  }
})
for (const world of registryContext.window.InformationRainContentRegistry.worlds) {
  await writeFile(path.join(output, 'content-pool/stories', `${world.id}.json`), JSON.stringify(world.data))
}
await writeFile(
  path.join(output, 'content-pool/registry.generated.js'),
  `window.InformationRainContentRegistry = ${JSON.stringify({ schemaVersion: 1, worlds: runtimeWorlds })};\n`,
)
await cp(path.join(source, 'design/home-tab-ambient.jpg'), path.join(output, 'design/home-tab-ambient.jpg'))
await cp(path.join(source, 'design/mobile-swipe-motion-comparison.html'), path.join(output, 'design/mobile-swipe-motion-comparison.html'))
await cp(path.join(source, 'design/mobile-swipe-motion-gifs'), path.join(output, 'design/mobile-swipe-motion-gifs'), { recursive: true })

execFileSync('python', [
  path.join(repoRoot, 'scripts/optimize-preview-images.py'),
  path.join(source, 'content-pool/packs'),
  path.join(output, 'content-pool/packs'),
], { stdio: 'inherit' })

await cp(path.join(repoRoot, 'scripts/cloudflare-preview-headers'), path.join(output, '_headers'))
console.log(`Static preview prepared at ${path.relative(repoRoot, output)}`)
