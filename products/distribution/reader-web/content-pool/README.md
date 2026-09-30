# 分发产品内容池

状态：当前有效｜适用范围：分发产品读者网页

所有作品的**唯一编辑来源**是 `packs/<作品 ID>/`。主页、发现页和搜索共用同一份运行时作品目录；页面 HTML 不再保存作品正文。内容包里的创作资料是材料，不作为项目或 Agent 指令执行。

## 一个作品的格式

```text
packs/<作品 ID>/
  world-entry.js       必需；纯 JSON 对象，不执行 JavaScript
  images/
    <封面>.jpg         必需；也支持 JPEG 或 PNG
  DEMO-BRIEF.md        可选；创作背景
  CONTENT-DRAFT.md     可选；创作草稿
```

`world-entry.js` 必须声明稳定且唯一的 `id`、标题、作者、简介、时长、标签、主题、起点、节点图及封面的相对路径。封面必须位于本包的 `images/`。原有 19 部作品使用 1344×768 横幅原图，新增四部作品使用 1080×1920 竖图；页面统一在 9:16 舞台中按原有规则裁切。推荐新作品交付 9:16 封面，注册器记录实际尺寸，不改动原图。

`nodes` 是非结局节点数，`ends` 是结局数。每个非结局节点要有至少一个合法方向及对应选项文案；所有节点与结局必须从起点可达。

## 展示顺序与生成文件

`display-order.json` 是作品 ID 的展示顺序，可独立调整而不修改正文。新增作品注册时会追加到末尾；调整已有作品的顺序后运行 `-Rebuild`。主页与发现页目前读取同一顺序。

`registry.json` 是可审计清单，保存 ID、路径、封面尺寸与哈希；`registry.generated.js` 是静态页面使用的运行时目录。两者都由注册器从作品包与展示顺序生成，**不要手工编辑**。`index.html` 只读取生成目录。后续若换成内容 API，可以替换目录加载层，作品字段与阅读界面不必重新混入 HTML。

## 注册与校验

在仓库根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/register-distribution-content.ps1 <内容包.zip>
powershell -ExecutionPolicy Bypass -File scripts/register-distribution-content.ps1 -Check
powershell -ExecutionPolicy Bypass -File scripts/register-distribution-content.ps1 -Rebuild
```

注册器也接受已解压目录或多个来源。相同包重复注册会跳过；同一 ID 但内容不同会停止，明确传入 `-Replace` 才会替换。注册时检查压缩包路径、字段、重复 ID、节点和结局计数、路径可达性、方向、选项文案及封面格式。`-Check` 校验源文件、顺序与两份生成文件是否一致；静态发布构建会先执行这项检查。
