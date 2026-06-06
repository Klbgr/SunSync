import unittest

from launchers import eden, faugus


class EdenBaseGameTests(unittest.TestCase):
    def test_update_and_dlc_rejected(self) -> None:
        self.assertFalse(eden._is_base_game_file("Game [update].nsp"))
        self.assertFalse(eden._is_base_game_file("Game [DLC].nsp"))

    def test_non_base_title_id_rejected(self) -> None:
        # Title IDs not ending in 000 are updates/DLC, not the base title.
        self.assertFalse(eden._is_base_game_file("Game [0100000000010800].nsp"))

    def test_base_title_id_accepted(self) -> None:
        self.assertTrue(eden._is_base_game_file("Game [0100000000010000].nsp"))

    def test_plain_name_accepted(self) -> None:
        self.assertTrue(eden._is_base_game_file("Some Game.xci"))


class FaugusParseBoolTests(unittest.TestCase):
    def test_truthy(self) -> None:
        for v in ("true", "1", "yes", "on", "True", '"true"'):
            self.assertTrue(faugus._parse_bool(v))

    def test_falsy(self) -> None:
        for v in ("false", "0", "no", "off"):
            self.assertFalse(faugus._parse_bool(v))

    def test_empty_and_unknown_are_none(self) -> None:
        self.assertIsNone(faugus._parse_bool(""))
        self.assertIsNone(faugus._parse_bool(None))
        self.assertIsNone(faugus._parse_bool("maybe"))

    def test_real_bool_passthrough(self) -> None:
        self.assertTrue(faugus._parse_bool(True))
        self.assertFalse(faugus._parse_bool(False))


if __name__ == "__main__":
    unittest.main()
