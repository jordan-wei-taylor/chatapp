import { getCookies } from "/static/js/utils.js" 
import { authenticate, updateUserModule } from "/static/js/events.js"

console.log('test')

document.getElementsByClassName('main')[0].innerHTML += '<button id="next">Next</button>'

document.getElementById('next').addEventListener('click', async () => {
    const cookie = getCookies().cookie
    await authenticate(cookie)
    if (window.location.href.includes('welcome')) {
        updateUserModule(cookie, 0)
        window.location.href = 'home'
    } else {
        const text = document.getElementsByClassName('main')[0].innerText
        document.cookie = `esther-module=${text.slice(0, text.indexOf('\n'))};path=/`
        window.location.href += '/chat'
    }
})

function back() { 
    if (window.location.href.includes('module')) { window.location.href = '/home' }
    else { window.location.href = document.referrer }
}