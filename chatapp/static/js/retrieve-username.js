import { retrieve } from "/static/js/events.js"

const Email = document.getElementById('email')
const Code  = document.getElementById('code')

document.getElementById('retrieve').addEventListener('click', async () => {
    if (!Email.checkValidity()) { alert('Invalid Email') }
    else {
        const email = Email.value.toLowerCase()
        const response = await retrieve({code: Code.value, email: email})
        alert(response.message)
        if (response.check) {
            window.location.href = '/'
        }
        
    }
})