import { getCookie } from "/static/js/utils.js"


var socket = io()

/**
 * emits `client-${event}` with optional data ``eventData`` and waits `server-${event}` to be emitted by the server
 * see https://socket.io/docs/v4/client-api/#socketonceeventname-callback for more details
 * 
 * @param {String} event      base string to be included in the client and server event names
 * @param {Object} eventData  object to send to the server [optional]
 * @returns 
 */
function emitWithPromise(event, eventData = null) {
    return new Promise((resolve) => {
        if (eventData == null) { socket.emit(`client-${event}`) }                 // emit client event
        else { socket.emit(`client-${event}`, eventData) }                   // emit client event with ``eventData``
        socket.once(`server-${event}`, (response) => { resolve(response) })  // halt code and wait for server to emit server event
    })
}

export async function signup(data) {
    const response = await emitWithPromise('signup', data)
    return response
}

export async function userExists(user) { 
    const exists = await emitWithPromise('user-exists', user)
    return exists
}

export async function login(user) {
    const cookie = await emitWithPromise('user-login', user)
    return cookie
}

export async function adminPassword(password) {
    const check = await emitWithPromise('admin-login', password)
    return check
}

export function logout() {
    const cookie = getCookie()
    socket.emit('client-logout', cookie)
    document.cookie = 'esther-cookie=;max-age=0'
    window.location.href = '/'
}

export function generateUsers(data) { socket.emit('client-generate-users', data)}

socket.on('server-get-treatments', (treatments) => {
    var Treatment       = document.getElementById('generate-treatment')
    Treatment.innerHTML = '<option disabled selected>Select a Treatment</option>'
    treatments.forEach((treatment, index) => {
        Treatment.innerHTML += `<option value = "${treatment}">${treatment}</option>`
    })
        
})

socket.on('server-get-options', (options) => {
    var Option       = document.getElementById('generate-option')
    Option.innerHTML = '<option disabled selected>Select an Option</option>'
    options.forEach((option, index) => {
        Option.innerHTML += `<option value = "${option}">${option}</option>`
    })
})

export function treatments() { socket.emit('client-get-treatments') }
export function options(treatment) { socket.emit('client-get-options', treatment) }

// receives {records: matrix}
socket.on('server-fetch-records', (data) => {
    const tableBody     = document.getElementById('table-rows');
    tableBody.innerHTML = '';
    
    // access records matrix and loop over each row
    data.records.forEach(record => {
        const row = document.createElement('tr');

        // populate a row of the table with row in matrix
        row.innerHTML = `<td>${record.map(String).join('</td><td>')}</td>`
 
        tableBody.appendChild(row);
    });

    const totalPages = Math.ceil(data.totalCount / data.limit);
    document.getElementById('pageInfo').textContent = `Page ${data.page} of ${totalPages}`;
    document.getElementById('prevPage').disabled = data.page === 1;
    document.getElementById('nextPage').disabled = data.page === totalPages;
});

export function fetchRecords(currentPage, limit) { socket.emit('client-fetch-records', { page: currentPage, limit: limit }) }
export function updateUserModule(cookie, module) { socket.emit('client-update-user-module', {cookie: cookie, module: module}) }

export async function fetchModulesCompleted(cookie) {
    const number = await emitWithPromise('fetch-modules-completed', cookie)
    return number
}

export async function fetchCue(module, cookie) {
    const cues = await emitWithPromise('fetch-cue', {module: module, cookie: cookie})
    return cues
}

export async function fetchPreamble(module, cookie) {
    const preamble = await emitWithPromise('fetch-preamble', {module: module, cookie: cookie})
    return preamble
}

export async function classify(data) {
    const response = await emitWithPromise('classify', data)
    return response
}

export async function authenticate(cookie) {
    const response = await emitWithPromise('auth', cookie)
    if (!response.authenticate) {
        document.cookie = `esther-auth-reject=${response.message}-new-auth;path=/`
        window.location.href = '/'
    }
}

export async function submitRecord(record) {
    const response = await emitWithPromise('submit-record', record)
    return response
}
export function amtWarmUp() { socket.emit('client-amt-warm-up') }

export async function getOption(cookie) {
    const option = await emitWithPromise('get-option', cookie)
    return option
}

export function addStudy(data) { socket.emit('client-add-study', data) }

export async function getStudies() {
    const response = await emitWithPromise('get-studies')
    return response
}

export async function getStudy(code) {
    const response = await emitWithPromise('get-study', code)
    return response
}

export function updateStudy(code, data) { socket.emit('client-update-study', { code: code, data: data}) }

export async function retrieve(data) {
    const response = await emitWithPromise('retrieve', data)
    return response
}

export async function getTreatments() {
    const response = await emitWithPromise('get-treatments-2')
    return response
}