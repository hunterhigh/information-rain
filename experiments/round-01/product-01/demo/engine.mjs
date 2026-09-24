import { worlds } from './content.mjs';

function snapshot(world, state, node, fromIndex = null, via = null) {
  const scene = world.scene(state, node);
  if (!scene || !Array.isArray(scene.choices)) {
    throw new Error(`内容位置 ${node} 未提供有效内容`);
  }
  return { node, fromIndex, via, scene: structuredClone(scene) };
}

export class DemoSession {
  constructor(worldId) {
    const world = worlds[worldId];
    if (!world) throw new Error(`未知内容：${worldId}`);
    this.worldId = worldId;
    this.world = world;
    this.state = world.initialState();
    this.history = [snapshot(world, this.state, world.initial)];
    this.viewIndex = 0;
  }

  getView() {
    const entry = this.history[this.viewIndex];
    const currentIndex = this.history.length - 1;
    const isCurrent = this.viewIndex === currentIndex;
    return {
      entry,
      index: this.viewIndex,
      currentIndex,
      isCurrent,
      canAct: isCurrent || this.world.canChooseFromHistory(entry, this.state),
      selectedIds: this.history.filter((item) => item.fromIndex === this.viewIndex).map((item) => item.via),
      state: structuredClone(this.state),
    };
  }

  show(index) {
    if (!Number.isInteger(index) || index < 0 || index >= this.history.length) throw new RangeError('无效的轨迹位置');
    this.viewIndex = index;
    return this.getView();
  }

  resume() {
    this.viewIndex = this.history.length - 1;
    return this.getView();
  }

  choose(choiceId) {
    const view = this.getView();
    if (!view.canAct) throw new Error('这段历史只可回看，不能从此处行动');
    const selected = view.entry.scene.choices.find((item) => item.id === choiceId);
    if (!selected) throw new Error(`此处没有可执行的方向：${choiceId}`);
    const nextState = structuredClone(this.state);
    this.world.apply(nextState, selected, view.entry);
    const next = snapshot(this.world, nextState, selected.to, this.viewIndex, selected.id);
    this.state = nextState;
    this.history.push(next);
    this.viewIndex = this.history.length - 1;
    return this.getView();
  }
}
