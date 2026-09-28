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
let experienceState = 'worlds.reading.ready';
const context = {
  worlds: [world],
  currentWorldIndex: 0,
  currentNodeId: 'start',
  pathHistory: ['start'],
  stats: { totalSteps: 0 },
  el: { nodeLayer: { style: {} } },
  showToast: message => events.push(['toast', message]),
  saveStats: () => events.push(['saved']),
  renderNode: nodeId => events.push(['render', nodeId]),
  experienceMatches: value => experienceState === value || experienceState.startsWith(`${value}.`),
  sendExperience: event => {
    events.push(['state', event]);
    if (event === 'MOVE') experienceState = 'worlds.reading.transitioning';
    if (event === 'NODE_READY') experienceState = 'worlds.reading.typing';
  },
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
assert.deepEqual(events.slice(1), [
  ['state', 'MOVE'],
  ['saved'],
  ['state', 'NODE_READY'],
  ['render', 'next'],
]);

assert.match(html, /aspect-ratio:\s*9\s*\/\s*16/, '作品舞台必须保留 9:16 竖屏比例');
assert.match(html, /swiper@14\.2\.0/, 'Swiper 必须固定到已核验版本');
assert.match(html, /xstate@5\.33\.2/, 'XState 必须固定到稳定版本');
assert.doesNotMatch(html, /let wheelLocked\b/, '不应恢复固定时长的滚轮锁');
assert.doesNotMatch(html, /逐字显示|typeWriter\(|finishTypewriter|typeTimer/, '正文不应再使用逐字输出效果');
const renderNodeStart = html.indexOf('function renderNode(nodeId, animType = \'fade\') {');
const renderNodeEnd = html.indexOf('function updateDirBtn(', renderNodeStart);
assert.ok(renderNodeStart >= 0 && renderNodeEnd > renderNodeStart, '找不到节点渲染函数');
assert.match(html.slice(renderNodeStart, renderNodeEnd), /el\.nodeText\.textContent\s*=\s*node\.text/, '节点正文应一次性完整显示');
assert.match(html, /content-pool\/registry\.generated\.js/, '页面必须加载内容注册表');
assert.match(html, /worlds\.push\(world\)/, '注册内容必须进入统一作品池');

const profileStart = html.indexOf('function updateProfileStats() {');
const profileEnd = html.indexOf('function toggleTextSize() {', profileStart);
assert.ok(profileStart >= 0 && profileEnd > profileStart, '找不到记录页统计函数');
const profile = {
  worlds: [{ id: 'kept', title: '保留内容' }],
  stats: { exploredWorlds: ['kept', 'removed'] },
  getBookmarks: () => ['kept', 'removed'],
  getCollectedEndings: () => ['kept::end', 'removed::end'],
  getFootprints: () => [
    { worldId: 'removed', endingTitle: '旧结局', time: 1 },
    { worldId: 'kept', endingTitle: '新结局', time: 1 },
  ],
  el: {
    statWorlds: { textContent: '' },
    statEndings: { textContent: '' },
    statBookmarks: { textContent: '' },
    footprintList: { innerHTML: '' },
  },
};
runInNewContext(html.slice(profileStart, profileEnd), profile);
profile.updateProfileStats();
assert.equal(profile.el.statWorlds.textContent, 1);
assert.equal(profile.el.statEndings.textContent, 1);
assert.equal(profile.el.statBookmarks.textContent, 1);
assert.match(profile.el.footprintList.innerHTML, /保留内容/);
assert.doesNotMatch(profile.el.footprintList.innerHTML, /未知内容|旧结局/);

console.log('方向导航与删选后的记录页：通过');
