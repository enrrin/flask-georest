from app import app
import unittest
import logging

logging.getLogger("consoleLogger").disabled = True


class TestGETDocumento(unittest.TestCase):

    # self.app = app.test_client() è la test fixture
    def setUp(self):
        self.app = app.test_client()

    def test_get_macbook(self):
        print("[/api/documenti/macbook presente]")
        href = "macbook"
        res = self.app.get(f"/api/documenti/{href}",
                           environ_base={'REMOTE_ADDR': '0.0.0.0'})
        self.assertEqual(200, res.status_code)

    def test_get_birre(self):
        print("[/api/documenti/birre presente]")
        href = "birre"
        res = self.app.get(f"/api/documenti/{href}",
                           environ_base={'REMOTE_ADDR': '0.0.0.0'})
        self.assertEqual(200, res.status_code)

    def test_get_animali(self):
        print("[/api/documenti/animali assente]")
        href = "animali"
        res = self.app.get(f"/api/documenti/{href}",
                           environ_base={'REMOTE_ADDR': '0.0.0.0'})
        self.assertEqual(404, res.status_code)

    def test_get_natura(self):
        print("[/api/documenti/natura assente]")
        href = "natura"
        res = self.app.get(f"/api/documenti/{href}",
                           environ_base={'REMOTE_ADDR': '0.0.0.0'})
        self.assertEqual(404, res.status_code)


if __name__ == '__main__':
    unittest.main()
