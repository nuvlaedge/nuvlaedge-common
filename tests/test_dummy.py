import mock
import unittest


class TestDummy(unittest.TestCase):

    @unittest.skip("dummy test")
    def test_main(self):
        """Dummy test."""
        main = mock.Mock()
        main.return_value = None
        self.assertIsNone(main())
