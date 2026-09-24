import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { dirname, extname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8' };
const port = Number(process.env.INFORMATION_RAIN_PORT || 4173);

createServer(async (request, response) => {
  try {
    const url = new URL(request.url, `http://${request.headers.host || 'localhost'}`);
    const pathname = decodeURIComponent(url.pathname === '/' ? '/index.html' : url.pathname);
    const path = resolve(root, `.${pathname}`);
    if (!path.startsWith(root + sep) || !types[extname(path)]) {
      response.writeHead(404).end('Not found');
      return;
    }
    const file = await readFile(path);
    response.writeHead(200, { 'Content-Type': types[extname(path)], 'Cache-Control': 'no-store' }).end(file);
  } catch {
    response.writeHead(404).end('Not found');
  }
}).listen(port, '127.0.0.1', () => {
  process.stdout.write(`Information Rain Demo: http://127.0.0.1:${port}/\n`);
});
