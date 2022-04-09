import json
import traceback
import logging
import logging.config
import geojson
from src.python.persistenza.DAOPosizione import DAOPosizione
from src.python.persistenza.DAODocumento import DAODocumento
from flask_restful import Resource
from flask import request, send_file
from python.utilita.RestUtility import RestUtility
from src.python.modello.dto.PosizioneClient import PosizioneClient
from src.python.persistenza.DAOPosizioneClient import DAOPosizioneClient

logging.config.fileConfig(
    fname='config/logging.conf', disable_existing_loggers=True)
console_logger = logging.getLogger('consoleLogger')
requests_logger = logging.getLogger('requestsLogger')
dao_posizione = DAOPosizione()
dao_documento = DAODocumento()
dao_client = DAOPosizioneClient()


class ControlloDocumento(Resource):

    def post(self):
        client_ip = request.remote_addr
        consenso = True
        try:
            errori = self.convalida_richiesta(json.loads(request.get_data()))
            if len(errori) != 0:
                return RestUtility.crea_400(errori)
            geoj_valido = geojson.loads(request.get_data())
            client = PosizioneClient(
                ip=client_ip, lat=geoj_valido.geometry.coordinates[1], lon=geoj_valido.geometry.coordinates[0], is_mobile=geoj_valido.properties["mobile"])
            tentativi_fake = dao_client.is_posizione_client_fake(client)
            if len(tentativi_fake) != 0:
                console_logger.info(
                    f"{client.ip} {request.method} {request.full_path} {403} {tentativi_fake}")
                requests_logger.info(
                    f"{client.ip} {request.method} {request.full_path} {403} {tentativi_fake}")
                return RestUtility.crea_403(tentativi_fake, client)
            console_logger.info(
                f"{client.ip} {request.method} {request.full_path} {200} (mobile={client.is_mobile} lat={client.lat} lon={client.lon})")
            requests_logger.info(
                f"{client.ip} {request.method} {request.full_path} {200} (mobile={client.is_mobile} lat={client.lat} lon={client.lon})")
            if client.is_mobile:
                posizioni = dao_posizione.find_by_latlon(
                    client.lat, client.lon)
                if posizioni is None:
                    return RestUtility.crea_geojson(
                        None, client.lat, client.lon, consenso)
                return RestUtility.crea_geojson(posizioni, client.lat, client.lon, consenso)
            posizioni = dao_posizione.find_by_latlon_buffer(
                client.lat, client.lon)
            if posizioni is None:
                return RestUtility.crea_geojson(
                    None, client.lat, client.lon, consenso)
            return RestUtility.crea_geojson(posizioni, client.lat, client.lon, consenso)
        except Exception as ex:
            requests_logger.error(
                f"{client_ip} {request.method} {request.full_path} {500} {ex}")
            console_logger.error(
                f" ### {request.full_path} {ex}")
            return RestUtility.crea_errore("Non è stato possibile eseguire l'operazione")

    def convalida_richiesta(self, body):
        errori = []
        # deve essere un geojson valido
        try:
            gjson = geojson.GeoJSON.to_instance(
                body, strict=True)
            # deve essere un Punto
            if gjson.geometry.type != "Point":
                errori.append(
                    "Il tipo di geometria deve essere un Point")
            # deve contenere almeno la proprietà "mobile"
            if "mobile" not in list(gjson.properties.keys()):
                errori.append(
                    "E' necessario specificare se il browser è mobile")
        except Exception:
            errori.append(
                "Il corpo della richiesta deve essere uno GeoJSON valido")
        return errori

    def get(self, href_id):
        client_ip = request.remote_addr
        try:
            documento = dao_documento.find_by_hrefid(href_id)
            if documento is None:
                RestUtility.crea_404(
                    "Nessun documento trovato con questo codice")
            href = documento.href.get(href_id)
            console_logger.info(
                f"{client_ip} {request.method} {request.full_path} {200}")
            requests_logger.info(
                f"{client_ip} {request.method} {request.full_path} {200}")
            return send_file(href)
        except FileNotFoundError as ex:
            console_logger.error(
                f"{client_ip} {request.method} {request.full_path} {404} {ex}")
            requests_logger.error(
                f"{client_ip} {request.method} {request.full_path} {404} {ex}")
            return RestUtility.crea_404(
                "Nessun documento trovato con questo codice")
        except Exception as ex:
            requests_logger.error(
                f"{client_ip} {request.method} {request.full_path} {500} {ex}")
            console_logger.error(
                f" ###### {request.full_path} {traceback.format_exc()}")
            return RestUtility.crea_errore(
                "Non è stato possibile eseguire l'operazione")
