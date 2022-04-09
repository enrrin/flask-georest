
import geojson
from flask import jsonify, make_response


class RestUtility:

    # Ritorna geojson con posizione (Multipoligono) e posizione utente (Punto)
    @staticmethod
    def crea_geojson(posizioni, client_lat, client_lon, consenso):
        docs_json = []
        features = []
        posizione_client = geojson.Feature(
            geometry=geojson.Point([float(client_lon), float(client_lat)]), properties={"docs": 0})
        if consenso:
            if posizioni is not None:
                for p in posizioni:
                    posizione_documenti = geojson.Feature(geometry=geojson.MultiPolygon(([p.get_geometria()], [p.get_regione_validita()])), properties={
                        "state": p.nazione, "city": p.citta, "location": p.locazione, "docs": [i.to_json() for i in p.documenti]})
                    for d in p.documenti:
                        docs_json.append(d.to_json())
                    features.append(posizione_documenti)
            # Necessario il parsing a float, altrimenti causerebbe eccezione nel caso di ricerca su ip2loc:
            # Il modulo geojson supporta solo le classi standard di python
            posizione_client = geojson.Feature(
                geometry=geojson.Point([float(client_lon), float(client_lat)]), properties={"docs": docs_json})
        else:
            if posizioni is not None:
                for p in posizioni:
                    for d in p.documenti:
                        docs_json.append(d.to_json())
                posizione_client = geojson.Feature(
                    geometry=geojson.Point([float(client_lon), float(client_lat)]), properties={"city": p.citta, "docs": len(docs_json)})
        features.append(posizione_client)
        feature_collection = geojson.FeatureCollection(features)
        response = make_response(
            jsonify(
                feature_collection
            ),
            200,
        )
        response.headers["Content-Type"] = "application/geo+json"
        return response

    # 400 bad request (richiesta malformata)
    @staticmethod
    def crea_400(messaggio):
        response = make_response(jsonify({
            "messaggio": messaggio
        }), 400)
        response.headers["Content-Type"] = "application/json"
        return response

    # 403 fobidden (fake ip, fake gps: rilevamento posizione consentita, ma che la richiesta non è stata eseguita. Viene negato l’accesso alla risorsa poiché non possiede il permesso necessario)
    @staticmethod
    def crea_403(messaggio, client):
        posizione_client = geojson.Feature(
            geometry=geojson.Point([float(client.lon), float(client.lat)]), properties={"messages": messaggio})
        response = make_response(
            jsonify(
                posizione_client
            ),
            403,
        )
        response.headers["Content-Type"] = "application/geo+json"
        return response

    @staticmethod
    def crea_404(messaggio):
        response = make_response(jsonify({
            "messaggio": messaggio
        }), 404)
        response.headers["Content-Type"] = "application/json"
        return response

    @staticmethod
    def crea_errore(messaggio):
        response = make_response(jsonify({
            "messaggio": messaggio
        }), 500)
        response.headers["Content-Type"] = "application/json"
        return response
