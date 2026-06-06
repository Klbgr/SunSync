import unittest
from unittest import mock

from sunshine import sunshine


class NormalizeTests(unittest.TestCase):
    def test_host_empty_falls_back_to_default(self) -> None:
        self.assertEqual(sunshine._normalize_api_host(""), sunshine.DEFAULT_SUNSHINE_HOST)
        self.assertEqual(sunshine._normalize_api_host(None), sunshine.DEFAULT_SUNSHINE_HOST)

    def test_host_strips_whitespace(self) -> None:
        self.assertEqual(sunshine._normalize_api_host("  host.lan  "), "host.lan")

    def test_port_valid(self) -> None:
        self.assertEqual(sunshine._normalize_api_port("47990"), 47990)

    def test_port_non_numeric_raises(self) -> None:
        with self.assertRaises(ValueError):
            sunshine._normalize_api_port("abc")

    def test_port_out_of_range_raises(self) -> None:
        with self.assertRaises(ValueError):
            sunshine._normalize_api_port(0)
        with self.assertRaises(ValueError):
            sunshine._normalize_api_port(70000)


class ApiConnectionTests(unittest.TestCase):
    def setUp(self) -> None:
        sunshine.set_api_connection(host=None, port=None)

    def tearDown(self) -> None:
        sunshine.set_api_connection(host=None, port=None)

    @mock.patch("sunshine.sunshine._load_api_connection_settings", return_value={})
    def test_environment_override(self, _settings) -> None:
        with mock.patch.dict(
            "os.environ",
            {"SUNSYNC_API_HOST": "10.0.0.5", "SUNSYNC_API_PORT": "12345"},
            clear=False,
        ):
            host, port = sunshine.get_api_connection(server_name="sunshine")
        self.assertEqual(host, "10.0.0.5")
        self.assertEqual(port, 12345)

    @mock.patch("sunshine.sunshine._load_api_connection_settings", return_value={})
    def test_defaults_when_nothing_set(self, _settings) -> None:
        with mock.patch.dict("os.environ", {}, clear=True):
            host, port = sunshine.get_api_connection(server_name="sunshine")
        self.assertEqual(host, sunshine.DEFAULT_SUNSHINE_HOST)
        self.assertEqual(port, sunshine.DEFAULT_SUNSHINE_PORT)


class ExistingAppsCacheTests(unittest.TestCase):
    def tearDown(self) -> None:
        sunshine.clear_existing_apps_cache()

    @mock.patch(
        "sunshine.sunshine.get_existing_apps",
        return_value=[{"name": "A", "index": 0}, {"name": "B", "index": 1}],
    )
    def test_cache_avoids_repeated_fetch(self, fetch) -> None:
        sunshine.prime_existing_apps_cache()
        self.assertEqual(sunshine._find_existing_app("B")["index"], 1)
        self.assertIsNone(sunshine._find_existing_app("missing"))
        # Primed once; lookups must not re-fetch.
        self.assertEqual(fetch.call_count, 1)

    @mock.patch(
        "sunshine.sunshine.get_existing_apps",
        return_value=[{"name": "A", "index": 0}],
    )
    def test_lookup_without_priming_fetches(self, fetch) -> None:
        sunshine.clear_existing_apps_cache()
        self.assertEqual(sunshine._find_existing_app("A")["index"], 0)
        self.assertEqual(fetch.call_count, 1)


if __name__ == "__main__":
    unittest.main()
