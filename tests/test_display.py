import tempfile
import unittest
from pathlib import Path
from unittest import mock

from display import manager


class DisplayStateTests(unittest.TestCase):
    def _patched(self, root: Path):
        state_path = root / "display.json"
        legacy = root / "legacy.json"
        return mock.patch.multiple(
            manager,
            DISPLAY_ROOT=root,
            DISPLAY_STATE_PATH=state_path,
            LEGACY_STATE_PATH=legacy,
        )

    def test_default_state_when_absent(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            with self._patched(Path(d)):
                state = manager.load_state()
        self.assertEqual(state["external_prep_do"], "")
        self.assertFalse(state["prefer_steamgriddb"])

    def test_set_and_get_prep_scripts_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            with self._patched(Path(d)):
                manager.set_external_prep_scripts("/bin/do.sh", "/bin/undo.sh")
                self.assertTrue(manager.has_external_prep_scripts())
                cmds = manager.get_external_prep_commands()
        self.assertEqual(cmds, [{"do": "/bin/do.sh", "undo": "/bin/undo.sh"}])

    def test_no_scripts_means_empty_commands(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            with self._patched(Path(d)):
                self.assertFalse(manager.has_external_prep_scripts())
                self.assertEqual(manager.get_external_prep_commands(), [])

    def test_prefer_steamgriddb_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            with self._patched(Path(d)):
                manager.set_prefer_steamgriddb(True)
                self.assertTrue(manager.get_prefer_steamgriddb())


if __name__ == "__main__":
    unittest.main()
