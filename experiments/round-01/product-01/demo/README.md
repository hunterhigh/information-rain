# Information Rain · product-01 机制 Demo

状态：v0.1，已撤回为内部机制样本，不作为合格产品 Demo 试用。预写文字与确定性规则；无实时推荐、生成或外部服务。撤回原因见[决定 0005](../../../../docs/project/decisions/0005-content-first-demo.md)。

在仓库根目录运行：

```powershell
node experiments/round-01/product-01/demo/server.mjs
```

浏览器打开 <http://127.0.0.1:4173/>。手机可通过浏览器开发者工具切换手机尺寸；服务默认只监听本机，不对局域网开放。切换三段内容时各自进度保留；刷新页面清空，亦可点「重新开始这一段」。

自动检查：

```powershell
node --test experiments/round-01/product-01/demo/engine.test.mjs
```

以下路径仅供开发者复核旧机制，不代表产品体验：

1. 「窗边」→「楼下的人」→从足迹打开旧「窗边」→进入此前未选的「街道的规律」。
2. 「停电」→任一初始决定→打开旧「倒计时」；旧选项仍可见但不可执行。
3. 「凌晨电台」→任一信号→「回到当前频段」→打开旧「旋钮」；比较旧信号和现在的新信号。

`MECHANISM.md` 说明机制与边界，`AUTO-REVIEW.md` 记录自动检查及自评。三段短样本不是后续要求的十分钟正式内容体验。
