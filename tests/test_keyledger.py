import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from keyledger import core


class KeyledgerTest(unittest.TestCase):
    def test_new_ledger_has_one_version(self):
        state = core.new_ledger("api", 10)
        self.assertEqual(len(state["versions"]), 1)
        self.assertEqual(state["versions"][0]["id"], 1)

    def test_rotate_appends_version(self):
        state = core.new_ledger("api", 10)
        core.rotate(state, 0, "r1", core.Counter())
        self.assertEqual(len(state["versions"]), 2)

    def test_rotate_returns_new_id(self):
        state = core.new_ledger("api", 10)
        self.assertEqual(core.rotate(state, 0, "r1", core.Counter()), 2)

    def test_newest_is_active(self):
        state = core.new_ledger("api", 10)
        core.rotate(state, 0, "r1", core.Counter())
        self.assertIn(2, core.active_at(state, 0, core.Counter()))

    def test_version_fields(self):
        state = core.new_ledger("api", 10)
        for v in state["versions"]:
            for field in ("id", "created", "retired"):
                self.assertIn(field, v)

    def test_save_load_roundtrip(self):
        import tempfile

        state = core.new_ledger("api", 10)
        core.rotate(state, 0, "r1", core.Counter())
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        try:
            core.save(state, path)
            self.assertEqual(len(core.load(path)["versions"]), 2)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
