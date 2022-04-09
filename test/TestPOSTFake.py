from app import app
import unittest
import logging

logging.getLogger("consoleLogger").disabled = True


class TestPOSTFake(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_proxy_desktop_francia(self):
        # https://www.freeproxylists.net/
        print("proxy in francia, mobile false")
        proxy = "194.5.193.183"
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': proxy},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": False
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        23.656555,
                                        43.954338
                                    ]
                                }
                            })
        self.assertEqual(403, res.status_code)

    def test_proxy_desktop_germania(self):
        # https://www.freeproxylists.net/
        print("proxy in germania, mobile false")
        proxy = "167.86.81.208"
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': proxy},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": False
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        23.656555,
                                        43.954338
                                    ]
                                }
                            })
        self.assertEqual(403, res.status_code)

    def test_proxy_desktop_us(self):
        # https://www.freeproxylists.net/
        print("proxy in us, mobile false")
        proxy = "140.227.211.47"
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': proxy},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": False
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        23.656555,
                                        43.954338
                                    ]
                                }
                            })
        self.assertEqual(403, res.status_code)

    def test_proxy_desktop_egitto(self):
        # https://www.freeproxylists.net/
        print("proxy in egitto, mobile false")
        proxy = "41.65.236.58"
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': proxy},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": False
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        23.656555,
                                        43.954338
                                    ]
                                }
                            })
        self.assertEqual(403, res.status_code)

    def test_proxy_desktop_china(self):
        # https://www.freeproxylists.net/
        print("proxy in cina, mobile false")
        proxy = "223.96.90.216"
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': proxy},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": False
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        23.656555,
                                        43.954338
                                    ]
                                }
                            })
        self.assertEqual(403, res.status_code)

    def test_proxy_desktop_japan(self):
        # https://www.freeproxylists.net/
        print("proxy in giappone, mobile false")
        proxy = "164.70.122.6"
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': proxy},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": False
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        44.6565,
                                        50.9338
                                    ]
                                }
                            })
        self.assertEqual(403, res.status_code)

    @unittest.skip("ip2proxy marzo non rileva il proxy")
    def test_proxy_desktop_bangladesh(self):
        # https://www.freeproxylists.net/
        print("proxy in bangladesh, mobile false")
        proxy = "103.138.182.3"
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': proxy},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": False
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        45.63365,
                                        10.93238
                                    ]
                                }
                            })
        self.assertEqual(403, res.status_code)

    def test_proxy_desktop_australia(self):
        # https://www.freeproxylists.net/
        print("proxy in australia, mobile false")
        proxy = "47.91.44.217"
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': proxy},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": False
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        35.6565,
                                        40.9338
                                    ]
                                }
                            })
        self.assertEqual(403, res.status_code)

    def test_proxy_mobile_brasile(self):
        # https://www.freeproxylists.net/
        print("proxy in brasile, mobile false")
        proxy = "186.216.80.166"
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': proxy},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": True
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        10.7118,
                                        45.4566
                                    ]
                                }
                            })
        self.assertEqual(403, res.status_code)

    def test_gps_mock(self):
        print("ip reale in us e gps a garda, mobile true")
        remote = "55.32.33.234"
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': remote},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": True
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        10.71484,
                                        45.45651
                                    ]
                                }
                            })
        self.assertEqual(403, res.status_code)

    def test_gps_mock_and_proxy_canada(self):
        print("proxy in canada e gps a garda, mobile true")
        remote = "67.212.83.55"
        res = self.app.post('/api/documenti',
                            environ_base={'REMOTE_ADDR': remote},
                            json={
                                "type": "Feature",
                                "properties": {
                                    "mobile": True
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [
                                        10.71484,
                                        45.45651
                                    ]
                                }
                            })
        self.assertEqual(403, res.status_code)


if __name__ == '__main__':
    unittest.main()
