import os
import tempfile
import unittest

from launchers import steam


class SteamVdfParsingTests(unittest.TestCase):
    def test_parse_vdf_value(self) -> None:
        self.assertEqual(steam.parse_vdf_value('\t\t"name"\t\t"Half-Life"'), "Half-Life")
        self.assertIsNone(steam.parse_vdf_value("not a kv line"))

    def test_parse_libraryfolders(self) -> None:
        content = '''"libraryfolders"
{
\t"0"
\t{
\t\t"path"\t\t"/home/u/.local/share/Steam"
\t}
\t"1"
\t{
\t\t"path"\t\t"/mnt/games/SteamLibrary"
\t}
}
'''
        with tempfile.TemporaryDirectory() as d:
            vdf = os.path.join(d, "libraryfolders.vdf")
            with open(vdf, "w") as f:
                f.write(content)
            paths = steam.parse_libraryfolders(vdf)
        self.assertEqual(
            paths, ["/home/u/.local/share/Steam", "/mnt/games/SteamLibrary"]
        )

    def test_parse_libraryfolders_missing(self) -> None:
        self.assertEqual(steam.parse_libraryfolders("/no/such/file.vdf"), [])

    def test_parse_appmanifest(self) -> None:
        content = '''"AppState"
{
\t"appid"\t\t"220"
\t"name"\t\t"Half-Life 2"
}
'''
        with tempfile.TemporaryDirectory() as d:
            manifest = os.path.join(d, "appmanifest_220.acf")
            with open(manifest, "w") as f:
                f.write(content)
            result = steam.parse_appmanifest(manifest)
        self.assertEqual(result, ("220", "Half-Life 2"))

    def test_parse_appmanifest_missing(self) -> None:
        self.assertIsNone(steam.parse_appmanifest("/no/such/manifest.acf"))


if __name__ == "__main__":
    unittest.main()
