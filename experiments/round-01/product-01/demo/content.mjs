const choice = (id, label, hint, to, effect) => ({ id, label, hint, to, effect });

const openScenes = {
  window: {
    eyebrow: '夜色 / 01',
    title: '每一扇亮着的窗，都像一条没有说完的消息。',
    body: '雨停后，街道仍在反光。对面有人把一盏灯留到很晚；路口的红灯依次亮起；更远处，一列车从楼群之间经过。你可以只看这一刻，也可以顺着任何一处细节走过去。',
    rule: '这里的方向会留在原处。回来时，没走过的仍可进入。',
    choices: [
      choice('person', '楼下的人', '那盏灯究竟为谁亮着？', 'person'),
      choice('pattern', '街道的规律', '每个路口仿佛在轮流说话。', 'pattern'),
      choice('horizon', '更远的一刻', '列车经过时，另一座城在做什么？', 'horizon'),
    ],
  },
  person: {
    eyebrow: '夜色 / 人', title: '他在门口站了七分钟，始终没有按铃。',
    body: '便利店的玻璃替他照亮半张脸。他看了三次手机，最后买了一瓶水。窗边的灯还亮着，但这段观察没有告诉你两者是否有关。',
    rule: '这是可继续探索的观察，不会封闭旧方向。',
    choices: [choice('person-detail', '跟上这条线索', '看看他最后去了哪里。', 'detail'), choice('person-window', '回到窗边', '重新看另外的亮处。', 'window')],
  },
  pattern: {
    eyebrow: '夜色 / 规律', title: '红灯把一条街切成了几段不同的寂静。',
    body: '出租车在第一段停下，清洁车穿过第二段。你以为自己找到了重复的节奏，却看见第三个路口今晚一直是绿灯。',
    rule: '你可以继续这条观察，也可以回到最初的窗边。',
    choices: [choice('pattern-detail', '追问例外', '为什么第三个路口不同？', 'detail'), choice('pattern-window', '回到窗边', '未选方向还在。', 'window')],
  },
  horizon: {
    eyebrow: '夜色 / 远处', title: '列车驶进隧道的一瞬，城市的边界突然消失。',
    body: '车窗里有人抬头，像刚刚错过一个站名。远处的事情未必和你眼前相连，但它让这片夜色多了一种尺度。',
    rule: '远行不会删除原处的其他可能。',
    choices: [choice('horizon-detail', '沿列车继续', '它会停在哪里？', 'detail'), choice('horizon-window', '回到窗边', '去看另一条方向。', 'window')],
  },
  detail: {
    eyebrow: '夜色 / 细节', title: '新的细节没有给出答案，却改变了你想问的问题。',
    body: '有人关灯，有车驶过，有个例外留在视野里。你走过的路线会被记下；还没走过的方向不会因为这一步被替你取消。',
    rule: '这段内容仍允许从旧观察继续分叉。',
    choices: [choice('detail-window', '回到窗边', '另选一条路。', 'window'), choice('detail-pattern', '看街道的规律', '从另一处接近问题。', 'pattern')],
  },
};

const blackoutScenes = {
  countdown: {
    eyebrow: '停电 / 倒计时', title: '整条街只剩下三分钟电。',
    body: '控制室里有一个开关、一份尚未读完的记录，还有通往楼梯的门。你只能在这一刻做一次决定；之后仍能回看，但不能让这三分钟重来。',
    rule: '选定一条后，事件前的其他动作不再可执行。',
    choices: [
      choice('switch', '切断外侧供电', '先保住医院这边。', 'after-switch', 'seal'),
      choice('wait', '再读一页记录', '可能找到更准确的分配方式。', 'after-wait', 'seal'),
      choice('leave', '先去楼梯间', '确认里面是否还有人。', 'after-leave', 'seal'),
    ],
  },
  'after-switch': { eyebrow: '停电 / 后果', title: '医院的灯没有灭，街口却暗了下来。', body: '远处传来一阵短促的欢呼，随后是更长的寂静。你完成了一次取舍，不知道街口还有谁正在等电。', rule: '旧倒计时可回看；下一步只能从这个后果出发。', choices: [choice('switch-witness', '去街口看', '看看这次选择落在谁身上。', 'witness'), choice('switch-record', '检查记录', '理解刚才的代价。', 'record')] },
  'after-wait': { eyebrow: '停电 / 后果', title: '记录读完时，整条街同时黑了。', body: '最后一行写着“备用回路已停用”。你获得了更完整的信息，也失去了刚才的三分钟。', rule: '旧倒计时可回看；不能回到当时改选。', choices: [choice('wait-witness', '去街口看', '黑暗中发生了什么？', 'witness'), choice('wait-record', '检查记录', '那行字是谁写下的？', 'record')] },
  'after-leave': { eyebrow: '停电 / 后果', title: '楼梯间有人回应了你，控制室的灯却熄灭了。', body: '你扶着一个陌生人走下半层台阶。供电决定已经不再由你作出；此刻需要的是另一种行动。', rule: '旧倒计时可回看；不能从旧位置重选。', choices: [choice('leave-witness', '带他到街口', '寻找下一处光亮。', 'witness'), choice('leave-record', '询问他看见什么', '补全刚才缺失的信息。', 'record')] },
  witness: { eyebrow: '停电 / 街口', title: '同一片黑暗里，人们看见了不同的结果。', body: '有人举起手机照路，有人开门借出手电。你的那一步已写进现在，接下来仍有新的路。', rule: '历史只保留事实，不提供重来按钮。', choices: [choice('witness-record', '核对记录', '寻找另一层解释。', 'record'), choice('witness-stay', '留在街口', '观察人们如何应对。', 'street')] },
  record: { eyebrow: '停电 / 记录', title: '纸上的系统图比现场整齐得多。', body: '一条断开的线旁边写了日期，却没有写是谁做的决定。真正发生的事仍在街上继续。', rule: '这里只允许向发生后的现场继续。', choices: [choice('record-witness', '去街口', '把纸面和现实对照。', 'witness'), choice('record-street', '沿线路走', '查看下一处节点。', 'street')] },
  street: { eyebrow: '停电 / 此刻', title: '人群开始自发传递光。', body: '三分钟前的选项已经不存在。现在的行动仍有很多，但它们属于这个被改变后的城市。', rule: '事件没有被撤销；从当前状态继续。', choices: [choice('street-witness', '回到街口', '看看人群的变化。', 'witness'), choice('street-record', '再看记录', '寻找原因。', 'record')] },
};

const signalPairs = [
  [['signal-0-a', '一段失真的访谈', '有人在杂音里重复同一个地名。', 'signal-a'], ['signal-0-b', '一封未寄的来信', '信纸上只有收件人的名字。', 'signal-b']],
  [['signal-1-a', '港口传来的天气', '今夜的风改变了航线。', 'signal-a'], ['signal-1-b', '一个临时频道', '频道号只保留到天亮。', 'signal-b']],
  [['signal-2-a', '清晨第一班车', '有人在站台播报失物。', 'signal-a'], ['signal-2-b', '旧楼里的回声', '昨天的录音在今天被重新听见。', 'signal-b']],
];

function signalScene(state, node) {
  if (node === 'radio') {
    const pair = signalPairs[state.wave % signalPairs.length];
    return {
      eyebrow: `凌晨电台 / 第 ${state.wave + 1} 次接收`,
      title: state.wave === 0 ? '旋钮停在两段尚未消失的声音之间。' : '你又回到频段，空气里已经是新的声音。',
      body: state.wave === 0 ? '窗外尚未天亮。两个信号同时进入耳机，你可以追听其中一段。它们不承诺一直存在。' : '刚才的信号已随时间滑走。轨迹仍记得它们，但眼前能进入的是此刻接收到的内容。',
      rule: '回到当前频段时重新接收。旧快照可看，过期信号不能再进入。',
      choices: pair.map(([id, label, hint, to]) => choice(id, label, hint, to, 'advance-wave')),
    };
  }
  if (node === 'archive') return { eyebrow: '凌晨电台 / 留声', title: '录音替你留住了声音，却留不住当时的入口。', body: '你可以知道自己听过什么；如果想继续听，必须回到正在播出的频段。', rule: '历史内容可辨认，但旧信号已经失效。', choices: [choice('archive-live', '回到当前频段', '接收正在出现的信号。', 'radio'), choice('archive-detail', '再听一个细节', '留在这段录音中。', 'signal-a')] };
  const side = node === 'signal-a' ? '左侧' : '右侧';
  return {
    eyebrow: `凌晨电台 / ${side}信号`,
    title: state.wave === 1 ? (node === 'signal-a' ? '地名在杂音里一再出现。' : '信封上没有邮戳。') : `第 ${state.wave} 次接收，把你带到另一段声音。`,
    body: state.wave === 1 ? (node === 'signal-a' ? '说话的人停顿了很久，像在等另一个人纠正自己。信号开始变弱。' : '读信的人只念了开头，就被一阵风声盖住。你不知道他是否会继续。') : '这一段并不替代过去听见的内容。它属于现在的频段，也会在你离开后成为一条记录。',
    rule: '继续追听或回到当前频段；旧频段不会重播。',
    choices: [choice(`${node}-live`, '回到当前频段', '看看现在有什么声音。', 'radio'), choice(`${node}-archive`, '留住这一段', '在轨迹里再看它。', 'archive')],
  };
}

export const worlds = {
  open: {
    name: '窗边', subtitle: '方向保留', marker: '01 / 可改选',
    summary: '走远后还能回来，进入当时没选的地方。',
    initial: 'window', initialState: () => ({}),
    scene: (_state, node) => openScenes[node],
    apply: () => {},
    canChooseFromHistory: () => true,
    historyNote: '这片内容允许从旧位置继续走。',
  },
  blackout: {
    name: '停电', subtitle: '后果留存', marker: '02 / 只回看',
    summary: '能看见当时的选择，但不能重做已发生的事。',
    initial: 'countdown', initialState: () => ({ sealed: false }),
    scene: (_state, node) => blackoutScenes[node],
    apply: (state, selected) => { if (selected.effect === 'seal') state.sealed = true; },
    canChooseFromHistory: () => false,
    historyNote: '这是当时的记录。事件已发生，旧动作不可重做。',
  },
  signal: {
    name: '凌晨电台', subtitle: '方向更新', marker: '03 / 会失效',
    summary: '回到正在播出的频段，旧信号消失，新信号出现。',
    initial: 'radio', initialState: () => ({ wave: 0 }),
    scene: signalScene,
    apply: (state, selected) => { if (selected.effect === 'advance-wave') state.wave += 1; },
    canChooseFromHistory: () => false,
    historyNote: '这是当时收到的信号。请从当前内容回到正在播出的频段。',
  },
};
