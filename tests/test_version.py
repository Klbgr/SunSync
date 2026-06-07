import io
import unittest
from contextlib import redirect_stdout

import sunsync


class VersionFlagTests(unittest.TestCase):
    def test_version_is_nonempty_string(self) -> None:
        self.assertIsInstance(sunsync.__version__, str)
        self.assertTrue(sunsync.__version__)

    def test_version_flag_prints_and_exits(self) -> None:
        buf = io.StringIO()
        with self.assertRaises(SystemExit) as ctx, redirect_stdout(buf):
            sunsync.parse_args(["--version"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertIn("sunsync", buf.getvalue())
        self.assertIn(sunsync.__version__, buf.getvalue())


if __name__ == "__main__":
    unittest.main()
