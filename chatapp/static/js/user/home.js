import { getCookies } from "/static/js/utils.js"
import { fetchModulesCompleted } from "/static/js/events.js"

const modules = document.querySelectorAll('.module')
const cookies = getCookies()
const number  = await fetchModulesCompleted(cookies.cookie)
const main    = Array.from(document.getElementById('main-modules').children)

modules.forEach(module => {
    module.addEventListener('click', () => {
        window.location.href = module.attributes.redirect.value
    })
})

main.forEach((module, index) => {
    if (number <= index - 1) {
        module.style.display = 'none';
    }
})

if (number < main.length) { document.getElementById('free-recall').style.display = 'none' }

