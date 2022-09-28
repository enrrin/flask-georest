let bottoneLocalizzazione = document.getElementById("bottone")

bottoneLocalizzazione.addEventListener("click", () => {
    navigator.geolocation.getCurrentPosition(localizzazioneConsentita, localizzazioneNegata, opzioniLocalizzazione)
})

let opzioniLocalizzazione = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
}

async function localizzazioneConsentita(position) {
    let lat = position.coords.latitude
    let lon = position.coords.longitude
    // let lon = 12.520388
    // let lat = 41.932538
    let response = await findDocumenti(lat, lon)
    console.log("[INFO] -> ", response.data)
    aggiornaPagina(response.data, response.status, true)
}

async function findDocumenti(latitude, longitude) {
    let posizione = {
        "type": "Feature",
        "properties": {
            mobile: isMobile()
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                longitude,
                latitude
            ]
        }
    }
    let request = {
        method: "POST",
        headers: {
            "Content-Type": "application/geo+json"
        },
        body: JSON.stringify(posizione)
    }
    try {
        let response = await fetch("/api/documenti", request)
        return {
            status: response.status,
            data: await response.json()
        }
    } catch (ex) {
        console.error("### [fetch /api/documenti] -> ", ex)
    }
}


async function localizzazioneNegata(error) {
    alert("Hai negato il consenso alla localizzazione. Cerco una posizione approssimata...")
    console.warn(`(${error.code}): ${error.message}`)
    let response = await findPosizione()
    console.log("[INFO] -> ", response.data)
    aggiornaPagina(response.data, response.status, false)
}

async function findPosizione() {
    try {
        let response = await fetch("/api/posizione")
        return {
            status: response.status,
            data: await response.json()
        }
    } catch (ex) {
        console.error("### [fetch /api/posizione] -> ", ex)
    }
}
