from app import app
import unittest
import logging

logging.getLogger("consoleLogger").disabled = True


class TestGETPosizione(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_negata_presente(self):
        print("[consenso negato, citta con documenti]")
        res = self.app.get('/api/posizione',
                           environ_base={'REMOTE_ADDR': '2.42.184.1'})
        self.assertEqual(200, res.status_code)
        self.assertEqual(
            "Potenza", res.json["features"][0]["properties"]["city"])

    def test_negata_assente(self):
        print("[consenso negato, citta senza documenti]")
        res = self.app.get('/api/posizione',
                           environ_base={'REMOTE_ADDR': '53.42.184.1'})
        self.assertEqual(200, res.status_code)
        self.assertEqual(
            0, res.json["features"][0]["properties"]["docs"])

    def test_negata_proxy(self):
        print("[consenso negato, ip proxy in Singapore]")
        res = self.app.get('/api/posizione',
                           environ_base={'REMOTE_ADDR': "145.40.73.102"})
        self.assertEqual(403, res.status_code)
        self.assertEqual(
            "Sembra che il tuo IP provenga da un open proxy!", res.json["properties"]["messages"])


if __name__ == '__main__':
    unittest.main()
