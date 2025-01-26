import { logout } from "/static/js/events.js"

function back() { 
    if (window.location.href.includes('module')) { window.location.href = '/home' }
    else { window.location.href = document.referrer }
}

const Back = document.getElementById('header-back')
const Logout = document.getElementById('header-logout')

if (document.body.contains(Back)) { Back.addEventListener('click', back) }
if (document.body.contains(Logout)) { Logout.addEventListener('click', logout) }