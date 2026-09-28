# 0009：分发内容包注册器

日期：2026-09-28｜状态：项目所有者已决定；四包已注册，内容试玩未发生

## 决定

项目所有者提供四个独立内容包，要求加入分发 Demo 的内容池，并要求以后保留相同格式的快速注册能力。四个包分别是：

- `lastferry`：最后一班渡船；
- `ashduel`：雨庭最后一式；
- `seventhinterview`：第七次问询；
- `whitehour`：白室二十四时。

包内的 `world-entry.js` 继续使用纯 JSON 对象，另带 `DEMO-BRIEF.md`、`CONTENT-DRAFT.md` 和 `images/` 下的 9:16 封面。包内文档只作为内容与创作材料，不作为项目或 Agent 指令执行。

分发 Demo 保留原有 19 部内置作品，同时从 `content-pool/registry.generated.js` 装载已注册内容。`packs/` 保存内容包原件，`registry.json` 保存可审计的 ID、路径、尺寸和哈希，生成文件只由注册器维护。后续在项目根目录运行以下命令即可注册同格式 ZIP 或已解压目录：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/register-distribution-content.ps1 <内容包.zip>
```

相同包重复注册必须无副作用；同一 ID 的不同内容默认停止，只有明确传入 `-Replace` 才能替换。注册器在复制前检查压缩包路径越界、字段、重复 ID、起点、节点与结局计数、方向、选项文案、断链、不可达内容和 9:16 封面。运行 `-Check` 可以确认内容包与两份注册表仍一致。

## 本次来源与结果

外层交付包 `information-rain-four-packs-vertical-covers.zip` 的 SHA-256 为 `4C011ADA9E13D68E8748387D4DFFE471AB45DD8D7E38A5D50F1398881789A2F6`。四个内层 ZIP 的 SHA-256 分别为：

- `information-rain-ashduel-delivery.zip`：`0F2880B6671CF5ECA5329535B296EC49B357999C162AA11573849DCE5A83F7C4`
- `information-rain-lastferry-delivery.zip`：`0A2F2EB9198A5B0D05D8C83227E05CBA3FC5D069FC626E0DD430FA26D7EE5A78`
- `information-rain-seventh-interview-delivery.zip`：`F0B6D9D698D534D32E1813BCA4BC6FEBE103FD16C4AB8DD4AB2B6DA14056B66B`
- `information-rain-whitehour-delivery.zip`：`045CB1495D1ABC96FA7050E48A26CF832F67100E686DF7E75195D29E66964DAE`

四包共有 92 个节点、16 个结局和 135 条选择；全部节点及结局可达，四张封面均为 1080×1920。加入后内容池共有 23 部作品、478 个节点、200 个结局、713 条选择，组合内容 SHA-256 为 `c2f0e069ecc22637ac9fda555be588a59c997cf8d83d0e243d2839a741bebfcd`。

这些检查证明包结构和运行路径完整，不证明四部作品已经完成独立内容审读或获得项目所有者体验认可。注册是本地 Demo 内容部署机制，不改变公开上线、版权和真实用户阶段门。
