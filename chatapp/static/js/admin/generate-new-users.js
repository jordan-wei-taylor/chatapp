import { generateUsers, options, treatments } from "/static/js/events.js"
import { getCookies } from "/static/js/utils.js"

var Num       = document.getElementById('generate-number')
var Treatment = document.getElementById('generate-treatment')
var Option    = document.getElementById('generate-option')
var Button    = document.getElementById('generate-button')

// generates new users
Button.addEventListener('click', () =>{

    if (Number.isInteger(+Num.value) & (Num.value > 0)) {

        generateUsers({
            number    : Num.value,
            treatment : Treatment.value,
            option    : Option.value
        })
        
        const cookies = getCookies()
        
        // download option
        if (confirm('download new users as txt?')) { window.open(`/admin/download=${cookies.cookie}`, '_blank') } 
    
    }
});

Treatment.addEventListener('change', () => {
    options(Treatment.value)
    Option.value = null
})

window.onload = function() { treatments() }   