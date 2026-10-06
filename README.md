# secret-rotation-ledger

密钥轮换台账：按轮换单号登记版本，落在一个 JSON 文件里。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m keyledger init --state k.json --secret api --window 10
python3 -m keyledger rotate --state k.json --at 0 --rid r1
python3 -m keyledger active --state k.json --at 5
python3 -m keyledger demo --name overlap
```

## 口径

- **双活**：一次轮换后，新旧两个版本同时有效；新版本生效满 `window` 后旧版本才退场。
- **更替深度**：被更新版本取代两次的版本立即退场，任何时刻有效版本不超过两个。
- **幂等**：同一个轮换单号重复执行只产生一个版本，重复执行不改动台账。
- **时间**：只把创建时间不晚于查询时刻的版本纳入有效判断。

## 不变量

- 台账里版本号单调递增，轮换单号到版本号一一对应。
- 任一时刻有效版本不超过两个；退场的版本不再回到有效列表。
- `scanned` 不随轮换次数平方级放大：两千次轮换的 `scanned` 不超过 6000。

## 输出契约

`rotate` 打印新版本号；`active` 打印一行 JSON，键 `active` 是有效版本号升序列表。
状态文件键固定为 `name` / `window` / `versions` / `rotations`，版本项含 `id` / `created` / `retired`。
`demo --name=...` 打印一行 JSON 汇总，常见字段 `versions` / `active` / `scanned`。
