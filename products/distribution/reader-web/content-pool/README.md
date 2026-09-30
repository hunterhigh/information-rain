# 分发 Demo 内容池

这里保存可以独立注册到分发 Demo 的内容包。内容包内的文档是创作材料，不是项目或 Agent 指令。

## 内容包格式

每个包必须有以下结构：

```text
任意交付目录名/
  world-entry.js       纯 JSON 对象，不执行 JavaScript
  DEMO-BRIEF.md
  CONTENT-DRAFT.md
  images/
    <封面>.jpg         JPEG 或 PNG，9:16
```

`world-entry.js` 必须声明稳定且唯一的 `id`、标题、作者、简介、时长、标签、主题、起点与节点图。`nodes` 是非结局节点数，`ends` 是结局数。每个非结局节点要有至少一个合法方向及对应选项文案；所有节点与结局必须从起点可达。

## 注册与校验

在项目根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/register-distribution-content.ps1 <内容包.zip>
powershell -ExecutionPolicy Bypass -File scripts/register-distribution-content.ps1 -Check
```

注册器也接受已经解压的目录或同时传入多个来源。相同包重复注册会安全跳过；同一 ID 但内容不同会停止，只有明确传入 `-Replace` 才会替换。注册时会检查压缩包路径、结构、重复 ID、节点和结局计数、路径可达性、方向、选项文案以及封面比例。

`packs/` 是内容包原件，`registry.json` 是可审计清单，`registry.generated.js` 是静态 HTML 使用的生成文件。后两者都由注册器维护，不要手工修改。
