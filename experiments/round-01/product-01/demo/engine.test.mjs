import test from 'node:test';
import assert from 'node:assert/strict';
import { DemoSession } from './engine.mjs';
import { worlds } from './content.mjs';

test('each content starts with multiple reachable choices', () => {
  for (const id of ['open', 'blackout', 'signal']) {
    const session = new DemoSession(id);
    assert.ok(session.getView().entry.scene.choices.length >= 2);
    assert.equal(session.getView().canAct, true);
  }
});

test('old unchosen direction remains executable only when the content permits it', () => {
  const session = new DemoSession('open');
  const original = session.getView().entry.scene.choices.map((item) => item.id);
  session.choose(original[0]);
  session.show(0);
  assert.equal(session.getView().canAct, true);
  session.choose(original[1]);
  assert.equal(session.history.length, 3);
  assert.equal(session.history[2].fromIndex, 0);
  assert.equal(session.history[2].via, original[1]);
  assert.deepEqual(session.history[0].scene.choices.map((item) => item.id), original);
});

test('irreversible event keeps a historical snapshot but forbids replay', () => {
  const session = new DemoSession('blackout');
  const oldChoices = session.getView().entry.scene.choices.map((item) => item.id);
  session.choose('switch');
  assert.equal(session.getView().state.sealed, true);
  session.show(0);
  assert.deepEqual(session.getView().entry.scene.choices.map((item) => item.id), oldChoices);
  assert.equal(session.getView().canAct, false);
  assert.throws(() => session.choose('wait'), /只可回看/);
  session.resume();
  assert.equal(session.getView().isCurrent, true);
  assert.ok(session.getView().entry.scene.choices.every((item) => !oldChoices.includes(item.id)));
});

test('live signal changes on a content-defined revisit and old signal expires', () => {
  const session = new DemoSession('signal');
  const oldChoices = session.getView().entry.scene.choices.map((item) => item.id);
  session.choose(oldChoices[0]);
  session.choose('signal-a-live');
  const newChoices = session.getView().entry.scene.choices.map((item) => item.id);
  assert.notDeepEqual(newChoices, oldChoices);
  assert.equal(session.getView().state.wave, 1);
  session.show(0);
  assert.deepEqual(session.getView().entry.scene.choices.map((item) => item.id), oldChoices);
  assert.equal(session.getView().canAct, false);
  assert.throws(() => session.choose(oldChoices[1]), /只可回看/);
  session.resume();
  assert.deepEqual(session.getView().entry.scene.choices.map((item) => item.id), newChoices);
});

test('unknown or stale choices cannot bypass the current content', () => {
  const session = new DemoSession('open');
  assert.throws(() => session.choose('switch'), /没有可执行的方向/);
  assert.throws(() => session.show(-1), RangeError);
});

test('reachable content links remain valid across several moves', () => {
  for (const world of Object.values(worlds)) {
    const queue = [{ state: world.initialState(), node: world.initial, depth: 0 }];
    while (queue.length) {
      const { state, node, depth } = queue.shift();
      const scene = world.scene(state, node);
      assert.ok(scene, `missing scene ${node}`);
      assert.ok(Array.isArray(scene.choices));
      assert.equal(new Set(scene.choices.map((item) => item.id)).size, scene.choices.length);
      if (depth === 4) continue;
      for (const item of scene.choices) {
        const nextState = structuredClone(state);
        world.apply(nextState, item);
        queue.push({ state: nextState, node: item.to, depth: depth + 1 });
      }
    }
  }
});
