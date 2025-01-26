// cookies
function getCookies() {
    const temp = Object.fromEntries(document.cookie.split('; ').map(v=>v.split(/=(.*)/s).map(decodeURIComponent)))
    const cookies = {}
    for (const [key, value] of Object.entries(temp)) {
        if (key.includes('esther')) {
            cookies[key.replace('esther-', '')] = value
        }
    }
    return cookies 
}

function getCookie() {
    return getCookies().cookie
}

// halts code for ms ms
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export { getCookies, getCookie, sleep }