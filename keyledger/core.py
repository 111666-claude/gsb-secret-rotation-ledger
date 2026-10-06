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
    """登记一次轮换，返回新版本号。

    同一轮换单号幂等：重复执行不改台账，直接返回原版本号。
    新版本生效满 window 后旧版本才退场；被取代两次的版本立即退场。
    只触碰台账尾部，比较次数为常数。
    """
    counter.scanned += 1
    existing = state["rotations"].get(rid)
    if existing is not None:
        return existing

    versions = state["versions"]
    window = state["window"]

    new_id = versions[-1]["id"] + 1
    prev = versions[-1]
    if prev["retired"] is None:
        prev["retired"] = at + window

    counter.scanned += 1
    if len(versions) >= 2:
        grand = versions[-2]
        if grand["retired"] is not None and grand["retired"] > at:
            grand["retired"] = at

    versions.append({"id": new_id, "created": at, "retired": None})
    state["rotations"][rid] = new_id
    return new_id


def active_at(state, at, counter):
    """查询某时刻的有效版本号（升序）。

    只纳入创建时间不晚于查询时刻的版本；最新版本恒有效，其前一版本
    仅在双活窗口内有效；已被取代两次的版本不再回到有效列表。
    """
    versions = state["versions"]
    window = state["window"]

    i = len(versions) - 1
    while i >= 0:
        counter.scanned += 1
        if versions[i]["created"] <= at:
            break
        i -= 1
    if i < 0:
        return []

    ids = []
    if i >= 1:
        counter.scanned += 1
        if i == len(versions) - 1 and at < versions[i]["created"] + window:
            ids.append(versions[i - 1]["id"])
    ids.append(versions[i]["id"])
    return ids
