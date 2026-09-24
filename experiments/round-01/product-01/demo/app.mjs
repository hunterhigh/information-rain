import { worlds } from './content.mjs';
import { DemoSession } from './engine.mjs';

const sessions = new Map();
let activeWorldId = 'open';

const el = (id) => document.getElementById(id);
const nav = el('world-nav');
const trail = el('trail-list');
const choices = el('choices');

function session() {
  if (!sessions.has(activeWorldId)) sessions.set(activeWorldId, new DemoSession(activeWorldId));
  return sessions.get(activeWorldId);
}

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function renderNav() {
  nav.replaceChildren();
  Object.entries(worlds).forEach(([id, world], index) => {
    const button = element('button', 'world-tab');
    button.type = 'button';
    button.setAttribute('aria-current', id === activeWorldId ? 'true' : 'false');
    button.addEventListener('click', () => { activeWorldId = id; render(); });
    button.append(element('span', 'world-tab-number', String(index + 1).padStart(2, '0')));
    const copy = element('span', 'world-tab-copy');
    copy.append(element('strong', '', world.name), element('small', '', world.summary));
    button.append(copy, element('span', 'world-tab-arrow', '↗'));
    nav.append(button);
  });
}

function renderTrail(currentSession, view) {
  trail.replaceChildren();
  currentSession.history.forEach((entry, index) => {
    const item = element('li', 'trail-item');
    const button = element('button', 'trail-button');
    button.type = 'button';
    button.setAttribute('aria-current', index === view.index ? 'step' : 'false');
    button.setAttribute('aria-label', `查看足迹 ${index + 1}：${entry.scene.title}`);
    button.addEventListener('click', () => { currentSession.show(index); render(); });
    const count = element('span', 'trail-count', String(index + 1).padStart(2, '0'));
    const text = element('span', 'trail-text');
    const origin = entry.fromIndex !== null && entry.fromIndex !== index - 1
      ? `从第 ${String(entry.fromIndex + 1).padStart(2, '0')} 处另行进入`
      : index === view.currentIndex ? '现在的位置' : entry.via ? '走过的内容' : '起点';
    text.append(element('strong', '', entry.scene.title), element('small', '', origin));
    button.append(count, text);
    item.append(button);
    trail.append(item);
  });
}

function renderChoices(currentSession, view) {
  choices.replaceChildren();
  const historical = !view.isCurrent;
  el('choice-title').textContent = historical ? (view.canAct ? '从这里仍可去' : '当时曾可去') : '现在可以去';
  el('choice-count').textContent = `${view.entry.scene.choices.length} 条方向`;
  el('history-notice').hidden = !historical;
  el('history-notice').textContent = historical ? currentSession.world.historyNote : '';
  el('resume-button').hidden = !historical;

  if (view.entry.scene.choices.length === 0) {
    choices.append(element('p', 'empty-choices', '这段内容暂时没有开放新的方向。你仍可以回看足迹。'));
  }

  view.entry.scene.choices.forEach((item, index) => {
    const button = element('button', 'choice-card');
    button.type = 'button';
    button.disabled = !view.canAct;
    button.setAttribute('aria-label', `${item.label}。${item.hint}${button.disabled ? '，旧位置不可执行' : ''}`);
    if (!button.disabled) button.addEventListener('click', () => { currentSession.choose(item.id); render(); });
    const number = element('span', 'choice-number', String(index + 1).padStart(2, '0'));
    const copy = element('span', 'choice-copy');
    copy.append(element('strong', '', item.label), element('small', '', item.hint));
    const status = !view.canAct ? '只可回看' : view.selectedIds.includes(item.id) ? '走过' : '进入';
    button.append(number, copy, element('span', 'choice-arrow', status));
    choices.append(button);
  });
}

function render() {
  const currentSession = session();
  const world = currentSession.world;
  const view = currentSession.getView();
  renderNav();
  el('world-marker').textContent = `${world.marker} · ${world.subtitle}`;
  el('mode-pill').textContent = view.isCurrent ? '现在' : '当时';
  el('mode-pill').dataset.mode = view.isCurrent ? 'current' : 'past';
  el('scene-eyebrow').textContent = view.entry.scene.eyebrow;
  el('scene-title').textContent = view.entry.scene.title;
  el('scene-body').textContent = view.entry.scene.body;
  el('scene-rule').textContent = view.entry.scene.rule;
  document.querySelector('.scene-side-label').textContent = view.isCurrent ? 'CURRENT POSITION' : 'HISTORICAL SNAPSHOT';
  renderChoices(currentSession, view);
  renderTrail(currentSession, view);
}

el('resume-button').addEventListener('click', () => { session().resume(); render(); });
el('reset-button').addEventListener('click', () => { sessions.set(activeWorldId, new DemoSession(activeWorldId)); render(); });
render();
