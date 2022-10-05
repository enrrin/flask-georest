const access_token = 'pk.eyJ1IjoiZXJ4eXoiLCJhIjoiY2t1eHl2cjM4MGE0bzJxcGJkcjd4cDk2YSJ9.sONz58Hdx_mw47981-iR4g'

function inserisciSvgs() {
    let ball = document.querySelector('#ball')
    let ballBounds = L.latLngBounds([coordsCampo[0], coordsCampo[2]])
    let ballOverlay = L.svgOverlay(ball, ballBounds, {
        opacity: 0.7,
        interactive: true
    }).addTo(map)
    let uni = document.querySelector('#uni')
    let uniBounds = L.latLngBounds([41.86896561377682, 12.477185726165771], [41.868654023439426, 12.47772753238678])
    let uniOverlay = L.svgOverlay(uni, uniBounds, {
        opacity: 0.7,
        interactive: true
    }).addTo(map)
}

function inserisciPOIs() {
    let campo = L.polygon(coordsCampo, { color: '#99d98c', weight: 2, fillOpacity: 0.6 }).addTo(map)
    let stand = L.polygon(coordsStand, { color: '#11d98c', weight: 2, fillOpacity: 0.6 }).addTo(map)

    campo.on('click', function (e) {
        let popLocation = e.latlng
        let popup = L.popup()
            .setLatLng(popLocation)
            .setContent('Campo dei robot calciatori')
            .openOn(map)
    })

    stand.on('click', function (e) {
        let popLocation = e.latlng
        let popup = L.popup()
            .setLatLng(popLocation)
            .setContent('Stand unibas')
            .openOn(map)
    })
}

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

                    let posizioneDocumenti = L.polygon(coordsDocs, { color: '#ff6b6b', weight: 2, opacity: 0.7, fillOpacity: 0.0 })
                    let regioneValidita = L.polygon(coordsRegioneValidita, { color: '#ffe66d', weight: 2, opacity: 0.7, fillOpacity: 0.0 })

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
            map.setView([clientLat - 0.0003, clientLon], 20)
        },
    })
}

let coordsIniziali = [41.8686, 12.4774]
// Inizializzazione mappa in zona fiera
let map = new L.map('map').setView(coordsIniziali, 18)

let coordsCampo = [
    [
        41.869301170903185,
        12.476761937141418
    ],
    [
        41.86894963482208,
        12.477035522460938
    ],
    [
        41.86912939783236,
        12.477432489395142
    ],
    [
        41.86948093292492,
        12.477158904075623

    ],
    [
        41.869301170903185,
        12.476761937141418
    ]
]

let coordsStand = [
    [
        41.868861750499754,
        12.477126717567444
    ],
    [
        41.86874190804734,
        12.4772447347641
    ],
    [
        41.86888172422,
        12.477571964263916
    ],
    [
        41.86901754535205,
        12.477448582649231

    ],
    [
        41.868861750499754,
        12.477126717567444
    ]
]

let layers = []

let opzioniLayer = {
    attribution: 'Map data &copy <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: access_token,
}

let tileLayer = new L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', opzioniLayer).addTo(map)

inserisciPOIs()
inserisciSvgs()


