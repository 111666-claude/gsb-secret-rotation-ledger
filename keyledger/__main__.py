"""命令行入口。"""

import argparse
import json

from . import core, samples


def main(argv=None):
    ap = argparse.ArgumentParser(prog="keyledger")
    sub = ap.add_subparsers(dest="cmd")

    p_init = sub.add_parser("init")
    p_init.add_argument("--state", required=True)
    p_init.add_argument("--secret", required=True)
    p_init.add_argument("--window", type=int, required=True)

    p_rot = sub.add_parser("rotate")
    p_rot.add_argument("--state", required=True)
    p_rot.add_argument("--at", type=int, required=True)
    p_rot.add_argument("--rid", required=True)

    p_act = sub.add_parser("active")
    p_act.add_argument("--state", required=True)
    p_act.add_argument("--at", type=int, required=True)

    p_demo = sub.add_parser("demo")
    p_demo.add_argument("--name", required=True)

    args = ap.parse_args(argv)

    if args.cmd == "init":
        core.save(core.new_ledger(args.secret, args.window), args.state)
        print("ok")
        return 0
    if args.cmd == "rotate":
        state = core.load(args.state)
        vid = core.rotate(state, args.at, args.rid, core.Counter())
        core.save(state, args.state)
        print(vid)
        return 0
    if args.cmd == "active":
        state = core.load(args.state)
        active = core.active_at(state, args.at, core.Counter())
        print(json.dumps({"active": active}, ensure_ascii=False))
        return 0
    if args.cmd == "demo":
        return samples.run(args.name)

    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
