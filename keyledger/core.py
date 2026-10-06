"""版本登记与有效判定。"""

import json


class Counter:
    """记录台账操作里做过的比较次数。"""

    def __init__(self):
        self.scanned = 0


def new_ledger(name, window):
    return {
        "name": name,
        "window": window,
        "versions": [{"id": 1, "created": 0, "retired": None}],
        "rotations": {},
    }


def save(state, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def rotate(state, at, rid, counter):
    """登记一次轮换，返回新版本号。"""
    rotations = state["rotations"]
    if rid in rotations:
        return rotations[rid]
    versions = state["versions"]
    counter.scanned += 1
    prev = versions[-1]
    prev["retired"] = at + state["window"]
    if len(versions) >= 2:
        counter.scanned += 1
        versions[-2]["retired"] = prev["created"]
    new_id = prev["id"] + 1
    versions.append({"id": new_id, "created": at, "retired": None})
    rotations[rid] = new_id
    return new_id


def active_at(state, at, counter):
    """查询某时刻的有效版本号。"""
    out = []
    for v in state["versions"]:
        counter.scanned += 1
        if v["created"] > at:
            continue
        if v["retired"] is not None and v["retired"] <= at:
            continue
        out.append(v["id"])
    return out
