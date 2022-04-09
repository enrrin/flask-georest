const modale = document.getElementById("id-modale")
const triggerModale = document.getElementById("campo-informazioni")
const bottoneChiusura = document.getElementsByClassName("modale-chiusura")[0]

window.addEventListener("click", (event) => {
    if (event.target == modale) {
        modale.style.display = "none"
    }
})


triggerModale.addEventListener("click", () => {
    modale.style.display = "block"
})


bottoneChiusura.addEventListener("click", () => {
    modale.style.display = "none"
})