import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const folder = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(folder, 'index.html'), 'utf8');
const start = html.indexOf('function handleDirection(');
const end = html.indexOf('// 结局展示', start);
assert.ok(start >= 0 && end > start, '找不到方向处理函数');

const world = {
  data: {
    start: { exits: { left: 'missing', right: 'next' } },
    next: { text: '下一节点' },
  },
};
const events = [];
let swipeCleanupCount = 0;
let experienceState = 'worlds.reading.ready';
const context = {
  worlds: [world],
  currentWorldIndex: 0,
  currentNodeId: 'start',
  pathHistory: ['start'],
  stats: { totalSteps: 0 },
  el: { nodeLayer: { style: {} }, stage: { classList: { add() {}, remove() {} } } },
  createScreenSnapshot: () => ({}),
  clearSwipeFeedback: () => { swipeCleanupCount++; },
  createNodeTextExitCopy: () => {},
  animateScreenSnapshot: () => {},
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
context.handleDirection('left', {});
assert.equal(swipeCleanupCount, 1, '松手时分支目标失效，必须清除拖动快照');
experienceState = 'worlds.reading.typing';
context.handleDirection('right', {});
assert.equal(swipeCleanupCount, 2, '页面状态不再允许选择时，必须清除拖动快照');
experienceState = 'worlds.reading.ready';

context.handleDirection('right');
assert.equal(context.currentNodeId, 'next', '有效方向应正常进入目标节点');
assert.deepEqual([...context.pathHistory], ['start', 'next']);
assert.equal(context.stats.totalSteps, 1);
assert.deepEqual(events.slice(2), [
  ['state', 'MOVE'],
  ['saved'],
  ['state', 'NODE_READY'],
  ['render', 'next'],
]);

const scrollStart = html.indexOf('function resolveTextTouchScroll(');
const scrollEnd = html.indexOf('\n        }', scrollStart) + '\n        }'.length;
assert.ok(scrollStart >= 0 && scrollEnd > scrollStart, '找不到正文手势滚动判定');
const scrollContext = {};
runInNewContext(html.slice(scrollStart, scrollEnd), scrollContext);
const scrollIntoText = scrollContext.resolveTextTouchScroll(120, -60, 300);
assert.equal(scrollIntoText.handled, true, '正文未到边界时，上划应继续滚动正文');
assert.equal(scrollIntoText.scrollTop, 180);
assert.equal(scrollContext.resolveTextTouchScroll(300, -60, 300).handled, false, '正文到底后，上划应交给上方分支');
assert.equal(scrollContext.resolveTextTouchScroll(0, 60, 300).handled, false, '正文到顶后，下划应交给作品切换');
assert.equal(scrollContext.resolveTextTouchScroll(120, 60, 300).scrollTop, 60, '正文中下划应滚回前文');
assert.match(html, /\.node-text \{ max-height: min\(58%, calc\(100% - 7rem\)\); touch-action: none; \}/, '手机正文需要由应用接管纵向触摸，避免浏览器吞掉分支手势');
assert.match(html, /mobileUpChoice/, '手机界面必须显示上方分支的具体出口文案');
assert.match(html, /snapshotSlides\.replaceChildren\(currentSlide\)/, '过场快照只保留当前作品，避免复制整组封面');
assert.match(html, /snapshot\.querySelectorAll\('#particlesLayer \.particle'\)/, '过场快照不应复制持续动画的粒子');
assert.match(html, /animateScreenSnapshot\(swipeTransition\.snapshot, swipeTransition\.direction, \(\) => \{/, '世界切换的模糊背景与粒子应延后到过场结束');
assert.match(html, /hidden = !\(leftExit \|\| rightExit \|\| upExit\)/, '只有上方分支时也必须显示方向提示');
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
assert.match(html, /window\.InformationRainContentRegistry\?\.worlds/, '页面必须从内容注册表读取作品');
assert.match(html, /\.screen-snapshot\.is-light-flow::after/, '拖动快照应承载画面内的光流');
assert.match(html, /touchSnapshot\.classList\.add\('is-light-flow'\)/, '触摸分支拖动应启用光流效果');
assert.match(html, /--flow-x/, '光流应随横向拖动方向移动');
assert.match(html, /--flow-y/ , '上滑分支应沿纵向牵引光流');
assert.match(html, /if \(direction === 'down'\) \{[\s\S]*?remove\('is-light-flow'\)/, '下滑切换作品不得套用分支光流');
assert.match(html, /\.world-stage\.is-branch-dragging \.gesture-feedback \{ display: none; \}/, '拖动时不应出现浮动文字提示框');
assert.match(html, /e\.changedTouches\.length !== 1 \|\| e\.touches\.length !== 0/, '多点触摸结束时应取消当前导航手势');
assert.match(html, /const clearTouchGesture = \(\) => \{[\s\S]*?clearSwipeFeedback\(\);[\s\S]*?\};/, '取消/失效手势应统一清理拖动快照和状态');

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
