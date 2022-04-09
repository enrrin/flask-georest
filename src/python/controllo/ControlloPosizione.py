import traceback
from src.python.persistenza.DAOPosizione import DAOPosizione
from flask_restful import Resource, request
from python.utilita.RestUtility import RestUtility
import logging
import logging.config

from src.python.modello.dto.PosizioneClient import PosizioneClient
from src.python.persistenza.DAOPosizioneClient import DAOPosizioneClient

logging.config.fileConfig(
    fname='config/logging.conf', disable_existing_loggers=True)
console_logger = logging.getLogger('consoleLogger')
requests_logger = logging.getLogger('requestsLogger')
dao_posizione = DAOPosizione()
dao_client = DAOPosizioneClient()


class ControlloPosizione(Resource):

    def get(self):
        client_ip = request.remote_addr
        consenso = False
        try:
            is_proxy = dao_client.is_ip_proxy(client_ip)
            ip2location = dao_client.find_by_ip(client_ip)
            posizione_client = PosizioneClient(
                ip=client_ip, lat=ip2location.latitude, lon=ip2location.longitude)
            posizioni = dao_posizione.find_by_citta(ip2location.city)
            console_logger.info(
                f"{client_ip} {request.method} {request.full_path} {200} (citta={ip2location.city} lat={posizione_client.lat} lon={posizione_client.lon})")
            requests_logger.info(
                f"{client_ip} {request.method} {request.full_path} {200} (citta={ip2location.city} lat={posizione_client.lat} lon={posizione_client.lon})")
            if is_proxy:
                console_logger.info(
                    f"{client_ip} {request.method} {request.full_path} {403} ( PROXY -> citta={ip2location.city} lat={posizione_client.lat} lon={posizione_client.lon})")
                requests_logger.info(
                    f"{client_ip} {request.method} {request.full_path} {403} (PROXY -> citta={ip2location.city} lat={posizione_client.lat} lon={posizione_client.lon})")
                return RestUtility.crea_403("Sembra che il tuo IP provenga da un open proxy!", posizione_client)
            if posizioni is None:
                return RestUtility.crea_geojson(
                    None, posizione_client.lat, posizione_client.lon, consenso)
            return RestUtility.crea_geojson(posizioni, posizione_client.lat, posizione_client.lon, consenso)
        except Exception as ex:
            requests_logger.error(
                f"{client_ip} {request.method} {request.full_path} {500} {ex}")
            console_logger.error(
                f" ### {request.full_path} {traceback.format_exc()}")
            return RestUtility.crea_errore("Non è stato possibile eseguire l'operazione")
