import os
import tempfile
import unittest
from unittest import mock

from PIL import Image

from utils import images


class SteamCoverTests(unittest.TestCase):
    def test_grid_cover_found_in_any_root(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            grid = os.path.join(root, "userdata", "12345", "config", "grid")
            os.makedirs(grid)
            cover = os.path.join(grid, "440p.png")
            Image.new("RGB", (2, 2)).save(cover)
            with mock.patch.object(images, "_STEAM_ROOTS", [root]):
                found = images.get_steam_cover("440")
            self.assertEqual(found, cover)

    def test_librarycache_cover_found(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            cache = os.path.join(root, "appcache", "librarycache")
            os.makedirs(cache)
            cover = os.path.join(cache, "440_library_600x900.jpg")
            Image.new("RGB", (2, 2)).save(cover)
            with mock.patch.object(images, "_STEAM_ROOTS", [root]):
                found = images.get_steam_cover("440")
            self.assertEqual(found, cover)

    def test_no_cover_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            with mock.patch.object(images, "_STEAM_ROOTS", [root]):
                self.assertIsNone(images.get_steam_cover("999"))


class PrepareCoverTests(unittest.TestCase):
    def test_missing_source_returns_none(self) -> None:
        self.assertIsNone(images.prepare_sunshine_cover("/no/such.png", "Game"))
        self.assertIsNone(images.prepare_sunshine_cover(None, "Game"))

    def test_converts_to_png_in_covers_dir(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "src.webp")
            Image.new("RGB", (4, 4), "red").save(src)
            covers = os.path.join(d, "covers")
            with mock.patch.object(images, "get_covers_path", return_value=covers):
                out = images.prepare_sunshine_cover(src, "My Game")
            self.assertIsNotNone(out)
            self.assertTrue(out.endswith("my-game.png"))
            self.assertTrue(os.path.exists(out))


if __name__ == "__main__":
    unittest.main()
