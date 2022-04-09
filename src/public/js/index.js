const schedaInformazioni = document.getElementById('campo-documenti')
const modaleHeader = document.getElementById('modale-header')
const modaleBody = document.getElementById('modale-body')
const modaleFooter = document.getElementsByClassName('modale-footer')

// verifica al meglio se il browser è di tipo mobile
// https://developer.mozilla.org/en-US/docs/Web/HTTP/Browser_detection_using_the_user_agent#mobile_device_detection
let isMobile = () => {
    let mobileBrowser = false
    if ("maxTouchPoints" in navigator) {
        mobileBrowser = navigator.maxTouchPoints > 0
    } else if ("msMaxTouchPoints" in navigator) {
        mobileBrowser = navigator.msMaxTouchPoints > 0
    } else {
        let mQ = window.matchMedia && matchMedia("(pointer:coarse)")
        if (mQ && mQ.media === "(pointer:coarse)") {
            mobileBrowser = !!mQ.matches
        } else if ('orientation' in window) {
            mobileBrowser = true // deprecated, but good fallback
        } else {
            // Only as a last resort, fall back to user agent sniffing
            let userAgent = navigator.userAgent
            mobileBrowser = (
                // tablet
                /\b(tablet|ipad|playbook|silk)|(android(?!.*mobi))\b/i.test(userAgent) ||
                // mobile
                /\b(Mobile|Android|iP(hone|od)|IEMobile|BlackBerry|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini))\b/i.test(userAgent)
            )
        }
    }
    return mobileBrowser
}

function initPagina() {
    schedaInformazioni.innerHTML = ""
    layers.forEach(element => {
        map.removeLayer(element)
    })
}

function aggiornaPagina(body, statusCode, consenso) {
    initPagina()
    aggiornaFinestraModale(consenso)
    switch (statusCode) {
        case 200:
            if (consenso) {
                aggiornaMappa(body)
                break
            } else {
                mostraDocumentiDisponibili(body.features[0].properties.docs)
                aggiornaPosizioneClient(body)
                break
            }
        // 403 fobidden (fake ip, fake gps: rilevamento posizione consentita, ma che la richiesta non è stata eseguita. Viene negato l’accesso alla risorsa poiché non possiede il permesso necessario)
        case 403:
            // proxy o coordinate fake
            aggiornaPosizioneClient(body)
            mostraMessaggio(body.properties.messages)
            break
        // 404 risorsa not found
        // 500 internal server error
        default:
            let messaggio = body.messaggio
            mostraMessaggio(messaggio)
    }
}

function mostraDocumentiDisponibili(listaDocumenti) {
    if (typeof (listaDocumenti) == "number" && listaDocumenti != 0) {
        schedaInformazioni.innerHTML = `Rilevando il tuo ip, nella tua citta ho trovato ${listaDocumenti} documenti.<br><br>Consenti l'accesso alla tua posizione per visualizzare i documenti disponibili`

    }
    else if (typeof (listaDocumenti) == "object" && listaDocumenti != null && listaDocumenti.length != 0) {
        let setDocumenti = []
        listaDocumenti.forEach(documento => {
            if (!setDocumenti.includes(documento.nome)) {
                console.log(setDocumenti)
                let link = `<li><a href=/api/documenti/${documento.href} style="color: #323639">${documento.nome}</a><br></li>`
                schedaInformazioni.innerHTML += link
                setDocumenti.push(documento.nome)
            }
        })
    } else {
        mostraMessaggio('Nessun documento accessibile da questa posizione')
    }
}

function aggiornaFinestraModale(consenso) {
    // trigger modale 
    if (isMobile() && consenso) {
        triggerModale.innerHTML = "Dal tuo dispositivo"
        modaleHeader.innerHTML = "<h2>Dal tuo dispositivo</h2>"
        modaleBody.innerHTML = "Viene utilizzata la posizione inviata dal tuo dispositivo che sembra dotato di GPS"
        modaleBody.innerHTML += "<br>Viene mostrata una lista di documenti accessibili da questa posizione"
    } else {
        triggerModale.innerHTML = "Dal tuo indirizzo IP"
        modaleHeader.innerHTML = "<h2>Dal tuo indirizzo IP</h2>"
        modaleBody.innerHTML = "La tua area generale viene stimata in base al tuo indirizzo IP, pertanto la posizione potrebbe essere incorretta e i documenti visualizzati potrebbero non essere quelli che cerchi"
        modaleBody.innerHTML += "<br>Se non è la posizione corretta o desideri maggiore precisione, consenti l'accesso alla posizione attraverso un dispositivo dotato di GPS"
    }
}

function mostraMessaggio(messaggi) {
    // verifica se il messaggio contiene più messaggi da uno stringbuilder
    if (typeof (messaggi) != "string" && messaggi.length != 1) {
        messaggi.forEach(messaggio => {
            schedaInformazioni.innerHTML += `<li>${messaggio}<br></li>`
        })
    } else {
        schedaInformazioni.innerHTML = `<li>${messaggi}<br></li>`
    }
}
