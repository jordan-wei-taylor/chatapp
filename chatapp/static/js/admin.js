const href = window.location.href;

Array.from(document.getElementById('sidebar').children).forEach((element) => {
    if (href.includes(element.id)) {
        element.className    = 'active'
        element.style.cursor = "unset"
    } else {
        element.addEventListener('click', () => { window.location.href = `/${element.id}` })
    }
})