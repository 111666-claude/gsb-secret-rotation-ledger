"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "idem":
        state = core.new_ledger("api", 10)
        counter = core.Counter()
        core.rotate(state, 0, "r1", counter)
        core.rotate(state, 0, "r1", counter)
        _line({"versions": len(state["versions"])})
        return 0
    if name == "overlap":
        state = core.new_ledger("api", 10)
        counter = core.Counter()
        core.rotate(state, 0, "r1", counter)
        core.rotate(state, 5, "r2", counter)
        _line({"active": core.active_at(state, 5, core.Counter())})
        return 0
    if name == "expire":
        state = core.new_ledger("api", 10)
        counter = core.Counter()
        core.rotate(state, 0, "r1", counter)
        core.rotate(state, 5, "r2", counter)
        core.rotate(state, 14, "r3", counter)
        _line({"active": core.active_at(state, 14, core.Counter())})
        return 0
    if name == "future":
        state = core.new_ledger("api", 10)
        counter = core.Counter()
        core.rotate(state, 0, "r1", counter)
        core.rotate(state, 5, "r2", counter)
        _line({"active": core.active_at(state, 3, core.Counter())})
        return 0
    if name == "work":
        state = core.new_ledger("api", 10)
        counter = core.Counter()
        for i in range(2000):
            core.rotate(state, i, "r%04d" % i, counter)
        _line({"rotations": 2000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
