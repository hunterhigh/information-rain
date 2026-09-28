import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const folder = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(folder, 'index.html'), 'utf8');
const start = html.indexOf('function handleDirection(dir) {');
const end = html.indexOf('// 结局展示', start);
assert.ok(start >= 0 && end > start, '找不到方向处理函数');

const world = {
  data: {
    start: { exits: { left: 'missing', right: 'next' } },
    next: { text: '下一节点' },
  },
};
const events = [];
const context = {
  worlds: [world],
  currentWorldIndex: 0,
  currentNodeId: 'start',
  isAnimating: false,
  pathHistory: ['start'],
  stats: { totalSteps: 0 },
  el: { nodeLayer: { style: {} } },
  showToast: message => events.push(['toast', message]),
  saveStats: () => events.push(['saved']),
  renderNode: nodeId => events.push(['render', nodeId]),
  setTimeout: callback => { callback(); return 1; },
};
runInNewContext(html.slice(start, end), context);

context.handleDirection('left');
assert.equal(context.currentNodeId, 'start', '失效方向不能改变当前位置');
assert.deepEqual([...context.pathHistory], ['start'], '失效方向不能写入足迹');
assert.equal(context.stats.totalSteps, 0, '失效方向不能计入步数');
assert.deepEqual(events, [['toast', '此方向暂不可进入']], '失效方向应给出即时反馈');

context.handleDirection('right');
assert.equal(context.currentNodeId, 'next', '有效方向应正常进入目标节点');
assert.deepEqual([...context.pathHistory], ['start', 'next']);
assert.equal(context.stats.totalSteps, 1);
assert.deepEqual(events.slice(1), [['saved'], ['render', 'next']]);

console.log('方向导航：失效目标不再导致空白，有效目标仍可进入');
