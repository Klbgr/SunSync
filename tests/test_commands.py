import shlex
import unittest
from unittest import mock

from sunshine.sunshine import build_game_command


class BuildGameCommandTests(unittest.TestCase):
    @mock.patch("sunshine.sunshine.get_lutris_command", return_value="lutris")
    def test_lutris(self, _cmd) -> None:
        cmd = build_game_command("123", "Lutris")
        self.assertEqual(cmd, f"lutris {shlex.quote('lutris:rungameid/123')}")

    @mock.patch("sunshine.sunshine.get_heroic_command", return_value=("heroic", "native"))
    def test_heroic_runners(self, _cmd) -> None:
        for runner in ("legendary", "gog", "nile", "sideload"):
            cmd = build_game_command("appid", runner)
            uri = shlex.quote(f"heroic://launch/{runner}/appid")
            self.assertEqual(cmd, f"heroic {uri} --no-gui --no-sandbox")

    @mock.patch("sunshine.sunshine.get_steam_command", return_value="steam")
    def test_steam(self, _cmd) -> None:
        self.assertEqual(
            build_game_command("440", "Steam"), f"steam {shlex.quote('steam://run/440')}"
        )

    def test_ryubing_quotes_game_id(self) -> None:
        cmd = build_game_command("foo; rm -rf ~", "Ryubing")
        self.assertIsNotNone(cmd)
        # The metacharacters survive only inside a single-quoted argument.
        self.assertIn("'foo; rm -rf ~'", cmd)

    @mock.patch("sunshine.sunshine.get_eden_command", return_value="eden")
    def test_eden(self, _cmd) -> None:
        cmd = build_game_command("/games/x.nsp", "Eden")
        self.assertEqual(cmd, f"eden -f -g {shlex.quote('/games/x.nsp')}")

    @mock.patch("sunshine.sunshine.get_eden_command", return_value="")
    def test_eden_no_binary_returns_none(self, _cmd) -> None:
        self.assertIsNone(build_game_command("/games/x.nsp", "Eden"))

    @mock.patch("sunshine.sunshine.get_faugus_command", return_value="faugus-run")
    def test_faugus(self, _cmd) -> None:
        cmd = build_game_command("gid", {"type": "Faugus"})
        self.assertEqual(cmd, f"faugus-run --game {shlex.quote('gid')}")

    @mock.patch("sunshine.sunshine.get_retroarch_command", return_value="retroarch")
    def test_retroarch(self, _cmd) -> None:
        cmd = build_game_command(
            "/roms/game.zip", {"type": "RetroArch", "core_path": "/cores/snes9x.so"}
        )
        self.assertIsNotNone(cmd)
        self.assertIn(f"-L {shlex.quote('/cores/snes9x.so')}", cmd)
        self.assertIn(shlex.quote("/roms/game.zip"), cmd)

    @mock.patch("sunshine.sunshine.get_retroarch_command", return_value="retroarch")
    def test_retroarch_no_core_returns_none(self, _cmd) -> None:
        self.assertIsNone(build_game_command("/roms/game.zip", {"type": "RetroArch"}))

    def test_bottles_dict_quotes_both_fields(self) -> None:
        cmd = build_game_command("game'name", {"type": "Bottles", "bottle": "bottle'name"})
        self.assertIsNotNone(cmd)
        self.assertIn("bottles-cli", cmd)
        # shlex.quote escapes embedded single quotes as the '"'"' sequence.
        self.assertIn("'\"'\"'", cmd)

    def test_bottles_missing_bottle_returns_none(self) -> None:
        self.assertIsNone(build_game_command("prog", {"type": "Bottles", "bottle": ""}))

    def test_unknown_runner_returns_none(self) -> None:
        self.assertIsNone(build_game_command("x", "TotallyUnknownRunner"))


if __name__ == "__main__":
    unittest.main()
