from src.python.modello.dto.PosizioneClient import PosizioneClient
from dotenv import load_dotenv

import pyproj

import IP2Location
import IP2Proxy
import os


class DAOPosizioneClient(PosizioneClient):

    def __init__(self):
        super().__init__()

    load_dotenv()

    def is_posizione_client_fake(self, client):
        tentativi_fake = []
        if self.is_ip_proxy(client.ip):
            tentativi_fake.append(
                "Sembra che il tuo IP provenga da un open proxy!")
        if client.is_mobile and self.is_gps_mock(client):
            tentativi_fake.append(
                "Sembra che il tuo GPS stia fornendo coordinate fake!")
        return tentativi_fake

    def is_ip_proxy(self, ip):
        db = IP2Proxy.IP2Proxy()
        is_proxy = False
        try:
            db.open(os.path.join(
                "data", os.environ.get("IP2PROXYBIN")))
            if db.is_proxy(ip) == 1:
                is_proxy = True
                return is_proxy
                # return db.get_all(ip)
            elif db.is_proxy(ip) == -1:
                raise Exception("Errore da IP2Proxy db [err -1]")
        except Exception as ex:
            raise Exception(f"Errore dal IP2PROXY db: {ex}")
        finally:
            db.close()

    def is_gps_mock(self, client):
        ip = self.find_by_ip(client.ip)
        geod = pyproj.Geod(ellps="WGS84")
        distanza = geod.inv(
            ip.longitude, ip.latitude, client.lon, client.lat)
        distanza_in_km = int(distanza[2] / 1000)
        if distanza_in_km > 2000:
            return True
        return False

    def find_by_ip(self, client_ip) -> IP2Location:
        db = IP2Location.IP2Location()
        try:
            db.open(os.path.join(
                "data", os.environ.get("IP2LOCBIN")))
            location_info = db.get_all(client_ip)
            if location_info is not None and location_info:
                return location_info
            elif location_info is None or not location_info:
                return None
        except Exception as ex:
            raise Exception(f"Errore dal IP2Loc db: {ex}")
        finally:
            db.close()
