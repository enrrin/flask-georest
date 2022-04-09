const access_token = '<mapbox-token>'

let layers = []

// Inizializzazione mappa su Italia
let map = new L.map('map').setView([41.88, 12.47], 6)

// Creazione tileLayer mapbox
let opzioniLayer = {
    attribution: 'Map data &copy <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: access_token,
}

let tileLayer = new L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', opzioniLayer).addTo(map)

function aggiornaMappa(body) {
    L.geoJSON(body, {
        onEachFeature: (feature) => {
            if (feature.geometry.type == "Point") {
                aggiornaPosizioneClient(feature)
                mostraDocumentiDisponibili(feature.properties.docs)
            } else {
                let posizioneTrovata = feature
                console.log("Multipoligono in", posizioneTrovata.properties.location)

                // - disegno poligoni in caso di posizioni non nulle
                if (posizioneTrovata != null && posizioneTrovata.length != 0) {
                    // - metodo statico di L.GeoJSON per invertire lon/lat
                    coordsDocs = L.GeoJSON.coordsToLatLngs(posizioneTrovata.geometry.coordinates[0], 1, false)
                    coordsRegioneValidita = L.GeoJSON.coordsToLatLngs(posizioneTrovata.geometry.coordinates[1], 1, false)

                    let posizioneDocumenti = L.polygon(coordsDocs, { color: '#00ff00', weight: 2, fillOpacity: 0.6 })
                    let regioneValidita = L.polygon(coordsRegioneValidita, { color: '#0000ff', weight: 0, opacity: 0.5, fillOpacity: 0.1 })

                    posizioneDocumenti.addTo(map)
                    layers.push(posizioneDocumenti)

                    if (!isMobile()) {
                        // regioneValidita.on('mouseover', () => {
                        //     layer.setStyle({
                        //         fillOpacity: 0.4
                        //     })
                        // })
                        regioneValidita.addTo(map)
                        layers.push(regioneValidita)
                    }

                    // layer.on('mouseover', function (e) {
                    //     layer.setStyle({
                    //         fillOpacity: 0.4
                    //     });
                    // });
                    // layer.on('mouseout', function (e) {
                    //     layer.setStyle({
                    //         fillOpacity: 0
                    //     });
                    // });
                }
            }
        }

    })

}

// marker alternativo. Da aggiungere nella creazione del marker
let iconaMarker = L.icon({
    iconUrl: '../img/marker.png',
    iconSize: [100, 87], // dimensioni icona
});

function aggiornaPosizioneClient(body) {
    L.geoJSON(body, {
        onEachFeature: (feature) => {
            clientLat = feature.geometry.coordinates[1]
            clientLon = feature.geometry.coordinates[0]
            let marker = new L.marker([clientLat, clientLon], { clickable: true }).addTo(map)
            layers.push(marker)
            let popup = new L.popup({ offset: L.point(0, -10) })
                .setLatLng([clientLat, clientLon])
                .setContent('<p>' + 'La tua posizione:' + '<br>' + clientLat.toFixed(4) + ' ' + clientLon.toFixed(4) + '</p>')
                .openOn(map)
            marker.bindPopup(popup, { showOnMouseOver: true })
            map.setView([clientLat, clientLon], 15)
        },
    })
}



