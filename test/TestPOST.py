from app import app
import unittest
import logging

logging.getLogger("consoleLogger").disabled = True


class TestPOST(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_geojson(self):
        print("[geojson valido su buffer in parco europa]")
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': '0.0.0.0'},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": False
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        15.8066,
                                        40.6465
                                    ]
                                }
                            })
        self.assertEqual(200, res.status_code)

    def test_geojson_mobile_properties1(self):
        print("[geojson con una properties != mobile]")
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': '0.0.0.0'},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "propr": False,
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        24.4331,
                                        33.9368
                                    ]
                                }
                            })
        self.assertEqual(400, res.status_code)
        self.assertEqual(
            "E' necessario specificare se il browser è mobile", res.get_json()["messaggio"][0])

    def test_geojson_mobile_properties2(self):
        print(
            "[geojson in buffer di parco europa con più properties ma almeno una mobile]")
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': '0.0.0.0'},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "Citta": "Potenza",
                                    "Numero": 123,
                                    "mobile": False
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        15.8066,
                                        40.6465
                                    ]
                                }
                            })
        self.assertEqual(200, res.status_code)

    def test_geojson_errato(self):
        print("[geojson errato]")
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': '0.0.0.0'},
                            json={
                                "type": "Tipo non feature",
                                "properties": {
                                    "mobile": False
                                },
                                "geometry": {
                                    "coordinates": [
                                        18.6565,
                                        23.9538,
                                        33.5333,
                                        11.32234
                                    ]
                                }
                            })
        self.assertEqual(
            "Il corpo della richiesta deve essere uno GeoJSON valido", res.get_json()["messaggio"][0])

    def test_polygon(self):
        print("[geojson poligono]")
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': '0.0.0.0'},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": False
                                },
                                "geometry": {
                                    "type": "Polygon",
                                    "coordinates": [
                                        11.6565,
                                        53.9238,
                                        16.9283,
                                        22.24441
                                    ]
                                }
                            })
        self.assertEqual(
            "Il tipo di geometria deve essere un Point", res.get_json()["messaggio"][0])

    def test_json(self):
        print("[semplice json]")
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': '0.0.0.0'},
                            json={
                                "key": "value"
                            })
        self.assertEqual(
            "Il corpo della richiesta deve essere uno GeoJSON valido", res.get_json()["messaggio"][0])


if __name__ == '__main__':
    unittest.main()
